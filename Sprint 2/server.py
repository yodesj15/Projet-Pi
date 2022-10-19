from flask import Flask, render_template, request
from gpiozero import DigitalOutputDevice
from gpiozero import DigitalInputDevice
from gpiozero import PWMOutputDevice
import datetime
from classe_camera import Camera

app = Flask(__name__)

MoteurGIN1 = DigitalOutputDevice(6)
MoteurGIN2 = DigitalOutputDevice(5)
MoteurGENA = PWMOutputDevice(13)
MoteurDIN3 = DigitalOutputDevice(15)
MoteurDIN4 = DigitalOutputDevice(14)
MoteurDENB = PWMOutputDevice(18)


ledYlw = DigitalOutputDevice(9)
ledGrn = DigitalOutputDevice(10)
ledGrn.on()


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

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    actionneur = ""
    if deviceName == 'ledYlw':
        actionneur = ledYlw
    if deviceName == 'moteur':
        actionneur = MoteurDENB
        
    if deviceName == 'camera':
        actionneur = Camera()
        if action == 'on':
            actionneur.execution()
           
    if action == "on":
        actionneur.on()
        
    if action == "off":
        actionneur.off()
    if action == "forward":
        avancer(0.6)
    if action == "stop":
        arreter()
    
        
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')