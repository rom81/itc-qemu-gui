from PySide2.QtWidgets import QMainWindow, QAction, QGridLayout, QPushButton, QWidget, QErrorMessage, QMessageBox, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit
from PySide2.QtGui import QIcon, QFont, QGuiApplication, QPixmap
from PySide2.QtCore import QSize, Slot, Qt

from package.memdumpwindow import MemDumpWindow
from package.registerview import RegisterView
from package.errorwindow import ErrorWindow
from package.preferences import Preferences
from package.memtree import MemTree
from package.qmpwrapper import QMP

from datetime import datetime, timezone
import threading
import time

class MainWindow(QMainWindow):

    def __init__(self, app):

        self.app = app
 
        self.qmp = QMP('localhost', 55555)
        self.qmp.start()

        self.qmp.stateChanged.connect(self.handle_pause_button)
        self.qmp.connectionChange.connect(self.handle_connect_button)

        self.paused = False

        super().__init__()
        self.init_ui()

        self.qmp.timeUpdate.connect(self.update_time)
        self.t = TimeThread(self.qmp)
        self.t.start()

        self.window = []

        self.default_theme = QGuiApplication.palette()

    def init_ui(self):

        # Window Setup
        self.setWindowTitle("QEMU Control")
        self.setGeometry(100, 100, 255, 200) # x, y, w, h 
        self.setFixedSize(self.size())

        # App Icon
        icon = QIcon('package/icons/qemu-official.png')
        self.setWindowIcon(icon)

        # User Interface
        self.menu_bar()
        self.grid_layout()

        self.show()

    def menu_bar(self):

        bar = self.menuBar()

        # Menu Bar Actions
        file_ = bar.addMenu("File")
        edit = bar.addMenu("Edit")
        run = bar.addMenu("Run")
        tools = bar.addMenu("Tools")
        help_ = bar.addMenu("Help")

        # File Menu Options
        open_ = QAction("Open Image", self)
        file_.addAction(open_)

        exit_ = QAction("Exit", self)
        exit_.triggered.connect(self.close)
        exit_.setShortcut('Ctrl+W')
        file_.addAction(exit_)

        # Edit Menu Options
        prefs = QAction("Preferences", self, triggered=lambda:self.open_new_window(Preferences(self.app, self.default_theme, self.qmp)))
        edit.addAction(prefs)

        # Run Menu Options
        pause = QAction("Pause", self, triggered=lambda:self.qmp.command('stop'))
        run.addAction(pause)

        play = QAction("Play", self, triggered=lambda:self.qmp.command('cont'))
        run.addAction(play)

        # Debug Menu Options
        hexdmp = QAction("Memory Dump", self, triggered=(lambda: self.open_new_window(MemDumpWindow(self.qmp)) if self.qmp.isSockValid() else None))
        tools.addAction(hexdmp)

        asm = QAction("Assembly View", self)
        tools.addAction(asm)

        registers = QAction("CPU Register View", self, triggered=(lambda: self.open_new_window(RegisterView(self.qmp)) if self.qmp.isSockValid() else None))
        tools.addAction(registers)

        errors = QAction("Error Log", self, triggered=lambda:self.open_new_window(ErrorWindow(self.qmp)))
        tools.addAction(errors)

        tree = QAction("Memory Tree", self, triggered=(lambda: self.open_new_window(MemTree(self.qmp, self)) if self.qmp.isSockValid() else None))
        tools.addAction(tree)

        # Help Menu Options 
        usage = QAction("Usage Guide", self)
        help_.addAction(usage)

    def grid_layout(self):

        grid = QVBoxLayout()
        grid.setSpacing(15)


        # Check if QMP is running initially
        if self.qmp.running == 'paused':
            self.paused = True
            # self.pause_button.setChecked(self.paused)

        self.pause_button = QPushButton(self)
        self.running_state = QLabel(self)

        def cont_sim():
            # self.pause_button.setIcon(QIcon('package/icons/icons8-pause-90.png'))
            self.pause_button.setText('■')
            self.running_state.setText('Current State: <font color="green">Running</font>')
            self.qmp.command('cont')

        def stop_sim():
            # self.pause_button.setIcon(QIcon('package/icons/icon8-play-90.png'))
            self.pause_button.setText('▶')
            self.running_state.setText('Current State: <font color="red">Paused</font>')
            self.qmp.command('stop')

        subgrid = QHBoxLayout()

        self.pause_button.clicked.connect(lambda: stop_sim() if not self.paused else cont_sim())
        self.pause_button.setFixedSize(QSize(50, 50))
        subgrid.addWidget(self.pause_button, 0)
        # self.pause_button.setCheckable(True)


        meatball = QLabel(self)
        logo = QPixmap('package/icons/nasa.png')
        logo = logo.scaled(75, 75, Qt.KeepAspectRatio)
        meatball.setPixmap(logo)
        subgrid.addWidget(meatball, 1)

        grid.addLayout(subgrid, 0)

        self.time = QLabel('Time: 00:00:00')
        self.time.setFont(QFont('Courier New'))
        grid.addWidget(self.time, 1)

        grid.addWidget(self.running_state, 2)

        banner = QLabel('QEMU Version ' + str(self.qmp.banner['QMP']['version']['package']))
        # print(self.qmp.banner)
        grid.addWidget(banner, 3)

        center = QWidget()
        center.setLayout(grid)
        self.setCentralWidget(center)

    def throwError(self):
        msgBox = QMessageBox(self)
        msgBox.setText('Lost Connection to QMP!')
        msgBox.show()

    @Slot(bool)
    def handle_pause_button(self, value):
        # Catches signals from QMPWrapper
        if value:
            self.paused = False
            # self.pause_button.setIcon(QIcon('package/icons/icons8-pause-90.png'))
            self.pause_button.setText('■')
            self.running_state.setText('Current State: <font color="green">Running</font>')
        elif not value:
            self.paused = True 
            # self.pause_button.setIcon(QIcon('package/icons/icons8-play-90.png'))
            self.pause_button.setText('▶')
            self.running_state.setText('Current State: <font color="red">Paused</font>')
        else:
            self.running_state.setText('Current State: Broken')
            self.throwError()

    def handle_connect_button(self, value):
        self.connect.setChecked(value)
        self.host.setReadOnly(value)
        self.port.setReadOnly(value)


    def open_new_window(self, new_window):
        if self.qmp.isSockValid():
            self.window.append(new_window)

    def update_time(self, time):
        date = datetime.fromtimestamp(time / 1000000000, timezone.utc)
        self.time.setText(f'Time: {date.day - 1:02}:{date.hour:02}:{date.minute:02}:{date.second:02}') # -1 for day because it starts from 1

class TimeThread(threading.Thread):

    def __init__(self, qmp):
        super().__init__()
        self.daemon = True
        self.qmp = qmp

    def run(self):
        while True:
            time.sleep(.5)
            args = {'clock': 'virtual'}
            self.qmp.command('itc-sim-time', args=args)
