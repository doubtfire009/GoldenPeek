import cv2
import numpy as np
import settings.settings as settings

def isnumber(aString):
    try:
        float(aString)
        return True
    except:
        return False

def halconPoints():
    img = cv2.imread(settings.catch_img_dir + "catched.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, th1 = cv2.threshold(gray, int(settings.halconThreshold), 255, cv2.THRESH_BINARY)

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

    # pointsFont = ['xMax_y', 'xMin_y', 'x_yMax', 'x_yMin']
    pointsFont = ['A', 'B', 'C', 'D']
    for i in Vertexes:
        cv2.circle(img, (int(i[0]), int(i[1])), 3, (55, 255, 155), 2)  # 修改最后一个参数
        cv2.putText(img, str(pointsFont[Vertexes.index(i)]), (int(i[0]), int(i[1])), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    cv2.imwrite(settings.halcon_img_dir + "halcon.jpg", img)


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

    settings.xMax_y = xMax_y
    settings.xMin_y = xMin_y
    settings.x_yMax = x_yMax
    settings.x_yMin = x_yMin
    settings.halconReview = [xMax_y, xMin_y, x_yMax, x_yMin]
    return [xMax_y, xMin_y, x_yMax, x_yMin]


# Check Robot points whether they are legal
def reviewRobotPoints():
    # print("reviewRobotPoints")
    halconReview = settings.halconReview

    flagRobotPoints = 0
    NoP1 = 0
    NoP2 = 0
    for itemI in halconReview:
        i = halconReview.index(itemI)
        for itemJ in halconReview:
            j = halconReview.index(itemJ)
            if j>i:
                halconReviewMatrix = np.matrix([
                    [itemI[0],itemI[1]],
                    [itemJ[0], itemJ[1]],
                ]);
                if halconReviewMatrix.ndim == 2:
                    flagRobotPoints = 1
                    NoP1 = i
                    NoP2 = j
                    break
        if flagRobotPoints == 1:
            break

    return NoP1,NoP2,flagRobotPoints




def halconCollectionCheck(halconCollection):
    illegalFlag = 1

    for halconItem in halconCollection:
        if halconItem[0] == '' or halconItem[1] == '':
            illegalFlag = 0
        else:
            if isnumber(halconItem[0]) and isnumber(halconItem[1]):
                pass
            else:
                illegalFlag = 0

    return illegalFlag




# halconPoints are obtained from the catched image.
# robotPoints are from the robot arms.
def marksHalconReverseConverter(halconP1 = (0,0),halconP2 = (0,0),robotP1 = (0,0),robotP2 = (0,0)):
    halconPointsMatrix = np.matrix([
        [float(halconP1[0]),float(halconP1[1])],
        [float(halconP2[0]), float(halconP2[1])]
    ])

    robotPointsMatrix = np.matrix([
        [float(robotP1[0]), float(robotP1[1])],
        [float(robotP2[0]), float(robotP2[1])]
    ])
    print(halconPointsMatrix)
    print(robotPointsMatrix)

    MatrixHalcon = (halconPointsMatrix.I)*robotPointsMatrix

    settings.halconConverterMatrix = MatrixHalcon








def modbusTransferrer():
    print("modbusTransferrer")