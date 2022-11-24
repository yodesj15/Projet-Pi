#Yoan Desjardins
import time
import serial

class Anchor:
    def __init__(self, px, py):
        self.x = px
        self.y = py

class RadioNav:
    def __init__(self, port, robot):
        self.robot = robot
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

    def reset_radio_nav(self):
        self.x_pos = 0
        self.y_pos = 0
        self.z_pos = 0
        self.certitude = 0

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
        while not self.robot.done:
            try:
                data = str(self.ser.readline())
                #convert data
                self.update_pos_robot(data)
                time.sleep(0.1)
            except Exception as e:
                print(e)
                pass
            except KeyboardInterrupt:
                self.ser.close()

    def update_pos_robot(self, data):
        
        if("POS" in data and "dwm" not in data):
            try:
                data = data.strip("b'")
                data = data.strip("\\r\\n'")
                data = data.strip("POS,")
                data = data.split(',')
                self.x_pos = float(data[0])
                self.y_pos = float(data[1])
                self.z_pos = float(data[2])
                self.certitude = str(data[3])
                self.robot.setPosition(self.x_pos, self.y_pos, self.z_pos)
            except Exception as e:
                print(e)
                pass

