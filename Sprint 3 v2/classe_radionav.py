#Yoan Desjardins
import time
import serial

class Anchor:
    def __init__(self, px, py):
        self.x = px
        self.y = py

class RadioNav:
    def __init__(self, port, robot):
        self.__robot = robot
        self.x_pos = 0
        self.y_pos = 0
        self.z_pos = 0
        self.certitude = 0

        try:
            self.ser = serial.Serial()
            self.connection(self.ser, port)
            self.ser.open()
        except Exception as e:
            print(e)

    def connection(self, ser, port):
        ser.port = port
        ser.baudrate = 115200
        ser.bytesize = serial.EIGHTBITS
        ser.parity = serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.timeout = 1
        ser.open()
        ser.write(b'\r\r')  # sequence d'octets
        time.sleep(1)
        ser.write(b'lep\n')  # Show pos. in CSV

    def execution(self):
        while not self.__robot.done:
            try:
                data = str(self.ser.readline())
                #convert data
                self.change_pos_robot(data)
                # self.return_pos_avec_distance(data)
                time.sleep(1)
            except Exception as e:
                print(e)
                pass
            except KeyboardInterrupt:
                self.ser.close()

    def change_pos_robot(self,data):
        if("POS" in data and "dwm" not in data):
            data = data.strip("b'")
            data = data.strip("\\r\\n'")
            data = data.strip("POS,")
            data = data.split(',')
            self.robot.set_pos(data[0],data[1],data[2]) 

        else: 
            print("Valeur robot non changé")
    # def return_pos_avec_distance(self, data):
        
    #     if("POS" in data and "dwm" not in data):
    #         data = data.strip("b'")
    #         data = data.strip("\\r\\n'")
    #         data = data.strip("POS,")
    #         data = data.split(',')
    #         self.x_pos = str(data[0])
    #         self.y_pos = str(data[1])
    #         self.z_pos = str(data[2])
    #         self.distance = str(data[3])
    #         pos = str(self.x_pos + (",") + self.y_pos + (",") +
    #                     self.z_pos + " Distance : " + self.distance)
    #         return pos

