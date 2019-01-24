import tkinter
from tkinter import ttk  # 导入ttk模块，因为下拉菜单控件在ttk中
from tkinter import messagebox  # 导入提示窗口包
import cv2
import time
import PIL.Image, PIL.ImageTk
from functools import partial
import time

import settings.settings as settings
import image_catcher.img_catcher as i_c
import halcon_cal.halcon_cal as hal_c
import image_processor.img_processor as i_p
import modbusGP.modbusGP as mdbsGp

class GoldenPeek:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)

        self.window.geometry("%dx%d" % (self.window.winfo_screenwidth(), self.window.winfo_screenheight()))

        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        retInit,frameInit = self.vid.get_frame()

        self.frameCanvas = tkinter.Frame(window)

        # Create a canvas that can fit the above video source size

        settings.canvasWidth = (frameInit.shape)[1];
        settings.canvasHeight = (frameInit.shape)[0];


        self.canvas = tkinter.Canvas(self.frameCanvas, width=2*settings.canvasWidth, height=settings.canvasHeight)
        self.canvas.grid(row=0, column=0, columnspan=1, rowspan=1, padx=2, pady=2, sticky='s')



        self.frameCanvas.grid(row=0, column=0, columnspan=1, rowspan=1, padx=2, pady=2, sticky='s')

        self.tabControl = ttk.Notebook(window)  # Create Tab Control


        self.tabHalcon = ttk.Frame(self.tabControl)  # Create a tab for Halcon
        self.tabControl.add(self.tabHalcon, text='定位')  # Add the tab for Halcon
        self.tabFinder = ttk.Frame(self.tabControl)  # Add a second tab for Finder
        self.tabControl.add(self.tabFinder, text='检测')

        self.tabControl.grid(row=1, column=0)  # Grid to make visible

        self.tabHalconShow()

        self.tabFinderShow()


        self.portAuto = 0
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        # keep obtaining the img on the canvas
        self.update()

        self.window.mainloop()

    def tabHalconShow(self):

        # HalconA
        self.labelHalconA = ttk.LabelFrame(self.tabHalcon, text=' 标定A点坐标 ')
        self.labelHalconA.grid(row=0, column=0, padx=8, pady=4)

        self.labelANo = ttk.Label(self.labelHalconA, text="对应编号")
        self.labelANo.grid(row=1, column=0, sticky='W')

        # Adding a Textbox Entry widget
        self.nameANo = tkinter.StringVar()
        self.nameANo_entered = ttk.Entry(self.labelHalconA, width=12, textvariable=self.nameANo)
        self.nameANo_entered.grid(row=1, column=1, sticky='W')  # align left/West

        #坐标的X
        self.labelAX = ttk.Label(self.labelHalconA, text="坐标X")
        self.labelAX.grid(row=2, column=0, sticky='W')

        # Adding a Textbox Entry widget
        self.nameAX = tkinter.StringVar()
        self.nameAX_entered = ttk.Entry(self.labelHalconA, width=12, textvariable=self.nameAX)
        self.nameAX_entered.grid(row=2, column=1, sticky='W')  # align left/West

        # 坐标的Y
        self.labelAY = ttk.Label(self.labelHalconA, text="坐标Y")
        self.labelAY.grid(row=3, column=0, sticky='W')

        self.nameAY = tkinter.StringVar()
        self.nameAY_entered = ttk.Entry(self.labelHalconA, width=12, textvariable=self.nameAY)
        self.nameAY_entered.grid(row=3, column=1, sticky='E')  # align left/West


        # HalconB
        self.labelHalconB = ttk.LabelFrame(self.tabHalcon, text=' 标定B点坐标 ')
        self.labelHalconB.grid(row=0, column=1, padx=8, pady=4)

        self.labelBNo = ttk.Label(self.labelHalconB, text="对应编号")
        self.labelBNo.grid(row=1, column=0, sticky='W')

        # Adding a Textbox Entry widget
        self.nameBNo = tkinter.StringVar()
        self.nameBNo_entered = ttk.Entry(self.labelHalconB, width=12, textvariable=self.nameBNo)
        self.nameBNo_entered.grid(row=1, column=1, sticky='W')  # align left/West


        self.labelBX = ttk.Label(self.labelHalconB, text="坐标X")
        self.labelBX.grid(row=2, column=0, sticky='W')

        # Adding a Textbox Entry widget
        self.nameBX = tkinter.StringVar()
        self.nameBX_entered = ttk.Entry(self.labelHalconB, width=12, textvariable=self.nameBX)
        self.nameBX_entered.grid(row=2, column=1, sticky='W')  # align left/West

        self.labelBY = ttk.Label(self.labelHalconB, text="坐标Y")
        self.labelBY.grid(row=3, column=0, sticky='W')

        self.nameBY = tkinter.StringVar()
        self.nameBY_entered = ttk.Entry(self.labelHalconB, width=12, textvariable=self.nameBY)
        self.nameBY_entered.grid(row=3, column=1, sticky='E')  # align left/West



        # HalconCatchedButton
        self.labelHalconCatchedButton = ttk.LabelFrame(self.tabHalcon, text=' 截图按钮 ')
        self.labelHalconCatchedButton.grid(row=1, column=0, padx=8, pady=4)
        # Adding Halcon Button
        self.halconCatchedButton = ttk.Button(self.labelHalconCatchedButton, text="获取截图", command=self.halconCatcher)
        self.halconCatchedButton.grid(row=1, column=0)

        # HalconButton
        self.labelHalconButton = ttk.LabelFrame(self.tabHalcon, text=' 标定按钮 ')
        self.labelHalconButton.grid(row=1, column=1, padx=8, pady=4)
        # Adding Halcon Button
        self.halconButton = ttk.Button(self.labelHalconButton, text="获取标定点", command=self.halconPoints)
        self.halconButton.grid(row=1, column=0)

        # HalconCalButton
        self.labelHalconCalButton = ttk.LabelFrame(self.tabHalcon, text=' 坐标系计算 ')
        self.labelHalconCalButton.grid(row=1, column=2, padx=8, pady=4)
        # Adding HalconCal Button
        self.halconCalButton = ttk.Button(self.labelHalconCalButton, text="获取矩阵", command=self.halconConversionCal)
        self.halconCalButton.grid(row=1, column=0)

        # HalconCalThreshold
        self.labelhalconHoughminRadius = ttk.LabelFrame(self.tabHalcon, text=' 圆半径最小值 ')
        self.labelhalconHoughminRadius.grid(row=0, column=2, padx=8, pady=4)
        # Adding HalconCal Scale Threshold
        self.halconHoughminRadius = tkinter.Scale(self.labelhalconHoughminRadius, from_=10, to=200, orient='horizontal', showvalue=1, command=partial(self.thresholdSetter,'halcon', 'halcon','halconHoughminRadius'))
        self.halconHoughminRadius.grid(row=1, column=0)

        # HalconCalThreshold
        self.labelhalconHoughmaxRadius = ttk.LabelFrame(self.tabHalcon, text=' 圆半径最大值 ')
        self.labelhalconHoughmaxRadius.grid(row=0, column=3, padx=8, pady=4)
        # Adding HalconCal Scale Threshold
        self.halconHoughmaxRadius = tkinter.Scale(self.labelhalconHoughmaxRadius, from_=10, to=200, orient='horizontal',
                                                  showvalue=1, command=partial(self.thresholdSetter, 'halcon', 'halcon','halconHoughmaxRadius'))
        self.halconHoughmaxRadius.grid(row=1, column=0)

        # HalconCalThreshold
        self.labelHalconCalThreshold = ttk.LabelFrame(self.tabHalcon, text=' 阈值设定 ')
        self.labelHalconCalThreshold.grid(row=0, column=4, padx=8, pady=4)
        # Adding HalconCal Scale Threshold
        self.halconCalThreshold = tkinter.Scale(self.labelHalconCalThreshold, from_=1, to=255, orient='horizontal',
                                                showvalue=1, command=self.halconThresholdSetter)
        self.halconCalThreshold.grid(row=1, column=0)

    def tabFinderShow(self):

        # 手动部分
        # Start Button
        self.labelFinderButton = ttk.LabelFrame(self.tabFinder, text=' 手动操作 ')
        self.labelFinderButton.grid(row=0, column=0, padx=8, pady=4)

        # Adding Start Button
        self.catcherButton = ttk.Button(self.labelFinderButton, text="截取图像", command=self.processorCatcher)
        self.catcherButton.grid(row=1, column=0)

        # Adding Process Button
        self.processorButton = ttk.Button(self.labelFinderButton, text="检测目标", command=self.processorImage)
        self.processorButton.grid(row=1, column=1)

        # Adding Process Button
        self.transferButton = ttk.Button(self.labelFinderButton, text="发送坐标", command=self.processorWrite)
        self.transferButton.grid(row=1, column=2)

        # Adding Process Button
        self.fetchSignalButton = ttk.Button(self.labelFinderButton, text="获取标志位", command=self.processorFetchSignal)
        self.fetchSignalButton.grid(row=1, column=3)

        # 自动部分
        # Start Button
        self.labelAutoFinderButton = ttk.LabelFrame(self.tabFinder, text=' 自动操作 ')
        self.labelAutoFinderButton.grid(row=0, column=1, padx=8, pady=4)

        # Adding Start Button
        self.launchButton = ttk.Button(self.labelAutoFinderButton, text="开始", command=self.autoLaunch)
        self.launchButton.grid(row=1, column=0)

        # Adding Cease Button
        self.ceaseButton = ttk.Button(self.labelAutoFinderButton, text="停止", command=self.autoCease)
        self.ceaseButton.grid(row=1, column=1)


        # Finder Threshold
        self.labelfinderCalThresholdLow = ttk.LabelFrame(self.tabFinder, text=' 像素阈值(低)设定 ')
        self.labelfinderCalThresholdLow.grid(row=1, column=0)
        # Adding HalconCal Scale Threshold
        self.finderCalThresholdLow = tkinter.Scale(self.labelfinderCalThresholdLow, from_=1, to=255, orient='horizontal',
                                                showvalue=1, command=partial(self.thresholdSetter,'finder','cal','low'))
        self.finderCalThresholdLow.grid(row=1, column=0)

        # Finder Threshold
        self.labelfinderCalThresholdHigh = ttk.LabelFrame(self.tabFinder, text=' 像素阈值(高)设定 ')
        self.labelfinderCalThresholdHigh.grid(row=1, column=1)
        # Adding HalconCal Scale Threshold
        self.finderCalThresholdHigh = tkinter.Scale(self.labelfinderCalThresholdHigh, from_=1, to=255, orient='horizontal',
                                                   showvalue=1, command=partial(self.thresholdSetter,'finder', 'cal','high'))
        self.finderCalThresholdHigh.grid(row=1, column=0)

        # Finder Threshold
        self.labelfinderHoughminRadius = ttk.LabelFrame(self.tabFinder, text=' 圆半径最小值 ')
        self.labelfinderHoughminRadius.grid(row=1, column=2)
        # Adding HalconCal Scale Threshold
        self.finderHoughminRadius = tkinter.Scale(self.labelfinderHoughminRadius, from_=1, to=100, orient='horizontal',
                                                   showvalue=1, command=partial(self.thresholdSetter,'finder', 'hough', 'finderHoughminRadius'))
        self.finderHoughminRadius.grid(row=1, column=0)

        # Finder Threshold
        self.labelfinderHoughmaxRadius = ttk.LabelFrame(self.tabFinder, text=' 圆半径最小值 ')
        self.labelfinderHoughmaxRadius.grid(row=1, column=3)
        # Adding HalconCal Scale Threshold
        self.finderHoughmaxRadius = tkinter.Scale(self.labelfinderHoughmaxRadius, from_=1, to=100, orient='horizontal',
                                                    showvalue=1,
                                                    command=partial(self.thresholdSetter,'finder', 'hough', 'finderHoughmaxRadius'))
        self.finderHoughmaxRadius.grid(row=1, column=0)



    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        #启动自动化流程
        if settings.autoSwitch == 1:
            self.autoDispatch()

        #######################

        if settings.displayerFlag == settings.INIT:
            self.obtained = PIL.ImageTk.PhotoImage(image=PIL.Image.open('./mountain.jpg'))
        if settings.displayerFlag == settings.CATCHED:
            self.obtained = PIL.ImageTk.PhotoImage(image=PIL.Image.open(settings.catch_img_dir + "catched.jpg").resize(
                (settings.canvasWidth, settings.canvasHeight), resample=PIL.Image.LANCZOS))
        if settings.displayerFlag == settings.HALCON:
            self.obtained = PIL.ImageTk.PhotoImage(image=PIL.Image.open(settings.halcon_img_dir + "halcon.jpg").resize(
                (settings.canvasWidth, settings.canvasHeight), resample=PIL.Image.LANCZOS))
        if settings.displayerFlag == settings.PROCESSED:
            self.obtained = PIL.ImageTk.PhotoImage(image=PIL.Image.open(settings.process_img_dir + "processed.jpg").resize(
                (settings.canvasWidth, settings.canvasHeight), resample=PIL.Image.LANCZOS))




        self.show_catched = self.canvas.create_image(0, 0, image=self.obtained,anchor = tkinter.NW)

        self.canvas.move(self.show_catched, 650, 0)

        self.window.after(self.delay, self.update)

    #截图
    def snapshot(self,displayerFlag=settings.CATCHED):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:

            i_c.img_catch(frame,displayerFlag)

    #用于halcon定位的截图
    def halconCatcher(self):

        self.snapshot(settings.CATCHED)

