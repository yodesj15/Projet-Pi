# Auteurs                 Date              Commentaires
#                          29 novembre 2022  Projet Intégration,
# BOUTIN-DUFOUR Anthony
# BOUCHER-BEAUDIN Erick
# DESJARDINS Yoan
# BERGEVIN Émeric
#
from pkgutil import get_data
import PyLidar3
import time,math


class Lidar:
    def __init__(self,port,robot):
        self.portLidar = port #"/dev/ttyUSB1"
        self.Obj = PyLidar3.YdLidarX4(self.portLidar)
        self.dataTab = []
        self.done = False
        self.robot = robot
        self.nbExecution = 0
        self.tab_p_x= [] # a utilisé pour reprensété lidar dans map en X
        self.tab_p_y= [] # a utilisé pour reprensété lidar dans map en Y
        
        
    def getData(self):
        if(self.Obj.Connect()):
            gen = self.Obj.StartScanning()
            while not self.done:

                self.dataTab = next(gen)
                
                self.tab_p_x, self.tab_p_y = self.trouver_distance_angle(self.dataTab)
                
                time.sleep(0.01) 
                       
            self.Obj.StopScanning()
            
    

    def trouver_distance_angle(self, tab):
        tabX= [] # index0 à 359 degré 
        tabY= [] # index0 à 359 degré
        
        for x in range(359):
            tabX.append(self.calculer_distance_point_mm("x",x,tab[x])) #ajoute dans le tabX
            tabY.append(self.calculer_distance_point_mm("y",x,tab[x])) #ajoute dans le tabY
        return tabX,tabY
    
    
    def calculer_distance_point_mm(self,type_point,angle,distance):
        point = 0
        if type_point == "x":
            point = (math.sin(math.radians(angle))) * distance
        else:
            point = (math.cos(math.radians(angle))) * distance
            
        return point
    
    
            
    def reset_lidar(self):
        self.Obj.Reset()
        
    def disconnect(self):
            self.Obj.Disconnect()

