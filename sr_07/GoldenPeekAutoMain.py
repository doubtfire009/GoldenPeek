import tkinter
from tkinter import ttk  # 导入ttk模块，因为下拉菜单控件在ttk中
from tkinter import messagebox  # 导入提示窗口包
import cv2
import time
import PIL.Image, PIL.ImageTk
from functools import partial

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



        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        # keep obtaining the img on the canvas
        self.update()

        self.window.mainloop()

    def tabHalconShow(self):

        # HalconA
        self.labelHalconA = ttk.LabelFrame(self.tabHalcon, text=' 标定A点坐标 ')
        self.labelHalconA.grid(row=0, column=0, padx=8, pady=4)

        self.labelAX = ttk.Label(self.labelHalconA, text="坐标X")
        self.labelAX.grid(row=1, column=0, sticky='W')

        # Adding a Textbox Entry widget
        self.nameAX = tkinter.StringVar()
        self.nameAX_entered = ttk.Entry(self.labelHalconA, width=12, textvariable=self.nameAX)
        self.nameAX_entered.grid(row=1, column=1, sticky='W')  # align left/West

        self.labelAY = ttk.Label(self.labelHalconA, text="坐标Y")
        self.labelAY.grid(row=2, column=0, sticky='W')

        self.nameAY = tkinter.StringVar()
        self.nameAY_entered = ttk.Entry(self.labelHalconA, width=12, textvariable=self.nameAY)
        self.nameAY_entered.grid(row=2, column=1, sticky='E')  # align left/West


        # HalconB
        self.labelHalconB = ttk.LabelFrame(self.tabHalcon, text=' 标定B点坐标 ')
        self.labelHalconB.grid(row=0, column=1, padx=8, pady=4)

        self.labelBX = ttk.Label(self.labelHalconB, text="坐标X")
        self.labelBX.grid(row=1, column=0, sticky='W')

        # Adding a Textbox Entry widget
        self.nameBX = tkinter.StringVar()
        self.nameBX_entered = ttk.Entry(self.labelHalconB, width=12, textvariable=self.nameBX)
        self.nameBX_entered.grid(row=1, column=1, sticky='W')  # align left/West

        self.labelBY = ttk.Label(self.labelHalconB, text="坐标Y")
        self.labelBY.grid(row=2, column=0, sticky='W')

        self.nameBY = tkinter.StringVar()
        self.nameBY_entered = ttk.Entry(self.labelHalconB, width=12, textvariable=self.nameBY)
        self.nameBY_entered.grid(row=2, column=1, sticky='E')  # align left/West

        # HalconC
        self.labelHalconC = ttk.LabelFrame(self.tabHalcon, text=' 标定C点坐标 ')
        self.labelHalconC.grid(row=0, column=2, padx=8, pady=4)

        self.labelCX = ttk.Label(self.labelHalconC, text="坐标X")
        self.labelCX.grid(row=1, column=0, sticky='W')

        # Adding a Textbox Entry widget
        self.nameCX = tkinter.StringVar()
        self.nameCX_entered = ttk.Entry(self.labelHalconC, width=12, textvariable=self.nameCX)
        self.nameCX_entered.grid(row=1, column=1, sticky='W')  # align left/West

        self.labelCY = ttk.Label(self.labelHalconC, text="坐标Y")
        self.labelCY.grid(row=2, column=0, sticky='W')

        self.nameCY = tkinter.StringVar()
        self.nameCY_entered = ttk.Entry(self.labelHalconC, width=12, textvariable=self.nameCY)
        self.nameCY_entered.grid(row=2, column=1, sticky='E')  # align left/West

        # HalconD
        self.labelHalconD = ttk.LabelFrame(self.tabHalcon, text=' 标定D点坐标 ')
        self.labelHalconD.grid(row=0, column=3, padx=8, pady=4)

        self.labelDX = ttk.Label(self.labelHalconD, text="坐标X")
        self.labelDX.grid(row=1, column=0, sticky='W')

        # Adding a Textbox Entry widget
        self.nameDX = tkinter.StringVar()
        self.nameDX_entered = ttk.Entry(self.labelHalconD, width=12, textvariable=self.nameDX)
        self.nameDX_entered.grid(row=1, column=1, sticky='W')  # align left/West

        self.labelDY = ttk.Label(self.labelHalconD, text="坐标Y")
        self.labelDY.grid(row=2, column=0, sticky='W')

        self.nameDY = tkinter.StringVar()
        self.nameDY_entered = ttk.Entry(self.labelHalconD, width=12, textvariable=self.nameDY)
        self.nameDY_entered.grid(row=2, column=1, sticky='E')  # align left/West

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
        self.labelHalconCalThreshold = ttk.LabelFrame(self.tabHalcon, text=' 阈值设定 ')
        self.labelHalconCalThreshold.grid(row=1, column=3, padx=8, pady=4)
        # Adding HalconCal Scale Threshold
        self.halconCalThreshold = tkinter.Scale(self.labelHalconCalThreshold, from_=0, to=255, orient='horizontal', showvalue=1, command=self.halconThresholdSetter)
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
        self.transferButton = ttk.Button(self.labelFinderButton, text="发送坐标", command=self.processorTransfer)
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
        self.finderCalThresholdLow = tkinter.Scale(self.labelfinderCalThresholdLow, from_=0, to=255, orient='horizontal',
                                                showvalue=1, command=partial(self.thresholdSetter,'finder','cal','low'))
        self.finderCalThresholdLow.grid(row=1, column=0)

        # Finder Threshold
        self.labelfinderCalThresholdHigh = ttk.LabelFrame(self.tabFinder, text=' 像素阈值(高)设定 ')
        self.labelfinderCalThresholdHigh.grid(row=1, column=1)
        # Adding HalconCal Scale Threshold
        self.finderCalThresholdHigh = tkinter.Scale(self.labelfinderCalThresholdHigh, from_=0, to=255, orient='horizontal',
                                                   showvalue=1, command=partial(self.thresholdSetter,'finder', 'cal','high'))
        self.finderCalThresholdHigh.grid(row=1, column=0)

        # Finder Threshold
        self.labelfinderAreaThresholdLow = ttk.LabelFrame(self.tabFinder, text=' 面积阈值(低)设定 ')
        self.labelfinderAreaThresholdLow.grid(row=1, column=2)
        # Adding HalconCal Scale Threshold
        self.finderAreaThresholdLow = tkinter.Scale(self.labelfinderAreaThresholdLow, from_=0, to=1000, orient='horizontal',
                                                   showvalue=1, command=partial(self.thresholdSetter,'finder', 'area','low'))
        self.finderAreaThresholdLow.grid(row=1, column=0)

        # Finder Threshold
        self.labelfinderAreaThresholdHigh = ttk.LabelFrame(self.tabFinder, text=' 面积阈值(高)设定 ')
        self.labelfinderAreaThresholdHigh.grid(row=1, column=3)
        # Adding HalconCal Scale Threshold
        self.finderAreaThresholdHigh = tkinter.Scale(self.labelfinderAreaThresholdHigh, from_=0, to=1000, orient='horizontal',
                                                    showvalue=1,
                                                    command=partial(self.thresholdSetter,'finder', 'area','high'))
        self.finderAreaThresholdHigh.grid(row=1, column=0)


    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        #启动自动化流程

        if settings.autoSwitch:
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

            # cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            i_c.img_catch(frame,displayerFlag)

    #用于halcon定位的截图
    def halconCatcher(self):
        
        self.snapshot(settings.CATCHED)

