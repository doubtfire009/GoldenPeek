import  cv2
import numpy as np
import settings.settings as settings

#载入并显示图片
bilateralImg=cv2.imread(settings.catch_img_dir + "sample3.6/catched2.1.1.jpg")
cv2.imshow('img',bilateralImg)

# b, g, r = cv2.split(img)
# cv2.imshow("Blue 1", b)
# cv2.imshow("Green 1", g)
# cv2.imshow("Red 1", r)

#灰度化
gray=cv2.cvtColor(bilateralImg,cv2.COLOR_BGR2GRAY)




cv2.imshow('gray',gray)
ret, th1 = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
cv2.imshow('th1',th1)

canny = cv2.Canny(th1,10,200)
cv2.imshow('canny',canny)

image, contours, hierarchy = cv2.findContours(th1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)


# res = cv2.GaussianBlur(image, (size, size), 0, 0)

imgContour = cv2.drawContours(bilateralImg, contours, -1, (255,255,255),-1)
cv2.imshow('imgContour',imgContour)

#灰度化
ICgray=cv2.cvtColor(imgContour,cv2.COLOR_BGR2GRAY)

ICret, ICth1 = cv2.threshold(ICgray, 70, 255, cv2.THRESH_BINARY)
cv2.imshow('ICth1',ICth1)



#输出图像大小，方便根据图像大小调节minRadius和maxRadius
print(bilateralImg.shape)
print(gray.shape)
print(th1.shape)

# cv2.imwrite(settings.catch_img_dir + "test/gray.jpg",gray)
# cv2.imwrite(settings.catch_img_dir + "test/th1.jpg",th1)

key = 1

if key == 1:
    for contour in contours:
        #椭圆检测
        print(contour.shape)
        if (contour.shape)[0] >= 5:
            ellipse = cv2.fitEllipse(contour)

            print(ellipse)
            print("gggg")
            cv2.ellipse(bilateralImg, ellipse, (255,0, 255), 1, cv2.LINE_AA)
            # print(contour)
            # #在原图用指定颜色标记出圆的位置
            # img=cv2.circle(bilateralImg,(x,y),r,(0,0,255),2)
            #显示新图像
        else:
            print("sss")
    cv2.imshow('res',bilateralImg)

#按任意键退出
cv2.waitKey(0)
cv2.destroyAllWindows()