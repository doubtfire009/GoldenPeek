import cv2
import settings.settings as settings


#
def img_catch(showing_frame):

    cv2.imwrite(settings.catch_dest+"catched.jpg", showing_frame)
    settings.click_frame = 1

