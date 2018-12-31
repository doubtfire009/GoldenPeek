import cv2
import numpy as np
import settings.settings as settings

#
def img_processor(type="default"):

    if type=="default":
        return default_img_processor_default()

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