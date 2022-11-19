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

threadLidarIsStarted = False
app = Flask(__name__)
pi_camera = VideoCamera(flip=False)  # flip pi camera if upside down.

lidar = Lidar("/dev/ttyUSB0")  # "/dev/ttyUSB1"    "/dev/ttyACM0"
robot = Robot()

# x = input('Veuillez entrez la position en x du anchor 1 : ')
# y = input('Veuillez entrez la position en y du anchor 1 : ')
anchor1 = Anchor(22, 33)

# x = input('Veuillez entrez la position en x du anchor 2 : ')
# y = input('Veuillez entrez la position en y du anchor 2 : ')
anchor2 = Anchor(11, 10)

# x = input('Veuillez entrez la position en x du anchor 3 : ')
# y = input('Veuillez entrez la position en y du anchor 3 : ')
anchor3 = Anchor(4, 21)

# x = input('Veuillez entrez la position en x du anchor 4 : ')
# y = input('Veuillez entrez la position en y du anchor 4 : ')
anchor4 = Anchor(3, 1)

map = Map(anchor1, anchor2, anchor3, anchor4, lidar)
threadLidar = Thread(target=lidar.getData)
threadLidar.start()

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def genMap(map):
    #get camera frame
    while True:
        f = map.get_map()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + f + b'\r\n\r\n')


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
    
    return Response(genMap(map),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/reset')
def reset():
    lidar.reset_lidar()
    print("Lidar reset")


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
        print("speed changed to " + str(robot.moteur.__vitesse))

    #code exécuter à chaque action

    #positionnement des anchors

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