###############################################
#      halcon定位
##############################################

    # 获取halcon的定位点
    def halconPoints(self):
        hal_c.halconHoughPoints()
        # hal_c.halconPoints()
        settings.displayerFlag = settings.HALCON

    #把halcon定位点结合输入的对应机械臂坐标，转化成变换矩阵
    def halconConversionCal(self):
        # print("halconConversionCal")
        halconA = [int(self.nameANo_entered.get()), self.nameAX_entered.get(), self.nameAY_entered.get()]
        halconB = [int(self.nameBNo_entered.get()), self.nameBX_entered.get(), self.nameBY_entered.get()]


        halconCollection = [halconA,halconB]
        if not(hal_c.halconCollectionCheck(halconCollection)):
            messagebox.showinfo(title='机械臂坐标', message="机械臂坐标不合法")

        # 检查halcon定位点坐标，是否能组成获取转换方程的矩阵
        flagRobotPoints = hal_c.reviewRobotPoints(halconCollection)

        if flagRobotPoints==1:
            hal_c.marksHalconReverseConverter(halconCollection)
            print("halconConverterMatrix")
            print(settings.halconConverterMatrix)
        else:
            print("请调整定位板角度或使用其他坐标点")
            messagebox.showinfo(title='定位板', message="请调整定位板角度再试一次")


    #halcon定位时候设定像素阈值
    def halconThresholdSetter(self, value):
        settings.halconThreshold = value
        print(settings.halconThreshold)

