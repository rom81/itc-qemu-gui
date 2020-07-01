from PySide2.QtWidgets import QWidget, QLabel, QShortcut, QRadioButton, QVBoxLayout, QMainWindow, QHBoxLayout, QAction, QFileDialog, QScrollArea
from PySide2.QtGui import QFont, QKeySequence
from PySide2.QtCore import Qt, QTimer
import os, re

class LoggingWindow(QMainWindow):
    
    def __init__(self, qmp):

        QMainWindow.__init__(self)
        self.qmp = qmp

        os.system('rm /tmp/errors.log 2>/dev/null')

        shortcut = QShortcut(QKeySequence('Ctrl+r'), self, activated=self.disp_output)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.disp_output)
        self.timer.start(100)

        self.activated = 0

        self.length = 100
        self.text_digest = ''

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

        self.loglist = QLabel(self)

        self.scroller = QScrollArea()
        self.scroller.setWidget(self.loglist)
        self.scroller.setWidgetResizable(True)

        self.disp_output()

        grid = QHBoxLayout()
        bg = QVBoxLayout()

        for n, button in enumerate(self.buttons):
            if n == self.activated:
                button.setChecked(True)
            button.toggled.connect(lambda state, n=n: self.change_checked(state, n))
            bg.addWidget(button)
       
        grid.addLayout(bg)

        grid.addWidget(self.scroller)

        center = QWidget()
        center.setLayout(grid)
        self.setCentralWidget(center)

        self.show()
    
    def disp_output(self):

        self.shorten_file()

        with open('/tmp/errors.log', 'r') as errors:

            digest = []
            lines = 0

            for line in errors:
                if not re.match(r"\d+@\d+\.\d+:.*", line):
                    digest.append(line)
                    lines += 1

            if not digest:
                digest = ['<font color="grey">Empty...</font>']
            
            self.text_digest = ''.join(digest[-self.length:])

            self.loglist.setText(self.text_digest)
            self.loglist.setFont(QFont('Monospace', 10))
            self.loglist.setTextInteractionFlags(Qt.TextSelectableByMouse)

    def shorten_file(self):

        with open('/tmp/errors.log', 'r+') as tracefile:

            content = ''.join(tracefile.readlines()[-(self.length * 3):])

            tracefile.seek(0)
            tracefile.truncate()

            tracefile.write(content)

    def change_checked(self, state, n):

        if state:
            self.activated = n
 
        self.qmp.hmp_command('log none')

        open('/tmp/errors.log', 'w').close()

        self.qmp.hmp_command('log ' + self.buttons[self.activated].text())

    def closeEvent(self, event):

        self.timer.stop()
        # os.system('rm /tmp/errors.log')
        event.accept()
    
    def export_log(self):

        name = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text files (*.txt)')

        log_file = open(name[0], 'w')
        log_file.write(self.text_digest)
        log_file.close()

    def menu_bar(self):

        bar = self.menuBar()

        file_menu = bar.addMenu('File')
        options = bar.addMenu('Options')

        toggle_refresh = QAction('Auto Refresh', self, checkable=True, triggered=lambda: self.timer.start(100) if toggle_refresh.isChecked() else self.timer.stop())
        toggle_refresh.setChecked(True)
        save_to_file = QAction('Save to File', self, triggered=self.export_log)

        options.addAction(toggle_refresh)
        file_menu.addAction(save_to_file)
