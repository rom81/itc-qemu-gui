from package.qmpwrapper import QMP
from PySide2.QtCore import QSemaphore, Signal, QObject, QThread, Qt
from PySide2.QtGui import QPainter, QFont
from PySide2.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QSpinBox, QLabel

import time
from threading import Thread
from datetime import datetime, timezone
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
        self.qmp.timeMetric.connect(self.handle_sample)

        self.kill_event = event

        self.data = 0

        self.lim = 10
        self.window = 10
        self.rate_value = 10


        self.sem = QSemaphore(1)

        self.all_min_val = -1
        self.all_max_val = -1

        self.plot_min_val = -1
        self.plot_max_val = -1

        self.initui()

    def initui(self):
        lay = QVBoxLayout(self)
        toolbar = QHBoxLayout()
        main_box = QHBoxLayout()
        stats_box = QVBoxLayout()

        self.rate = QSpinBox()
        self.rate.setValue(self.rate_value)
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

        main_box.addWidget(self.canvas)

        self.ax = fig.add_subplot()
        self.line, *_ = self.ax.plot([])
        
        self.ax.set_ylim(0, 1.1)
        self.ax.set_xlim(0, 1)

        self.ax.set_yticks(numpy.arange(0, 1.2, .1))

        self.ax.set_xlabel('Simulation Time (s)')
        self.ax.set_ylabel('Multiplier')
        self.fill = self.ax.fill_between(self.line.get_xdata(), self.line.get_ydata(), color='blue', alpha=.3, interpolate=True)

        self.canvas.draw()

        all_data = QLabel("All Data")
        bold_font = QFont()
        bold_font.setBold(True)
        all_data.setFont(bold_font)
        stats_box.addWidget(all_data)

        self.all_min = QLabel('Min:')
        stats_box.addWidget(self.all_min)

        self.all_max = QLabel('Max:')
        stats_box.addWidget(self.all_max)

        plot_data = QLabel("On Screen Data")
        plot_data.setFont(bold_font)
        stats_box.addWidget(plot_data)

        self.plot_min = QLabel('Min:')
        stats_box.addWidget(self.plot_min)

        self.plot_max = QLabel('Max:')
        stats_box.addWidget(self.plot_max)

        self.plot_med = QLabel('Median:')
        stats_box.addWidget(self.plot_med)

        self.plot_avg = QLabel('Mean:')
        stats_box.addWidget(self.plot_avg)

        main_box.addLayout(stats_box)

        lay.addLayout(main_box)
        self.setLayout(lay)

    def handle_refresh(self, val):
        self.rate_value = self.rate.value() if self.rate.value() > 0 else 10
        self.updateRate.emit(self.rate_value)

        self.lim = self.limit.value() if self.limit.value() > 0 else 10
        self.window = self.window_input.value() if self.window_input.value() > 0 else 10
        
    def start(self):
        self.sim_prev = None
        self.real_prev = time.time() * (10 ** 9) # converting from s to ns
        self.start_time = self.real_prev
        self.data = []
        self.lim_data = [] # data within limit
        self.t = SamplingThread()
        self.kill_event.connect(self.t.end_thread)
        self.t.sample.connect(self.get_time)
        self.updateRate.connect(self.t.update) 
        self.t.start()

    def handle_sample(self, val):
        self.sem.acquire()
        if not self.sim_prev:
            self.sim_prev = val[0]['time_ns']
            self.real_prev = val[1]['time_ns']
            self.sem.release()
            return
        diff = (val[0]['time_ns'] - self.sim_prev) / (val[1]['time_ns'] - self.real_prev)
        self.sim_prev = val[0]['time_ns']
        self.real_prev = val[1]['time_ns']
        self.data.append(diff)
        if len(self.data) > self.window:
            self.data = self.data[-1 * self.window:]
        avg = sum(self.data)/len(self.data)
        if len(self.lim_data) > self.lim * self.rate_value:
            self.lim_data = self.lim_data[-1 * self.lim * self.rate_value:]
        self.lim_data.append(avg)
        self.handle_stats()
        self.line.set_xdata(numpy.append(self.line.get_xdata(), (val[1]['time_ns'] - self.start_time) / (10 ** 9)))
        self.line.set_ydata(numpy.append(self.line.get_ydata(), avg))
        self.ax.set_xlim((val[1]['time_ns'] - self.start_time) / (10 ** 9) - self.lim, (val[1]['time_ns'] - self.start_time) / (10 ** 9))
        
        #self.ax.collections.remove(self.fill)
        #self.fill = self.ax.fill_between(self.line.get_xdata(), self.line.get_ydata(), color='blue', alpha=.2, interpolate=True)
        self.canvas.draw()
        self.sem.release()
        
    def handle_stats(self):
        if self.lim_data[-1] > self.all_max_val or self.all_max_val < 0:
            self.all_max_val = self.lim_data[-1]
            self.all_max.setText(f'Max: {self.lim_data[-1]:.03f}')
        if self.lim_data[-1] < self.all_min_val or self.all_min_val < 0:
            self.all_min_val = self.lim_data[-1]
            self.all_min.setText(f'Min: {self.lim_data[-1]:.03f}')

        if self.lim_data[-1] > self.plot_max_val or self.plot_max_val > max(self.lim_data):
            self.plot_max_val = self.lim_data[-1]
            self.plot_max.setText(f'Max: {self.lim_data[-1]:.03f}')
        if self.lim_data[-1] < self.plot_min_val or self.plot_min_val < min(self.lim_data):
            self.plot_min_val = self.lim_data[-1]
            self.plot_min.setText(f'Min: {self.lim_data[-1]:.03f}')
        self.ax.set_ylim(0, max(1.1, self.plot_max_val + .1))
        self.ax.set_yticks(numpy.arange(0, max(1.1, self.plot_max_val + .1), .1))
        avg = sum(self.lim_data)/len(self.lim_data)
        self.plot_avg.setText(f'Mean: {avg:.03f}')

        med = numpy.median(self.lim_data)
        self.plot_med.setText(f'Median: {med:.03f}')
    
    def get_time(self):
        self.qmp.command('itc-time-metric')

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