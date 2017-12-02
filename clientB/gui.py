import sys, bridge
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import datetime
import requests,time,threading
width = 1280
height = 1024
btn_width = 60
btn_height = 60


class Dialog(QWidget):
    def __init__(self, site_info, id, parent=None,alert_content=""):
        dialog_width=800
        dialog_height=600
        QWidget.__init__(self, parent)
        l1 = QLabel()
        l2 = QLabel()
        new_list_widget = QListWidget()
        old_list_widget = QListWidget()

        l1.setAlignment(Qt.AlignVCenter)
        l1.setText("SITE INFORMATION for ID: "+str(id))
        l1.setStyleSheet('font-size:16px')
        l2.setStyleSheet('font-size:14px;border-bottom: medium dashed blue; ')
        new_scroll = QScrollArea(self)
        old_scroll = QScrollArea(self)
        old_list_widget.setStyleSheet('font-size:12px;color:blue;')
        new_list_widget.setStyleSheet('font-size:12px;color:red;')
        if site_info is None:
            l2.setText("This site is not active.")

        else:
            l2.setText("Site Description:    " + site_info["description"] + "\n\n" + "Contact:    " + site_info[
                "contact"] + "\n\n" + "Address:    " + site_info["address"] )

            new_list = []
            if alert_content == "":
                new_list.append("No new suspicious activity at this site")
                self.setStyleSheet('background-color:rgb(0,166,50)')
            else:
                self.setStyleSheet('background-color:rgb(255,165,186); ')
                alert_content = alert_content.split("`")
                alert_content.pop()
                for alert in alert_content:
                    time, activity, location_description = alert.split("~")
                    new_list.append("Activity Detected:  " + activity + "\n" + "Time:  " + time + "\n" + "Location Description:  " + location_description)

            old_list = []
            try:
                with open(str(id) + ".txt", "r") as log_file:
                    alert_content = log_file.read()
            except OSError:
                alert_content = ""
            if alert_content == "":
                old_list.append("No old suspicious activity at this site")
                self.setStyleSheet('background-color:rgb(0,166,50)')
            else:
                self.setStyleSheet('background-color:rgb(255,165,186); ')
                alert_content = alert_content.split("`")
                alert_content.pop()
                for alert in alert_content:
                    time, activity, location_description = alert.split("~")
                    old_list.append("Activity Detected:  " + activity + "\n" + "Time:  " + time + "\n" + "Location Description:  " + location_description)

            new_list_widget.addItems(new_list)
            old_list_widget.addItems(old_list)
            new_scroll.setWidget(new_list_widget)
            old_scroll.setWidget(old_list_widget)

        l1.setAlignment(Qt.AlignCenter)
        l2.setAlignment(Qt.AlignCenter)
        # new_list_widget.setAlignment(Qt.AlignCenter)
        self.setFixedSize(dialog_width,dialog_height)
        vbox = QVBoxLayout()
        vbox.setSpacing(1)
        vbox.setContentsMargins(0,0,1,0)

        vbox.addWidget(l1)
        #vbox.addStretch()
        vbox.addWidget(l2)
        #vbox.addStretch()
        hbox = QHBoxLayout()

        hbox.setSpacing(1)
        hbox.addWidget(old_scroll)
        hbox.addWidget(new_scroll)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.setWindowTitle("Site Information")


def rectify_time_zone(Time):
    Time_obj=datetime.datetime.strptime(Time, '%a, %d %b %Y %H:%M:%S %Z')
    import pytz
    tz=pytz.timezone('Asia/Kolkata')
    Time_obj.replace(tzinfo=tz)
    return datetime.datetime.strftime(Time_obj,'%a, %d %b %Y %H:%M:%S %Z'+time.localtime().tm_zone)
    pass


class Example(QWidget):
    def __init__(self, server_address):
        super().__init__()
        self.server_address=server_address
        self.grid=QGridLayout()
        self.button = [None] * 100
        self.new_alert= [None] * 100
        self.alert_content = [None] * 100
        self.initUI()

    def handle_new_alert(self,message_content):
        id=message_content["SourceID"]
        Time=message_content["Time"]
        # Time=rectify_time_zone(Time)

        activity=message_content["activity_recognized"]
        location_description=message_content["location_description"]

        self.alert_content[id] += (str(Time) + "~" + activity + "~" + location_description +"`")

        self.activate_btn(id)
        self.new_alert[id]=1

    def initUI(self):

        # self.grid.addWidget(QPushButton('c'), 10, 11)

        self.dia=None
        for i in range(0, 5):
            for j in range(1, 11):

                self.button[i*10+j] = QPushButton(str(i * 10 + j),self)
                self.button[i*10+j].setFixedSize(btn_width, btn_height)
                self.button[i*10+j].clicked.connect(self.buttonClicked)
                self.grid.addWidget(self.button[i*10+j], i, j)
                self.normal_state(i * 10 + j)
        self.move(300, 150)
        self.setWindowTitle('City View')
        self.setLayout(self.grid)

        self.show()

    def normal_state(self, id):

        self.new_alert[id] = 0
        if self.alert_content[id] is not None:
            with open(str(id) + ".txt", "a+") as log_file:
                log_file.write(self.alert_content[id])
        self.alert_content[id] = ""
        self.button[id].setStyleSheet("color: rgb(40,55,225);background-color:rgb(23,22,33);font-size:24px")
        self.button[id].setEnabled(True)

    def activate_btn(self, id):
        self.button[id].setStyleSheet("color: rgb(222,223,225);background-color:rgb(255,20,0);font-size:24px")

        # self.button[id].setStyleSheet("background-color: rgb(153,153,102)")
        self.button[id].setEnabled(True)

    def buttonClicked(self):

        id=int(self.sender().text())

        print(self.sender().text() + ' was pressed')
        site_info=(bridge.get_client_info(id,self.server_address))
        self.dia=Dialog(site_info,id,None,self.alert_content[id])
        self.dia.show()
        self.normal_state(id)

# class MainWidget(QWidget):
#     def __init__(self, server_address):
#         super().__init__()
#         self.example_widget = None
#         self.server_address = server_address
#         self.title = 'PyQt5 simple window - pythonspot.com'
#         self.left = 10
#         self.top = 10
#         self.width = width+10
#         self.height = height+10
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)
#
#         scroll = QScrollArea(self)
#         # self.example_widget = Example(self.server_address)
#
#         label = QLabel()
#         label.setAlignment(Qt.AlignVCenter)
#         label.setText("SITE INFORMATION for ID: " + str(id))
#         label.setStyleSheet('font-size:30px')
#
#         scroll.setFixedSize(width, height)
#         scroll.setWidget(label)
#         # scroll.show()
#
#         # self.statusBar().showMessage('Message in statusbar.')
#         self.show()

def rock(server_address):
    app = QApplication(sys.argv)
    ex = Example(server_address)
    return ex, app
