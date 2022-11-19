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
        self.__pos_x = 0
        self.__pos_y = 0
        self.__pos_z = 0
        self.moteur = Moteur(0.5)
        self.done = False

    def setVitesse(self, nouvelle_vitesse):
        self.moteur.__vitesse = nouvelle_vitesse
    
    def setPosition(self, x, y, z):
        self.__pos_x = x
        self.__pos_y = y
        self.__pos_z = z
    
    #méthode qui lit chaque touches au clavier et converti les touches en action à faire comme avancer, reculer, freiner, etc...
    #def demarrerRobot(self):
    #    self.done = False
    #    while not self.done:
    #        img = np.zeros((512,512,3),np.uint8)
    #        cv2.imshow('Labo 1',img)         
    #        key = cv2.waitKey(120)
    #        self.moteur.reset()
    #        if key==ord('q'):
    #            self.moteur.avancer_gauche()
    #        if key==ord('w'):
    #            self.moteur.avancer()
    #        if key==ord('e'):
    #            self.moteur.avancer_droite()
    #        if key==ord('a'):
    #            self.moteur.tourner_gauche()       
    #        if key==ord('s'):
    #            self.moteur.reculer()
    #        if key==ord('d'):
    #            self.moteur.tourner_droite()
    #        if key==ord(' '):
    #            self.moteur.freiner()
    #        if key==ord('='):
    #            if self.moteur.__vitesse < 0.99:
    #                self.moteur.__vitesse+= 0.10
    #            print(self.moteur.__vitesse)
    #        if key==ord('-'):
    #            if self.moteur.__vitesse > 0.0:
    #                self.moteur.__vitesse-=0.10
    #            print(self.moteur.__vitesse)
    #        if key==ord('x'):
    #            self.moteur.reset()
    #            self.done = True