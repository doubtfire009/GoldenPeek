import  cv2
import numpy as np
import settings.settings as settings

#载入并显示图片
img=cv2.imread(settings.catch_img_dir + "test/catched5.jpg")
cv2.imshow('img',img)

# b, g, r = cv2.split(img)
# cv2.imshow("Blue 1", b)
# cv2.imshow("Green 1", g)
# cv2.imshow("Red 1", r)

bilateralImg = cv2.bilateralFilter(img,9,75,75)
cv2.imshow('bilateralImg',bilateralImg)
#灰度化
gray=cv2.cvtColor(bilateralImg,cv2.COLOR_BGR2GRAY)




cv2.imshow('gray',gray)
ret, th1 = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)
cv2.imshow('th1',th1)

canny = cv2.Canny(th1,0,200)
cv2.imshow('canny',canny)

image, contours, hierarchy = cv2.findContours(th1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)


# res = cv2.GaussianBlur(image, (size, size), 0, 0)

imgContour = cv2.drawContours(bilateralImg, contours, -1, (255,255,255),-1)
cv2.imshow('imgContour',imgContour)

cv2.imwrite(settings.catch_img_dir + "test/imgContour.jpg",imgContour)





#输出图像大小，方便根据图像大小调节minRadius和maxRadius
print(img.shape)
print(gray.shape)
print(th1.shape)

# cv2.imwrite(settings.catch_img_dir + "test/gray.jpg",gray)
# cv2.imwrite(settings.catch_img_dir + "test/th1.jpg",th1)

key = 1

if key == 1:
    #霍夫变换圆检测
    circles= cv2.HoughCircles(th1,cv2.HOUGH_GRADIENT,1,5,param1=200,param2=13,minRadius=1,maxRadius=200)
    #输出返回值，方便查看类型
    print(circles)
    #输出检测到圆的个数
    # print(len(circles[0]))

    for circle in circles[0]:
        #圆的基本信息
        print(circle[2])
        #坐标行列
        x=int(circle[0])
        y=int(circle[1])
        #半径
        r=int(circle[2])
        #在原图用指定颜色标记出圆的位置
        img=cv2.circle(img,(x,y),r,(0,0,255),-1)
    #显示新图像
    cv2.imshow('res',img)

#按任意键退出
cv2.waitKey(0)
cv2.destroyAllWindows()