from package.qmpwrapper import QMP
from PySide2.QtCore import QSemaphore, Signal, QObject, QThread, Qt
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QSpinBox, QLabel

import time
from threading import Thread

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy

class TimeMultiplier(QWidget):
    updateRate = Signal(int)
    def __init__(self, qmp, event):
        super().__init__()
        self.running = qmp.running        

        self.totalRunning = 0
        self.total = 0

        self.qmp = qmp
        self.qmp.stateChanged.connect(self.handle_running)

        self.kill_event = event

        self.data = 0

        self.lim = 10
        self.window = 10
        self.win_counter = self.window

        self.alpha = .5 ** (1/(15 * 10 - 1))

        self.initui()

    def initui(self):
        lay = QVBoxLayout(self)
        toolbar = QHBoxLayout()

        self.rate = QSpinBox()
        self.rate.setValue(10)
        toolbar.addWidget(QLabel('Sampling Rate (Hz):'))
        toolbar.addWidget(self.rate)

        self.window_input = QSpinBox()
        self.window_input.setValue(self.window)
        toolbar.addWidget(QLabel('Window:'))
        toolbar.addWidget(self.window_input)

        self.limit = QSpinBox()
        self.limit.setValue(self.lim)
        toolbar.addWidget(QLabel('Limit (s):'))
        toolbar.addWidget(self.limit)

        self.refresh_button = QPushButton('Refresh')
        self.refresh_button.clicked.connect(self.handle_refresh)
        toolbar.addWidget(self.refresh_button)

        lay.addLayout(toolbar)

        fig = Figure(figsize=(7, 5), dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.canvas = FigureCanvas(fig)

        lay.addWidget(self.canvas)

        self.ax = fig.add_subplot()
        self.line, *_ = self.ax.plot([])
        
        self.ax.set_ylim(0, 1.1)
        self.ax.set_xlim(0, 1)

        self.ax.set_yticks(numpy.arange(0, 1.2, .1))

        self.ax.set_xlabel('Simulation Time (s)')
        self.ax.set_ylabel('Multiplier')
        self.fill = self.ax.fill_between(self.line.get_xdata(), self.line.get_ydata(), color='blue', alpha=.3, interpolate=True)

        self.canvas.draw()

        self.setLayout(lay)

    def handle_refresh(self, val):
        to_emit = self.rate.value() if self.rate.value() > 0 else 10
        self.alpha = .5 ** (1/(15 * to_emit - 1))
        self.updateRate.emit(to_emit)

        self.lim = self.limit.value() if self.limit.value() > 0 else 10
        self.window = self.window_input.value() if self.window_input.value() > 0 else 10
        


    def reset(self):
        self.totalRunning = 0
        self.total = 0
        
    def start(self):
        self.t = SamplingThread()
        self.kill_event.connect(self.t.end_thread)
        self.t.sample.connect(self.handle_sample)
        self.updateRate.connect(self.t.update) 

    def handle_running(self, value):
        if not self.t.isRunning(): 
            if value:
                self.data = 1
            else:
                self.data = 0
            self.line.set_xdata([])
            self.line.set_ydata([])
            self.ax.set_xlim(0, self.lim)
            self.canvas.draw()

            self.start_time = time.time()
    
            
            self.t.start()
        else:
            self.handle_sample()
        self.running = value

    def handle_sample(self):
        if self.win_counter <= 0:
            self.win_counter = self.window
            self.reset() 
        self.win_counter -= 1
        now = time.time()
        if self.running:
            self.totalRunning += 1
        self.total += 1
        diff = self.totalRunning / self.total
        self.data = (1 - self.alpha) * diff + self.alpha * self.data
        self.line.set_xdata(numpy.append(self.line.get_xdata(), now - self.start_time))
        self.line.set_ydata(numpy.append(self.line.get_ydata(), self.data))
        self.ax.set_xlim(now - self.start_time - self.lim, now - self.start_time)
        
        #self.ax.collections.remove(self.fill)
        #self.fill = self.ax.fill_between(self.line.get_xdata(), self.line.get_ydata(), color='blue', alpha=.2, interpolate=True)
        self.canvas.draw()
        


class SamplingThread(QThread):
    sample = Signal()
    def __init__(self):
        super().__init__()
        self.sem = QSemaphore()
        self.rate = 10
        
    def run(self):
        while True:
            if self.sem.tryAcquire(1, (1.0/self.rate) * 1000):
                break
            self.sample.emit()

    def end_thread(self):
        self.sem.release()

    def update(self, rate):
        self.rate = rate