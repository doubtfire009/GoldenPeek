
#coding=utf-8
import tkinter as tk
from PIL import Image, ImageTk
import cv2
#引入自定义的模块
import settings.settings as settings
import image_catcher.img_catcher as i_c




# width, height = 2976/6, 3968/6
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
#
# ret, frame = cap.read()
#
# cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
catch_dest = 'images_storage/catched/'
cap = cv2.VideoCapture(0)
while(1):
    # get a frame
    ret, frame = cap.read()
    # show a frame
    cv2.imshow("capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite(catch_dest+"catched.jpg", frame)
        break
cap.release()
cv2.destroyAllWindows()






