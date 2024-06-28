import threading

# Función que transforma un entero en un string de 3 caracteres
def int_to_str(num):
    # si el número es None, se retorna '000'
    if num is None:
        return '000'
    return str(num).zfill(3)

class BMI_CONFIG:
    def __init__(self):
        self.power_modes = {
            "Suspendido": "S",
            "Baja potencia": "L",
            "Normal": "N",
            "Alta potencia": "P"
        }
        self.odr_accel = {
            "0.78125 Hz": 0x01,
            "1.5625 Hz": 0x02,
            "3.125 Hz": 0x03,
            "6.25 Hz": 0x04,
            "12.5 Hz": 0x05,
            "25 Hz": 0x06,
            "50 Hz": 0x07,
            "100 Hz": 0x08,
            "200 Hz": 0x09,
            "400 Hz": 0x0A,
            "800 Hz": 0x0B,
            "1600 Hz": 0x0C
        }
        self.range_accel = {
            "+/- 2g": 0x00,
            "+/- 4g": 0x01,
            "+/- 8g": 0x02,
            "+/- 16g": 0x03
        }
        self.odr_gyro = {
            "25 Hz": 0x06,
            "50 Hz": 0x07,
            "100 Hz": 0x08,
            "200 Hz": 0x09,
            "400 Hz": 0x0A,
            "800 Hz": 0x0B,
            "1600 Hz": 0x0C,
            "3200 Hz": 0x0D
        }
        self.range_gyro = {
            "+/- 2000 dps": 0x00,
            "+/- 1000 dps": 0x01,
            "+/- 500 dps": 0x02,
            "+/- 250 dps": 0x03,
            "+/- 125 dps": 0x04
        }

        self.ready_event = threading.Event()

        self.chosen_mode = None
        self.chosen_odr_accel = None
        self.chosen_range_accel = None
        self.chosen_odr_gyro = None
        self.chosen_range_gyro = None
        self.sample_size = None

        # arreglo para guardar los arreglos de datos de acc en m/s^2
        self.acc_data_m_s2 =  [[] for _ in range(17)]
        # arreglo para guardar los arreglos de datos de acc en g
        self.acc_data_g =  [[] for _ in range(17)]
        # arreglo para guardar los arreglos de datos de gyro en rad/s
        self.gyro_data_rad_s = [[] for _ in range(17)]

        # diccionario con los índices de los arreglos de datos, para acc en m/s^2, g y rad/s, con el identificador de la medida
        # como llave y el índice del arreglo como valor, para los arreglos de window_size
        self.window_size_index= {
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

        self.plots_info = {
            'Acc_x (m/s^2)': {
                'title': 'Aceleración en x [m/s^2]',
                'data': self.acc_data_m_s2,
                'index': 0,
                'color': 'orange',
                'xlabel': 'Muestra',
                'ylabel': 'Aceleración [m/s^2]'
            },
            'Acc_y (m/s^2)': {
                'title': 'Aceleración en y [m/s^2]',
                'data': self.acc_data_m_s2,
                'index': 1,
                'color': 'orange',
                'xlabel': 'Muestra',
                'ylabel': 'Aceleración [m/s^2]'
            },
            'Acc_z (m/s^2)': {
                'title': 'Aceleración en z [m/s^2]',
                'data': self.acc_data_m_s2,
                'index': 2,
                'color': 'orange',
                'xlabel': 'Muestra',
                'ylabel': 'Aceleración [m/s^2]'
            },
            'FFTx_RE (m/s^2)': {
                'title': 'FFT en eje x Real [U.A.]',
                'data': self.acc_data_m_s2,
                'index': 3,
                'color': 'orange',
                'xlabel': 'Muestra',
                'ylabel': 'FFT [U.A.]'
            },
            'FFTx_IM (m/s^2)': {
                'title': 'FFT en eje x Imaginario [U.A.]',
                'data': self.acc_data_m_s2,
                'index': 4,
                'color': 'orange',
                'xlabel': 'Muestra',
                'ylabel': 'FFT [U.A.]'
            },
            'FFTy_RE (m/s^2)': {
                'title': 'FFT en eje y Real [U.A.]',
                'data': self.acc_data_m_s2,
                'index': 5,
                'color': 'orange',
                'xlabel': 'Muestra',
                'ylabel': 'FFT [U.A.]'
            },
            'FFTy_IM (m/s^2)': {
                'title': 'FFT en eje y Imaginario [U.A.]',
                'data': self.acc_data_m_s2,
                'index': 6,
                'color': 'orange',
                'xlabel': 'Muestra',
                'ylabel': 'FFT [U.A.]'
            },
            'FFTz_RE (m/s^2)': {
                'title': 'FFT en eje z Real [U.A.]',
                'data': self.acc_data_m_s2,
                'index': 7,
                'color': 'orange',
                'xlabel': 'Muestra',
                'ylabel': 'FFT [U.A.]'
            },
            'FFTz_IM (m/s^2)': {
                'title': 'FFT en eje z Imaginario [U.A.]',
                'data': self.acc_data_m_s2,
                'index': 8,
                'color': 'orange',
                'xlabel': 'Muestra',
                'ylabel': 'FFT [U.A.]'
            },
            'RMSx (m/s^2)': {
                'title': 'RMS en eje x [U.A.]',
                'data': self.acc_data_m_s2,
                'index': 9,
                'color': 'orange',
                'xlabel': 'Muestra',
                'ylabel': 'RMS [U.A.]'
            },
            'RMSy (m/s^2)': {
                'title': 'RMS en eje y [U.A.]',
                'data': self.acc_data_m_s2,
                'index': 10,
                'color': 'orange',
                'xlabel': 'Muestra',
                'ylabel': 'RMS [U.A.]'
            },
            'RMSz (m/s^2)': {
                'title': 'RMS en eje z [U.A.]',
                'data': self.acc_data_m_s2,
                'index': 11,
                'color': 'orange',
                'xlabel': 'Muestra',
                'ylabel': 'RMS [U.A.]'
            },
            '5peaks_RMSx (m/s^2)': {
                'title': '5 Peaks de RMS en eje x [U.A.]',
                'data': self.acc_data_m_s2,
                'index': 12,
                'color': 'orange',
                'xlabel': '5 Peaks',
                'ylabel': 'RMS [U.A.]'
            },
            '5peaks_RMSy (m/s^2)': {
                'title': '5 Peaks de RMS en eje y [U.A.]',
                'data': self.acc_data_m_s2,
                'index': 13,
                'color': 'orange',
                'xlabel': '5 Peaks',
                'ylabel': 'RMS [U.A.]'
            },
            '5peaks_RMSz (m/s^2)': {
                'title': '5 Peaks de RMS en eje z [U.A.]',
                'data': self.acc_data_m_s2,
                'index': 14,
                'color': 'orange',
                'xlabel': '5 Peaks',
                'ylabel': 'RMS [U.A.]'
            },
            '5peaks_acc_x (m/s^2)': {
                'title': '5 Peaks de Aceleración en eje x [m/s^2]',
                'data': self.acc_data_m_s2,
                'index': 15,
                'color': 'orange',
                'xlabel': '5 Peaks',
                'ylabel': 'Aceleración [m/s^2]'
            },
            '5peaks_acc_y (m/s^2)': {
                'title': '5 Peaks de Aceleración en eje y [m/s^2]',
                'data': self.acc_data_m_s2,
                'index': 16,
                'color': 'orange',
                'xlabel': '5 Peaks',
                'ylabel': 'Aceleración [m/s^2]'
            },
            '5peaks_acc_z (m/s^2)': {
                'title': '5 Peaks de Aceleración en eje z [m/s^2]',
                'data': self.acc_data_m_s2,
                'index': 17,
                'color': 'orange',
                'xlabel': '5 Peaks',
                'ylabel': 'Aceleración [m/s^2]'
            },
            'Acc_x (g)': {
                'title': 'Aceleración en x [g]',
                'data': self.acc_data_g,
                'index': 0,
                'color': 'red',
                'xlabel': 'Muestra',
                'ylabel': 'Aceleración [g]'
            },
            'Acc_y (g)': {
                'title': 'Aceleración en y [g]',
                'data': self.acc_data_g,
                'index': 1,
                'color': 'red',
                'xlabel': 'Muestra',
                'ylabel': 'Aceleración [g]'
            },
            'Acc_z (g)': {
                'title': 'Aceleración en z [g]',
                'data': self.acc_data_g,
                'index': 2,
                'color': 'red',
                'xlabel': 'Muestra',
                'ylabel': 'Aceleración [g]'
            },
            'FFTx_RE (g)': {
                'title': 'FFT en eje x Real [U.A.]',
                'data': self.acc_data_g,
                'index': 3,
                'color': 'red',
                'xlabel': 'Muestra',
                'ylabel': 'FFT [U.A.]'
            },
            'FFTx_IM (g)': {
                'title': 'FFT en eje x Imaginario [U.A.]',
                'data': self.acc_data_g,
                'index': 4,
                'color': 'red',
                'xlabel': 'Muestra',
                'ylabel': 'FFT [U.A.]'
            },
            'FFTy_RE (g)': {
                'title': 'FFT en eje y Real [U.A.]',
                'data': self.acc_data_g,
                'index': 5,
                'color': 'red',
                'xlabel': 'Muestra',
                'ylabel': 'FFT [U.A.]'
            },
            'FFTy_IM (g)': {
                'title': 'FFT en eje y Imaginario [U.A.]',
                'data': self.acc_data_g,
                'index': 6,
                'color': 'red',
                'xlabel': 'Muestra',
                'ylabel': 'FFT [U.A.]'
            },
            'FFTz_RE (g)': {
                'title': 'FFT en eje z Real [U.A.]',
                'data': self.acc_data_g,
                'index': 7,
                'color': 'red',
                'xlabel': 'Muestra',
                'ylabel': 'FFT [U.A.]'
            },
            'FFTz_IM (g)': {
                'title': 'FFT en eje z Imaginario [U.A.]',
                'data': self.acc_data_g,
                'index': 8,
                'color': 'red',
                'xlabel': 'Muestra',
                'ylabel': 'FFT [U.A.]'
            },
            'RMSx (g)': {
                'title': 'RMS en eje x [U.A.]',
                'data': self.acc_data_g,
                'index': 9,
                'color': 'red',
                'xlabel': 'Muestra',
                'ylabel': 'RMS [U.A.]'
            },
            'RMSy (g)': {
                'title': 'RMS en eje y [U.A.]',
                'data': self.acc_data_g,
                'index': 10,
                'color': 'red',
                'xlabel': 'Muestra',
                'ylabel': 'RMS [U.A.]'
            },
            'RMSz (g)': {
                'title': 'RMS en eje z [U.A.]',
                'data': self.acc_data_g,
                'index': 11,
                'color': 'red',
                'xlabel': 'Muestra',
                'ylabel': 'RMS [U.A.]'
            },
            '5peaks_RMSx (g)': {
                'title': '5 Peaks de RMS en eje x [U.A.]',
                'data': self.acc_data_g,
                'index': 12,
                'color': 'red',
                'xlabel': '5 Peaks',
                'ylabel': 'RMS [U.A.]'
            },
            '5peaks_RMSy (g)': {
                'title': '5 Peaks de RMS en eje y [U.A.]',
                'data': self.acc_data_g,
                'index': 13,
                'color': 'red',
                'xlabel': '5 Peaks',
                'ylabel': 'RMS [U.A.]'
            },
            '5peaks_RMSz (g)': {
                'title': '5 Peaks de RMS en eje z [U.A.]',
                'data': self.acc_data_g,
                'index': 14,
                'color': 'red',
                'xlabel': '5 Peaks',
                'ylabel': 'RMS [U.A.]'
            },
            '5peaks_acc_x (g)': {
                'title': '5 Peaks de Aceleración en eje x [g]',
                'data': self.acc_data_g,
                'index': 15,
                'color': 'red',
                'xlabel': '5 Peaks',
                'ylabel': 'Aceleración [g]'
            },
            '5peaks_acc_y (g)': {
                'title': '5 Peaks de Aceleración en eje y [g]',
                'data': self.acc_data_g,
                'index': 16,
                'color': 'red',
                'xlabel': '5 Peaks',
                'ylabel': 'Aceleración [g]'
            },
            '5peaks_acc_z (g)': {
                'title': '5 Peaks de Aceleración en eje z [g]',
                'data': self.acc_data_g,
                'index': 17,
                'color': 'red',
                'xlabel': '5 Peaks',
                'ylabel': 'Aceleración [g]'
            },
            'Gyro_x (rad/s)': {
                'title': 'Velocidad angular en eje x [rad/s]',
                'data': self.gyro_data_rad_s,
                'index': 0,
                'color': 'navy',
                'xlabel': 'Muestra',
                'ylabel': 'Giroscopio [rad/s]'
            },
            'Gyro_y (rad/s)': {
                'title': 'Velocidad angular en eje y [rad/s]',
                'data': self.gyro_data_rad_s,
                'index': 1,
                'color': 'navy',
                'xlabel': 'Muestra',
                'ylabel': 'Giroscopio [rad/s]'
            },
            'Gyro_z (rad/s)': {
                'title': 'Velocidad angular en eje z [rad/s]',
                'data': self.gyro_data_rad_s,
                'index': 2,
                'color': 'navy',
                'xlabel': 'Muestra',
                'ylabel': 'Giroscopio [rad/s]'
            },
            'FFTx_RE (rad/s)': {
                'title': 'FFT en eje x Real [U.A.]',
                'data': self.gyro_data_rad_s,
                'index': 3,
                'color': 'navy',
                'xlabel': 'Muestra',
                'ylabel': 'FFT [U.A.]'
            },
            'FFTx_IM (rad/s)': {
                'title': 'FFT en eje x Imaginario [U.A.]',
                'data': self.gyro_data_rad_s,
                'index': 4,
                'color': 'navy',
                'xlabel': 'Muestra',
                'ylabel': 'FFT [U.A.]'
            },
            'FFTy_RE (rad/s)': {
                'title': 'FFT en eje y Real [U.A.]',
                'data': self.gyro_data_rad_s,
                'index': 5,
                'color': 'navy',
                'xlabel': 'Muestra',
                'ylabel': 'FFT [U.A.]'
            },
            'FFTy_IM (rad/s)': {
                'title': 'FFT en eje y Imaginario [U.A.]',
                'data': self.gyro_data_rad_s,
                'index': 6,
                'color': 'navy',
                'xlabel': 'Muestra',
                'ylabel': 'FFT [U.A.]'
            },
            'FFTz_RE (rad/s)': {
                'title': 'FFT en eje z Real [U.A.]',
                'data': self.gyro_data_rad_s,
                'index': 7,
                'color': 'navy',
                'xlabel': 'Muestra',
                'ylabel': 'FFT [U.A.]'
            },
            'FFTz_IM (rad/s)': {
                'title': 'FFT en eje z Imaginario [U.A.]',
                'data': self.gyro_data_rad_s,
                'index': 8,
                'color': 'navy',
                'xlabel': 'Muestra',
                'ylabel': 'FFT [U.A.]'
            },
            'RMSx (rad/s)': {
                'title': 'RMS en eje x [U.A.]',
                'data': self.gyro_data_rad_s,
                'index': 9,
                'color': 'navy',
                'xlabel': 'Muestra',
                'ylabel': 'RMS [U.A.]'
            },
            'RMSy (rad/s)': {
                'title': 'RMS en eje y [U.A.]',
                'data': self.gyro_data_rad_s,
                'index': 10,
                'color': 'navy',
                'xlabel': 'Muestra',
                'ylabel': 'RMS [U.A.]'
            },
            'RMSz (rad/s)': {
                'title': 'RMS en eje z [U.A.]',
                'data': self.gyro_data_rad_s,
                'index': 11,
                'color': 'navy',
                'xlabel': 'Muestra',
                'ylabel': 'RMS [U.A.]'
            },
            '5peaks_RMSx (rad/s)': {
                'title': '5 Peaks de RMS en eje x [U.A.]',
                'data': self.gyro_data_rad_s,
                'index': 12,
                'color': 'navy',
                'xlabel': '5 Peaks',
                'ylabel': 'RMS [U.A.]'
            },
            '5peaks_RMSy (rad/s)': {
                'title': '5 Peaks de RMS en eje y [U.A.]',
                'data': self.gyro_data_rad_s,
                'index': 13,
                'color': 'navy',
                'xlabel': '5 Peaks',
                'ylabel': 'RMS [U.A.]'
            },
            '5peaks_RMSz (rad/s)': {
                'title': '5 Peaks de RMS en eje z [U.A.]',
                'data': self.gyro_data_rad_s,
                'index': 14,
                'color': 'navy',
                'xlabel': '5 Peaks',
                'ylabel': 'RMS [U.A.]'
            },
            '5peaks_gyr_x (rad/s)': {
                'title': '5 Peaks de Giroscopio en eje x [rad/s]',
                'data': self.gyro_data_rad_s,
                'index': 15,
                'color': 'navy',
                'xlabel': '5 Peaks',
                'ylabel': 'Giroscopio [rad/s]'
            },
            '5peaks_gyr_y (rad/s)': {
                'title': '5 Peaks de Giroscopio en eje y [rad/s]',
                'data': self.gyro_data_rad_s,
                'index': 16,
                'color': 'navy',
                'xlabel': '5 Peaks',
                'ylabel': 'Giroscopio [rad/s]'
            },
            '5peaks_gyr_z (rad/s)': {
                'title': '5 Peaks de Giroscopio en eje z [rad/s]',
                'data': self.gyro_data_rad_s,
                'index': 17,
                'color': 'navy',
                'xlabel': '5 Peaks',
                'ylabel': 'Giroscopio [rad/s]'
            }
        }

        # diccionario con los índices de los arreglos de datos, para acc en m/s^2, g y rad/s, con el identificador de la medida
        # como llave y el índice del arreglo como valor, para los arreglos de 5
        self.five_peaks_index= {
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

    # función para inicializar los arreglos de datos
    def initialize_data(self, window_size):
        # window_size se pasa a int
        window_size = int(window_size)

        # se borran los datos anteriores
        self.acc_data_m_s2.clear()
        self.acc_data_g.clear()
        self.gyro_data_rad_s.clear()
        
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
                self.acc_data_m_s2.append([0]*window_size)
                self.acc_data_g.append([0]*window_size)
                self.gyro_data_rad_s.append([0]*window_size)
            else:
                self.acc_data_m_s2.append([0]*5)
                self.acc_data_g.append([0]*5)
                self.gyro_data_rad_s.append([0]*5)

    def set_mode(self, mode):
        # Se cambia el modo de operación
        self.chosen_mode = self.power_modes[mode]

        # Si el modo es "S", se resetean los valores de la aceleración
        if self.chosen_mode == "S":
            self.chosen_odr_accel = int_to_str(None)
            self.chosen_range_accel = int_to_str(None)
            self.chosen_odr_gyro = int_to_str(None)
            self.chosen_range_gyro = int_to_str(None)

        # Si el modo es "L", se resetean los valores del giroscopio
        elif self.chosen_mode == "L":
            self.chosen_odr_gyro = int_to_str(None)
            self.chosen_range_gyro = int_to_str(None)
        
    # Se cambia el ODR del acelerómetro
    def set_odr_accel(self, odr_key):
        self.chosen_odr_accel = int_to_str(self.odr_accel[odr_key])
    
    # Se cambia el rango del acelerómetro
    def set_range_accel(self, range_key):
        self.chosen_range_accel = int_to_str(self.range_accel[range_key])
    
    # Se cambia el ODR del giroscopio
    def set_odr_gyro(self, odr_key):
        self.chosen_odr_gyro = int_to_str(self.odr_gyro[odr_key])
    
    # Se cambia el rango del giroscopio
    def set_range_gyro(self, range_key):
        self.chosen_range_gyro = int_to_str(self.range_gyro[range_key])
    
    # Se cambia el tamaño de la muestra
    def set_sample_size(self, sample_size):
        self.sample_size = int_to_str(sample_size)
    
    # Se revisa que todos los valores necesarios estén definidos
    def is_ready_changed(self):
        # Si el modo de operación no está definido, se retorna False
        if self.chosen_mode is None:
            self.ready_event.clear()

        # Si el modo de operación es "L", se revisa que el ODR, el rango del acelerómetro y el tamaño de la muestra estén definidos
        if self.chosen_mode == "L":
            if self.chosen_odr_accel is None or self.chosen_range_accel is None or self.sample_size is None:
                self.ready_event.clear()
    
        # Si el modo de operación es "N" o "P", se revisa que el ODR, el rango del acelerómetro, el ODR y el rango del giroscopio y el tamaño de la muestra estén definidos
        if self.chosen_mode == "N" or self.chosen_mode == "P":
            if self.chosen_odr_accel is None or self.chosen_range_accel is None or self.chosen_odr_gyro is None or self.chosen_range_gyro is None or self.sample_size is None:
                self.ready_event.clear()
        
        self.ready_event.set()
    
    # Se transforma la configuración en un string
    def to_string(self):
        # Si la configuración no está lista, se retorna None
        if not self.ready_event.is_set():
            return None
        
        # Se retorna el string con la configuración
        return 'BEGIN' + self.chosen_mode + self.chosen_odr_accel + self.chosen_range_accel + self.chosen_odr_gyro + self.chosen_range_gyro + self.sample_size + '\0'
    
    # Se limpian los valores de la configuración
    def clear(self):
        self.chosen_mode = None
        self.chosen_odr_accel = None
        self.chosen_range_accel = None
        self.chosen_odr_gyro = None
        self.chosen_range_gyro = None
        self.sample_size = None

    # función para parsear una linea de datos
    def parse_line(self, line):
        # se saca \r\n del final
        line = line[:-2]
        try:
            # se convierte a string
            line = line.decode('utf-8')
        except:
            return
        
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
                index_array = self.window_size_index[measure]
                # se consigue el arreglo de datos
                array = self.acc_data_m_s2[index_array]
                # se añade el valor al arreglo de datos
                array[sample_number - 1] = value

            elif data_type == 'Top':
                # se consigue el índice del arreglo de datos
                index_array = self.five_peaks_index[measure]
                # se consigue el arreglo de datos
                array = self.acc_data_m_s2[index_array]
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
                index_array = self.window_size_index[measure]
                # se consigue el arreglo de datos
                array = self.acc_data_g[index_array]
                # se añade el valor al arreglo de datos
                array[sample_number - 1] = value

            elif data_type == 'Top':
                # se consigue el índice del arreglo de datos
                index_array = self.five_peaks_index[measure]
                # se consigue el arreglo de datos
                array = self.acc_data_g[index_array]
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
                index_array = self.window_size_index[measure]
                # se consigue el arreglo de datos
                array = self.gyro_data_rad_s[index_array]
                # se añade el valor al arreglo de datos
                array[sample_number - 1] = value

            elif data_type == 'Top':
                # se consigue el índice del arreglo de datos
                index_array = self.five_peaks_index[measure]
                # se consigue el arreglo de datos
                array = self.gyro_data_rad_s[index_array]
                # se añade el valor al arreglo de datos
                array[sample_number - 1] = value

class BME_CONFIG:
    def __init__(self):
        self.power_modes = {
            "Suspendido": "S",
            "Forzado": "F",
            "Paralelo": "P",
        }


        self.ready_event = threading.Event()

        self.chosen_mode = None
        self.sample_size = None

        # arreglo para guardar los arreglos de datos de temp, presión, humedad, gas, 5 peaks de temp, presión, humedad y gas
        self.data = [[] for _ in range(8)]

        self.plots_info = {
            'Temperatura (°C)': {
                'title': 'Temperatura [°C]',
                'data': self.data,
                'index': 0,
                'color': 'red',
                'xlabel': 'Muestra',
                'ylabel': 'Temperatura [°C]'
            },
            'Presión (pa)': {
                'title': 'Presión [Pa]',
                'data': self.data,
                'index': 1,
                'color': 'blue',
                'xlabel': 'Muestra',
                'ylabel': 'Presión [Pa]'
            },
            'Humedad (%)': {
                'title': 'Humedad [%]',
                'data': self.data,
                'index': 2,
                'color': 'green',
                'xlabel': 'Muestra',
                'ylabel': 'Humedad [%]'
            },
            'Gas (Ohm)': {
                'title': 'Gas [Ohm]',
                'data': self.data,
                'index': 3,
                'color': 'orange',
                'xlabel': 'Muestra',
                'ylabel': 'Gas [Ohm]'
            },
            '5peaks_Temperatura (°C)': {
                'title': '5 Peaks de Temperatura [°C]',
                'data': self.data,
                'index': 4,
                'color': 'red',
                'xlabel': '5 Peaks',
                'ylabel': 'Temperatura [°C]'
            },
            '5peaks_Presión (pa)': {
                'title': '5 Peaks de Presión [Pa]',
                'data': self.data,
                'index': 5,
                'color': 'blue',
                'xlabel': '5 Peaks',
                'ylabel': 'Presión [Pa]'
            },
            '5peaks_Humedad (%)': {
                'title': '5 Peaks de Humedad [%]',
                'data': self.data,
                'index': 6,
                'color': 'green',
                'xlabel': '5 Peaks',
                'ylabel': 'Humedad [%]'
            },
            '5peaks_Gas (Ohm)': {
                'title': '5 Peaks de Gas [Ohm]',
                'data': self.data,
                'index': 7,
                'color': 'orange',
                'xlabel': '5 Peaks',
                'ylabel': 'Gas [Ohm]'
            }
        }

    def initialize_data(self, window_size):
        # window_size se pasa a int
        window_size = int(window_size)

        # se borran los datos anteriores
        self.data.clear()

        # se añaden los arreglos de datos
        # se añaden arreglos que guardaran la informacion de las medidas
        # 0 -> temp, 1 -> presión, 2 -> humedad, 3 -> gas
        # 4 -> temp_5_peaks, 5 -> presión_5_peaks, 6 -> humedad_5_peaks, 7 -> gas_5_peaks
        # los arreglos del 0 al 3 son de window_size elementos
        # del 4 al 7 son de 5 elementos
        for i in range(8):
            if i < 4:
                self.data.append([0]*window_size)
            else:
                self.data.append([0]*5)

    def set_mode(self, mode):
        # Se cambia el modo de operación
        self.chosen_mode = self.power_modes[mode]
    
    def set_sample_size(self, sample_size):
        self.sample_size = int_to_str(sample_size)

    def is_ready_changed(self):
        # Si el modo de operación no está definido, se retorna False
        if self.chosen_mode is None:
            self.ready_event.clear()
        
        # Si el modo de operación es "S", se revisa que el tamaño de la muestra esté definido
        if self.chosen_mode == "F" or self.chosen_mode == "P":
            if self.sample_size is None:
                self.ready_event.clear()
        
        self.ready_event.set()
    
    def to_string(self):
        # Si la configuración no está lista, se retorna None
        if not self.ready_event.is_set():
            return None
        
        # Se retorna el string con la configuración
        return 'BEGIN' + self.chosen_mode + self.sample_size + '\0'

    def clear(self):
        self.chosen_mode = None
        self.sample_size = None
    
    def parse_line(self, line):
        # se saca \r\n del final
        line = line[:-2]
        try:
            # se convierte a string
            line = line.decode('utf-8')
        except:
            return
        
        # si existe '[Temperatura]' en la linea
        if '[Temperatura]' in line:
            # se divide la linea en los datos por un espacio en blanco
            line = line.split(' ')
            # se consigue si es 'Lectura', 'Dato' o 'Top'
            data_type = line[1]
            # se consigue el número de muestra
            sample_number = int(line[2][:-1])
            # se consigue el valor de la medida
            value = float(line[3])

            if data_type == 'Lectura':
                # se añade el valor al arreglo de datos
                self.data[0][sample_number - 1] = value
            
            elif data_type == 'Top':
                # se añade el valor al arreglo de datos
                self.data[4][sample_number - 1] = value
        
        # si existe '[Presi\xc3\xb3n]' en la linea
        elif '[Presión]' in line:
            # se divide la linea en los datos por un espacio en blanco
            line = line.split(' ')
            # se consigue si es 'Lectura', 'Dato' o 'Top'
            data_type = line[1]
            # se consigue el número de muestra
            sample_number = int(line[2][:-1])
            # se consigue el valor de la medida
            value = float(line[3])

            if data_type == 'Lectura':
                # se añade el valor al arreglo de datos
                self.data[1][sample_number - 1] = value
            
            elif data_type == 'Top':
                # se añade el valor al arreglo de datos
                self.data[5][sample_number - 1] = value

        # si existe '[Humedad]' en la linea
        elif '[Humedad]' in line:
            # se divide la linea en los datos por un espacio en blanco
            line = line.split(' ')
            # se consigue si es 'Lectura', 'Dato' o 'Top'
            data_type = line[1]
            # se consigue el número de muestra
            sample_number = int(line[2][:-1])
            # se consigue el valor de la medida
            value = float(line[3])

            if data_type == 'Lectura':
                # se añade el valor al arreglo de datos
                self.data[2][sample_number - 1] = value
            
            elif data_type == 'Top':
                # se añade el valor al arreglo de datos
                self.data[6][sample_number - 1] = value
        
        # si existe '[Resistencia]' en la linea
        elif '[Resistencia]' in line:
            # se divide la linea en los datos por un espacio en blanco
            line = line.split(' ')
            # se consigue si es 'Lectura', 'Dato' o 'Top'
            data_type = line[1]
            # se consigue el número de muestra
            sample_number = int(line[2][:-1])
            # se consigue el valor de la medida
            value = float(line[3])

            if data_type == 'Lectura':
                # se añade el valor al arreglo de datos
                self.data[3][sample_number - 1] = value
            
            elif data_type == 'Top':
                # se añade el valor al arreglo de datos
                self.data[7][sample_number - 1] = value
    
    
        

        