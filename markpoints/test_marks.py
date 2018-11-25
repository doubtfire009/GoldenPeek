import tkinter
from tkinter import ttk  # 导入ttk模块，因为下拉菜单控件在ttk中
from tkinter import messagebox  # 导入提示窗口包
import cv2
import PIL.Image, PIL.ImageTk
import time
#
import settings.settings as settings
import image_catcher.img_catcher as i_c
import image_processor.img_processor as i_p


class App:
    def __init__(self, window, window_title, video_source=1):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = 3*self.vid.width, height = self.vid.height)
        self.canvas.grid(row=0, column=0, columnspan=4, rowspan=1, padx=5, pady=5, sticky='s')

        self.threshold_frame = tkinter.LabelFrame(window, width=300, height=80, text='阈值')
        self.threshold_frame.grid(row=1, column=0)



        # Create a combox for threshold
        self.combox = ttk.Combobox(self.threshold_frame)
        self.combox['value'] = list(range(1,256))
        self.combox.state(['readonly'])
        self.combox.current(0)
        self.combox.bind("<<ComboboxSelected>>", self.thresholdset)
        self.combox.grid(row=0, column=0, columnspan=4, rowspan=1, padx=5, pady=5, sticky='s')

        self.radVar2 = tkinter.IntVar()  # 通过IntVar() 获取单选按钮value参数对应的值
        self.radVar2.set(2)
        self.radio_detection1 = tkinter.Radiobutton(self.threshold_frame, text="定位", variable=self.radVar2,  value=0, command=self.detection_style_cmd)
        self.radio_detection1.grid(row=1, column=0)
        self.radio_detection2 = tkinter.Radiobutton(self.threshold_frame, text="图像处理", variable=self.radVar2, value=1, command=self.detection_style_cmd)
        self.radio_detection2.grid(row=1, column=1)


        self.mark_points_frame = tkinter.LabelFrame(window, width=300, height=80, text='标定点')
        self.mark_points_frame.grid(row=1, column=1)

        self.mark_points_label_x_1 = tkinter.Label(self.mark_points_frame, text='X')
        self.mark_points_label_x_1.grid(row=0, column=1)
        self.mark_points_label_y_1 = tkinter.Label(self.mark_points_frame, text='Y')
        self.mark_points_label_y_1.grid(row=0, column=2)
        self.mark_points_label_x_2 = tkinter.Label(self.mark_points_frame, text='X')
        self.mark_points_label_x_2.grid(row=0, column=4)
        self.mark_points_label_y_2 = tkinter.Label(self.mark_points_frame, text='Y')
        self.mark_points_label_y_2.grid(row=0, column=5)
        # Entry mark points1
        self.mark_point1_label = tkinter.Label(self.mark_points_frame, text='M1')
        self.mark_point1_label.grid(row=1, column=0)
        self.mark_point1_x = tkinter.Entry(self.mark_points_frame,width=10)
        self.mark_point1_x.grid(row=1, column=1, columnspan=1, rowspan=1, padx=5, pady=5, sticky='s')
        self.mark_point1_y = tkinter.Entry(self.mark_points_frame,width=10)
        self.mark_point1_y.grid(row=1, column=2, columnspan=1, rowspan=1, padx=5, pady=5, sticky='s')

        # Entry mark points2
        self.mark_point2_label = tkinter.Label(self.mark_points_frame, text='M2')
        self.mark_point2_label.grid(row=1, column=3)
        self.mark_point2_x = tkinter.Entry(self.mark_points_frame,width=10)
        self.mark_point2_x.grid(row=1, column=4, columnspan=1, rowspan=1, padx=5, pady=5, sticky='s')
        self.mark_point2_y = tkinter.Entry(self.mark_points_frame,width=10)
        self.mark_point2_y.grid(row=1, column=5, columnspan=1, rowspan=1, padx=5, pady=5, sticky='s')

        # Entry mark points3
        self.mark_point3_label = tkinter.Label(self.mark_points_frame, text='M3')
        self.mark_point3_label.grid(row=2, column=0)
        self.mark_point3_x = tkinter.Entry(self.mark_points_frame, width=10)
        self.mark_point3_x.grid(row=2, column=1, columnspan=1, rowspan=1, padx=5, pady=5, sticky='s')
        self.mark_point3_y = tkinter.Entry(self.mark_points_frame, width=10)
        self.mark_point3_y.grid(row=2, column=2, columnspan=1, rowspan=1, padx=5, pady=5, sticky='s')

        # # Entry mark points4
        self.mark_point4_label = tkinter.Label(self.mark_points_frame, text='M4')
        self.mark_point4_label.grid(row=2, column=3)
        self.mark_point4_x = tkinter.Entry(self.mark_points_frame, width=10)
        self.mark_point4_x.grid(row=2, column=4, columnspan=1, rowspan=1, padx=5, pady=5, sticky='s')
        self.mark_point4_y = tkinter.Entry(self.mark_points_frame, width=10)
        self.mark_point4_y.grid(row=2, column=5, columnspan=1, rowspan=1, padx=5, pady=5, sticky='s')




        # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="图像获取", width=50, command=self.snapshot)
        self.btn_snapshot.grid(row=3, column=0, columnspan=1, rowspan=1, padx=5, pady=5, sticky='s')

        # Button that process images
        self.btn_imgprocess = tkinter.Button(window, text="图像处理", width=50, command=self.img_process)
        self.btn_imgprocess.grid(row=3, column=1, columnspan=1, rowspan=1, padx=5, pady=5, sticky='s')
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        #keep obtaining the img on the canvas
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame(self)

        if ret:
            # cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            i_c.img_catch(frame)

    def img_process(self):
        if settings.detection_style_cmd == 1:
            x, y, area_max, radius,threshold = i_p.img_processor("default")
            messagebox.showinfo("x-y-area_max-radius-threshold", str(x)+"-"+str(y)+"-"+str(area_max)+"-"+str(radius)+"-"+str(threshold))
        else:
            settings.mark_point1_x = self.mark_point1_x.get()
            settings.mark_point2_x = self.mark_point2_x.get()
            settings.mark_point3_x = self.mark_point3_x.get()
            settings.mark_point4_x = self.mark_point4_x.get()
            settings.mark_point1_y = self.mark_point1_x.get()
            settings.mark_point2_y = self.mark_point2_x.get()
            settings.mark_point3_y = self.mark_point3_x.get()
            settings.mark_point4_y = self.mark_point4_x.get()
            i_p.detection_marks()


    def detection_style_cmd(self):
        settings.detection_style_cmd = self.radVar2.get()
        print(settings.detection_style_cmd)

    def thresholdset(self, event = None):
        settings.process_threshold = self.combox.get()
        print(settings.process_threshold)

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        if settings.click_frame == 0:
            self.obtained = PIL.ImageTk.PhotoImage(image = PIL.Image.open('./mountain.jpg'))
        else:
            self.obtained = PIL.ImageTk.PhotoImage(image=PIL.Image.open(settings.catch_img_dir+"catched.jpg"))
        self.show_catched = self.canvas.create_image(0, 0, image=self.obtained,anchor = tkinter.NW)

        self.canvas.move(self.show_catched, 650, 0)

        self.window.after(self.delay, self.update)

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
            # if default:
            #     self.vid.set(cv2.CAP_PROP_FRAME_WIDTH,2688)
            #     self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT,1520)
            # else:
            #     self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            #     self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

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
App(tkinter.Tk(), "李之玉出品")