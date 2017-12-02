import sys

import gui

ex=None
app=None
def gui_init(server_address):
    global ex,app
    print('Initializing GUI')
    ex, app = gui.rock(server_address)
    sys.exit(app.exec_())
#
# server_address='localhost:5000'
# server_address='http://' + server_address + '/'
# control_gui(server_address)


def new_alert(message_content):
   ex.handle_new_alert(message_content)

gui_init("127.0.0.1")