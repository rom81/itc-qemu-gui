from PySide2.QtWidgets import QWidget, QLabel, QGridLayout, QAction, QShortcut
from PySide2.QtGui import QKeySequence, QFont
from PySide2.QtCore import Qt

class RegisterView(QWidget):

    def __init__(self, qmp):

        QWidget.__init__(self)

        self.qmp = qmp

        self.init_ui()
        self.show()

    def init_ui(self):

        self.setWindowTitle('Register View')
        self.setGeometry(100, 100, 800, 500) # x, y, w, h

        data = self.qmp.hmp_command('info registers')
        self.registers = QLabel(data['return'], self)
        self.registers.setFont(QFont('Monospace', 12))
        self.registers.setTextInteractionFlags(Qt.TextSelectableByMouse)

        shortcut = QShortcut(QKeySequence('Ctrl+r'), self, activated=self.refresh)
    
    def refresh(self):

        data = self.qmp.hmp_command('info registers')
        self.registers.setText(data['return'])