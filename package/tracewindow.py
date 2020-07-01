from PySide2.QtWidgets import QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QLineEdit, QPushButton, QCompleter, QAction, QCheckBox, QSplitter, QScrollArea, QFileDialog
from PySide2.QtGui import Qt, QFont 
from PySide2.QtCore import QTimer, QSize

import os, re

class TraceWindow(QMainWindow):

    def __init__(self, qmp):

        QMainWindow.__init__(self)

        self.qmp = qmp

        os.system('rm /tmp/errors.log 2>/dev/null')

        self.trace_events = self.qmp.hmp_command('info trace-events')
        self.qmp.hmp_command('logfile /tmp/errors.log')

        self.trace_events = sorted(self.trace_events['return'].split('\r\n'))[1:]
        self.activated = []

        self.length = 100

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.disp_output)
        self.timer.start(100)

        self.init_ui()
    
    def init_ui(self):

        self.setWindowTitle('Trace Event Window')
        self.setGeometry(100, 100, 800, 600)

        bar = self.menuBar()

        file_ = bar.addMenu('File')
        export_log = QAction('Save to File', self, triggered=lambda: self.save_log())

        options = bar.addMenu('Options')
        auto_refresh = QAction('Auto Refresh', self, checkable=True, triggered=lambda: self.timer.start(100) if auto_refresh.isChecked() else self.timer.stop())
        auto_refresh.setChecked(True)

        options.addAction(auto_refresh)
        file_.addAction(export_log)

        vgrid = QVBoxLayout()
        grid = QHBoxLayout()

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(['Name'])

        self.top = []
        self.lst = []

        for n, event in enumerate(self.trace_events):
            word = event.split('_')[0]
            if word not in self.top:
                self.top.append(word)
                item = QTreeWidgetItem(self.tree)
                self.lst.append(item)
                item.setText(0, word)
            subitem = QTreeWidgetItem(item)
            subitem.setText(0, '    ' + event.split(' : ')[0])
            # subitem.setCheckState(0, Qt.Unchecked)
            cbox = QCheckBox()
            cbox.stateChanged.connect(lambda state, text=subitem.text(0): self.handle_checked(state, text))
            self.tree.setItemWidget(subitem, 0, cbox)
        
        # self.tree.setColumnWidth(0, 25)

        self.tracelist = QLabel()
        self.disp_output()

        self.traceview = QScrollArea()
        self.traceview.setWidget(self.tracelist)
        self.traceview.setWidgetResizable(True)

        search = QHBoxLayout()
        
        self.search_bar = QLineEdit(self)

        self.completer = QCompleter(self.top, self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)

        self.search_bar.setCompleter(self.completer)

        search_button = QPushButton('Search')
        search_button.clicked.connect(lambda: self.tree.setCurrentItem(self.lst[self.top.index(self.search_bar.text())])) 

        expand = QPushButton('▼')
        expand.setFixedSize(QSize(25, 25))
        expand.clicked.connect(lambda: self.tree.expandAll())

        collapse = QPushButton('▲')
        collapse.setFixedSize(QSize(25, 25))
        collapse.clicked.connect(lambda: self.tree.collapseAll())

        self.search_bar.returnPressed.connect(lambda: search_button.click())
    
        search.addWidget(self.search_bar)
        search.addWidget(search_button)
        search.addWidget(expand)
        search.addWidget(collapse)

        self.digest = QLabel()

        vgrid.addLayout(search)
        vgrid.addWidget(self.tree)

        vgridwid = QWidget()
        vgridwid.setLayout(vgrid)

        split = QSplitter(Qt.Horizontal)

        split.addWidget(vgridwid)
        split.addWidget(self.traceview)

        split.setStretchFactor(1, 1)

        # grid.addLayout(vgrid)
        grid.addWidget(split)
        # grid.addWidget(self.tracelist)

        self.disp_output()

        center = QWidget()
        center.setLayout(grid)
        self.setCentralWidget(center)
        self.show()

    def disp_output(self):

        self.shorten_file()

        with open('/tmp/errors.log', 'r') as errors:

            self.digest = []
            lines = 0

            for line in errors:
                if re.match(r"\d+@\d+\.\d+:.*", line):
                    self.digest.append(line)
                    lines += 1

            if not self.digest:
                self.digest = ['<font color="grey">Empty...</font>']
            
            self.digest = ''.join(self.digest[-self.length:])

            self.tracelist.setText(self.digest)
            self.tracelist.setFont(QFont('Monospace', 10))
            self.tracelist.setTextInteractionFlags(Qt.TextSelectableByMouse)
    
    def shorten_file(self):

        with open('/tmp/errors.log', 'r+') as tracefile:

            content = ''.join(tracefile.readlines()[-(self.length * 3):])

            tracefile.seek(0)
            tracefile.truncate()

            tracefile.write(content)

    def save_log(self):

        name = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text files (*.txt)')

        log_file = open(name[0], 'w')
        log_file.write(self.digest)
        log_file.close()
    
    def handle_checked(self, state, text):

        if state:
            self.qmp.hmp_command('trace-event %s on' % text.strip())
            self.activated.append(text)
        else:
            self.qmp.hmp_command('trace-event %s off' % text.strip())
            self.activated.remove(text)
    
    def closeEvent(self, event):

        self.timer.stop()

        for e in self.activated:
            self.qmp.hmp_command('trace-event %s off' % e.strip())
        
        os.system('rm /tmp/errors.log')

        event.accept()






