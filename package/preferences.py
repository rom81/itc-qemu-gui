from PySide2.QtWidgets import QMainWindow, QCheckBox, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel
from PySide2.QtGui import QPalette, QColor, QGuiApplication
from PySide2.QtCore import Qt

class Preferences(QMainWindow):

    def __init__(self, app, default, qmp):

        QMainWindow.__init__(self)

        self.app = app

        self.default = default

        self.qmp = qmp

        self.init_ui()
        self.show()
    
    def init_ui(self):

        self.setWindowTitle('Preferences')
        self.setGeometry(100, 100, 400, 200)

        grid = QVBoxLayout()
        grid.setSpacing(15)

        self.darkmode = QCheckBox('Dark Mode', self)

        self.app.setStyle("Fusion")

        if QGuiApplication.palette() != self.default:
            self.darkmode.setChecked(True)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(25, 25, 25)) # 53 53 53
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(53, 53, 53)) # 25 25 25
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)

        self.darkmode.toggled.connect(lambda:self.app.setPalette(palette) if self.darkmode.isChecked() else self.app.setPalette(self.default))

        conn_grid = QHBoxLayout()

        self.connect = QPushButton("Connect")
        self.connect.setCheckable(True)
        self.connect.clicked.connect(self.qmp_start)

        self.host = QLineEdit()
        self.host.returnPressed.connect(lambda: self.connect.click() if not self.connect.isChecked() else None)
        conn_grid.addWidget(self.host)

        self.port = QLineEdit()
        self.port.returnPressed.connect(lambda: self.connect.click() if not self.connect.isChecked() else None)
        conn_grid.addWidget(self.port)

        conn_grid.addWidget(self.connect)

        grid.addLayout(conn_grid)
        grid.addWidget(self.darkmode, 1)

        center = QWidget()
        center.setLayout(grid)
        self.setCentralWidget(center)

        self.show()
            
    def qmp_start(self):
        if self.qmp.isSockValid():
            self.qmp.sock_disconnect()
            return
        else:
            self.qmp.sock_connect(self.host.text(), int(self.port.text()))
        if not self.qmp.isAlive():
            self.qmp.start()
        if not self.t.isAlive():
            self.t.start()