###############################################
#     图像处理（手动）
##############################################

    #用于图像处理的截图
    def processorCatcher(self):
        self.snapshot(settings.CATCHED)
    #处理图像
    def processorImage(self, processType = settings.processType):
        thresholdCal = settings.thresholdInfo['finder']['cal']
        thresHough = settings.thresholdInfo['finder']['hough']
        print("threshold")
        print(thresholdCal)
        print(thresHough)
        if int(thresholdCal['low'])>int(thresholdCal['high']) or int(thresHough['low'])>int(thresHough['high']):
            messagebox.showinfo(title='阈值参数', message="阈值上下限设置有误")
        else:
            processType = 'hough'
            i_p.img_processor(processType)
            settings.displayerFlag = settings.PROCESSED

    #传输处理结果给Modbus
    def processorWrite(self):
        i_p.writeTxt()
        messagebox.showinfo(title='Modbus传输', message="已写入")


    #获取处理完成的信号
    def processorFetchSignal(self):
        watchDog = mdbsGp.recvWatchDog()
        if watchDog == settings.watchDog:
            messagebox.showinfo(title='Modbus传输', message="机械臂已读取完成")
            return True
        else:
            return False

    #对于不同来源设置阈值的不同数值
    def thresholdSetter(self,source = settings.thresholdSource[0],type = settings.thresholdType[0],
                        level = settings.thresholdLevel[0],value=0):

        settings.thresholdInfo[source][type][level] = value

