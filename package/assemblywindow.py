from pygdbmi.gdbcontroller import GdbController
from PySide2.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QPushButton, QVBoxLayout, QTextEdit
from PySide2.QtGui import QFont
from pprint import pprint
class AssemblyWindow(QWidget):
    def __init__(self, qmp):
        super().__init__()
        self.gdb = None
        self.qmp = qmp

        self.running = qmp.running
        self.qmp.stateChanged.connect(self.set_running)


        self.initui()

        self.show()

    def initui(self):
        connect_box = QHBoxLayout()
        main_box = QVBoxLayout()
        button_box = QHBoxLayout()

        self.host = QLineEdit()
        connect_box.addWidget(self.host)

        self.port = QLineEdit()
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
        if host == '' or port == '':
            host = 'localhost'
            port = 1234
        elif not port.isnumeric():
            return

        if self.gdb:
            self.gdb.exit()
        else:
            self.gdb = GdbController(gdb_args=['--interpreter=mi'])
        self.gdb.write(f'target remote {host}:{port}')
        self.display_instrs(self.gdb.write('display/30i $pc'))

    def set_running(self, value):
        self.running = value            
    
    def step_gdb(self):
        resp = self.gdb.write('si')
        self.display_instrs(resp)

    def next_gdb(self):
        resp = self.gdb.write('ni')
        self.display_instrs(resp)

    def display_instrs(self, resp):
        asm = []
        for r in resp:
            if r['type'] == 'console':
                asm.append(r['payload'])
        asm = asm[1:31]
        self.box.clear()
        self.box.setText((''.join(asm).replace('\\t', '\t')).replace('\\n', '\n'))
        
        