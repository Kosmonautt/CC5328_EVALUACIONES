import serial
from bmi_config import BMI_CONFIG
from struct import pack, unpack

# Se configura el puerto y el BAUD_Rate
PORT = 'COM3'  # Esto depende del sistema operativo
BAUD_RATE = 115200  # Debe coincidir con la configuracion de la ESP32

# Se abre la conexion serial
ser = serial.Serial(PORT, BAUD_RATE, timeout = 1)

# Funciones
def send_message(message):
    """ Funcion para enviar un mensaje a la ESP32 """
    ser.write(message)

# Esta función también imprime en la consola de python para que el usuario siempre vea lo que se está recibiendo
def receive_response():
    """ Funcion para recibir un mensaje de la ESP32 """
    response = ser.readline()
    print(response)
    return response

# Función que transforma un entero en un string de 3 caracteres
def int_to_str(num):
    return str(num).zfill(3)

# Función para el loop principal
def loop():
    # Se lee data por la conexion serial
    while True:
        if ser.in_waiting > 0:
            try:
                # se lee la data
                response = receive_response()
                # si el mensaje es b'Esperando inicio de lectura\r\n'
                if response == b'Esperando inicio de lectura\r\n':
                    # esperar a que el usuario presione enter
                    input('Presiona enter para comenzar la lectura')
                    # se envia el mensaje de inicio de lectura
                    begin_message = pack('6s','BEGIN\0'.encode())
                    send_message(begin_message)


            except KeyboardInterrupt:
                print('Finalizando comunicacion')
                break
            except:
                print('Error en leer mensaje')
                continue

# Se ejecuta el loop principal
loop()
