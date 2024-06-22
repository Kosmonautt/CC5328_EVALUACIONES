# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Embedido_tarea2.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from bmi_config import BMI_CONFIG

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(774, 836)

        # Sensor activo label
        self.label_sensor = QtWidgets.QLabel(Dialog)
        self.label_sensor.setGeometry(QtCore.QRect(350, 130, 101, 21))
        self.label_sensor.setStyleSheet("color: rgb(0, 0, 0);\n"
"\n"
"")
        self.label_sensor.setObjectName("label_sensor")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(460, 130, 118, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        # Sensor activo dropdown
        self.comboBox_sensor = QtWidgets.QComboBox(Dialog)
        self.comboBox_sensor.setGeometry(QtCore.QRect(350, 160, 181, 31))
        self.comboBox_sensor.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_sensor.setObjectName("comboBox_sensor")
        self.comboBox_sensor.addItem("")
        self.comboBox_sensor.addItem("")
        self.comboBox_sensor.addItem("")

        # Frecuencia de muestreo de acelerometro label
        self.label_acc_ODR = QtWidgets.QLabel(Dialog)
        self.label_acc_ODR.setGeometry(QtCore.QRect(120, 180, 81, 31))
        self.label_acc_ODR.setObjectName("label_acc_ODR")

        ## ODR de acelerometro label
        self.label_acc_range = QtWidgets.QLabel(Dialog)
        self.label_acc_range.setGeometry(QtCore.QRect(120, 130, 81, 31))
        self.label_acc_range.setObjectName("label_acc_range")

        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(350, 40, 71, 41))
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        ## ODR de acelerometro dropdown
        self.comboBox_acc_odr = QtWidgets.QComboBox(Dialog)
        self.comboBox_acc_odr.setGeometry(QtCore.QRect(210, 180, 104, 31))
        self.comboBox_acc_odr.setObjectName("comboBox_acc_odr")
        for i in range(12):
                self.comboBox_acc_odr.addItem("")

        ## Modo de funcionamiento dropdown
        self.comboBox_mode = QtWidgets.QComboBox(Dialog)
        self.comboBox_mode.setGeometry(QtCore.QRect(360, 230, 181, 31))
        self.comboBox_mode.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_mode.setObjectName("comboBox_mode")
        self.comboBox_mode.addItem("")
        self.comboBox_mode.addItem("")

        # Modo de funcionamiento label
        self.label_mode = QtWidgets.QLabel(Dialog)
        self.label_mode.setGeometry(QtCore.QRect(390, 200, 121, 21))
        self.label_mode.setStyleSheet("color: rgb(0, 0, 0);\n"
"\n"
"")
        self.label_mode.setObjectName("label_mode")

        self.label_32 = QtWidgets.QLabel(Dialog)
        self.label_32.setGeometry(QtCore.QRect(170, 100, 121, 21))
        self.label_32.setStyleSheet("color: rgb(0, 0, 0);\n"
"\n"
"")
        self.label_32.setObjectName("label_32")
        self.label_33 = QtWidgets.QLabel(Dialog)
        self.label_33.setGeometry(QtCore.QRect(170, 220, 121, 21))
        self.label_33.setStyleSheet("color: rgb(0, 0, 0);\n"
"\n"
"")
        self.label_33.setObjectName("label_33")

        # ODR de giroscopio label
        self.label_gyr_range = QtWidgets.QLabel(Dialog)
        self.label_gyr_range.setGeometry(QtCore.QRect(120, 250, 81, 31))
        self.label_gyr_range.setObjectName("label_gyr_range")
        self.label_gyr_ODR = QtWidgets.QLabel(Dialog)
        self.label_gyr_ODR.setGeometry(QtCore.QRect(120, 300, 81, 31))
        self.label_gyr_ODR.setObjectName("label_gyr_ODR")

        # ODR de giroscopio dropdown
        self.comboBox_gyr_odr = QtWidgets.QComboBox(Dialog)
        self.comboBox_gyr_odr.setGeometry(QtCore.QRect(210, 300, 104, 31))
        self.comboBox_gyr_odr.setObjectName("comboBox_gyr_odr")
        for i in range(8):
                self.comboBox_gyr_odr.addItem("")

        # Rango de giroscopio dropdown
        self.comboBox_gyr_range = QtWidgets.QComboBox(Dialog)
        self.comboBox_gyr_range.setGeometry(QtCore.QRect(210, 250, 104, 31))
        self.comboBox_gyr_range.setObjectName("comboBox_gyr_range")
        for i in range(5):
                self.comboBox_gyr_range.addItem("")


        self.Plot1 = QtWidgets.QGraphicsView(Dialog)
        self.Plot1.setGeometry(QtCore.QRect(60, 420, 291, 181))
        self.Plot1.setFrameShape(QtWidgets.QFrame.Box)
        self.Plot1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Plot1.setObjectName("Plot1")
        self.Plot2 = QtWidgets.QGraphicsView(Dialog)
        self.Plot2.setGeometry(QtCore.QRect(390, 420, 291, 181))
        self.Plot2.setFrameShape(QtWidgets.QFrame.Box)
        self.Plot2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Plot2.setObjectName("Plot2")
        self.Plot3 = QtWidgets.QGraphicsView(Dialog)
        self.Plot3.setGeometry(QtCore.QRect(60, 640, 291, 181))
        self.Plot3.setFrameShape(QtWidgets.QFrame.Box)
        self.Plot3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Plot3.setObjectName("Plot3")
        self.Plot4 = QtWidgets.QGraphicsView(Dialog)
        self.Plot4.setGeometry(QtCore.QRect(390, 640, 291, 181))
        self.Plot4.setFrameShape(QtWidgets.QFrame.Box)
        self.Plot4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Plot4.setObjectName("Plot4")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(120, 390, 151, 21))
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setFrameShape(QtWidgets.QFrame.Box)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(440, 390, 151, 21))
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setFrameShape(QtWidgets.QFrame.Box)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(120, 610, 151, 21))
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setFrameShape(QtWidgets.QFrame.Box)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(440, 610, 151, 21))
        self.label_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_6.setFrameShape(QtWidgets.QFrame.Box)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(550, 160, 141, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(320, 370, 101, 41))
        self.pushButton_2.setObjectName("pushButton_2")

        # Rango de acelerometro dropdown
        self.comboBox_acc_range = QtWidgets.QComboBox(Dialog)
        self.comboBox_acc_range.setGeometry(QtCore.QRect(210, 130, 101, 31))
        self.comboBox_acc_range.setObjectName("comboBox_acc_range")
        for i in range(4):
                self.comboBox_acc_range.addItem("")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "UI Sensores"))

        # Sensor activo label valor
        self.label_sensor.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" text-decoration: underline;\">Sensor activo</span></p></body></html>"))
        
        # Sensor activo dropdown valores
        self.comboBox_sensor.setItemText(0, _translate("Dialog", "<Ninguno>"))
        self.comboBox_sensor.setItemText(1, _translate("Dialog", "BMI270"))
        self.comboBox_sensor.setItemText(2, _translate("Dialog", "BME688"))
        
        self.label_acc_ODR.setText(_translate("Dialog", "Frecuencia de \n"
" muestreo"))
        self.label_acc_range.setText(_translate("Dialog", "Rango"))
        self.label_2.setText(_translate("Dialog", "Configuracion \n"
" Sensor"))
        self.comboBox_mode.setItemText(0, _translate("Dialog", "Paralelo"))
        self.comboBox_mode.setItemText(1, _translate("Dialog", "Forzado"))
        self.label_mode.setText(_translate("Dialog", "Modo de Funcionamiento"))
        self.label_32.setText(_translate("Dialog", "<html><head/><body><p><span style=\" text-decoration: underline;\">Acelerómetro</span></p></body></html>"))
        self.label_33.setText(_translate("Dialog", "<html><head/><body><p><span style=\" text-decoration: underline;\">Giroscopio</span></p></body></html>"))
        self.label_gyr_range.setText(_translate("Dialog", "Rango"))
        self.label_gyr_ODR.setText(_translate("Dialog", "Frecuencia de \n"
" muestreo"))
        self.label_3.setText(_translate("Dialog", "Datos 1: <Datos>"))
        self.label_4.setText(_translate("Dialog", "Datos 2: <Datos>"))
        self.label_5.setText(_translate("Dialog", "Datos 3: <Datos>"))
        self.label_6.setText(_translate("Dialog", "Datos 4: <Datos>"))
        self.pushButton.setText(_translate("Dialog", "Iniciar configuración"))
        self.pushButton_2.setText(_translate("Dialog", "Iniciar captación \n"
" de datos"))
        
        # para acceder a los valores de los dropdowns
        bmi_config = BMI_CONFIG()

        # Valores de rangos de acelerometro dropdown
        for i in range(4):
                self.comboBox_acc_range.setItemText(i, _translate("Dialog", list(bmi_config.range_accel.keys())[i]))

        # Valores de ODR de acelerometro dropdown
        for i in range(12):
                self.comboBox_acc_odr.setItemText(i, _translate("Dialog", list(bmi_config.odr_accel.keys())[i]))


        # Valores de rangos de giroscopio dropdown
        for i in range(5):
                self.comboBox_gyr_range.setItemText(i, _translate("Dialog", list(bmi_config.range_gyro.keys())[i]))

        # Valores de ODR de giroscopio dropdown
        for i in range(8):
                self.comboBox_gyr_odr.setItemText(i, _translate("Dialog", list(bmi_config.odr_gyro.keys())[i]))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
