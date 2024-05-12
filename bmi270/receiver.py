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
    # si el número es None, se retorna '000'
    if num is None:
        return '000'
    return str(num).zfill(3)

# objeto de configuracion de la BMI270
bmi_config = BMI_CONFIG()

# Función para el loop principal
def loop():
    # Se lee data por la conexion serial
    while True:
        if ser.in_waiting > 0:
            try:
                # se lee lo que la ESP32 imprime en la consola
                response = receive_response()

                # si el mensaje es b'Esperando inicio de lectura\r\n'
                if response == b'Esperando inicio de lectura\r\n':
                    # esperar a que el usuario seleccione los parametros
                    bmi_config.user_input()
                    # el mensaje a enviar empieza con BEGIN
                    begin_with_config = 'BEGIN'
                    # se obtienen los parametros de la BMI270
                    bmi_params = bmi_config.get_user_input()
                    # se añade al string el modo de potencia (1 char)
                    begin_with_config += bmi_params['mode']
                    # se añade al string el ODR del acelerometro (3 chars)
                    begin_with_config += int_to_str(bmi_params['odr_accel'])
                    # se añade al string el rango del acelerometro (3 chars)
                    begin_with_config += int_to_str(bmi_params['range_accel'])
                    # se añade al string el ODR del giroscopio (3 chars)
                    begin_with_config += int_to_str(bmi_params['odr_gyro'])
                    # se añade al string el rango del giroscopio (3 chars)
                    begin_with_config += int_to_str(bmi_params['range_gyro'])
                    # se añade al string el tamaño de la muestra (3 chars)
                    begin_with_config += int_to_str(bmi_params['sample_size'])
                    # se agrega el 0 final
                    begin_with_config += '\0'

                    # se envia el mensaje de inicio de lectura, este también contiene la configuración de la BMI270
                    begin_message = pack('{}s'.format(len(begin_with_config)),begin_with_config.encode())
                    send_message(begin_message)


            except KeyboardInterrupt:
                print('Finalizando comunicacion')
                break
            except:
                print('Error en leer mensaje')
                continue

# Se ejecuta el loop principal
loop()
