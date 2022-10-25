from flask import Flask, render_template, Response, request, send_from_directory
from gpiozero import DigitalOutputDevice
from gpiozero import DigitalInputDevice
from gpiozero import PWMOutputDevice
from camera import VideoCamera

import datetime

app = Flask(__name__)
pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

MoteurGIN1 = DigitalOutputDevice(6)
MoteurGIN2 = DigitalOutputDevice(5)
MoteurGENA = PWMOutputDevice(13)
MoteurDIN3 = DigitalOutputDevice(15)
MoteurDIN4 = DigitalOutputDevice(14)
MoteurDENB = PWMOutputDevice(18)

ledYlw = DigitalOutputDevice(9)
ledGrn = DigitalOutputDevice(10)
ledGrn.on()

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



def avancer(vitesse):
    MoteurGIN1.on()
    MoteurGENA.value = vitesse
    MoteurDIN3.on()
    MoteurDENB.value = vitesse


def arreter():
    MoteurGIN1.off()
    MoteurGIN2.off()
    MoteurDIN3.off()
    MoteurDIN4.off()


def reculer(vitesse):
    MoteurGIN2.on()
    MoteurGENA.value = vitesse
    MoteurDIN4.on()
    MoteurDENB.value = vitesse

    #méthode pour tourner à droite sur place.


def tourner_gaucheplace(vitesse):
    MoteurGENA.value = vitesse
    MoteurDENB.value = vitesse
    MoteurGENA.on()
    MoteurGIN1.on()
    MoteurDENB.on()
    MoteurDIN4.on()

    #méthode pour tourner à gauche sur place.


def tourner_droiteplace(vitesse):
    MoteurDENB.value = vitesse
    MoteurGENA.value = vitesse
    MoteurDENB.on()
    MoteurDIN3.on()
    MoteurGIN2.on()
    MoteurGENA.on()


@app.route('/')
def index():
    return render_template('index.html')
    # return render_template('cam.html')
    
@app.route('/joy')
def joy():
    return render_template('joy.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    actionneur = ""
    if deviceName == 'ledYlw':
        actionneur = ledYlw
    if deviceName == 'moteur':
        actionneur = MoteurDENB

    if action == "on":
        actionneur.on()
    if action == "off":
        actionneur.off()
    if action == "forward":
        arreter()
        avancer(0.3)
    if action == "backward":
        arreter()
        reculer(0.3)
    if action == "left":
        arreter()
        tourner_gaucheplace(0.3)
    if action == "right":
        arreter()
        tourner_droiteplace(0.3)
    if action == "stop":
        arreter()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
