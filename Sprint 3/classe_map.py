# Importing the necessary libraries
import cv2
import numpy as np
from classe_radionav import RadioNav, Anchor



class Map:
    def __init__(self, a1, a2, a3, a4, robot, lidar):
        self.anchor1 = a1
        self.anchor2 = a2
        self.anchor3 = a3
        self.anchor4 = a4
        
        self.robot = robot
        
        self.FACTEUR_PIXEL = 50
        self.FENETRE_WIDTH = 430
        self.FENETRE_HEIGHT = 430
        self.FENETRE_CENTRE_X = self.FENETRE_WIDTH / 2
        self.FENETRE_CENTRE_Y = self.FENETRE_HEIGHT / 2
        self.MAP_WIDTH = 4
        self.MAP_HEIGHT = 4
        
        self.img = np.zeros((430,430,3),np.uint8)
        self.lidar = lidar #"/dev/ttyUSB1"    "/dev/ttyACM0"

    def CalculerPointX(self, x):
        return int(self.P_INIT_X + (float(x) * self.FACTEUR_PIXEL))

    def CalculerPointY(self, y):
        return int(self.P_INIT_Y + (float(y) * self.FACTEUR_PIXEL))
    
    def dessiner_lidar(self):
        
        tabPoint = self.lidar.dataTab
        LIMITE_LIDAR = 700 #en cm
        #dessiner point 
        for i in tabPoint:
            print(i[0])
            if(i <= LIMITE_LIDAR):
                cv2.circle(self.img,(self.CalculerPointX(i),self.CalculerPointY(i)),4,(255,0,0),-1)
                
            
            
    
    def get_map(self,radio_nav):
        #Déterminer à l'aide de méthode MAP_WIDTH ainsi que MAP_HEIGHT

        self.P_INIT_X = int(self.FENETRE_CENTRE_X - (self.MAP_WIDTH * self.FACTEUR_PIXEL / 2))
        self.P_INIT_Y = int(self.FENETRE_CENTRE_Y - (self.MAP_HEIGHT * self.FACTEUR_PIXEL / 2))

        #dessiner Lidar
        # self.dessiner_lidar()

        #clear map
        self.img = np.zeros((430,430,3),np.uint8)
        
        #Old positions representations
        firstIteration = True
        for position in self.robot.positions_precedentes:
            cv2.circle(self.img,(self.CalculerPointX(position[0]), self.CalculerPointY(position[1])),2,(255, 153, 255),-1)
            
            if not firstIteration:
                cv2.circle(self.img,(self.CalculerPointX(prec[0]), self.CalculerPointY(prec[1])),2,(255, 153, 255),-1)
                cv2.line(self.img,(self.CalculerPointX(prec[0]),self.CalculerPointY(prec[1])),(self.CalculerPointX(position[0]),self.CalculerPointY(position[1])),(255,153,255),2)
                
            prec = (position[0], position[1])
                
            
        
        #Anchors representation in the map
        cv2.circle(self.img,(self.P_INIT_X,self.P_INIT_Y),4,(0,255,0),-1)
        cv2.circle(self.img,(self.CalculerPointX(self.anchor2.x),self.CalculerPointY(self.anchor2.y)),3,(0,255,0),-1)
        cv2.circle(self.img,(self.CalculerPointX(self.anchor3.x),self.CalculerPointY(self.anchor3.y)),3,(0,255,0),-1)
        cv2.circle(self.img,(self.CalculerPointX(self.anchor4.x),self.CalculerPointY(self.anchor4.y)),3,(0,255,0),-1)

        #robot representation in the map
        
        cv2.circle(self.img,(self.CalculerPointX(self.robot.x), self.CalculerPointY(self.robot.y)),4,(0,0,255),-1)

        cv2.line(self.img,(self.P_INIT_X,self.P_INIT_Y),(self.CalculerPointX(self.anchor2.x),self.CalculerPointY(self.anchor2.y)),(255,255,255),2)
        cv2.line(self.img,(self.CalculerPointX(self.anchor2.x),self.CalculerPointY(self.anchor2.y)),(self.CalculerPointX(self.anchor3.x),self.CalculerPointY(self.anchor3.y)),(255,255,255),2)
        cv2.line(self.img,(self.CalculerPointX(self.anchor3.x),self.CalculerPointY(self.anchor3.y)),(self.CalculerPointX(self.anchor4.x),self.CalculerPointY(self.anchor4.y)),(255,255,255),2)
        cv2.line(self.img,(self.CalculerPointX(self.anchor4.x),self.CalculerPointY(self.anchor4.y)),(self.P_INIT_X,self.P_INIT_Y),(255,255,255),2)

        #flip image for graph representation
        self.img = cv2.flip(self.img, 0)

        #cv2.imshow('graphique', 

        ret, jpeg = cv2.imencode(".jpg", self.img)
        return jpeg.tobytes()
