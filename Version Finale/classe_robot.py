# Auteurs                 Date              Commentaires
#                          29 novembre 2022  Projet Intégration,
# BOUTIN-DUFOUR Anthony
# BOUCHER-BEAUDIN Erick
# DESJARDINS Yoan
# BERGEVIN Émeric
#
from gpiozero import DigitalOutputDevice
from gpiozero import DigitalInputDevice
from gpiozero import PWMOutputDevice
import numpy as np
import cv2
import time
from classe_moteur import Moteur
from enum import Enum


class Robot:
    Etat = Enum('Etat', 'innactif actif')

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.positions_precedentes = []
        self.moteur = Moteur()
        self.done = False
        self.etat = self.Etat.innactif
        self.objetDetecteAvant = False

    def setVitesse(self, nouvelle_vitesse):
        self.moteur.__vitesse = nouvelle_vitesse
        
    def setPosition(self, x, y, z):
        if self.etat == self.Etat.actif:
            print('actif')
            self.positions_precedentes.append((self.x,self.y))
        self.x = x
        self.y = y
        self.z = z
