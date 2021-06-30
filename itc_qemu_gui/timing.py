# Copyright (C) 2009 - 2020 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
# 
# This software is provided "as is" without any warranty of any kind, either expressed, implied, or statutory, including, but not
# limited to, any warranty that the software will conform to specifications, any implied warranties of merchantability, fitness
# for a particular purpose, and freedom from infringement, and any warranty that the documentation will conform to the program, or
# any warranty that the software will be error free.
# 
# In no event shall NASA be liable for any damages, including, but not limited to direct, indirect, special or consequential damages,
# arising out of, resulting from, or in any way connected with the software or its documentation, whether or not based upon warranty,
# contract, tort or otherwise, and whether or not loss was sustained from, or arose out of the results of, or use of, the software,
# documentation or services provided hereunder.
# 
# ITC Team
# NASA IV&V
# ivv-itc@lists.nasa.gov

import statistics
from dataclasses import dataclass

from PySide2.QtWidgets import QWidget
from PySide2.QtGui import Qt, QPainter
from PySide2.QtCore import QBasicTimer

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from itc_qemu_gui.ui.timing import Ui_timing

@dataclass
class TimeSample(object):
    """time metric sample"""
    tsim: float
    twall: float
    multiplier: float = 0.0

class TimingWindow(QWidget):
    """qemu timing metrics window"""

    def __init__(self, qmp, parent=None):
        """init window"""
        super().__init__(parent)
        # qmp connection
        self.qmp = qmp
        self.qmp.timeMetric.connect(self.on_timeSample) 
        self.qmp.stateChanged.connect(self.on_stateChange)
        # sample request timer
        self.timer = QBasicTimer()
        # time metric samples and statistics
        self.samples = []
        self.multiplier_min = -1
        self.multiplier_max = -1
        # parameters
        self.rate = 10
        self.limit = 10
        self.window = 10
        # init user interface
        self.init_ui()

    def init_ui(self):
        """init user interface"""
        # init ui
        self.ui = Ui_timing()
        self.ui.setupUi(self)

        # control widgets
        self.ui.spin_rate.setValue(self.rate)
        self.ui.spin_rate.valueChanged.connect(self.on_rate_change)
        self.ui.spin_limit.setValue(self.limit)
        self.ui.spin_limit.valueChanged.connect(self.on_limit_change)
        self.ui.spin_window.setValue(self.window)
        self.ui.spin_window.valueChanged.connect(self.on_window_change)
        self.update_sample_timer()

        # plot widgets 
        figure = Figure()
        self.axes = figure.add_subplot()
        self.axes.set(xlabel='Simulation Time (s)',
                      xlim=[0, self.limit],
                      ylabel='Multiplier',
                      ylim=[0, 1.1])
        self.axes.grid(which='major')
        self.axes.grid(which='minor', linestyle='--')
        self.axes.minorticks_on()
        self.axes.tick_params(axis='x', labelrotation=45)
        self.line = self.axes.plot([], antialiased=True, color='b')[0]

        self.canvas = FigureCanvas(figure)
        self.canvas.draw()
        self.ui.figure.addWidget(self.canvas)

    def on_rate_change(self, rate):
        """rate change callback"""
        self.rate = rate
        self.update_sample_timer()

    def on_window_change(self, window):
        """window change callback"""
        self.window = window
        self.update_plot()

    def on_limit_change(self, limit):
        """limit change callback"""
        self.limit = limit
        self.update_plot()

    def get_window_index(self):
        """get index of first sample in window to perform multiplier calculations"""
        index = None
        if self.samples:
            index = 0
            if self.limit > 0:
                current_tsim = self.samples[-1].tsim
                for i, sample in enumerate(reversed(self.samples)):
                    if current_tsim - sample.tsim > self.limit:
                        index = len(self.samples) - i - 1
                        break
                if self.window > 1:
                    index -= self.window
                index = max(index, 0)
        return index

    def get_window_multiplier_averages(self):
        """get window multiplier moving averages"""
        sim_times = []
        moving_averages = []
        index = self.get_window_index()
        if index is not None:
            cumsum = [0]
            sim_times = [sample.tsim for sample in self.samples[index + self.window:]]
            for i, sample in enumerate(self.samples[index:]):
                cumsum.append(cumsum[-1] + sample.multiplier)
                if i >= self.window:
                    moving_average = (cumsum[i] - cumsum[i - self.window]) / self.window
                    moving_averages.append(moving_average)
        return [sim_times, moving_averages]

    def on_timeSample(self, data): 
        """new time sample received callback"""
        # new time sample
        sample = TimeSample(data[0]['time_ns'] / 10**9, data[1]['time_ns'] / 10**9)
        # store first sample and return immediately
        if not self.samples:
            self.samples.append(sample)
            return
        # calculate multiplier and add sample
        prev_sample = self.samples[-1]
        sample.multiplier = (sample.tsim - prev_sample.tsim) / (sample.twall - prev_sample.twall)
        self.samples.append(sample)
        # total multiplier min/max
        if self.multiplier_min == -1:
            self.multiplier_min = sample.multiplier
        self.multiplier_min = min(self.multiplier_min, sample.multiplier)
        self.multiplier_max = max(self.multiplier_max, sample.multiplier)
        # update plot
        self.update_plot()

    def update_plot(self):
        """update time plot"""
        # get window multipliers
        sim_times, multipliers = self.get_window_multiplier_averages()
        if multipliers:
            # update ui metrics
            window_min = min(multipliers)
            window_max = max(multipliers)
            window_mean = statistics.mean(multipliers)
            window_median = statistics.median(multipliers)
            self.ui.out_min.setText(f'{self.multiplier_min:.03f}')
            self.ui.out_max.setText(f'{self.multiplier_max:.03f}')
            self.ui.out_window_min.setText(f'{window_min:.03f}')
            self.ui.out_window_max.setText(f'{window_max:.03f}')
            self.ui.out_window_mean.setText(f'{window_mean:.03f}')
            self.ui.out_window_median.setText(f'{window_median:.03f}')
            # calculate x/y axis limits 
            xlim = [sim_times[0], sim_times[-1] + 0.1]
            ylim = [0, max(1.1, window_max + 0.1)]
            # update plot data
            self.line.set_data(sim_times, multipliers)
        else:
            xlim = [0, self.limit]
            ylim = [0, 1.1]
        # update axis limits
        self.axes.set_xlim(xlim[0], xlim[1])
        self.axes.set_ylim(ylim[0], ylim[1])
        # update widget
        self.canvas.draw()

    def update_sample_timer(self):
        """update sample timer"""
        if self.qmp.running:
            self.timer.start((1.0 / float(self.rate)) * 1000.0, self)
        else:
            self.timer.stop()

    def on_stateChange(self, state):
        """qemu state change callback"""
        self.update_sample_timer()

    def timerEvent(self, event):
        """overriden timer event"""
        if event.timerId() == self.timer.timerId():
            self.qmp.command('itc-time-metric')
        else:
            super().timerEvent(event)
    
    def closeEvent(self, event):
        self.timer.stop()

if __name__ == "__main__":
    import sys
    from PySide2.QtWidgets import QApplication
    from itc_qemu_gui.qmpwrapper import QMP
    if len(sys.argv) != 3:
        sys.exit(f"usage: {sys.argv[0]} host port")
    host, port = sys.argv[1:]
    qmp = QMP()
    qmp.sock_connect(host, int(port))
    qmp.start()
    app = QApplication(sys.argv)
    win = TimingWindow(qmp, None)
    win.show()
    app.exec_()

