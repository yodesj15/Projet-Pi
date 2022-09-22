# Auteurs                 Date              Commentaires
#                          13 Avril 2022  Main pour exécuter,
# BOUTIN-DUFOUR Anthony
# BOUCHER-BEAUDIN Erick
#
#
#
from classe_robot import Robot
from classe_camera import Camera
import time
import threading

robot = Robot()
camera = Camera()

threadRobot = threading.Thread(target=robot.demarrerRobot)
threadCamera = threading.Thread(target=camera.demarrer)

threadRobot.start()
threadCamera.start()