###############################################
#     自动化流程
##############################################

    #设置自动化流程的开始信号
    def autoLaunch(self):
        settings.autoSwitch = 1
        self.portAuto = mdbsGp.portBuilder()





        # 自动化调度
        # 注：1.所有的端口收必须在调度内完成
        #    2.每一次的update只能进行一次端口的操作，发和收一视同仁

    def autoDispatch(self):
        # 寄存器通信
        self.regCommunication()

        # 自动化功能执行
        self.autoLaunchMachine(settings.stepIndicator)

    ###################################
    #和寄存器通信的函数
    def regCommunication(self):


        #等待机械臂初始化状态
        # 阶段 = 0
        if settings.stepNow == 0:
            settings.stepIndicator = mdbsGp.recvWatchDog(self.portAuto, settings.stepIndicatorReg)
            if settings.stepIndicator >= 0:
                settings.stepNow = settings.stepIndicator
        #图像处理阶段1.1，1.2
        # 阶段 = 1
        elif settings.stepNow == 1:
            if settings.stepFinish1 == 0:
                pass
            else:
                mdbsGp.modbusAutoTransferrer(self.portAuto, settings.stepIndicatorReg, 2)
                settings.stepNow = 0
                settings.stepFinish1 = 0


        # 图像处理阶段2.1，2.2
        # 阶段 = 2
        else:
            print('stepFinish2')
            print(settings.stepFinish2)
            print('coordinateReady')
            print(settings.coordinateReady)
            if settings.stepFinish2 == 0:
                #可进行写坐标操作
                if settings.coordinateReady == 0:
                    pass
                elif settings.coordinateReady == 0.5:
                    mdbsGp.modbusAutoTransferrer(self.portAuto, settings.coordinateReadyReg, 1)
                    settings.coordinateReady = 0.8
                else:
                    coordinateReadyTmp = settings.coordinateReady
                    settings.coordinateReady = mdbsGp.recvWatchDog(self.portAuto, settings.coordinateReadyReg)
                    if settings.coordinateReady < 0:
                        settings.coordinateReady = coordinateReadyTmp
            else:
                mdbsGp.modbusAutoTransferrer(self.portAuto, settings.stepIndicatorReg, 0)
                settings.stepFinish2 = 0
                settings.stepNow = 0
                settings.coordinateReady =0
                print('coordinateReady branch')
                print(settings.coordinateReady)



    #自动化功能的函数
    ##########################################
    #自动化截图
    def autoImgCatcher(self):
        self.snapshot(settings.CATCHED)

    #自动化处理图像，获取坐标序列
    def autoProcessor(self):
        self.processorImage()


    def autoTransfer(self):
        # portAuto = mdbsGp.portBuilder()
        if len(settings.finderProcessResult) > 0:
            #坐标数据就绪标志为0，说明机械臂已经取走数据，发送成功
            if settings.coordinateReady == 0 or settings.coordinateReady == 0.8:
                itemTransfer = settings.finderProcessResult.pop()
                mdbsGp.modbusAutoListTransferrer(self.portAuto,settings.XDataStore, 2, itemTransfer)
                settings.coordinateReady = 0.5
        else:
            if settings.coordinateReady == 0:
                settings.stepFinish2 = 1

    # 自动化操作执行流程
    def autoLaunchMachine(self,step=0):
        #监听等待
        if step == 0:
            settings.stepFinish1 = 0
            settings.stepFinish2 = 0
        #内部处理
        elif step == 1:
            if settings.stepFinish1 == 0:
                self.autoImgCatcher()
                # self.autoProcessor()
                # 此处不管有没有监测到，都直接顺次进行了
                settings.stepFinish1 = 1
        #发送坐标
        elif step == 2:

            if settings.coordinateReady == 0:
                self.autoTransfer()
        else:
            pass


    #设置自动化流程结束信号
    def autoCease(self):
        self.autoSwitchReset()

    #自动化流程结束的操作函数
    def autoSwitchReset(self):
        settings.autoSwicth = 0
        settings.displayerFlag == settings.INIT

class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)


    def get_frame(self,default=0):
        if self.vid.isOpened():
            if default:
                self.vid.set(cv2.CAP_PROP_FRAME_WIDTH,2688)
                self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT,1520)
            else:
                self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (0,None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


# Create a window and pass it to the Application object
GoldenPeek(tkinter.Tk(), "  李之玉出品 V2.3-20190108 ")
