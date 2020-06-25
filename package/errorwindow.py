from PySide2.QtWidgets import QWidget, QLabel, QShortcut, QRadioButton, QVBoxLayout, QMainWindow, QHBoxLayout, QAction, QFileDialog
from PySide2.QtGui import QFont, QKeySequence
from PySide2.QtCore import Qt, QTimer
import os

class ErrorWindow(QMainWindow):
    
    def __init__(self, qmp):

        QMainWindow.__init__(self)
        self.qmp = qmp

        shortcut = QShortcut(QKeySequence('Ctrl+r'), self, activated=self.disp_output)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.disp_output)
        # self.timer.start(100)

        self.activated = 0

        open('/tmp/errors.log', 'w').close()

        self.qmp.hmp_command('logfile /tmp/errors.log')
        self.qmp.hmp_command('log guest_error')

        self.setWindowTitle('Error Log')
        self.setGeometry(100, 100, 600, 400)

        self.menu_bar()
        self.init_ui()
    
    def init_ui(self):

        guesterrors = QRadioButton('guest_errors')
        outasm = QRadioButton('out_asm')
        inasm = QRadioButton('in_asm')
        op = QRadioButton('op')
        opout = QRadioButton('op_out')
        opind = QRadioButton('op_ind')
        int = QRadioButton('int')
        exec = QRadioButton('exec')
        cpu = QRadioButton('cpu')
        fpu = QRadioButton('fpu')
        mmu = QRadioButton('mmu')
        pcall = QRadioButton('pcall')
        cpureset = QRadioButton('cpu_reset')
        unimp = QRadioButton('unimp')
        nonexistent = QRadioButton('non-existent')
        page = QRadioButton('page')
        nochain = QRadioButton('nochain')
    
        self.buttons = [guesterrors, outasm, inasm, op, opout, opind, int, exec, cpu, fpu, mmu, pcall, cpureset, unimp, nonexistent, page, nochain]

        self.errorlist = QLabel(self)

        self.disp_output()

        grid = QHBoxLayout()
        bg = QVBoxLayout()

        for n, button in enumerate(self.buttons):
            if n == self.activated:
                button.setChecked(True)
            button.toggled.connect(lambda state, n=n: self.change_checked(state, n))
            bg.addWidget(button)
       
        grid.addLayout(bg)

        grid.addWidget(self.errorlist)

        center = QWidget()
        center.setLayout(grid)
        self.setCentralWidget(center)

        self.show()
    
    def disp_output(self):

        with open('/tmp/errors.log', 'r') as errors:

            digest = ''.join(errors.readlines()[-30:])

            if not digest:
                digest = '<font color="grey">Empty...</font>'

            self.errorlist.setText(digest)
            self.errorlist.setFont(QFont('Monospace', 10))
            self.errorlist.setTextInteractionFlags(Qt.TextSelectableByMouse)

    def change_checked(self, state, n):

        if state:
            self.activated = n
 
        self.qmp.hmp_command('log none')

        open('/tmp/errors.log', 'w').close()

        self.qmp.hmp_command('log ' + self.buttons[self.activated].text())

    def closeEvent(self, event):

        self.timer.stop()
        os.system('rm /tmp/errors.log')
        event.accept()
    
    def export_log(self):

        name = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text files (*.txt)')

        log_file = open(name[0], 'w')
        log_file.write(open('/tmp/errors.log', 'r').read())
        log_file.close()

    def menu_bar(self):

        bar = self.menuBar()

        file_menu = bar.addMenu('File')
        options = bar.addMenu('Options')

        toggle_refresh = QAction('Auto Refresh', self, checkable=True, triggered=lambda: self.timer.start(100) if toggle_refresh.isChecked() else self.timer.stop())
        save_to_file = QAction('Save to File', self, triggered=self.export_log)

        options.addAction(toggle_refresh)
        file_menu.addAction(save_to_file)
