# Auteurs                 Date              Commentaires
#                          29 novembre 2022  Projet Intégration,
# BOUTIN-DUFOUR Anthony
# BOUCHER-BEAUDIN Erick
# DESJARDINS Yoan
# BERGEVIN Émeric
#
from flask import Flask, render_template, Response, request, send_from_directory
from classe_moteur import Moteur
from classe_robot import Robot
from classe_radionav import RadioNav, Anchor

from camera import VideoCamera
import matplotlib.pyplot as plt
from threading import Thread
import datetime,time
from classe_map import Map
from classe_lidar import Lidar
from classe_radar import Radar
from enum import Enum

app = Flask(__name__)
pi_camera = VideoCamera(flip=False)  # flip pi camera if upside down.

robot = Robot()
lidar = Lidar("/dev/ttyUSB0", robot)  # "/dev/ttyUSB1"    "/dev/ttyACM0"
radar = Radar(lidar)

radio_nav = RadioNav("/dev/ttyACM0", robot)

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
anchor4 = Anchor(1.34, 3.81)

map = Map(anchor1, anchor2, anchor3, anchor4, robot, lidar)

threadRadioNav = Thread(target=radio_nav.execution)
threadRadioNav.start()
threadLidar = Thread(target=lidar.getData)
threadLidar.start()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def genMap(map):
    while True:
        f = map.get_map()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + f + b'\r\n\r\n')


def genRadar(radar):
    while True:

        f = radar.get_radar()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + f + b'\r\n\r\n')


@app.route('/offLidar')
def offLidar():
    lidar.done = True 
    threadLidar.join()
    lidar.disconnect()
    
    
    print("Lidar reset")
    # return render_template('index.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/map_feed')
def map_feed():
    return Response(genMap(map),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/lidar_feed')
def lidar_feed():
    return Response(genRadar(radar),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/reset')
def reset():
    print("radionav reset")
    # radio_nav.robot.done = True
    # threadRadioNav.join()
    radio_nav.reset_radio_nav()
    # print(str(radio_nav.x_pos))
    # time.sleep(2)
    # return render_template('index.html')
    
    # lidar.done = True 
    # threadLidar.join()
    # lidar.reset_lidar()
    # threadLidar.start()
    
    


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
    if action == "backward":
        robot.moteur.reculer(v)
    if action == "left":
        robot.moteur.tourner_gauche(v)
    if action == "right":
        robot.moteur.tourner_droite(v)
    if action == "stop":
        robot.moteur.reset()
    if action == "speed":
        robot.moteur.__vitesse = v

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
