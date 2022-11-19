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
    
    def __init__(self, vitesse):

        #Instances des composants
        self.MoteurGIN1 = DigitalOutputDevice(6)
        self.MoteurGIN2 = DigitalOutputDevice(5)
        self.MoteurGENA = PWMOutputDevice(13)
        self.MoteurDIN3 = DigitalOutputDevice(15)
        self.MoteurDIN4 = DigitalOutputDevice(14)
        self.MoteurDENB = PWMOutputDevice(18)
        
        self.__vitesse = vitesse
    
    #méthode pour faire avancer le robot selon une vitesse indiquée.
    def avancer(self, v):
        self.reset()
        self.MoteurGIN1.on()
        self.MoteurDIN3.on()
        self.MoteurGENA.value = v
        self.MoteurDENB.value = v
    
    #méthode pour faire arrêter le robot.
    def reset(self):
        self.MoteurGIN1.off()
        self.MoteurGIN2.off()
        self.MoteurDIN3.off()
        self.MoteurDIN4.off()
    
    #méthode pour faire reculer le robot selon une vitesse indiquée.
    def reculer(self, v):
        self.reset()
        self.MoteurGIN2.on()
        self.MoteurDIN4.on()
        self.MoteurGENA.value = v
        self.MoteurDENB.value = v
    
    #méthode pour tourner à gauche.
    def tourner_gauche(self, v):
        self.reset()
        self.MoteurDENB.on()
        self.MoteurDIN3.on()
        self.MoteurGIN2.on()
        self.MoteurGENA.on()
        if v <= 4: 
            vitesse = 5
        else: 
            vitesse = v
        self.MoteurGENA.value = vitesse
        self.MoteurDENB.value = vitesse
        self.MoteurDIN3.value = vitesse
        self.MoteurGIN2.value = vitesse
        

    #méthode pour tourner à droite.
    def tourner_droite(self, v):
        self.reset()
        self.MoteurGENA.on()
        self.MoteurGIN1.on()
        self.MoteurDENB.on()
        self.MoteurDIN4.on()
        if v <= 4: 
            vitesse = 5
        else: 
            vitesse = v
        self.MoteurGENA.value = vitesse
        self.MoteurDENB.value = vitesse
        self.MoteurDIN3.value = vitesse
        self.MoteurGIN2.value = vitesse
        

    #méthode pour avancer en tournant à gauche.
    def avancer_droite(self):
        self.reset()
        self.avancer()
        self.tourner_droite()

    #méthode pour avancer en tournant à droite.
    def avancer_gauche(self):
        self.reset()
        self.avancer()
        self.tourner_gauche()

    #méthode pour faire freiner le robot.
    def freiner(self):
        self.MoteurDENB.on()
        self.MoteurGIN1.on()
        self.MoteurGIN2.on()
        self.MoteurDIN3.on()
        self.MoteurDIN4.on()
        self.MoteurGENA.on()