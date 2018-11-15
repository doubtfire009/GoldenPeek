import cv2
import numpy as np

width = 450
height = 350
length = 50

radius = 10
circleGap =50

image = np.zeros((height,width),dtype = np.uint8)
# cv2.circle(image, (circleGap, circleGap), radius, 255, -1)
for i in range((int)(height/circleGap)):
    # print(j*circleGap)
    for j in range(width):
        if((int)(i%circleGap)==0) and i*j > 0:
            cv2.circle(image, (i, j*circleGap), radius, 255, -1)
# cv2.circle(image, (i, j*circleGap), radius, 255, -1)
cv2.imwrite("./img/halcon.jpg",image)
cv2.imshow("halcon",image)
cv2.waitKey(0)

