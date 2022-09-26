# import PyLidar3
# import time # Time module
# 
# 
# #Serial port to which lidar connected, Get it from device manager windows
# #In linux type in terminal -- ls /dev/tty* 
# port = "/dev/ttyUSB1" #linux
# Obj = PyLidar3.YdLidarX4(port) #PyLidar3.your_version_of_lidar(port,chunk_size) 
# if(Obj.Connect()):
#     print(Obj.GetDeviceInfo())
#     gen = Obj.StartScanning()
#     t = time.time() # start time 
#     while (time.time() - t) < 10: #scan for 30 seconds
#         print(next(gen))
#         time.sleep(0.5)
#     Obj.StopScanning()
#     Obj.Disconnect()
# else:
#     print("Error connecting to device")


import threading
import PyLidar3
import matplotlib.pyplot as plt
import math    
import time

is_plot = True

def draw():
    global is_plot
    while is_plot:
        plt.figure(1)
        plt.cla()
        plt.ylim(-9000,9000)
        plt.xlim(-9000,9000)
        plt.scatter(x,y,c='r',s=8)
        plt.pause(0.001)
    plt.close("all")
    
                

x=[]
y=[]
for _ in range(360):
    x.append(0)
    y.append(0)

port =  "/dev/ttyUSB0" #windows
Obj = PyLidar3.YdLidarX4(port)  #PyLidar3.your_version_of_lidar(port,chunk_size)
threading.Thread(target=draw).start()
if(Obj.Connect()):
    print(Obj.GetDeviceInfo())
    gen = Obj.StartScanning()
    t = time.time() # start time 
    while (time.time() - t) < 30: #scan for 30 seconds
        data = next(gen)
        for angle in range(0,360):
            if(data[angle]>1000):
                x[angle] = data[angle] * math.cos(math.radians(angle))
                y[angle] = data[angle] * math.sin(math.radians(angle))
    is_plot = False
    Obj.StopScanning()
    Obj.Disconnect()
else:
    print("Error connecting to device")