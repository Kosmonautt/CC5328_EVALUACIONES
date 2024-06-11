from embebidos import Ui_Dialog
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
import numpy as np
import serial
import time

class Controller:
    def __init__(self, parent):
        self.ui = Ui_Dialog()
        self.parent = parent
        self.ser = serial.Serial('COM3', 115200, timeout=1)
        self.data_buffer = {"BMI270": [], "BME688": []}

    def setSignals(self):
        self.ui.selec_12.currentIndexChanged.connect(self.leerModoOperacion)
        self.ui.pushButton.clicked.connect(self.leerConfiguracion)
        self.ui.pushButton_2.clicked.connect(self.startDataCapture)

    def leerConfiguracion(self):
        conf = dict()
        conf['AccSamp'] = self.ui.comboBox_acc_sampling.currentText()
        conf['AccSen'] = self.ui.text_acc_sensibity.toPlainText()
        # Enviar la configuración a la ESP32
        self.ser.write(f"CONF,{conf['AccSamp']},{conf['AccSen']}\n".encode())
        print(conf)
        return conf

    def leerModoOperacion(self):
        index = self.ui.selec_12.currentIndex()
        texto = self.ui.selec_12.itemText(index)
        # Enviar el modo de operación a la ESP32
        self.ser.write(f"MODE,{texto}\n".encode())
        print(texto)
        return texto

    def startDataCapture(self):
        print('Captando datos')
        self.ser.write("START\n".encode())
        self.data_timer = QtCore.QTimer()
        self.data_timer.timeout.connect(self.updateData)
        self.data_timer.start(1000)

    def updateData(self):
        data = self.ser.readline().decode().strip()
        if data:
            sensor_type, values = data.split(":")
            values = [float(val) for val in values.split(",")]
            self.data_buffer[sensor_type].append(values)
            self.plotData(sensor_type, values)

    def plotData(self, sensor_type, values):
        if sensor_type == "BMI270":
            self.plot(self.ui.Plot1, values)
        elif sensor_type == "BME688":
            self.plot(self.ui.Plot2, values)

    def plot(self, canvas, values):
        ax = canvas.figure.subplots()
        ax.clear()
        ax.plot(values)
        canvas.draw()

    def criticalError(self):
        popup = QtWidgets.QMessageBox(parent= self.parent)
        popup.setWindowTitle('Error Critico')
        popup.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        popup.exec()
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
