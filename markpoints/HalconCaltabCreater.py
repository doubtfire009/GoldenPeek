import cv2
import numpy as np

width = 594
height = 420
length = 80

radius = 20
circleGap =60

image = np.zeros((height,width),dtype = np.uint8)
# image = np.ones((height,width),dtype = np.uint8)
# cv2.circle(image, (circleGap+400, circleGap), radius, 255, -1)
for i in range(height):

    if ((int)(i%length)==0) and i>0:
        for j in range(width):
            if((int)(j%circleGap)==0) and j>0:
                if (i+radius)<height:
                    cv2.circle(image, (j, i), radius, 255, -1)

# for i in range(height):
#     print(i)
#     for j in range(width):
#         image[i][j] = 255 - image[i][j]




# cv2.circle(image, (i, j*circleGap), radius, 255, -1)
cv2.imwrite("./img/halcon.jpg",image)
cv2.imshow("halcon",image)
cv2.waitKey(0)

