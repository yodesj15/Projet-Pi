# Auteurs                 Date              Commentaires
#                          29 novembre 2022  Projet Intégration,
# BOUTIN-DUFOUR Anthony
# BOUCHER-BEAUDIN Erick
# DESJARDINS Yoan
# BERGEVIN Émeric
#
import cv2
import numpy as np
import time


class Radar:
    def __init__(self, lidar_param):
        self.lidar = lidar_param

        self.FACTEUR_PIXEL = 30
        self.FENETRE_WIDTH = 430
        self.FENETRE_HEIGHT = 430
        self.FENETRE_CENTRE_X = int(self.FENETRE_WIDTH / 2)
        self.FENETRE_CENTRE_Y = int(self.FENETRE_HEIGHT / 2)
        self.RADAR_WIDTH = 4
        self.RADAR_HEIGHT = 4

        self.img = np.zeros((430, 430, 3), np.uint8)

    def CalculerPointX(self, x):
        return int(self.FENETRE_CENTRE_X + ((float(x / 125) * self.FACTEUR_PIXEL)))

    def CalculerPointY(self, y):
        return int(self.FENETRE_CENTRE_Y + ((float(y / 125) * self.FACTEUR_PIXEL)))

    def get_radar(self):
        #Déterminer à l'aide de méthode MAP_WIDTH ainsi que MAP_HEIGHT

        self.P_INIT_X = int(self.FENETRE_CENTRE_X)
        self.P_INIT_Y = int(self.FENETRE_CENTRE_Y)

        #clear map
        self.img = np.zeros((430, 430, 3), np.uint8)

        #get distances points
        tab_x = self.lidar.tab_p_x
        tab_y = self.lidar.tab_p_y

        #distances points representation
        for i in range(0, 359):
            cv2.circle(self.img, (self.CalculerPointX(
                tab_x[i]), self.CalculerPointY(tab_y[i])), 10, (125, 125, 125), -1)

        #filtrage des points displayed
        # Creating kernel
        kernel = np.ones((8, 8), np.uint8)
        # Using cv2.erode() method
        self.img = cv2.erode(self.img, kernel)
        self.img = cv2.erode(self.img, kernel)
        #self.img = cv2.erode(self.img, kernel)

        #self.img = cv2.dilate(self.img, kernel, iterations=1)

        #draw ATH
        #cv2.line(self.img,(self.FENETRE_CENTRE_X - int(self.RADAR_WIDTH / 2),self.FENETRE_CENTRE_Y),(self.FENETRE_CENTRE_X + int(self.RADAR_WIDTH / 2),self.FENETRE_CENTRE_Y),(0,255,0),1)
        #cv2.line(self.img,(self.FENETRE_CENTRE_X,self.FENETRE_CENTRE_Y - int(self.RADAR_HEIGHT / 2)),(self.FENETRE_CENTRE_X,self.FENETRE_CENTRE_Y + int(self.RADAR_HEIGHT / 2)),(0,255,0),1)
        cv2.line(self.img, (0, 215), (430, 215), (0, 255, 0), 1)
        cv2.line(self.img, (215, 0), (215, 430), (0, 255, 0), 1)

        #robot representation in the map
        cv2.rectangle(self.img, (self.FENETRE_CENTRE_X - 26, self.FENETRE_CENTRE_Y - 24),
                      (self.FENETRE_CENTRE_X + 26, self.FENETRE_CENTRE_Y + 24), (255, 0, 0), 2)

        #flip image for graph representation
        self.img = cv2.flip(self.img, 1)
        cv2.rotate(self.img, cv2.ROTATE_90_CLOCKWISE)

        time.sleep(0.2)

        ret, jpeg = cv2.imencode(".jpg", self.img)
        return jpeg.tobytes()
