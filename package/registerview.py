from PySide2.QtWidgets import QMainWindow, QWidget, QLabel, QGridLayout, QAction, QShortcut, QListWidget, QVBoxLayout, QGroupBox, QPushButton, QLineEdit
from PySide2.QtGui import QKeySequence, QFont
from PySide2.QtCore import Qt
import re

class RegisterView(QMainWindow):

    def __init__(self, qmp):

        QMainWindow.__init__(self)

        self.qmp = qmp

        self.init_ui()
        self.show()

    def init_ui(self):

        self.setWindowTitle('Register View')
        # self.setGeometry(100, 100, 800, 500) # x, y, w, h

        grid = QGridLayout()
        grid.setSpacing(5)

        data = self.qmp.hmp_command('info registers')

        d = {}
        for e in filter(None, re.split('=| |\r\n', data['return'])): # string to dictionary
            # if not '[' in e:
            if not re.match('[0-9a-f]+', e) and '[' not in e:
                temp = e
                d[e] = ''
                # d[e] = []
            else:
                d[temp] += (e + ' ')
    
        columns = 3
        rows = (max([len(d[i]) for i in d]) + 1) * columns

        for y, reg in enumerate(d):
            lab = QLabel(reg, self)
            lab.setFont(QFont('Monospace', 12))
            grid.addWidget(lab, y // columns, (y * 2) % (columns * 2)) # x, y
            # grid.addWidget(lab, y // columns, (y * 5) % 15) # x, y
            # for x, val in enumerate(d[reg]):
                # valbox = QLineEdit(self)
                # valbox.setText(val)
                # valbox.setFont(QFont('Monospace', 12))
                # grid.addWidget(valbox, y // columns, ((y * 5) % 15) + x + 1)
            valbox = QLineEdit(self)
            valbox.setText(d[reg])
            valbox.setReadOnly(True)
            valbox.setFont(QFont('Monospace', 12))
            grid.addWidget(valbox, y // columns, ((y * 2) % (columns * 2)) + 1)


        center = QWidget()
        center.setLayout(grid)
        self.setCentralWidget(center)


    #     self.registers = QLabel(data['return'], self)
    #     self.registers.setFont(QFont('Monospace', 12))
    #     self.registers.setTextInteractionFlags(Qt.TextSelectableByMouse)



        shortcut = QShortcut(QKeySequence('Ctrl+r'), self, activated=self.init_ui) # refresh registers