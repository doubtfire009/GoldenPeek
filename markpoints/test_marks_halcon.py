import cv2
def vertexFinder(xList,yList):
    xMaxIndex = max(xList)
    yMaxIndex = max(yList)
    xMinIndex = min(xList)
    yMinIndex = min(yList)

    if xList.count(xMaxIndex)==1:
        xMax_y = [xMaxIndex, yList[xList.index(xMaxIndex)]]
        xMin_y = [xMinIndex, yList[xList.index(xMinIndex)]]
        x_yMax = [xList[yList.index(yMaxIndex)], yMaxIndex]
        x_yMin = [xList[yList.index(yMinIndex)], yMinIndex]
    else:
        xMax_y = [xMaxIndex, yList[xList.index(xMaxIndex)]]
        xMin_y = [xMinIndex, yList[xList.index(xMinIndex)]]
        x_yMax = [xList[yList.index(yMaxIndex)], yMaxIndex]
        x_yMin = [xList[yList.index(yMinIndex)], yMinIndex]
    # xMax_y = (xMaxIndex,yList[xList.index(xMaxIndex)])
    # xMin_y = (xMinIndex,yList[xList.index(xMinIndex)])
    # x_yMax = (xList[yList.index(yMaxIndex)],yMaxIndex)
    # x_yMin = (xList[yList.index(yMinIndex)],yMinIndex)



    print([xMax_y,xMin_y,x_yMax,x_yMin])
    return [xMax_y,xMin_y,x_yMax,x_yMin]

threshold = 160
img = cv2.imread("./img/halcon.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, th1 = cv2.threshold(gray, int(threshold), 255, cv2.THRESH_BINARY)
# cv2.imwrite(settings.process_img_dir + "processed_gray.jpg", gray)
# cv2.imwrite(settings.process_img_dir + "processed_th1.jpg", th1)
image, contours, hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img,contours,-1,(0,0,255),3)
# cv2.circle(img, (874, 1503), 100, (55, 255, 155), 30)
key = 0
xList = []
yList = []
for element in contours:
    (x, y), radius = cv2.minEnclosingCircle(contours[key])
    xList.append(x)
    yList.append(y)
    # cv2.circle(img, (int(x), int(y)), 3, (55, 255, 155), 2)  # 修改最后一个参数
    key = key + 1
print(xList)
print(yList)
Vertexes = vertexFinder(xList,yList)

# for i in Vertexes:
#
#     cv2.circle(img, (int(i[0]),int(i[1])), 3, (55, 255, 155), 2)  # 修改最后一个参数

    # print(Vertexes.index(i))
cv2.circle(img, (60,320), 3, (55, 255, 155), 2)  # 修改最后一个参数
cv2.imshow("mark1", img)

cv2.waitKey(0)


def ListMaxFinder(list):
    return list.index(max(list)),max(list)

def ListMinFinder(list):
    return list.index(min(list)),min(list)

