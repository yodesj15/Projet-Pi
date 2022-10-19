# Auteurs                 Date              Commentaires
#                          13 Avril 2022  Classe camera,
# BOUTIN-DUFOUR Anthony
# BOUCHER-BEAUDIN Erick
#
#
#
import cv2

class Camera:
    def __init__(self):
        self.__vcap = cv2.VideoCapture(0)
        self.__done = False

    def demarrer(self):
        self.__vcap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) #320
        self.__vcap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)#240
        self.__vcap.set(cv2.CAP_PROP_FPS,60)
        while not self.__done:
            ok,image=self.__vcap.read()
            if not ok:
                print("Erreur durant la capture de l'image")
                break

            cv2.imshow("Vidéo",image)
            choix = cv2.waitKey(1) #1

            if choix == ord('x'):
                self.__done = True
                break
