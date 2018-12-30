import cv2
import settings.settings as settings



def img_catch(showing_frame,displayerFlag=settings.CATCHED):

    showing_frame = cv2.cvtColor(showing_frame, cv2.COLOR_BGR2RGB)

    if displayerFlag == settings.CATCHED:
        cv2.imwrite(settings.catch_img_dir+displayerFlag+".jpg", showing_frame)
    if displayerFlag == settings.HALCON:
        cv2.imwrite(settings.halcon_img_dir + displayerFlag + ".jpg", showing_frame)
    if displayerFlag == settings.PROCESSED:
        cv2.imwrite(settings.process_img_dir + displayerFlag + ".jpg", showing_frame)

    settings.displayerFlag = displayerFlag




