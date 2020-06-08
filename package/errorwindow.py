from PySide2.QtWidgets import QWidget, QLabel, QShortcut
from PySide2.QtGui import QFont, QKeySequence
from PySide2.QtCore import Qt
import os

class ErrorWindow(QWidget):
    
    def __init__(self, qmp):

        QWidget.__init__(self)
        self.qmp = qmp

        self.qmp.hmp_command('logfile /tmp/errors.log')
        self.qmp.hmp_command('log guest_errors')

        self.init_ui()
    
    def init_ui(self):

        self.setWindowTitle('Error Log')
        self.setGeometry(100, 100, 800, 600)

        with open('/tmp/errors.log', 'r') as errors:

            digest = ''.join(errors.readlines()[-30:])

            if not digest:
                digest = 'No errors to show.'

            errorlist = QLabel(digest, self)
            errorlist.setFont(QFont('Monospace', 12))
            errorlist.setTextInteractionFlags(Qt.TextSelectableByMouse)

        shortcut = QShortcut(QKeySequence('Ctrl+r'), self, activated=self.init_ui)

        self.show()
    
    def closeEvent(self, event):

        os.system('rm /tmp/errors.log')
        event.accept()