import serial
from struct import pack, unpack

class ESP32_COM:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate, timeout=1)
    
    def send_message(self, message):
        """ Funcion para enviar un mensaje a la ESP32 """
        self.ser.write(message)

    def receive_response(self):
        """ Funcion para recibir un mensaje de la ESP32 """
        response = self.ser.readline()
        print(response)
        return response
    
    def encode_message(self, message):
        """ Funcion para codificar un mensaje """
        return pack('{}s'.format(len(message)),message.encode())