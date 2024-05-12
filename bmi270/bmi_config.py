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

    def print_settings(self):
        print("Configuraciones actuales:")
        print("Modos de Potencia:", self.power_modes)
        print("ODR Acelerómetro:", self.odr_accel)
        print("Rango Acelerómetro:", self.range_accel)
        print("ODR Giroscopio:", self.odr_gyro)
        print("Rango Giroscopio:", self.range_gyro)

    def user_input(self):
        ## al parameters are set to None
        self.chosen_mode = None
        self.chosen_odr_accel = None
        self.chosen_range_accel = None
        self.chosen_odr_gyro = None
        self.chosen_range_gyro = None
        self.sample_size = None
        

        print("Selecciona una opción para cambiar los parámetros:")

        def choose_option(options, prompt):
            for i, option in enumerate(options):
                print(f"{i}: {option}")
            index = int(input(prompt))
            return options[index]

        def choose_sample_size(self):
            print("Selecciona la cantidad de datos de la muestra (50 a 500):")
            size = int(input())
            while size < 50 or size > 500:
                print("Elige un número entre 50 y 500:")
                size = int(input())
            print(f"Tamaño de muestra seleccionado: {size}")
            self.sample_size = size

        # Modo de potencia
        mode = choose_option(self.power_modes, "Selecciona el modo de potencia: ")
        print(f"Modo de potencia seleccionado: {mode}")
        self.chosen_mode = mode

        if mode == "S":
            return

        # ODR Acelerómetro
        odr_accel = choose_option(list(self.odr_accel.keys()), "Selecciona el ODR del acelerómetro: ")
        print(f"ODR del acelerómetro seleccionado: {odr_accel}")
        self.chosen_odr_accel = odr_accel
        # Rango Acelerómetro
        range_accel = choose_option(list(self.range_accel.keys()), "Selecciona el rango del acelerómetro: ")
        print(f"Rango del acelerómetro seleccionado: {range_accel}")
        self.chosen_range_accel = range_accel

        if mode in ["N", "P"]:
            # ODR Giroscopio
            odr_gyro = choose_option(list(self.odr_gyro.keys()), "Selecciona el ODR del giroscopio: ")
            print(f"ODR del giroscopio seleccionado: {odr_gyro}")
            self.chosen_odr_gyro = odr_gyro
            # Rango Giroscopio
            range_gyro = choose_option(list(self.range_gyro.keys()), "Selecciona el rango del giroscopio: ")
            print(f"Rango del giroscopio seleccionado: {range_gyro}")
            self.chosen_range_gyro = range_gyro

        choose_sample_size(self)

    def get_user_input(self):
        return {
            "mode": self.chosen_mode,
            "odr_accel": self.odr_accel[self.chosen_odr_accel],
            "range_accel": self.range_accel[self.chosen_range_accel],
            "odr_gyro": self.odr_gyro[self.chosen_odr_gyro] if self.chosen_odr_gyro else None,
            "range_gyro": self.range_gyro[self.chosen_range_gyro] if self.chosen_range_gyro else None,
            "sample_size": self.sample_size
        }

