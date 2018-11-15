
#coding=utf-8
import tkinter as tk
from PIL import Image, ImageTk
import cv2





window = tk.Tk()
window.title('my window')
window.geometry('1500x1000')

# 这里是窗口的内容

# s=r'montain.jpg' # jpg图片文件名 和 路径。

s='./contour.jpg' # jpg图片文件名 和 路径。
im=Image.open(s)
w, h = im.size
im.thumbnail((w//6, h//6))

print(w)
print(h)

tkimg=ImageTk.PhotoImage(im) # 执行此函数之前， Tk() 必须已经实例化。

label = tk.Label(window,image=tkimg)
label.grid(row=0, column=0, columnspan=1, rowspan=1, padx=5, pady=5,sticky='s')

button1 = tk.Button(window, text='点击保存')
button1.grid(row=1, column=0)

s='./contour.jpg' # jpg图片文件名 和 路径。
im1=Image.open(s)
im1.thumbnail((w//5, h//5))
tkimg1=ImageTk.PhotoImage(im1) # 执行此函数之前， Tk() 必须已经实例化。
label = tk.Label(window,image=tkimg1)
label.grid(row=0, column=1, columnspan=1, rowspan=1, padx=5, pady=5,sticky='s')

button2 = tk.Button(window, text='点击处理')
button2.grid(row=1, column=1)



window.mainloop()



