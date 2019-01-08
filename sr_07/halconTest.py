import cv2
import numpy as np




def vertexFinder(xList, yList):
    xMaxIndex = max(xList)
    yMaxIndex = max(yList)
    xMinIndex = min(xList)
    yMinIndex = min(yList)

    if xList.count(xMaxIndex) == 1:
        xMax_y = [xMaxIndex, yList[xList.index(xMaxIndex)]]
        xMin_y = [xMinIndex, yList[xList.index(xMinIndex)]]
        x_yMax = [xList[yList.index(yMaxIndex)], yMaxIndex]
        x_yMin = [xList[yList.index(yMinIndex)], yMinIndex]
    else:
        xMax_y = [xMaxIndex, yMaxIndex]
        xMin_y = [xMinIndex, yMinIndex]
        x_yMax = [xMinIndex, yMaxIndex]
        x_yMin = [xMaxIndex, yMinIndex]

    return [xMax_y, xMin_y, x_yMax, x_yMin]

dir = "/Users/liz187/Documents/chisheng/GoldenPeek/sr_07/images_storage/catched/"
img = cv2.imread(dir+"test.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite(dir + "halconGray.jpg", gray)
ret, th1 = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
cv2.imwrite(dir + "halconGray1.jpg", th1)

image, contours, hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours, -1, (0, 0, 255), 3)

key = 0
xList = []
yList = []
for element in contours:
    (x, y), radius = cv2.minEnclosingCircle(contours[key])
    xList.append(x)
    yList.append(y)
    key = key + 1

Vertexes = vertexFinder(xList, yList)

pointsFont = ['A', 'B', 'C', 'D']
for i in Vertexes:
    cv2.circle(img, (int(i[0]), int(i[1])), 3, (55, 255, 155), 2)  # 修改最后一个参数
    cv2.putText(img, str(pointsFont[Vertexes.index(i)]), (int(i[0]), int(i[1])), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (0, 255, 0), 3)

cv2.imwrite(dir + "halconKK.jpg", img)
cv2.namedWindow('myimg1')
cv2.imshow('halconKK',img)
cv2.waitKey()
cv2.destroyAllWindows()


