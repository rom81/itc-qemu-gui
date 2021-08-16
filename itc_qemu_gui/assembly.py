from pygdbmi.gdbcontroller import GdbController
from PySide2.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QPushButton, QVBoxLayout, QTextEdit
from PySide2.QtGui import QFont
from pprint import pprint
class AssemblyWindow(QWidget):
    def __init__(self, qmp, parent=None):
        super().__init__(parent)
        self.gdb = None
        self.qmp = qmp

        self.running = qmp.running
        self.qmp.stateChanged.connect(self.set_running)

        self.connected = False

        self.initui()

        self.show()

    def initui(self):
        connect_box = QHBoxLayout()
        main_box = QVBoxLayout()
        button_box = QHBoxLayout()

        self.host = QLineEdit()
        self.host.setPlaceholderText("GDB Hostname")
        connect_box.addWidget(self.host)


        self.port = QLineEdit()
        self.port.setPlaceholderText("GDB Port")
        connect_box.addWidget(self.port)

        self.connect = QPushButton("Connect")
        self.connect.setCheckable(True)
        self.connect.clicked.connect(lambda: self.connect_gdb(self.host.text(), self.port.text()))
        connect_box.addWidget(self.connect)

        main_box.addLayout(connect_box)

        self.step = QPushButton("Step")
        self.step.clicked.connect(self.step_gdb)
        button_box.addWidget(self.step)

        self.next = QPushButton("Next")
        self.next.clicked.connect(self.next_gdb)
        button_box.addWidget(self.next)

        main_box.addLayout(button_box)

        self.box = QTextEdit()
        self.box.setReadOnly(True)
        self.box.setLineWrapMode(QTextEdit.NoWrap)
        self.box.setCurrentFont(QFont('Courier New'))
        self.box.setGeometry(100,100,250,500)
        main_box.addWidget(self.box)

        self.setLayout(main_box)

    def connect_gdb(self, host, port):
        self.qmp.command('stop')
        if host == '' or port == '':
            host = 'localhost'
            port = 1234
            self.host.setText('localhost')
            self.port.setText('1234')
        elif not port.isnumeric():
            return

        if self.gdb and self.connected:
            self.gdb.exit()
            self.connected = False
        elif not self.connected:
            self.gdb = GdbController(gdb_args=['--interpreter=mi3'])
            other_resp = self.gdb.write(f'set may-interrupt off')
            print("other_resp: ", other_resp)
            resp = self.gdb.write(f'target remote {host}:{port}')
            print(resp)
            for r in resp:
                if r['type'] == 'result' and r['message'] == 'error':
                    self.box.clear()
                    self.box.setText(f'Could not connect to {host}:{port}.')
                    self.connect.setChecked(False)
                    self.connected = False
                    return

            self.display_instrs(self.gdb.write('display/30i $pc'))
            self.connected = True

    def set_running(self, value):
        self.running = value            
    
    def step_gdb(self):
        print("start of step_gdb: self.qmp.running = ", self.qmp.running)

        # Execute step if gdb is connected
        if self.gdb:
            # self.step.clicked.disconnect(self.step_gdb)
            # print("mid 1 of step_gdb: self.qmp.running = ", self.qmp.running)
            
            # self.qmp.command('stop')
            print("mid 2 of step_gdb: self.qmp.running = ", self.qmp.running)

            resp = self.gdb.write('si')
            # print("si result: ", resp, "\n\n")

            print("mid 3 of step_gdb: self.qmp.running = ", self.qmp.running)

            self.display_instrs(resp)
            print("mid 4 of step_gdb: self.qmp.running = ", self.qmp.running)

            # self.step.clicked.connect(self.step_gdb)
        
        print("end of step_gdb: self.qmp.running = ", self.qmp.running)


    def next_gdb(self):
        print("start of next_gdb: self.qmp.running = ", self.qmp.running)

        # Execute step if gdb is connected
        if self.gdb:
            self.next.clicked.disconnect(self.next_gdb)
            self.qmp.command('stop')
            resp = self.gdb.write('ni')
            # print("ni result: ", resp, "\n\n")
            self.display_instrs(resp)
            self.next.clicked.connect(self.next_gdb)

        print("end of next_gdb: self.qmp.running = ", self.qmp.running)
        

    def display_instrs(self, resp):
        asm = []
        for r in resp:
            if r['type'] == 'console':
                asm.append(r['payload'])
        asm = asm[1:31]
        # print(asm)
        self.box.clear()
        self.box.setText((''.join(asm).replace('\\t', '\t')).replace('\\n', '\n'))