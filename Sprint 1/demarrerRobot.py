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
from classe_radionav import RadioNav

import time
import threading

robot = Robot()
camera = Camera()
lidar = Lidar("/dev/ttyUSB0")
radio_nav = RadioNav("/dev/ttyACM0")


threadRobot = threading.Thread(target=robot.demarrerRobot)
threadCamera = threading.Thread(target=camera.demarrer)
threadLidar = threading.Thread(target=lidar.getData)
threadRadioNav = threading.Thread(target=radio_nav.execution)


threadLidar.start()
threadRobot.start()
threadCamera.start()
threadRadioNav.start()



#lidar.disconect()