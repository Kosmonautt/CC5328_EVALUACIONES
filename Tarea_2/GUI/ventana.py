import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog
import sys

class MyDialog(QDialog):
    def __init__(self):
        super(MyDialog, self).__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'Embedido_tarea2.ui') 
        uic.loadUi(ui_path, self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec_())
