from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QGridLayout, QPushButton 
from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QIcon 

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        self.init_ui()

    def init_ui(self):

        # Window Setup
        self.setWindowTitle("QEMU Control")
        self.setGeometry(100, 100, 400, 300) # x, y, w, h 

        # App Icon
        icon = QIcon('package/icons/nasa.png')
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
        exit_.triggered.connect(QApplication.instance().quit)
        file_.addAction(exit_)

        # Edit Menu Options
        prefs = QAction("Preferences", self)
        edit.addAction(prefs)

        # Run Menu Options
        pause = QAction("Pause", self)
        run.addAction(pause)

        play = QAction("Play", self)
        run.addAction(play)

        step = QAction("Step", self)
        run.addAction(step)

        # Debug Menu Options
        hexdmp = QAction("Memory Dump", self)
        tools.addAction(hexdmp)

        asm = QAction("Assembly View", self)
        tools.addAction(asm)

        registers = QAction("Register View", self)
        tools.addAction(registers)

        stack = QAction("Stack View", self)
        tools.addAction(stack)

        errors = QAction("Error Log", self)
        tools.addAction(errors)

        # Help Menu Options 
        usage = QAction("Usage Guide", self)
        help_.addAction(usage)

    def grid_layout(self):
        
        grid = QGridLayout()
        grid.setSpacing(15)

        pause_button = QPushButton("Pause", self)
        pause_button.setIcon(QIcon('package/icons/icons8-pause-90.png'))
        grid.addWidget(pause_button, 0, 0) # row, column

        play_button = QPushButton("Play", self)
        play_button.setIcon(QIcon('package/icons/icons8-play-90.png'))
        grid.addWidget(play_button, 0, 1) # row, column

        center = QWidget()
        center.setLayout(grid)
        self.setCentralWidget(center)


