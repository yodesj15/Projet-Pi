# Auteurs                 Date              Commentaires
#                          13 Avril 2022  Classe moteur,
# BOUTIN-DUFOUR Anthony
# BOUCHER-BEAUDIN Erick
#
#
#
from gpiozero import DigitalOutputDevice
from gpiozero import DigitalInputDevice
from gpiozero import PWMOutputDevice

class Moteur:
    
    def __init__(self):

        #Instances des composants
        self.MoteurGIN1 = DigitalOutputDevice(6)
        self.MoteurGIN2 = DigitalOutputDevice(5)
        self.MoteurGENA = PWMOutputDevice(13)
        self.MoteurDIN3 = DigitalOutputDevice(15)
        self.MoteurDIN4 = DigitalOutputDevice(14)
        self.MoteurDENB = PWMOutputDevice(18)
        self.vitesse = 0.1
        self.IRD = DigitalInputDevice(23)
        self.IRG = DigitalInputDevice(24)
    
    #méthode pour faire avancer le robot selon une vitesse indiquée.
    def avancer(self,vitesse):
        self.MoteurGIN1.on()
        self.MoteurGENA.value = vitesse
        self.MoteurDIN3.on()
        self.MoteurDENB.value = vitesse
    
    #méthode pour faire arrêter le robot.
    def arreter(self):
        self.MoteurGIN1.off()
        self.MoteurGIN2.off()
        self.MoteurDIN3.off()
        self.MoteurDIN4.off()
    
    #méthode pour faire reculer le robot selon une vitesse indiquée.
    def reculer(self,vitesse):
        self.MoteurGIN2.on()
        self.MoteurGENA.value = vitesse
        self.MoteurDIN4.on()
        self.MoteurDENB.value = vitesse
    
    #méthode pour tourner à gauche.
    def tourner_droite(self,vitesse):
        self.MoteurDIN3.on()
        self.MoteurDENB.on()
        self.MoteurGENA.on()

    #méthode pour tourner à droite.
    def tourner_gauche(self,vitesse):
        self.MoteurGENA.on()
        self.MoteurGIN1.on()
        self.MoteurDENB.on()

    #méthode pour tourner à droite sur place.
    def tourner_gaucheplace(self,vitesse):
        self.MoteurGENA.value = vitesse
        self.MoteurDENB.value = vitesse
        self.MoteurGENA.on()
        self.MoteurGIN1.on()
        self.MoteurDENB.on()
        self.MoteurDIN4.on()

    #méthode pour tourner à gauche sur place.
    def tourner_droiteplace(self,vitesse):
        self.MoteurDENB.value = vitesse
        self.MoteurGENA.value = vitesse
        self.MoteurDENB.on()
        self.MoteurDIN3.on()
        self.MoteurGIN2.on()
        self.MoteurGENA.on()

    #méthode pour avancer en tournant à gauche.
    def avancer_droite(self,vitesse):
        self.arreter()
        self.avancer(vitesse)
        self.MoteurGENA.value = vitesse / 6
        self.MoteurDENB.value = vitesse 
        self.MoteurDENB.on()
        self.MoteurDIN3.on()

    #méthode pour avancer en tournant à droite.
    def avancer_gauche(self,vitesse):
        self.arreter()
        self.avancer(vitesse)
        self.MoteurDENB.value = vitesse / 6
        self.MoteurGENA.value = vitesse
        self.MoteurGENA.on()
        self.MoteurGIN1.on()

    #méthode pour faire freiner le robot.
    def freiner(self):
        self.MoteurDENB.on()
        self.MoteurGIN1.on()
        self.MoteurGIN2.on()
        self.MoteurDIN3.on()
        self.MoteurDIN4.on()
        self.MoteurGENA.on()