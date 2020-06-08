from PySide2.QtWidgets import QMainWindow, QWidget, QLabel, QGridLayout, QShortcut, QLineEdit
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

        grid = QGridLayout()
        grid.setSpacing(5)

        data = self.qmp.hmp_command('info registers')

        d = {}
        for e in filter(None, re.split('=| |\r\n', data['return'])): # string to dictionary
            if not re.match('[0-9a-f]+', e) and '[' not in e:
                temp = e
                d[e] = ''
            else:
                d[temp] += (e + ' ')
    
        columns = 3

        for y, reg in enumerate(d):

            lab = QLabel(reg, self)
            lab.setFont(QFont('Monospace', 12))
            grid.addWidget(lab, y // columns, (y * 2) % (columns * 2))
            valbox = QLineEdit(self)
            valbox.setText(d[reg])
            valbox.setReadOnly(True)
            valbox.setFont(QFont('Monospace', 12))
            grid.addWidget(valbox, y // columns, ((y * 2) % (columns * 2)) + 1)

        shortcut = QShortcut(QKeySequence('Ctrl+r'), self, activated=self.init_ui) # refresh registers

        center = QWidget()
        center.setLayout(grid)
        self.setCentralWidget(center)
