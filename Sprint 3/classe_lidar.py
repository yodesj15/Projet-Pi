from pkgutil import get_data
import PyLidar3
import time,math


class Lidar:
    def __init__(self,port,robot):
        self.portLidar = port #"/dev/ttyUSB1"
        self.Obj = PyLidar3.YdLidarX4(self.portLidar)
        self.dataTab = []
        self.__done = False
        self.robot = robot
        self.nbExecution = 0
        self.tab_p_x= [] # a utilisé pour reprensété lidar dans map en X
        self.tab_p_y= [] # a utilisé pour reprensété lidar dans map en Y
        
        
    def getData(self):
        distance_proche = 175 # 600 proximité et 175 limite
        i = 0
        if(self.Obj.Connect()):
            gen = self.Obj.StartScanning()
            while not self.__done:

                self.dataTab = next(gen)
                
                #if self.nbExecution == 0:
                    #self.nbExecution += 1
                self.tab_p_x, self.tab_p_y = self.trouver_distance_angle(self.dataTab)
                
                time.sleep(0.01) #1
                #print(self.dataTab[179])
                if (self.dataTab[179] < distance_proche and self.dataTab[179] != 0):
                    i = i + 1
                    print('Objet devant! oups ' + str(i))
                    self.robot.moteur.fonction = False
                    self.robot.moteur.freiner() 
                    
                
                #for d in self.dataTab:
                #    if(int(self.dataTab[d]) < 50 and int(self.dataTab[d]) != 0):
                #        if int(d) == 180:#devant degree 315 a 45 #cote droit 46 a 135#cote droit 136 a 225#cote droit 226 a 315
                #            i = i + 1
                #            print('Objet devant! oups ' + str(i))
                #            self.robot.moteur.fonction = False
                #            self.robot.moteur.freiner()            
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
            
            
#         else:
#             print("Error connecting to device")
    def reset_lidar(self):
        self.Obj.Reset()
        
    def disconnect(self):
            # self.Obj.Reset()
        
            self.Obj.StopScanning()
            self.Obj.Disconnect()


