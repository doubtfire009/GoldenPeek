import cv2
import numpy
import settings.settings as settings


#
def img_processor(type="default"):

    # cv2.imwrite(settings.catch_dest+"catched.jpg", showing_frame)
    # settings.click_frame = 1
    if type=="default":
        return debug_img_processor_default()

def debug_img_processor_default():
    threshold = settings.process_threshold
    print(threshold)
    img = cv2.imread(settings.catch_dest+"catched.jpg", cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, th1 = cv2.threshold(gray, int(threshold), 255, cv2.THRESH_BINARY)
    cv2.imwrite(settings.process_img_dir + "processed_gray.jpg", gray)
    cv2.imwrite(settings.process_img_dir + "processed_th1.jpg", th1)
    image, contours, hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    area_max = 0
    key = 0
    key_max = 0
    for element in contours:
        area = cv2.contourArea(contours[key])
        if area_max<area:
            area_max = area
            key_max = key
        key = key+1

    (x, y), radius = cv2.minEnclosingCircle(contours[key_max])

    img = cv2.circle(img, (int(x),int(y)), int(radius), (0, 255, 0), 2)
    cv2.imwrite(settings.process_img_dir + "processed.jpg", img)
    return x,y,area_max,radius,threshold