# Auteurs                 Date              Commentaires
#                          13 Avril 2022  Classe robot,
# BOUTIN-DUFOUR Anthony
# BOUCHER-BEAUDIN Erick
#
#
#
from gpiozero import DigitalOutputDevice
from gpiozero import DigitalInputDevice
from gpiozero import PWMOutputDevice
import numpy as np
import cv2
import time
from classe_moteur import Moteur

class Robot:

    def __init__(self):
        self.moteur = Moteur()
    
    
    #méthode qui lit chaque touches au clavier et converti les touches en action à faire comme avancer, reculer, freiner, etc...
    def demarrerRobot(self):
        fini = False
        while not fini:
            img = np.zeros((512,512,3),np.uint8)
            cv2.imshow('Labo 1',img)         
            key = cv2.waitKey(120)
            self.moteur.arreter()
            if key==ord('q'):
                self.moteur.avancer_gauche(self.moteur.vitesse)
            if key==ord('w'):
                self.moteur.avancer(self.moteur.vitesse)
            if key==ord('e'):
                self.moteur.avancer_droite(self.moteur.vitesse)
            if key==ord('a'):
                self.moteur.tourner_gaucheplace(self.moteur.vitesse)       
            if key==ord('s'):
                self.moteur.reculer(self.moteur.vitesse)
            if key==ord('d'):
                self.moteur.tourner_droiteplace(self.moteur.vitesse)
            if key==ord(' '):
                self.moteur.freiner()
            if key==ord('='):
                if self.moteur.vitesse < 0.99:
                    self.moteur.vitesse+= 0.10
                print(self.moteur.vitesse)
            if key==ord('-'):
                if self.moteur.vitesse > 0.0:
                    self.moteur.vitesse-=0.10
                print(self.moteur.vitesse)
            if key==ord('x'):
                self.moteur.arreter()
                fini = True