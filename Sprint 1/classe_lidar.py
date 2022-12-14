#Émeric Bergevin
from pkgutil import get_data
import PyLidar3
import time

class Lidar:
    def __init__(self,port):
        self.portLidar = port #"/dev/ttyUSB1"
        self.Obj = PyLidar3.YdLidarX4(self.portLidar)
        self.dataTab = []
        self.__done = False
        
    def getData(self):
        if(self.Obj.Connect()):
            gen = self.Obj.StartScanning()
            while not self.__done:

                self.dataTab = next(gen)
                print(self.dataTab)

                time.sleep(1)
#         else:
#             print("Error connecting to device")
            
    def disconect(self):
            self.Obj.StopScanning()
            self.Obj.Disconnect()


