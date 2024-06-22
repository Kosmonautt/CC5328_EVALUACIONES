# Función que transforma un entero en un string de 3 caracteres
def int_to_str(num):
    # si el número es None, se retorna '000'
    if num is None:
        return '000'
    return str(num).zfill(3)

class BMI_CONFIG:
        def __init__(self):
                self.power_modes = ["S", "L", "N", "P"]
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

                self.chosen_mode = None
                self.chosen_odr_accel = None
                self.chosen_range_accel = None
                self.chosen_odr_gyro = None
                self.chosen_range_gyro = None
                self.sample_size = None

        def set_mode(self, mode):
                # Se cambia el modo de operación
                self.chosen_mode = mode

                # Si el modo es "S", se resetean los valores de la aceleración
                if mode == "S":
                        self.chosen_odr_accel = int_to_str(None)
                        self.chosen_range_accel = int_to_str(None)
                        self.chosen_odr_gyro = int_to_str(None)
                        self.chosen_range_gyro = int_to_str(None)

                # Si el modo es "L", se resetean los valores del giroscopio
                elif mode == "L":
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
        def is_ready(self):
                # Si el modo de operación no está definido, se retorna False
                if self.chosen_mode is None:
                        return False

                # Si el modo de operación es "L", se revisa que el ODR, el rango del acelerómetro y el tamaño de la muestra estén definidos
                if self.chosen_mode == "L":
                        if self.chosen_odr_accel is None or self.chosen_range_accel is None or self.sample_size is None:
                                return False
            
                # Si el modo de operación es "N" o "P", se revisa que el ODR, el rango del acelerómetro, el ODR y el rango del giroscopio y el tamaño de la muestra estén definidos
                if self.chosen_mode == "N" or self.chosen_mode == "P":
                        if self.chosen_odr_accel is None or self.chosen_range_accel is None or self.chosen_odr_gyro is None or self.chosen_range_gyro is None or self.sample_size is None:
                                return False
                
                return True
        
        # Se transforma la configuración en un string
        def to_string(self):
                # Si la configuración no está lista, se retorna None
                if not self.is_ready():
                        return None
                
                # Se retorna el string con la configuración
                return 'BEGIN' + self.chosen_mode + self.chosen_odr_accel + self.chosen_range_accel + self.chosen_odr_gyro + self.chosen_range_gyro + self.sample_size + '\0'
        
        

        