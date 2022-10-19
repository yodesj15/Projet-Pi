import cv2
import numpy as np
# from robot import Robot
import time


class Camera:
    def __init__(self):
        self.vcap = cv2.VideoCapture(0)
        self.vcap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.vcap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        # self.robot = Robot()

        # teinte = 197
        # sat_min = 98
        # sat_max = 255
        # val_min = 135
        # val_max = 215
        # delta = 25

        # self.teinte_min = np.array([teinte - delta, sat_min, val_min])
        # self.teinte_max = np.array([teinte + delta, sat_max, val_max])

        if not self.vcap.isOpened():
            print("Impossible d'ouvrir la caméra")
            exit()

    def set_camera(self):
        ret_sts, frame_bgr = self.vcap.read()

        # frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
        # frame_disc = cv2.inRange(frame_hsv, self.teinte_min, self.teinte_max)
        # contours, _ = cv2.findContours(
        #     frame_disc, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # if len(contours) > 0:
        #     aire_max = 0
        #     plus_grand = 0
        #     for c in contours:
        #         x, y, l, h = cv2.boundingRect(c)
        #         aire_rect = l*h

        #         if aire_rect > aire_max:
        #             aire_max = aire_rect
        #             plus_grand = x, y, l, h

        #     aire = plus_grand[2] * plus_grand[3]
        #     print(aire)
        #     max = 12000
        #     min = 150
        #     limite_loin = 1500

        #     if aire <= min:
        #         self.robot.rien()
        #         print('Balle trop loin')

        #     elif aire >= max:
        #         self.robot.rien()
        #         print('Balle trop près')

        #     elif aire <= limite_loin:
        #         print("avancer loin")
        #         self.robot.avancer(0.2)

        #     elif plus_grand[0] >= 0 and plus_grand[0] < 80:
        #         self.robot.tourner_gauche(0.3)
        #         print('gauche')

        #     elif plus_grand[0] >= 80 and plus_grand[0] < 150:
        #         print('avancer')
        #         self.robot.avancer(0.2)

        #     elif plus_grand[0] >= 150 and plus_grand[0] < 300:
        #         print('droite')
        #         self.robot.tourner_droite(0.3)
        # else:

        #     self.robot.rien()

        cv2.imshow("Image disc", frame_bgr)

    def execution(self):
        while True:
            self.set_camera()

            choix = cv2.waitKey(33)
            if choix == ord('q'):
                break
        self.vcap.release()
        cv2.destroyAllWindows()
