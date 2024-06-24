import threading
from embebidos import Ui_Dialog
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QGraphicsScene
from esp32_com import ESP32_COM
from sensor_config import BMI_CONFIG, BME_CONFIG
from serial.serialutil import SerialException
from enum import Enum

# Se configura el puerto y el BAUD_Rate
PORT = 'COM3'  # Esto depende del sistema operativo
BAUD_RATE = 115200  # Debe coincidir con la configuracion de la ESP32

bmi_config = BMI_CONFIG()
bme_config = BME_CONFIG()

class Sensor(Enum):
    BMI270 = 1
    BME688 = 2

class SerialWorker(QtCore.QObject):
    detectedSensorSignal = QtCore.pyqtSignal(Sensor)
    progressBarSignal = QtCore.pyqtSignal(int)
    initBMI270 = QtCore.pyqtSignal()
    initBME688 = QtCore.pyqtSignal()
    setPlotSignal = QtCore.pyqtSignal(int)

class Controller:
    def __init__(self, parent):
        self.ui = Ui_Dialog()
        self.parent = parent
        self.worker = SerialWorker()
        self.worker.detectedSensorSignal.connect(self.setDetectedSensor)
        self.worker.progressBarSignal.connect(self.setProgressBar)
        self.worker.initBMI270.connect(self.initBMI270)
        self.worker.initBME688.connect(self.initBME688)
        self.worker.setPlotSignal.connect(self.setPlot)
        self.uiReady = False
        self.chosen_sensor = None
        self.plotIndex = 0
        self.numberOfPlots = None
    
    def initBMI270(self):
        if self.uiReady:
            return

        self.uiReady = True

        _translate = QtCore.QCoreApplication.translate

        # Para el rango del acelerometro
        for i in range(4):
                self.ui.comboBox_acc_range.addItem("")
        # Valores de rango de acelerometro dropdown
        for i in range(4):
                self.ui.comboBox_acc_range.setItemText(i, _translate("Dialog", list(bmi_config.range_accel.keys())[i]))
        
        # Para el ODR del acelerometro
        for i in range(12):
                self.ui.comboBox_acc_odr.addItem("")
        # Valores de ODR de acelerometro dropdown
        for i in range(12):
                self.ui.comboBox_acc_odr.setItemText(i, _translate("Dialog", list(bmi_config.odr_accel.keys())[i]))
        
        # Para el rango del giroscopio
        for i in range(5):
            self.ui.comboBox_gyr_range.addItem("")
        # Valores de rangos de giroscopio dropdown
        for i in range(5):
                self.ui.comboBox_gyr_range.setItemText(i, _translate("Dialog", list(bmi_config.range_gyro.keys())[i]))
        
        # Para el ODR del giroscopio
        for i in range(8):
                self.ui.comboBox_gyr_odr.addItem("")
        # Valores de ODR de giroscopio dropdown
        for i in range(8):
                self.ui.comboBox_gyr_odr.setItemText(i, _translate("Dialog", list(bmi_config.odr_gyro.keys())[i]))
        
        # Para el modo de operacion
        for i in range(4):
                self.ui.comboBox_mode.addItem("")
        # Modo de funcionamiento dropdown valores
        for i in range(4):
                self.ui.comboBox_mode.setItemText(i, _translate("Dialog", list(bmi_config.power_modes.keys())[i]))
    
    def initBME688(self):
        if self.uiReady:
            return

        self.uiReady = True

        _translate = QtCore.QCoreApplication.translate
        
        # Para el modo de operacion
        for i in range(3):
                self.ui.comboBox_mode.addItem("")
        # Modo de funcionamiento dropdown valores
        for i in range(3):
                self.ui.comboBox_mode.setItemText(i, _translate("Dialog", list(bme_config.power_modes.keys())[i]))

    def setSignals(self):
        self.ui.button_configure.clicked.connect(self.leerConfiguracion)
        self.ui.button_start_read.clicked.connect(self.beginRead)
        self.ui.button_next_plot.clicked.connect(self.siguientePlot)
        self.ui.button_previous_plot.clicked.connect(self.anteriorPlot)
    
    def siguientePlot(self):
        if self.plotIndex < self.numberOfPlots - 1:
            self.plotIndex += 1
            self.worker.setPlotSignal.emit(self.plotIndex)
    def anteriorPlot(self):
        if self.plotIndex > 0:
            self.plotIndex -= 1
            self.worker.setPlotSignal.emit(self.plotIndex)
    
    def setPlot(self, index):
        # se consigue el elemento index del diccionario plots_info
        if self.chosen_sensor == Sensor.BMI270:
            key = list(bmi_config.plots_info.keys())[index]
        elif self.chosen_sensor == Sensor.BME688:
            pass
        
        dicc = bmi_config.plots_info[key]

        self.ui.labelPlot.setText(dicc['title'])

        # Se crea una figura
        figure = Figure()
        # Se crea un canvas para la figura
        canvas = FigureCanvas(figure)

        # se consiguen los datos del grafico	
        y = dicc['data'][dicc['index']]
        # se consigue el largo de los datos
        x = range(1, len(y) + 1)

        # Optional: Add a subplot to the figure and plot something
        ax = figure.add_subplot(111)
        ax.plot(x, y, dicc['color'])
        ax.set_title(dicc['title'])
        ax.set_xlabel(dicc['xlabel'])
        ax.set_ylabel(dicc['ylabel'])

        # Se crea una escena
        scene = QGraphicsScene()
        scene.addWidget(canvas)

        # Se añade la escena al plot
        self.ui.Plot.setScene(scene)
    
    def setDetectedSensor(self, sensor):
        self.chosen_sensor = sensor
        if sensor == Sensor.BMI270:
            self.ui.label_set_sensor.setText('BMI270')
        elif sensor == Sensor.BME688:
            self.ui.label_set_sensor.setText('BME688')
    
    def setProgressBar(self, value):
        self.ui.progressBar.setProperty("value", value)

    def leerConfiguracion(self):
        conf = dict()

        if self.chosen_sensor == Sensor.BMI270:
            conf['Mode'] = self.ui.comboBox_mode.currentText()
            conf['AccODR'] = self.ui.comboBox_acc_odr.currentText()
            conf['AccRange'] = self.ui.comboBox_acc_range.currentText()
            conf['GyroODR'] = self.ui.comboBox_gyr_odr.currentText()
            conf['GyroRange'] = self.ui.comboBox_gyr_range.currentText()
            conf['SampleSize'] = self.ui.spinBox_window_size.value()

            # Se configura la BMI270
            bmi_config.set_mode(conf['Mode'])
            bmi_config.set_odr_accel(conf['AccODR'])
            bmi_config.set_range_accel(conf['AccRange'])
            bmi_config.set_odr_gyro(conf['GyroODR'])
            bmi_config.set_range_gyro(conf['GyroRange'])
            bmi_config.set_sample_size(conf['SampleSize'])
        
        elif self.chosen_sensor == Sensor.BME688:
            conf['Mode'] = self.ui.comboBox_mode.currentText()
            conf['SampleSize'] = self.ui.spinBox_window_size.value()

            # Se configura la BME688
            bme_config.set_mode(conf['Mode'])
            bme_config.set_sample_size(conf['SampleSize'])
    
    def beginRead(self):
        if self.chosen_sensor == Sensor.BMI270:
            # Se revisa si la configuración está lista
            bmi_config.is_ready_changed()
        elif self.chosen_sensor == Sensor.BME688:
            # Se revisa si la configuración está lista
            bme_config.is_ready_changed()


    def criticalError(self):
        popup = QtWidgets.QMessageBox(parent= self.parent)
        popup.setWindowTitle('Error Critico')
        popup.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        popup.exec()
        return

    def stop(self):
        print('Captando datos')

    def start_read_thread(self):
        thread = threading.Thread(target=self.read_loop_BMI)
        thread.daemon = True  # Set the thread as a daemon
        thread.start()

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
                        if response == b'Esperando inicio de lectura.\r\n':

                            # Se pone en 100 el progressBar
                            self.worker.progressBarSignal.emit(100)

                            if self.chosen_sensor == Sensor.BMI270:
                                # si la configuración no ha sido seleccionada, se espera
                                bmi_config.ready_event.wait()

                                print('Configuracion lista')

                                bmi_config.initialize_data(bmi_config.sample_size)

                                # se codifica la configuración de la BMI270
                                begin_message = esp32_com.encode_message(bmi_config.to_string())

                                # se envia el mensaje de inicio de lectura, este también contiene la configuración de la BMI270
                                esp32_com.send_message(begin_message)

                                # se limpian los valores de la configuración
                                bmi_config.clear()

                                # se pone el evento en estado clear
                                bmi_config.ready_event.clear()

                            elif self.chosen_sensor == Sensor.BME688:
                                # si la configuración no ha sido seleccionada, se espera
                                bme_config.ready_event.wait()

                                print('Configuracion lista')

                                # se codifica la configuración de la BME688
                                begin_message = esp32_com.encode_message(bme_config.to_string())

                                # se envia el mensaje de inicio de lectura, este también contiene la configuración de la BME688
                                esp32_com.send_message(begin_message)

                                # se limpian los valores de la configuración
                                bme_config.clear()

                                # se pone el evento en estado clear
                                bme_config.ready_event.clear()
                        
                        # Si el mensaje es b'Chip BMI270 reconocido.\r\n'
                        elif response == b'Chip BMI270 reconocido.\r\n':
                            self.worker.detectedSensorSignal.emit(Sensor.BMI270)
                            self.worker.initBMI270.emit()
                            self.worker.progressBarSignal.emit(50)
                            self.numberOfPlots = len(bmi_config.plots_info)

                        # Si el mensaje es b'Chip BME688 reconocido.\r\n'
                        elif response == b'Chip BME688 reconocido.\r\n':
                            self.worker.detectedSensorSignal.emit(Sensor.BME688)
                            self.worker.initBME688.emit()
                            self.worker.progressBarSignal.emit(50)
                            self.numberOfPlots = len(bme_config.plots_info)

                        elif response == b'Softreset: OK\r\n':
                             self.worker.progressBarSignal.emit(25)
                            
                        ## si el mensaje es b'Procesamiento finalizado\n\n'
                        elif response == b'Procesamiento finalizado\r\n':
                            self.plotIndex = 0
                            self.worker.setPlotSignal.emit(self.plotIndex)

                        else:
                            if self.chosen_sensor == Sensor.BMI270:
                                bmi_config.parse_line(response)
                            elif self.chosen_sensor == Sensor.BME688:
                                bme_config.parse_line(response)

                    except KeyboardInterrupt:
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
    cont.start_read_thread()
    sys.exit(app.exec_())