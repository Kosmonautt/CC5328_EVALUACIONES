import serial
from struct import pack, unpack

# Se configura el puerto y el BAUD_Rate
PORT = 'COM6'  # Esto depende del sistema operativo
BAUD_RATE = 115200  # Debe coincidir con la configuracion de la ESP32

WINDOW_SIZE = 500

# Se abre la conexion serial
ser = serial.Serial(PORT, BAUD_RATE, timeout = 1)

# Funciones
def send_message(message):
    """ Funcion para enviar un mensaje a la ESP32 """
    ser.write(message())

def receive_response():
    """ Funcion para recibir un mensaje de la ESP32 """
    response = ser.readline()
    return response.decode()


# Each window is sent as a packet of following order :
# "START" byte to represent the start of a packet
# WINDOW_SIZE*sizeof(float) number of bytes for x acceleration
# WINDOW_SIZE*sizeof(float) number of bytes for y acceleration
# WINDOW_SIZE*sizeof(float) number of bytes for z acceleration
# WINDOW_SIZE*sizeof(float) number of bytes for x RMS acceleration
# WINDOW_SIZE*sizeof(float) number of bytes for y RMS acceleration
# WINDOW_SIZE*sizeof(float) number of bytes for z RMS acceleration
# WINDOW_SIZE*sizeof(float) number of bytes for x FFT acceleration  ---> not sure of size of FFT data to receive (size of window ?)
# WINDOW_SIZE*sizeof(float) number of bytes for y FFT acceleration
# WINDOW_SIZE*sizeof(float) number of bytes for z FFT acceleration
# 5*sizeof(float) number of bytes for x acceleration FFT peaks
# 5*sizeof(float) number of bytes for y acceleration FFT peaks
# 5*sizeof(float) number of bytes for z acceleration FFT peaks
# 5*sizeof(float) number of bytes for x acceleration peaks
# 5*sizeof(float) number of bytes for y acceleration peaks
# 5*sizeof(float) number of bytes for z acceleration peaks

#do the same for angular velocity
def receive_data():
    print("Receiving data")

    # Waiting for START of packet
    while True:
        response = ser.read(6)
        print(response.decode())
        if response == b'START\x00':
            print("START received -> Start of packet")
            break

    # reading the packet
    acc_x_m_s2 = ser.read(WINDOW_SIZE*4)
    acc_y_m_s2 = ser.read(WINDOW_SIZE*4)
    acc_z_m_s2 = ser.read(WINDOW_SIZE*4)

    acc_x_RMS = ser.read(WINDOW_SIZE*4)
    acc_y_RMS = ser.read(WINDOW_SIZE*4)
    acc_z_RMS = ser.read(WINDOW_SIZE*4)

    acc_x_FFT = ser.read(WINDOW_SIZE*4)
    acc_y_FFT = ser.read(WINDOW_SIZE*4)
    acc_z_FFT = ser.read(WINDOW_SIZE*4)

    acc_x_RMS_peaks = ser.read(5*4)
    acc_y_RMS_peaks = ser.read(5*4)
    acc_z_RMS_peaks = ser.read(5*4)

    acc_x_peaks = ser.read(5*4)
    acc_y_peaks = ser.read(5*4)
    acc_z_peaks = ser.read(5*4)


    # unpacking
    acc_x_m_s2 = unpack("f"*WINDOW_SIZE, acc_x_m_s2)
    acc_y_m_s2 = unpack("f"*WINDOW_SIZE, acc_y_m_s2)
    acc_z_m_s2 = unpack("f"*WINDOW_SIZE, acc_z_m_s2)

    acc_x_RMS = unpack("f"*WINDOW_SIZE, acc_x_RMS)
    acc_y_RMS = unpack("f"*WINDOW_SIZE, acc_y_RMS)
    acc_z_RMS = unpack("f"*WINDOW_SIZE, acc_z_RMS)

    acc_x_FFT = unpack("f"*WINDOW_SIZE, acc_x_FFT)
    acc_y_FFT = unpack("f"*WINDOW_SIZE, acc_y_FFT)
    acc_z_FFT = unpack("f"*WINDOW_SIZE, acc_z_FFT)

    acc_x_RMS_peaks = unpack("f"*5, acc_x_RMS_peaks)
    acc_y_RMS_peaks = unpack("f"*5, acc_y_RMS_peaks)
    acc_z_RMS_peaks = unpack("f"*5, acc_z_RMS_peaks)

    acc_x_peaks = unpack("f"*5, acc_x_peaks)
    acc_y_peaks = unpack("f"*5, acc_y_peaks)
    acc_z_peaks = unpack("f"*5, acc_z_peaks)

    # printing for x axis only
    print("acc x : ", acc_x_m_s2)
    print("acc RMS x : ", acc_x_RMS)
    print("acc FFT x : ", acc_x_FFT)
    print("acc RMS x peaks: ", acc_x_RMS_peaks)
    print("acc x peaks: ", acc_x_peaks)

    return None


def change_mode(mode):
    """ Funcion para cambiar el modo de operacion del sensor ESP32"""
    if mode == 'low':
        send_message('LOW')
    elif mode == 'normal':
        send_message('NORMAL')
    elif mode == 'performance':
        send_message('PERFORMANCE')
    else:
        print("Modo no reconocido")

def send_end_message():
    """ Funcion para enviar un mensaje de finalizacion a la ESP32 """
    end_message = pack('4s', 'END\0'.encode())
    ser.write(end_message)

# # Se lee data por la conexion serial
# counter = 0
while True:
    try:
        receive_data()
    except KeyboardInterrupt:
        print('Finalizando comunicacion')
        break
    except:
        print('Error en leer mensaje')
        continue
