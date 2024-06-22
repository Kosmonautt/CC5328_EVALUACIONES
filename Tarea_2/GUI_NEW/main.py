from embebidos import Ui_Dialog
from PyQt5 import QtCore, QtGui, QtWidgets
class Controller:

    def __init__(self, parent):
        self.ui = Ui_Dialog()
        self.parent = parent

    def setSignals(self):
        self.ui.comboBox_sensor.currentIndexChanged.connect(self.leerModoOperacion)
        self.ui.pushButton.clicked.connect(self.leerConfiguracion)
        # self.ui.pushButton_2.clicked.connect(self.stop())

    def leerConfiguracion(self):
        conf = dict()
        conf['AccRange'] = self.ui.comboBox_acc_range.currentText()
        conf['AccODR'] = self.ui.comboBox_acc_odr.currentText()
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
        #SE.serial_cycle()

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