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

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(settings.halcon_img_dir + "halconGray.jpg", gray)
    ret, th1 = cv2.threshold(gray, int(settings.halconThreshold), 255, cv2.THRESH_BINARY)
    cv2.imwrite(settings.halcon_img_dir + "halconThreshold.jpg", th1)
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
        cv2.putText(img, str(pointsFont[Vertexes.index(i)]), (int(i[0]), int(i[1])), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    cv2.imwrite(settings.halcon_img_dir + "halcon.jpg", img)

def halconHoughPoints():
    img = cv2.imread(settings.catch_img_dir + "catched.jpg")


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(settings.halcon_img_dir + "halconGray.jpg", gray)


    ret, th1 = cv2.threshold(gray, int(settings.halconThreshold), 255, cv2.THRESH_BINARY)

    cv2.imwrite(settings.halcon_img_dir + "halconThreshold.jpg", th1)

    # circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 100,
    #                            param1=100, param2=30, minRadius=100, maxRadius=200)
    # https://blog.csdn.net/tengfei461807914/article/details/77507820
    settings.halconCircle = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=int(settings.halconHoughParam1), param2 = int(settings.halconHoughParam2), minRadius = int(settings.thresholdInfo['halcon']['halcon']['halconHoughminRadius']), maxRadius = int(settings.thresholdInfo['halcon']['halcon']['halconHoughmaxRadius']))
    settings.halconCircle = settings.halconCircle[0]

    key = 0
    for circle in settings.halconCircle:
        # 圆的基本信息
        # 坐标行列
        x = int(circle[0])
        y = int(circle[1])
        # 半径
        r = int(circle[2])
        # 在原图用指定颜色标记出圆的位置
        img = cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        cv2.putText(img, str(key), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0, 0, 255), 1)
        key = key + 1

    cv2.imwrite(settings.halcon_img_dir + "halcon.jpg", img)


def halconEllipsePoints():
    img = cv2.imread(settings.catch_img_dir + "catched.jpg")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(settings.halcon_img_dir + "halconGray.jpg", gray)

    ret, th1 = cv2.threshold(gray, int(settings.halconThreshold), 255, cv2.THRESH_BINARY)

    cv2.imwrite(settings.halcon_img_dir + "halconThreshold.jpg", th1)

    image, contours, hierarchy = cv2.findContours(th1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    imgContour = cv2.drawContours(img, contours, -1, (255, 255, 255), -1)

    iCgray = cv2.cvtColor(imgContour, cv2.COLOR_BGR2GRAY)

    iCret, iCth1 = cv2.threshold(iCgray, int(settings.halconThreshold), 255, cv2.THRESH_BINARY)

    iCimage, iCcontours, iChierarchy = cv2.findContours(iCth1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    settings.halconCircle = []
    for iCcontour in iCcontours:
        if (iCcontour.shape)[0] >= 5:
            ellipse = cv2.fitEllipse(iCcontour)
            settings.halconCircle.append([ellipse[0][0], ellipse[0][1]])
            cv2.ellipse(img, ellipse, (255, 0, 255), 1, cv2.LINE_AA)

    cv2.imwrite(settings.halcon_img_dir + "halcon.jpg", img)


def vertexFinder(xList, yList):
    xMaxIndex = max(xList)
    yMaxIndex = max(yList)
    xMinIndex = min(xList)
    yMinIndex = min(yList)

    #说明四个点是分开的
    if xList.count(xMaxIndex) == 1:
        xMax_y = [xMaxIndex, yList[xList.index(xMaxIndex)]]
        xMin_y = [xMinIndex, yList[xList.index(xMinIndex)]]
        x_yMax = [xList[yList.index(yMaxIndex)], yMaxIndex]
        x_yMin = [xList[yList.index(yMinIndex)], yMinIndex]
    # 说明四个点有重合
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
def reviewRobotPoints(halconCollection):

    if (halconCollection[0][0] == halconCollection[1][0]
            or halconCollection[0][1] == halconCollection[1][1]
            or halconCollection[0][2] == halconCollection[1][2]):
        flagRobotPoints = 0
    else:
        flagRobotPoints = 1

    return flagRobotPoints




def halconCollectionCheck(halconCollection):
    illegalFlag = 1

    for halconItem in halconCollection:
        if halconItem[0] == '' or halconItem[1] == '' or halconItem[2] == '':
            illegalFlag = 0
        else:
            if isinstance(halconItem[0],int) and isnumber(halconItem[1]) and isnumber(halconItem[1]):
                pass
            else:
                illegalFlag = 0

    return illegalFlag




# halconPoints are obtained from the catched image.
# robotPoints are from the robot arms.
def marksHalconReverseConverter(halconCollection):

    halconAssembleX = np.array([
        [settings.halconCircle[halconCollection[0][0]][0], settings.halconCircle[halconCollection[1][0]][0]],
        [1, 1]
    ])
    halconAssembleY = np.array([
        [settings.halconCircle[halconCollection[0][0]][1], settings.halconCircle[halconCollection[1][0]][1]],
        [1, 1]
    ])
    robotAssembleX = np.array([
        [halconCollection[0][1], halconCollection[1][1]]
    ])
    robotAssembleY = np.array([
        [halconCollection[0][2], halconCollection[1][2]]
    ])

    halconConverterX = robotAssembleX * (halconAssembleX.I)
    halconConverterY = robotAssembleY * (halconAssembleY.I)

    settings.halconConverterX = halconConverterX.tolist()
    settings.halconConverterY = halconConverterY.tolist()


