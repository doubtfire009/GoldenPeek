
#coding=utf-8
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import math
import gc
#
import settings.settings as settings
import image_catcher.img_catcher as i_c



window = tk.Tk()
window.title('my window')
window.geometry('1500x1000')


width, height = 2976/6, 3968/6

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
tkimg = tkimg1 = None
@profile
def show_frame(cap):

    # # get a frame
    ret, frame = cap.read()

    settings.showing_frame = frame

    # ret, frame = cap.read()

    frame_res = cv2.resize(frame, (round(width), round(height)), interpolation=cv2.INTER_CUBIC)
    cv2image = cv2.cvtColor(frame_res, cv2.COLOR_BGR2RGB)

    img = Image.fromarray(cv2image)

    tkimg = ImageTk.PhotoImage(img)  #
    label = tk.Label(window)

    label.imgtk = tkimg
    label.configure(image=tkimg)
    label.grid(row=0, column=0, columnspan=1, rowspan=1, padx=5, pady=5, sticky='s')

    # # cv2.imshow('test',cv2image)
    del(frame)
    del(frame_res)
    del(cv2image)
    del(img)
    del(tkimg)
    del(label)
    #
    # #
    # if settings.click_frame == 0:
    #     s = './mountain.jpg'  #
    # else:
    #     s = settings.catch_img_dir+"catched.jpg"  #
    #
    # im1=Image.open(s)
    # im1.thumbnail((width, height))
    # tkimg1=ImageTk.PhotoImage(im1) #
    #
    # label = tk.Label(window)
    # label.imgtk = tkimg1
    # label.configure(image=tkimg1)
    # label = tk.Label(window,image=tkimg1)
    # label.grid(row=0, column=1, columnspan=1, rowspan=1, padx=5, pady=5,sticky='s')
    #
    # del (im1)
    # del (tkimg1)
    # del (label)

    gc.collect()
    window.after(10, show_frame,cap)


show_frame(cap)


button1 = tk.Button(window, text='save',command=lambda:i_c.img_catch(settings.showing_frame))
button1.grid(row=1, column=0)
button2 = tk.Button(window, text='process')
button2.grid(row=1, column=1)



window.mainloop()






