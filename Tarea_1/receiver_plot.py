import serial
from bmi_config import BMI_CONFIG
from struct import pack, unpack
from matplotlib import pyplot as plt

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

# arreglo para guardar los arreglos de datos de acc en m/s^2
acc_data_m_s2 = []

# arreglo para guardar los arreglos de datos de acc en g
acc_data_g = []

# arreglo para guardar los arreglos de datos de gyro en rad/s
gyro_data_rad_s = []

# función para inicializar los arreglos de datos
def initialize_data(window_size):
    # se borran los datos anteriores
    acc_data_m_s2.clear()
    acc_data_g.clear()
    gyro_data_rad_s.clear()
    
    # se añaden los arreglos de datos
    # se añaden arreglos que guardaran la informacion de las medidas
    # 0 -> x, 1 -> y, 2 -> z
    # 3 -> FFTxReal, 4 -> FFTxImag, 5 -> FFTyReal, 6 -> FFTyImag, 7 -> FFTzReal, 8 -> FFTzImag
    # 9 -> RMSx, 10 -> RMSy, 11 -> RMSz
    # 12 -> RMSx_5_peaks, 13 -> RMSy_5_peaks, 14 -> RMSz_5_peaks
    # 15 -> x_5_peaks, 16 -> y_5_peaks, 17 -> z_5_peaks
    # los arreglos del 0 al 11 son de window_size elementos
    # del 12 al 17 son de 5 elementos
    for i in range(18):
        if i < 12:
            acc_data_m_s2.append([0]*window_size)
            acc_data_g.append([0]*window_size)
            gyro_data_rad_s.append([0]*window_size)
        else:
            acc_data_m_s2.append([0]*5)
            acc_data_g.append([0]*5)
            gyro_data_rad_s.append([0]*5)

    print('Arreglos de datos inicializados!')

# diccionario con los índices de los arreglos de datos, para acc en m/s^2, g y rad/s, con el identificador de la medida
# como llave y el índice del arreglo como valor, para los arreglos de window_size
window_size_index= {
    'acc_x': 0,
    'acc_y': 1,
    'acc_z': 2,
    'gyr_x': 0,
    'gyr_y': 1,
    'gyr_z': 2,
    'FFTx_RE': 3,
    'FFTx_IM': 4,
    'FFTy_RE': 5,
    'FFTy_IM': 6,
    'FFTz_RE': 7,
    'FFTz_IM': 8,
    'RMSx': 9,
    'RMSy': 10,
    'RMSz': 11
}

# diccionario con los índices de los arreglos de datos, para acc en m/s^2, g y rad/s, con el identificador de la medida
# como llave y el índice del arreglo como valor, para los arreglos de 5
five_peaks_index= {
    'RMSx': 12,
    'RMSy': 13,
    'RMSz': 14,
    'acc_x': 15,
    'acc_y': 16,
    'acc_z': 17,
    'gyr_x': 15,
    'gyr_y': 16,
    'gyr_z': 17
}