###############################################
#      halcon定位
##############################################

    # 获取halcon的定位点
    def halconPoints(self):
        hal_c.halconPoints()
        settings.displayerFlag = settings.HALCON

    #把halcon定位点结合输入的对应机械臂坐标，转化成变换矩阵
    def halconConversionCal(self):
        # print("halconConversionCal")
        halconA = [self.nameAX_entered.get(), self.nameAY_entered.get()]
        halconB = [self.nameBX_entered.get(), self.nameBY_entered.get()]
        halconC = [self.nameCX_entered.get(), self.nameCY_entered.get()]
        halconD = [self.nameDX_entered.get(), self.nameDY_entered.get()]

        halconCollection = [halconA,halconB,halconC,halconD]

        if not(hal_c.halconCollectionCheck(halconCollection)):
            messagebox.showinfo(title='机械臂坐标', message="机械臂坐标不合法")


        # 检查halcon定位点坐标，是否能组成获取转换方程的矩阵
        NoP1,NoP2,flagRobotPoints = hal_c.reviewRobotPoints()

        if flagRobotPoints==1:
            hal_c.marksHalconReverseConverter(settings.halconReview[NoP1],settings.halconReview[NoP2],halconCollection[NoP1],halconCollection[NoP2])
            print("halconConverterMatrix")
            print(settings.halconConverterMatrix)
        else:
            print("请调整定位板角度再试一次")
            messagebox.showinfo(title='定位板', message="请调整定位板角度再试一次")

        # 发送测试代码

        mdbsGp.modbusTransferrer(0x01,600,settings.halconConverterMatrix[0][0])
        mdbsGp.modbusTransferrer(0x01,1000,settings.halconConverterMatrix[0][1])
        mdbsGp.modbusTransferrer(0x01,1400,settings.halconConverterMatrix[1][0])
        mdbsGp.modbusTransferrer(0x01,1800,settings.halconConverterMatrix[1][1])


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
        thresholdArea = settings.thresholdInfo['finder']['area']
        print("threshold")
        print(thresholdCal)
        print(thresholdArea)
        if int(thresholdCal['low'])>int(thresholdCal['high']) or int(thresholdArea['low'])>int(thresholdArea['high']):
            messagebox.showinfo(title='阈值参数', message="阈值上下限设置有误")
        else:
            i_p.img_processor(processType)
            settings.displayerFlag = settings.PROCESSED

    #传输处理结果给Modbus
    def processorTransfer(self):
        ret = mdbsGp.modbusListTransferrer(settings.finderProcessResult)
        if ret == -1:
            messagebox.showinfo(title='Modbus传输', message="尚未得到传输值")
        elif ret==0:
            messagebox.showinfo(title='Modbus传输', message="传输值不合法")
        else:
            messagebox.showinfo(title='Modbus传输', message="传输已成功")

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



    #自动化调度
    def autoDispatch(self):
        portAuto = mdbsGp.portBuilder()
        stepIndicator = mdbsGp.recvWatchDog(portAuto, settings.stepIndicatorReg)


        # if stepIndicator == settings.stepStart:
        if stepIndicator == settings.stepImgProcess:
            if settings.stepFinish == 0:
                self.autoLaunchMachine(stepIndicator)

        elif stepIndicator == settings.stepRobot:
            if settings.stepFinish == 1:
                self.autoLaunchMachine(stepIndicator)
        else:
            self.autoLaunchMachine(stepIndicator)


    #自动化截图
    def autoImgCatcher(self):
        self.snapshot(settings.CATCHED)

    #自动化处理图像，获取坐标序列
    def autoProcessor(self):
        self.processorImage()


    def autoTransfer(self):
        portAuto = mdbsGp.portBuilder()
        if len(settings.finderProcessResult) > 0:
            #坐标数据就绪标志
            coordinateReady = mdbsGp.recvWatchDog(portAuto, settings.coordinateReadyReg)
            #坐标数据就绪标志为0，说明机械臂已经取走数据，发送成功
            if coordinateReady == 0:
                itemTransfer = settings.finderProcessResult.pop()
                mdbsGp.modbusTransferrer(settings.modbusTransferAddress,settings.XDataStore,itemTransfer[0])
                mdbsGp.modbusTransferrer(settings.modbusTransferAddress,settings.YDataStore,itemTransfer[1])
                #告诉机械臂发送成功
                mdbsGp.modbusTransferrer(portAuto, settings.coordinateReadyReg, 1)
        else:
            settings.stepFinish = 1

    # 自动化操作执行流程
    def autoLaunchMachine(self,step):
        #监听等待
        if step == 0:
            settings.stepFinish = 0
        #内部处理
        elif step == 1:
            self.autoImgCatcher()
            self.autoProcessor()
            # 此处不管有没有监测到，都直接顺次进行了
            settings.stepFinish = 1
        #发送坐标
        elif step == 2:
            self.autoTransfer()
            settings.stepFinish = 1
            mdbsGp.modbusTransferrer(settings.modbusTransferAddress, settings.stepIndicatorReg, 0)
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
