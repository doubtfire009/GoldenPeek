import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
#
import settings.settings as settings
import image_catcher.img_catcher as i_c

class App:
    def __init__(self, window, window_title, video_source=1):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = 2*self.vid.width, height = self.vid.height)
        self.canvas.grid(row=0, column=0, columnspan=1, rowspan=1, padx=5, pady=5, sticky='s')
        # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.grid(row=1, column=0, columnspan=1, rowspan=1, padx=5, pady=5, sticky='s')
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        #keep obtaining the img on the canvas
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame(self,1)

        if ret:
            # cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            i_c.img_catch(frame)

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

        self.canvas.move(self.show_catched, 800, 0)

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
App(tkinter.Tk(), "Tkinter and OpenCV")