# función para parsear una linea de datos
def parse_line(line):
    # se saca \r\n del final
    line = line[:-2]
    # se convierte a string
    line = line.decode('utf-8')
    
    # si existe '[Acc m/s2]' en la linea
    if '[Acc m/s2]' in line:
        # se divide la linea en los datos por un espacio en blanco
        line = line.split(' ')
        # se consigue si es 'Lectura', 'Dato' o 'Top'
        data_type = line[2]
        # se consigue el número de muestra
        sample_number = int(line[3][:-1])
        # se consigue el identificador de la medida
        measure = line[4].split(':')[0]
        # se consigue el valor de la medida
        value = float(line[5])

        if data_type == 'Lectura' or data_type == 'Dato':
            # se consigue el índice del arreglo de datos
            index_array = window_size_index[measure]
            # se consigue el arreglo de datos
            array = acc_data_m_s2[index_array]
            # se añade el valor al arreglo de datos
            array[sample_number - 1] = value

        elif data_type == 'Top':
            # se consigue el índice del arreglo de datos
            index_array = five_peaks_index[measure]
            # se consigue el arreglo de datos
            array = acc_data_m_s2[index_array]
            # se añade el valor al arreglo de datos
            array[sample_number - 1] = value

    # si existe '[Acc g]' en la linea
    elif '[Acc g]' in line:
        # se divide la linea en los datos por un espacio en blanco
        line = line.split(' ')
        # se consigue si es 'Lectura', 'Dato' o 'Top'
        data_type = line[2]
        # se consigue el número de muestra
        sample_number = int(line[3][:-1])
        # se consigue el identificador de la medida
        measure = line[4].split(':')[0]
        # se consigue el valor de la medida
        value = float(line[5])

        if data_type == 'Lectura' or data_type == 'Dato':
            # se consigue el índice del arreglo de datos
            index_array = window_size_index[measure]
            # se consigue el arreglo de datos
            array = acc_data_g[index_array]
            # se añade el valor al arreglo de datos
            array[sample_number - 1] = value

        elif data_type == 'Top':
            # se consigue el índice del arreglo de datos
            index_array = five_peaks_index[measure]
            # se consigue el arreglo de datos
            array = acc_data_g[index_array]
            # se añade el valor al arreglo de datos
            array[sample_number - 1] = value

    # si existe '[Ang_Vel rad/s]' en la linea
    elif '[Ang_Vel rad/s]' in line:
        # se divide la linea en los datos por un espacio en blanco
        line = line.split(' ')
        # se consigue si es 'Lectura', 'Dato' o 'Top'
        data_type = line[2]
        # se consigue el número de muestra
        sample_number = int(line[3][:-1])
        # se consigue el identificador de la medida
        measure = line[4].split(':')[0]
        # se consigue el valor de la medida
        value = float(line[5])

        if data_type == 'Lectura' or data_type == 'Dato':
            # se consigue el índice del arreglo de datos
            index_array = window_size_index[measure]
            # se consigue el arreglo de datos
            array = gyro_data_rad_s[index_array]
            # se añade el valor al arreglo de datos
            array[sample_number - 1] = value

        elif data_type == 'Top':
            # se consigue el índice del arreglo de datos
            index_array = five_peaks_index[measure]
            # se consigue el arreglo de datos
            array = gyro_data_rad_s[index_array]
            # se añade el valor al arreglo de datos
            array[sample_number - 1] = value

