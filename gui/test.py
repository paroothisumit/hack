import sys

import time
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QScrollArea, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
import gui_controller
import threading

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 simple window - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        # self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # button = QPushButton('PyQt5 button', self)
        # button.setToolTip('This is an example button')
        # button.move(100, 70)
        # button.clicked.connect(self.on_click)

        scroll = QScrollArea(self)
        label = QLabel()
        label.setAlignment(Qt.AlignVCenter)
        label.setText("SITE INFORMATION for ID: " + str(id))
        label.setStyleSheet('font-size:30px')

        scroll.setFixedSize(200, 100)
        scroll.setWidget(label)
        # scroll.show()

        # self.statusBar().showMessage('Message in statusbar.')
        self.show()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # ex = App()
    # sys.exit(app.exec_())
    threading.Thread(target=gui_controller.gui_init, kwargs={'server_address': "127.0.0.1"}).start()
    time.sleep(3)
    gui_controller.new_alert(gui_controller.create_new_alert())
    gui_controller.new_alert(gui_controller.create_new_alert(sourceId=1, activity_recognized="multiple people running",
                                                             location_description="City Palace"))