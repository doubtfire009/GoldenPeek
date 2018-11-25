import cv2


threshold = 160
img = cv2.imread("./img/test_points.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, th1 = cv2.threshold(gray, int(threshold), 255, cv2.THRESH_BINARY)
# cv2.imwrite(settings.process_img_dir + "processed_gray.jpg", gray)
# cv2.imwrite(settings.process_img_dir + "processed_th1.jpg", th1)
image, contours, hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img,contours,-1,(0,0,255),3)
# cv2.circle(img, (874, 1503), 100, (55, 255, 155), 30)
key = 0
for element in contours:
    (x, y), radius = cv2.minEnclosingCircle(contours[key])
    print(x)
    print(y)
    cv2.circle(img, (int(x), int(y)), 3, (55, 255, 155), 2)  # 修改最后一个参数
    key = key + 1

cv2.imshow("mark1", img)
cv2.imwrite("./img/mark1_th.jpg", th1)
cv2.imwrite("./img/mark1_con.jpg", img)
cv2.waitKey(0)