# función para graficar los datos de acc en m/s^2
def plot_data_acc_m_s2(window_size):
    # color de los puntos/lineas de los gráficos
    line_color = 'orange'

    # se crea un arreglo de 1 a window_size
    x = [i for i in range(1, window_size + 1)]

    # se crea un arreglo de 1 a 5
    x_5 = [i for i in range(1, 6)]

    # se grafican los datos de acc_x en m/s^2
    plt.plot(x, acc_data_m_s2[0], color=line_color)
    plt.title('Aceleración en eje x [m/s^2]')
    plt.xlabel('Muestra')
    plt.ylabel('Aceleración [m/s^2]')
    plt.show()
    
    # se grafican los datos de acc_y en m/s^2
    plt.plot(x, acc_data_m_s2[1], color=line_color)
    plt.title('Aceleración en eje y [m/s^2]')
    plt.xlabel('Muestra')
    plt.ylabel('Aceleración [m/s^2]')
    plt.show()

    # se grafican los datos de acc_z en m/s^2
    plt.plot(x, acc_data_m_s2[2], color=line_color)
    plt.title('Aceleración en eje z [m/s^2]')
    plt.xlabel('Muestra')
    plt.ylabel('Aceleración [m/s^2]')
    plt.show()

    # se grafican los datos de FFTxRE en unidades arbitrarias
    plt.plot(x, acc_data_m_s2[3], color=line_color)
    plt.title('FFT en eje x Real [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('FFT [U.A.]')
    plt.show()

    # se grafican los datos de FFTxIM en unidades arbitrarias
    plt.plot(x, acc_data_m_s2[4], color=line_color)
    plt.title('FFT en eje x Imaginario [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('FFT [U.A.]')
    plt.show()

    # se grafican los datos de FFTyRE en unidades arbitrarias
    plt.plot(x, acc_data_m_s2[5], color=line_color)
    plt.title('FFT en eje y Real [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('FFT [U.A.]')
    plt.show()

    # se grafican los datos de FFTyIM en unidades arbitrarias
    plt.plot(x, acc_data_m_s2[6], color=line_color)
    plt.title('FFT en eje y Imaginario [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('FFT [U.A.]')
    plt.show()

    # se grafican los datos de FFTzRE en unidades arbitrarias
    plt.plot(x, acc_data_m_s2[7], color=line_color)
    plt.title('FFT en eje z Real [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('FFT [U.A.]')
    plt.show()

    # se grafican los datos de FFTzIM en unidades arbitrarias
    plt.plot(x, acc_data_m_s2[8], color=line_color)
    plt.title('FFT en eje z Imaginario [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('FFT [U.A.]')
    plt.show()

    # se grafican los datos de RMSx en unidades arbitrarias
    plt.plot(x, acc_data_m_s2[9], color=line_color)
    plt.title('RMS en eje x [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('RMS [U.A.]')
    plt.show()

    # se grafican los datos de RMSy en unidades arbitrarias
    plt.plot(x, acc_data_m_s2[10], color=line_color)
    plt.title('RMS en eje y [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('RMS [U.A.]')
    plt.show()

    # se grafican los datos de RMSz en unidades arbitrarias
    plt.plot(x, acc_data_m_s2[11], color=line_color)
    plt.title('RMS en eje z [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('RMS [U.A.]')
    plt.show()

    # se grafican los datos de RMSx_5_peaks en unidades arbitrarias
    plt.scatter(x_5, acc_data_m_s2[12], color=line_color)
    plt.title('5 Peaks de RMS en eje x [U.A.]')
    plt.xlabel('5 Peaks')
    plt.ylabel('RMS [U.A.]')
    plt.show()

    # se grafican los datos de RMSy_5_peaks en unidades arbitrarias
    plt.scatter(x_5, acc_data_m_s2[13], color=line_color)
    plt.title('5 Peaks de RMS en eje y [U.A.]')
    plt.xlabel('5 Peaks')
    plt.ylabel('RMS [U.A.]')
    plt.show()

    # se grafican los datos de RMSz_5_peaks en unidades arbitrarias
    plt.scatter(x_5, acc_data_m_s2[14], color=line_color)
    plt.title('5 Peaks de RMS en eje z [U.A.]')
    plt.xlabel('5 Peaks')
    plt.ylabel('RMS [U.A.]')
    plt.show()

    # se grafican los datos de acc_x_5_peaks en m/s^2
    plt.scatter(x_5, acc_data_m_s2[15], color=line_color)
    plt.title('5 Peaks de Aceleración en eje x [m/s^2]')
    plt.xlabel('5 Peaks')
    plt.ylabel('Aceleración [m/s^2]')
    plt.show()

    # se grafican los datos de acc_y_5_peaks en m/s^2
    plt.scatter(x_5, acc_data_m_s2[16], color=line_color)
    plt.title('5 Peaks de Aceleración en eje y [m/s^2]')
    plt.xlabel('5 Peaks')
    plt.ylabel('Aceleración [m/s^2]')
    plt.show()

    # se grafican los datos de acc_z_5_peaks en m/s^2
    plt.scatter(x_5, acc_data_m_s2[17], color=line_color)
    plt.title('5 Peaks de Aceleración en eje z [m/s^2]')
    plt.xlabel('5 Peaks')
    plt.ylabel('Aceleración [m/s^2]')
    plt.show()

# función para graficar los datos de acc en g
def plot_data_acc_g(window_size):
    # color de los puntos/lineas de los gráficos
    line_color = 'red'

    # se crea un arreglo de 1 a window_size
    x = [i for i in range(1, window_size + 1)]

    # se crea un arreglo de 1 a 5
    x_5 = [i for i in range(1, 6)]

    # se grafican los datos de acc_x en g
    plt.plot(x, acc_data_g[0], color=line_color)
    plt.title('Aceleración en eje x [g]')
    plt.xlabel('Muestra')
    plt.ylabel('Aceleración [g]')
    plt.show()
    
    # se grafican los datos de acc_y en g
    plt.plot(x, acc_data_g[1], color=line_color)
    plt.title('Aceleración en eje y [g]')
    plt.xlabel('Muestra')
    plt.ylabel('Aceleración [g]')
    plt.show()

    # se grafican los datos de acc_z en g
    plt.plot(x, acc_data_g[2], color=line_color)
    plt.title('Aceleración en eje z [g]')
    plt.xlabel('Muestra')
    plt.ylabel('Aceleración [g]')
    plt.show()

    # se grafican los datos de FFTxRE en unidades arbitrarias
    plt.plot(x, acc_data_g[3], color=line_color)
    plt.title('FFT en eje x Real [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('FFT [U.A.]')
    plt.show()

    # se grafican los datos de FFTxIM en unidades arbitrarias
    plt.plot(x, acc_data_g[4], color=line_color)
    plt.title('FFT en eje x Imaginario [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('FFT [U.A.]')
    plt.show()

    # se grafican los datos de FFTyRE en unidades arbitrarias
    plt.plot(x, acc_data_g[5], color=line_color)
    plt.title('FFT en eje y Real [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('FFT [U.A.]')
    plt.show()

    # se grafican los datos de FFTyIM en unidades arbitrarias
    plt.plot(x, acc_data_g[6], color=line_color)
    plt.title('FFT en eje y Imaginario [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('FFT [U.A.]')
    plt.show()

    # se grafican los datos de FFTzRE en unidades arbitrarias
    plt.plot(x, acc_data_g[7], color=line_color)
    plt.title('FFT en eje z Real [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('FFT [U.A.]')
    plt.show()

    # se grafican los datos de FFTzIM en unidades arbitrarias
    plt.plot(x, acc_data_g[8], color=line_color)
    plt.title('FFT en eje z Imaginario [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('FFT [U.A.]')
    plt.show()

    # se grafican los datos de RMSx en unidades arbitrarias
    plt.plot(x, acc_data_g[9], color=line_color)
    plt.title('RMS en eje x [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('RMS [U.A.]')
    plt.show()

    # se grafican los datos de RMSy en unidades arbitrarias
    plt.plot(x, acc_data_g[10], color=line_color)
    plt.title('RMS en eje y [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('RMS [U.A.]')
    plt.show()

    # se grafican los datos de RMSz en unidades arbitrarias
    plt.plot(x, acc_data_g[11], color=line_color)
    plt.title('RMS en eje z [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('RMS [U.A.]')
    plt.show()

    # se grafican los datos de RMSx_5_peaks en unidades arbitrarias
    plt.scatter(x_5, acc_data_g[12], color=line_color)
    plt.title('5 Peaks de RMS en eje x [U.A.]')
    plt.xlabel('5 Peaks')
    plt.ylabel('RMS [U.A.]')
    plt.show()

    # se grafican los datos de RMSy_5_peaks en unidades arbitrarias
    plt.scatter(x_5, acc_data_g[13], color=line_color)
    plt.title('5 Peaks de RMS en eje y [U.A.]')
    plt.xlabel('5 Peaks')
    plt.ylabel('RMS [U.A.]')
    plt.show()

    # se grafican los datos de RMSz_5_peaks en unidades arbitrarias
    plt.scatter(x_5, acc_data_g[14], color=line_color)
    plt.title('5 Peaks de RMS en eje z [U.A.]')
    plt.xlabel('5 Peaks')
    plt.ylabel('RMS [U.A.]')
    plt.show()

    # se grafican los datos de acc_x_5_peaks en g
    plt.scatter(x_5, acc_data_g[15], color=line_color)
    plt.title('5 Peaks de Aceleración en eje x [g]')
    plt.xlabel('5 Peaks')
    plt.ylabel('Aceleración [g]')
    plt.show()

    # se grafican los datos de acc_y_5_peaks en g
    plt.scatter(x_5, acc_data_g[16], color=line_color)
    plt.title('5 Peaks de Aceleración en eje y [g]')
    plt.xlabel('5 Peaks')
    plt.ylabel('Aceleración [g]')
    plt.show()

    # se grafican los datos de acc_z_5_peaks en g
    plt.scatter(x_5, acc_data_g[17], color=line_color)
    plt.title('5 Peaks de Aceleración en eje z [g]')
    plt.xlabel('5 Peaks')
    plt.ylabel('Aceleración [g]')
    plt.show()

# función para graficar los datos de gyr en rad/s
def plot_data_gyr_rad_s(window_size):
    # color de los puntos/lineas de los gráficos
    line_color = 'navy'

    # se crea un arreglo de 1 a window_size
    x = [i for i in range(1, window_size + 1)]

    # se crea un arreglo de 1 a 5
    x_5 = [i for i in range(1, 6)]

    # se grafican los datos de gyr_x en rad/s
    plt.plot(x, gyro_data_rad_s[0], color=line_color)
    plt.title('Velocidad angular en eje x [rad/s]')
    plt.xlabel('Muestra')
    plt.ylabel('Velocidad angular [rad/s]')
    plt.show()
    
    # se grafican los datos de gyr_y en rad/s
    plt.plot(x, gyro_data_rad_s[1], color=line_color)
    plt.title('Velocidad angular en eje y [rad/s]')
    plt.xlabel('Muestra')
    plt.ylabel('Velocidad angular [rad/s]')
    plt.show()

    # se grafican los datos de gyr_z en rad/s
    plt.plot(x, gyro_data_rad_s[2], color=line_color)
    plt.title('Velocidad angular en eje z [rad/s]')
    plt.xlabel('Muestra')
    plt.ylabel('Velocidad angular [rad/s]')
    plt.show()

    # se grafican los datos de FFTxRE en unidades arbitrarias
    plt.plot(x, gyro_data_rad_s[3], color=line_color)
    plt.title('FFT en eje x Real [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('FFT [U.A.]')
    plt.show()

    # se grafican los datos de FFTxIM en unidades arbitrarias
    plt.plot(x, gyro_data_rad_s[4], color=line_color)
    plt.title('FFT en eje x Imaginario [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('FFT [U.A.]')
    plt.show()

    # se grafican los datos de FFTyRE en unidades arbitrarias
    plt.plot(x, gyro_data_rad_s[5], color=line_color)
    plt.title('FFT en eje y Real [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('FFT [U.A.]')
    plt.show()

    # se grafican los datos de FFTyIM en unidades arbitrarias
    plt.plot(x, gyro_data_rad_s[6], color=line_color)
    plt.title('FFT en eje y Imaginario [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('FFT [U.A.]')
    plt.show()

    # se grafican los datos de FFTzRE en unidades arbitrarias
    plt.plot(x, gyro_data_rad_s[7], color=line_color)
    plt.title('FFT en eje z Real [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('FFT [U.A.]')
    plt.show()

    # se grafican los datos de FFTzIM en unidades arbitrarias
    plt.plot(x, gyro_data_rad_s[8], color=line_color)
    plt.title('FFT en eje z Imaginario [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('FFT [U.A.]')
    plt.show()

    # se grafican los datos de RMSx en unidades arbitrarias
    plt.plot(x, gyro_data_rad_s[9], color=line_color)
    plt.title('RMS en eje x [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('RMS [U.A.]')
    plt.show()

    # se grafican los datos de RMSy en unidades arbitrarias
    plt.plot(x, gyro_data_rad_s[10], color=line_color)
    plt.title('RMS en eje y [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('RMS [U.A.]')
    plt.show()

    # se grafican los datos de RMSz en unidades arbitrarias
    plt.plot(x, gyro_data_rad_s[11], color=line_color)
    plt.title('RMS en eje z [U.A.]')
    plt.xlabel('Muestra')
    plt.ylabel('RMS [U.A.]')
    plt.show()

    # se grafican los datos de RMSx_5_peaks en unidades arbitrarias
    plt.scatter(x_5, gyro_data_rad_s[12], color=line_color)
    plt.title('5 Peaks de RMS en eje x [U.A.]')
    plt.xlabel('5 Peaks')
    plt.ylabel('RMS [U.A.]')
    plt.show()

    # se grafican los datos de RMSy_5_peaks en unidades arbitrarias
    plt.scatter(x_5, gyro_data_rad_s[13], color=line_color)
    plt.title('5 Peaks de RMS en eje y [U.A.]')
    plt.xlabel('5 Peaks')
    plt.ylabel('RMS [U.A.]')
    plt.show()

    # se grafican los datos de RMSz_5_peaks en unidades arbitrarias
    plt.scatter(x_5, gyro_data_rad_s[14], color=line_color)
    plt.title('5 Peaks de RMS en eje z [U.A.]')
    plt.xlabel('5 Peaks')
    plt.ylabel('RMS [U.A.]')
    plt.show()

    # se grafican los datos de gyr_x_5_peaks en rad/s
    plt.scatter(x_5, gyro_data_rad_s[15], color=line_color)
    plt.title('5 Peaks de Velocidad angular en eje x [rad/s]')
    plt.xlabel('5 Peaks')
    plt.ylabel('Velocidad angular [rad/s]')
    plt.show()

    # se grafican los datos de gyr_y_5_peaks en rad/s
    plt.scatter(x_5, gyro_data_rad_s[16], color=line_color)
    plt.title('5 Peaks de Velocidad angular en eje y [rad/s]')
    plt.xlabel('5 Peaks')
    plt.ylabel('Velocidad angular [rad/s]')
    plt.show()

    # se grafican los datos de gyr_z_5_peaks en rad/s
    plt.scatter(x_5, gyro_data_rad_s[17], color=line_color)
    plt.title('5 Peaks de Velocidad angular en eje z [rad/s]')
    plt.xlabel('5 Peaks')
    plt.ylabel('Velocidad angular [rad/s]')
    plt.show()

# objeto de configuracion de la BMI270
bmi_config = BMI_CONFIG()

# función para el loop principal
def loop():
    # se lee data por la conexion serial
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
                    
                    # si el mode no es '0' (modo de potencia suspendido)
                    if bmi_params['mode'] != 'S':
                        # se inicializan los arreglos de datos
                        initialize_data(bmi_params['sample_size'])

                    # se envia el mensaje de inicio de lectura, este también contiene la configuración de la BMI270
                    begin_message = pack('{}s'.format(len(begin_with_config)),begin_with_config.encode())
                    send_message(begin_message)

                ## si el mensaje es b'Procesamiento finalizado\n\n'
                elif response == b'Procesamiento finalizado\r\n':
                    # se imprimen los gráficos
                    plot_data_acc_m_s2(bmi_params['sample_size'])
                    plot_data_acc_g(bmi_params['sample_size'])
                    # si es el modo es normal o performance
                    if bmi_params['mode'] == 'N' or bmi_params['mode'] == 'P':
                        plot_data_gyr_rad_s(bmi_params['sample_size'])
                    
                else:
                    # se parsea la linea para ver si se debe guardar en los arreglos de datos
                    parse_line(response)

            except KeyboardInterrupt:
                print('Finalizando comunicacion')
                break
            except:
                print('Error en leer mensaje')
                continue

# se ejecuta el loop principal
loop()
