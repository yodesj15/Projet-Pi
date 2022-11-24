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
        self.tab_distance_mm_x= [] # a utilisé pour reprensété lidar dans map en X
        self.tab_distance_mm_y= [] # a utilisé pour reprensété lidar dans map en Y
        
        
    def getData(self):
        distance_proche = 450
        i = 0
        if(self.Obj.Connect()):
            gen = self.Obj.StartScanning()
            while not self.__done:

                self.dataTab = next(gen)
                
                if self.nbExecution == 0:
                    self.nbExecution += 1
                    self.tab_distance_mm_x, self.tab_distance_mm_y = self.trouver_distance_angle(self.dataTab)
                
                time.sleep(0.1) #1
                print(self.dataTab[179])
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
        tabDistanceX= [] # index0 à 359 degré 
        tabDistanceY= [] # index0 à 359 degré 
        
          
        for d in tab:
            tabDistanceX.append(self.calculer_distance_point_mm("x",d,tab[d])) #ajoute dans le tabX
            tabDistanceY.append(self.calculer_distance_point_mm("y",d,tab[d])) #ajoute dans le tabY
        return tabDistanceX,tabDistanceY
    
    
    def calculer_distance_point_mm(self,type_point,angle,distance):
        distance_mm = 0
        if type_point == "x":
            distance_mm = (math.cos(angle)) * distance
        else:
            distance_mm = (math.sin(angle)) * distance
            
        return distance_mm
            
            
#         else:
#             print("Error connecting to device")
    def reset_lidar(self):
        self.Obj.Reset()
        
    def disconnect(self):
            # self.Obj.Reset()
        
            self.Obj.StopScanning()
            self.Obj.Disconnect()


