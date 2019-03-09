import cv2
import numpy as np
import settings.settings as settings
import os

#
def img_processor(type="default"):

    if type == "default":
        return default_img_processor_default()
    elif type == "hough":
        return hough_img_processor_default()
    elif type == "ellipse":
        return ellipse_img_processor_default()
    halconConverter()

def default_img_processor_default():
    thresholdCal = settings.thresholdInfo['finder']['cal']
    thresholdArea = settings.thresholdInfo['finder']['area']
    result = [[0,0]]

    img = cv2.imread(settings.catch_img_dir+"catched.jpg", cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, th1 = cv2.threshold(gray, int(thresholdCal['low']), int(thresholdCal['high']), cv2.THRESH_BINARY)
    cv2.imwrite(settings.process_img_dir + "processed_gray.jpg", gray)
    cv2.imwrite(settings.process_img_dir + "processed_th1.jpg", th1)
    image, contours, hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours))
    key = 0
    for element in contours:
        area = cv2.contourArea(contours[key])

        if int(thresholdArea['low'])<=area and int(thresholdArea['high'])>area:

            (x, y), radius = cv2.minEnclosingCircle(contours[key])
            img = cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 0), 2)

            #转化成机械臂坐标
            print('halconConverterMatrix')
            print(settings.halconConverterMatrix)
            xyMatrx = np.matrix([
                [x,y]
            ])

            res = xyMatrx * settings.halconConverterMatrix

            res = res[0,:].tolist()
            result.append([res[0][0],res[0][1]])

        key = key+1

    cv2.imwrite(settings.process_img_dir + "processed.jpg", img)
    # 将result的长度写入第一个元素
    result[0][0] = len(result)

    settings.finderProcessResult = result

def hough_img_processor_default():
    thresholdCal = settings.thresholdInfo['finder']['cal']
    threshough = settings.thresholdInfo['finder']['hough']
    result = [[0,0]]

    img = cv2.imread(settings.catch_img_dir+"catched.jpg", cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, th1 = cv2.threshold(gray, int(thresholdCal['low']), int(thresholdCal['high']), cv2.THRESH_BINARY)
    cv2.imwrite(settings.process_img_dir + "processed_gray.jpg", gray)
    cv2.imwrite(settings.process_img_dir + "processed_th1.jpg", th1)

    settings.processCircle = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=int(settings.halconHoughParam1),
                                             param2=int(settings.halconHoughParam2), minRadius=int(threshough['halconHoughminRadius']),
                                              maxRadius=int(threshough['halconHoughmaxRadius']))

    print(settings.processCircle)
    halconConverterMatrix = np.array(settings.halconConverterMatrix)

    for i in settings.processCircle[0, :]:
        # draw the outer circle
        cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # draw the center of the circle
        cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

        # circleImg = np.mat(i)
        #
        # settings.finderProcessResult.append(circleImg * halconConverterMatrix)

    cv2.imwrite(settings.process_img_dir + "processed.jpg", img)

def ellipse_img_processor_default ():
    thresholdCal = settings.thresholdInfo['finder']['cal']
    settings.processCircle = []

    img = cv2.imread(settings.catch_img_dir + "catched.jpg", cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, th1 = cv2.threshold(gray, int(thresholdCal['low']), int(thresholdCal['high']), cv2.THRESH_BINARY)
    cv2.imwrite(settings.process_img_dir + "processed_gray.jpg", gray)
    cv2.imwrite(settings.process_img_dir + "processed_th1.jpg", th1)
    image, contours, hierarchy = cv2.findContours(th1, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    imgContour = cv2.drawContours(img, contours, -1, (255,255,255),-1)

    iCgray = cv2.cvtColor(imgContour, cv2.COLOR_BGR2GRAY)

    iCret, iCth1 = cv2.threshold(iCgray, int(thresholdCal['low']), int(thresholdCal['high']), cv2.THRESH_BINARY)

    iCimage, iCcontours, iChierarchy = cv2.findContours(iCth1, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    for iCcontour in iCcontours:
        if (iCcontour.shape)[0] >= 5:
            ellipse = cv2.fitEllipse(iCcontour)
            settings.processCircle.append([ellipse[0][0], ellipse[0][1]])
            cv2.ellipse(img, ellipse, (255, 0, 255), 1, cv2.LINE_AA)

    cv2.imwrite(settings.process_img_dir + "processed.jpg", img)


def halconConverter():

    processCircle = (np.array(settings.processCircle)).transpose()

    kConverter = np.array([
        [settings.halconConverterX[0], 0],
        [0, settings.halconConverterY[0]]
    ])
    bConverter = np.array([
        [settings.halconConverterX[1], settings.halconConverterY[1]]
    ])

    finderProcessResult = kConverter * processCircle + bConverter
    settings.finderProcessResult = finderProcessResult.tolist()



def writeTxt():

    fobj = open(settings.process_img_dir + "processed.txt", 'w')
    for robot in settings.finderProcessResult:
        fobj.write('\n' + robot[0] + ',' + robot[1])

    fobj.close()