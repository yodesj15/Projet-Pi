# Auteurs                 Date              Commentaires
#                          26 Septembre 2022  Main pour exécuter,
# BOUTIN-DUFOUR Anthony
# BOUCHER-BEAUDIN Erick
# BERGEVIN Émeric
# DESJARDINS Yoan
#
from classe_robot import Robot
from classe_camera import Camera
from classe_lidar import Lidar
import time
import threading

robot = Robot()
camera = Camera()
lidar = Lidar("/dev/ttyUSB1")

threadRobot = threading.Thread(target=robot.demarrerRobot)
threadCamera = threading.Thread(target=camera.demarrer)
threadLidar = threading.Thread(target=lidar.getData)

threadLidar.start()
threadRobot.start()
threadCamera.start()

lidar.disconect()