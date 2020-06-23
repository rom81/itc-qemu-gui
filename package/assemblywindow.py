from pygdbmi.gdbcontroller import GdbController
from PySide2.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QPushButton, QVBoxLayout, QTextEdit
from PySide2.QtGui import QFont, QTextCharFormat, QTextCursor, QIcon
from pprint import pprint
from PySide2.QtCore import Qt
import re

class AssemblyWindow(QWidget):
    def __init__(self, qmp):
        super().__init__()
        # self.gdb = None
        self.qmp = qmp

        # self.connected = False

        self.instr = re.compile(r"(^(0x[0-9a-f]+:)((\s+[0-9a-f]{2})+)\s+(.+?)$)+(?m)")
        self.addr = re.compile(r"^\s*-?(0x)?[0-9a-f]+\s*$")
        self.baseAddress = -1
        self.maxAddress = -1

        self.initui()

        self.set_running(self.qmp.running)
        self.qmp.stateChanged.connect(self.set_running)

        self.show()

    def initui(self):
        connect_box = QHBoxLayout()
        main_box = QVBoxLayout()
        button_box = QHBoxLayout()

        # self.host = QLineEdit()
        # connect_box.addWidget(self.host)

        # self.port = QLineEdit()
        # connect_box.addWidget(self.port)

        # self.connect = QPushButton("Connect")
        # self.connect.setCheckable(True)
        # self.connect.clicked.connect(lambda: self.connect_gdb(self.host.text(), self.port.text()))
        # connect_box.addWidget(self.connect)

        # main_box.addLayout(connect_box)

        # self.step = QPushButton("Step")
        # self.step.clicked.connect(self.step_gdb)
        # button_box.addWidget(self.step)

        # self.next = QPushButton("Next")
        # self.next.clicked.connect(self.next_gdb)
        # button_box.addWidget(self.next)

        # main_box.addLayout(button_box)

        self.box = QTextEdit()
        self.box.setReadOnly(True)
        self.box.setLineWrapMode(QTextEdit.NoWrap)
        self.box.setCurrentFont(QFont('Courier New'))
        
        main_box.addWidget(self.box)

        self.setLayout(main_box)
        self.setGeometry(100,100,650,300)

    # def connect_gdb(self, host, port):
    #     self.qmp.command('stop')
    #     if host == '' or port == '':
    #         host = 'localhost'
    #         port = 1234
    #     elif not port.isnumeric():
    #         return

    #     if self.gdb and self.connected:
    #         self.gdb.exit()
    #         self.connected = False
    #     elif not self.connected:
    #         self.gdb = GdbController(gdb_args=['--interpreter=mi'])
    #         resp = self.gdb.write(f'target remote {host}:{port}')
    #         for r in resp:
    #             if r['type'] == 'result' and r['message'] == 'error':
    #                 self.box.clear()
    #                 self.box.setText(f'Could not connect to {host}:{port}.')
    #                 self.connect.setChecked(False)
    #                 self.connected = False
    #                 return

    #         self.display_instrs(self.gdb.write('display/30i $pc'))
    #         self.connected = True

    def set_running(self, value):
        self.running = value
        if not self.running:
            data = None
            while True:
                data = self.qmp.hmp_command('print $eip')
                if 'return' in data:
                        data = data['return']
                        if not (data is dict) and self.addr.match(str(data)):
                            break
            pc = int(data, 0) 
            pc = pc & 0xffffffff
            if pc >= self.baseAddress and pc <= self.maxAddress:
                self.clear_highlight()
                self.highlight(pc)
            else:
                while True:
                    data = self.qmp.hmp_command('x/30i $eip')
                    if 'return' in data:
                        data = data['return']
                        if self.instr.match(str(data)):
                            break
                try:
                    self.display_instrs(data, pc)
                except:
                    self.set_running(False)            
    
    # def step_gdb(self):
    #     self.step.clicked.disconnect(self.step_gdb)
    #     self.qmp.command('stop')
    #     resp = self.gdb.write('si')
    #     self.display_instrs(resp)
    #     self.step.clicked.connect(self.step_gdb)

    # def next_gdb(self):
    #     self.next.clicked.disconnect(self.next_gdb)
    #     self.qmp.command('stop')
    #     resp = self.gdb.write('ni')
    #     self.display_instrs(resp)
    #     self.next.clicked.connect(self.next_gdb)

    def clear_highlight(self):
        fmt = QTextCharFormat()
        fmt.setFont('Courier New')

        cur = self.box.textCursor()
        cur.select(QTextCursor.Document)
        cur.setCharFormat(fmt)
        self.box.setTextCursor(cur)


    def highlight(self, addr):
        fmt = QTextCharFormat()
        fmt.setBackground(Qt.cyan)
        fmt.setFont('Courier New')

        cur = self.box.textCursor()

        text = self.box.toPlainText()
        count = 0
        for line in text.split('\n'):
            if len(line) > 0:
                line_addr = line.split()[0]
                n = (len(line_addr[2:-1]) * 4)
                mask = (2 ** n) - 1
                if int(line_addr[:-1],16) == (addr & mask):
                    break
                count += 1
        block = self.box.document().findBlockByLineNumber(count)
        cur.setPosition(block.position())

        cur.select(QTextCursor.LineUnderCursor)   

        cur.setCharFormat(fmt)

        self.box.setTextCursor(cur)

    def display_instrs(self, resp, addr):
        # asm = []
        # for r in resp:
        #     if r['type'] == 'console':
        #         asm.append(r['payload'])
        # asm = asm[1:31]
        # self.box.clear()
        # self.box.setText(((''.join(asm).replace('\\t', '\t')).replace('\\n', '\n')).replace('=>', '  '))
        
        self.box.clear()
        self.clear_highlight()

        self.box.setText(resp)

        last_line = self.box.toPlainText().split('\n')[-2].split()
        if len(last_line) > 0:
            address = int(last_line[0][:-1], 16)
            self.maxAddress = address
        first_line = self.box.toPlainText().split('\n')[0].split()
        if len(first_line) > 0:
            address = int(first_line[0][:-1], 16)
            self.baseAddress = address
        self.highlight(addr)

        

        