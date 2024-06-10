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
                    # # se imprimen los gráficos
                    # se imprimen los datos de acc en m/s^2, en el eje z
                    # print(acc_data_m_s2[2])
                    pass

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
