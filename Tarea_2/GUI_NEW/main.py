from embebidos import Ui_Dialog
from PyQt5 import QtCore, QtGui, QtWidgets
from esp32_com import ESP32_COM
from bmi_config import BMI_CONFIG
from serial.serialutil import SerialException

# Se configura el puerto y el BAUD_Rate
PORT = 'COM3'  # Esto depende del sistema operativo
BAUD_RATE = 115200  # Debe coincidir con la configuracion de la ESP32

bmi_config = BMI_CONFIG()

class Controller:
    def __init__(self, parent):
        self.ui = Ui_Dialog()
        self.parent = parent        
        self.esp32_ready = False # determines if the ESP32 is ready to receive the begin message


    def setSignals(self):
        self.ui.comboBox_sensor.currentIndexChanged.connect(self.leerModoOperacion)
        self.ui.button_configure.clicked.connect(self.leerConfiguracion)
        self.ui.button_start_read.clicked.connect(self.read_loop_BMI)

    def leerConfiguracion(self):
        conf = dict()
        conf['Mode'] = self.ui.comboBox_mode.currentText()
        conf['AccODR'] = self.ui.comboBox_acc_odr.currentText()
        conf['AccRange'] = self.ui.comboBox_acc_range.currentText()
        conf['GyroODR'] = self.ui.comboBox_gyr_odr.currentText()
        conf['GyroRange'] = self.ui.comboBox_gyr_range.currentText()
        conf['SampleSize'] = 50

        # Se configura la BMI270
        bmi_config.set_mode(conf['Mode'])
        bmi_config.set_odr_accel(conf['AccODR'])
        bmi_config.set_range_accel(conf['AccRange'])
        bmi_config.set_odr_gyro(conf['GyroODR'])
        bmi_config.set_range_gyro(conf['GyroRange'])
        bmi_config.set_sample_size(conf['SampleSize'])

        print (conf)
        return conf

    def leerModoOperacion(self):
        index = self.ui.comboBox_sensor.currentIndex()
        texto = self.ui.comboBox_sensor.itemText(index)
        print(texto)
        return texto

    def criticalError(self):
        popup = QtWidgets.QMessageBox(parent= self.parent)
        popup.setWindowTitle('Error Critico')
        popup.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        popup.exec()
        return

    def stop(self):
        print('Captando datos')

    def read_loop_BMI(self):
        try:
            esp32_com = ESP32_COM(PORT, BAUD_RATE)

            # se lee data por la conexion serial
            while True:
                if esp32_com.ser.in_waiting > 0:
                    try:
                        # se lee lo que la ESP32 imprime en la consola
                        response = esp32_com.receive_response()

                        # si el mensaje es b'Esperando inicio de lectura\r\n'
                        if response == b'Esperando inicio de lectura\r\n' or self.esp32_ready == True:

                            # si la configuración no ha sido seleccionada
                            if bmi_config.is_ready() == False:
                                print('Configuracion no seleccionada')
                                self.esp32_ready = True
                                return

                            # se codifica la configuración de la BMI270
                            begin_message = esp32_com.encode_message(bmi_config.to_string())

                            # # se envia el mensaje de inicio de lectura, este también contiene la configuración de la BMI270
                            esp32_com.send_message(begin_message)

                        ## si el mensaje es b'Procesamiento finalizado\n\n'
                        elif response == b'Procesamiento finalizado\r\n':
                            self.esp32_ready = True
                            return  
                        else:
                            pass

                    except KeyboardInterrupt:
                        self.esp32_ready = False
                        print('Finalizando comunicacion')
                        return

        except SerialException:
            print('Error al conectar con el puerto serial')
            return


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    cont = Controller(parent=Dialog)
    ui = cont.ui
    ui.setupUi(Dialog)
    Dialog.show()
    cont.setSignals()
    sys.exit(app.exec_())