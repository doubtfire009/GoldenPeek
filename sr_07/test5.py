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
        # Create a combox for threshold
        self.combox = ttk.Combobox(window)
        self.combox['value'] = list(range(1,256))
        self.combox.state(['readonly'])
        self.combox.current(0)
        self.combox.bind("<<ComboboxSelected>>", self.thresholdset)
        self.combox.grid(row=1, column=0, columnspan=4, rowspan=1, padx=5, pady=5, sticky='s')
        # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="图像获取", width=50, command=self.snapshot)
        self.btn_snapshot.grid(row=2, column=0, columnspan=1, rowspan=1, padx=5, pady=5, sticky='s')

        # Button that process images
        self.btn_imgprocess = tkinter.Button(window, text="图像处理", width=50, command=self.img_process)
        self.btn_imgprocess.grid(row=2, column=1, columnspan=1, rowspan=1, padx=5, pady=5, sticky='s')
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
        x, y, area_max, radius,threshold = i_p.img_processor("default")
        messagebox.showinfo("x-y-area_max-radius-threshold", str(x)+"-"+str(y)+"-"+str(area_max)+"-"+str(radius)+"-"+str(threshold))


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