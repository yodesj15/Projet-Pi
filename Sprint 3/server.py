from flask import Flask, render_template, Response, request, send_from_directory
from classe_moteur import Moteur
from classe_robot import Robot
from classe_radionav import RadioNav, Anchor

from camera import VideoCamera
import matplotlib.pyplot as plt
from threading import Thread
import datetime
from classe_map import Map
from classe_lidar import Lidar
from enum import Enum

#threadLidarIsStarted = False
app = Flask(__name__)
pi_camera = VideoCamera(flip=False)  # flip pi camera if upside down.

robot = Robot()
lidar = Lidar("/dev/ttyUSB1", robot)  # "/dev/ttyUSB1"    "/dev/ttyACM0"
radio_nav = RadioNav("/dev/ttyACM1", robot)

Etat = Enum('Etat', 'innactif actif')

# x = input('Veuillez entrez la position en x du anchor 1 : ')
# y = input('Veuillez entrez la position en y du anchor 1 : ')
anchor1 = Anchor(0, 0)

# x = input('Veuillez entrez la position en x du anchor 2 : ')
# y = input('Veuillez entrez la position en y du anchor 2 : ')
anchor2 = Anchor(2.73, 0)

# x = input('Veuillez entrez la position en x du anchor 3 : ')
# y = input('Veuillez entrez la position en y du anchor 3 : ')
anchor3 = Anchor(0.34, 3.81)

# x = input('Veuillez entrez la position en x du anchor 4 : ')
# y = input('Veuillez entrez la position en y du anchor 4 : ')
anchor4 = Anchor(0, 0)

map = Map(anchor1, anchor2, anchor3, anchor4, robot, lidar)
threadLidar = Thread(target=lidar.getData)
threadLidar.start()

threadRadioNav = Thread(target=radio_nav.execution)
threadRadioNav.start()


def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def genMap(map, radio_nav):
    #get camera frame
    while True:
        f = map.get_map(radio_nav)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + f + b'\r\n\r\n')


def genMapLidar(map, radio_nav):
    while True:
        
        f = map.get_map(radio_nav) #ici il faut mettre la fonction qui dessine dans une map
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + f + b'\r\n\r\n')


@app.route('/offLidar')
def offLidar():
   lidar.disconnect()
   print("Lidar reset")


@app.route('/showLidar')
def showLidar():
    #ici tu dois ajouter pour faire afficher la map
    pass


@app.route('/')
def index():

    return render_template('index.html')
    # return render_template('cam.html')


@app.route('/video_feed')
def video_feed():

    # lidar.__done  = True
    # threadLidar.join()

    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/map_feed')
def map_feed():

    return Response(genMap(map, radio_nav),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/lidar_feed')
def lidar_feed():
    #ici il faut mettre la fonction qui dessine dans une map dans le return
    return Response(genMap(map, radio_nav),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/reset')
def reset():
   print("Lidar + radionav reset")
   lidar.reset_lidar()
   radio_nav.reset_radio_nav()


@app.route("/<deviceName>/<action>/<vitesse>")
def action(deviceName, action, vitesse):
    actionneur = ""
    v = float(vitesse) * 0.1

    if deviceName == 'moteur':
        actionneur = robot.moteur

    if action == "on":
        actionneur.on()
    if action == "off":
        actionneur.off()
    if action == "forward":
        robot.moteur.avancer(v)
        robot.etat = Etat.actif
    if action == "backward":
        robot.moteur.reculer(v)
        robot.etat = Etat.actif
    if action == "left":
        robot.moteur.tourner_gauche(v)
        robot.etat = Etat.actif
    if action == "right":
        robot.moteur.tourner_droite(v)
        robot.etat = Etat.actif
    if action == "stop":
        robot.moteur.reset()
        robot.etat = Etat.innactif
    if action == "speed":
        robot.moteur.__vitesse = v

    #code exécuter à chaque action

    #positionnement des anchors

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
