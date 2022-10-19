#Yoan Desjardins
import time
import serial

class RadioNav:
    def __init__(self, port):
        self.__done = False
        self.x_pos = 0
        self.y_pos = 0
        self.z_pos = 0
        self.distance = 0

        try:
            self.ser = serial.Serial()
            self.connection(self.ser, port)
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
        self.ser.open()
        while not self.__done:
            try:
                data = str(self.ser.readline())
                #convert data
                print(self.return_pos(data))
                time.sleep(1)
            except Exception as e:
                print(e)
                self.__done = True
                pass
            except KeyboardInterrupt:
                self.ser.close()
                self.__done = True

    def return_pos_avec_distance(self, data):
        pos = 0
        if("POS" in data):
            data = data.strip("b'\r\n")
            data = data.strip("POS,")
            data = data.split(',')
            self.x_pos = float(data[0])
            self.y_pos = float(data[1])
            self.z_pos = float(data[2])
            self.distance = float(data[3])
            pos = str(self.x_pos + (",") + self.y_pos + (",") +
                        self.z_pos + " Distance : " + self.distance)
        return pos
