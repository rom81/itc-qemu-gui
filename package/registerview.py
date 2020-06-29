from PySide2.QtWidgets import QMainWindow, QWidget, QLabel, QGridLayout, QShortcut, QLineEdit, QAction, QFileDialog
from PySide2.QtGui import QKeySequence, QFont
from PySide2.QtCore import Qt, QTimer
import re

class RegisterView(QMainWindow):

    def __init__(self, qmp):

        QMainWindow.__init__(self)

        self.qmp = qmp

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.init_ui)
        # self.timer.start(100)

        self.fancy = True
        self.registers = None

        self.init_ui()
        self.menu_bar()
        self.show()

        self.shortcut = QShortcut(QKeySequence('Ctrl+r'), self, activated=self.init_ui) # refresh registers

    def init_ui(self):

        self.setWindowTitle('CPU Registers')

        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        if self.fancy:
            self.fancy_view()
        else: self.ugly_view()
 
        center = QWidget()
        center.setLayout(self.grid)
        self.setCentralWidget(center)
   
    def fancy_view(self):

        data = self.qmp.hmp_command('info registers')
        self.registers = data

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
            self.grid.addWidget(lab, y // columns, (y * 2) % (columns * 2))
            valbox = QLineEdit(self)
            valbox.setText(d[reg])
            valbox.setReadOnly(True)
            valbox.setFont(QFont('Monospace', 12))
            self.grid.addWidget(valbox, y // columns, ((y * 2) % (columns * 2)) + 1)
    
    def ugly_view(self):

        self.grid.setSpacing(15)

        data = self.qmp.hmp_command('info registers')
        self.registers = data

        lab = QLabel(data['return'], self)
        lab.setFont(QFont('Monospace', 12))

        self.grid.addWidget(lab, 0, 0)
    
    def switch_view(self):

        self.fancy = not self.fancy

        self.init_ui()
    
    def export_registers(self):

        name = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text files (*.txt)')

        register_file = open(name[0], 'w')
        register_file.write(self.registers['return'])
        register_file.close()
        

    def menu_bar(self):

        bar = self.menuBar()

        file_menu = bar.addMenu('File')
        options = bar.addMenu('Options')

        toggle_refresh = QAction('Auto Refresh', self, checkable=True, triggered=lambda: self.timer.start(100) if toggle_refresh.isChecked() else self.timer.stop())
        toggle_ugly = QAction('Text View', self, checkable=True, triggered=lambda:self.switch_view())
        save_to_file = QAction('Save to File', self, triggered=self.export_registers)

        options.addAction(toggle_refresh)
        options.addAction(toggle_ugly)

        file_menu.addAction(save_to_file)
