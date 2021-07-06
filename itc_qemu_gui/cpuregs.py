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

import re
import os.path
import json
import math

from PySide2.QtWidgets import QWidget, QFileDialog, QGridLayout, QLabel, QLineEdit, QHBoxLayout
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt, QTimer

from itc_qemu_gui.ui.cpuregs import Ui_cpuregs

class CpuRegistersWindow(QWidget):
    """cpu registers window"""

    def __init__(self, qmp, parent=None):
        """init window"""
        super().__init__(parent)
        # qmp connection
        self.qmp = qmp
        self.info = None
        self.registers = {}
        # refresh timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        # init gui
        self.register_widgets = {}
        self.init_ui()

    def init_ui(self):
        """init user interface"""
        # init ui
        self.ui = Ui_cpuregs()
        self.ui.setupUi(self)
        # menu
        self.ui.action_file_save.triggered.connect(self.on_save)
        self.ui.action_options_autorefresh.triggered.connect(self.on_autorefresh)
        self.ui.action_options_autorefresh.setChecked(False)
        self.on_autorefresh(False)
        self.ui.action_options_textview.triggered.connect(self.on_textview)
        # dynamically populate register widgets
        self.get_info()
        self.ui.register_widgets = {}
        grid = QGridLayout()
        self.ui.page_regs.setLayout(grid)

        regs = list(self.registers.keys())
        vals = list(self.registers.values())
        k = 0
        for i in range(0, 3):
            for j in range(0, math.ceil(len(self.registers)/3)):
                horizontalLayout = QHBoxLayout()
                horizontalLayout.addWidget(QLabel(regs[k], self))
                le_val = QLineEdit(str(vals[k]), self)
                le_val.setReadOnly(True)
                le_val.setCursorPosition(0)
                le_val.setFont(QFont('Monospace'))
                horizontalLayout.addWidget(le_val)
                grid.addLayout(horizontalLayout, j, i)
                # self.ui.register_widgets[regs[k]].append(le_val)

                k = k + 1
                
        for i in range(1, grid.columnCount()):
            grid.setColumnMinimumWidth(i, 40)
        grid.setRowStretch(grid.rowCount(), 1)

    def on_save(self):
        """save registers to file callback"""
        if self.info:
            filename = QFileDialog.getSaveFileName(self, 'Save File', os.path.expanduser('~'), 'Text files (*.txt)')[0]
            if filename:
                with open(filename, 'w') as fout:
                    fout.write(self.info)

    def on_autorefresh(self, state):
        """auto refresh callback"""
        if state:
            self.timer.start(100)
        else:
            self.timer.stop()

    def on_textview(self, state):
        """plain text view callback"""
        if state:
            self.ui.stack.setCurrentIndex(1)
        else:
            self.ui.stack.setCurrentIndex(0)

    def update(self):
        """update gui info"""
        # get current info
        self.get_info()
        # update plain text view
        self.ui.out_cpuregs.setPlainText(self.info)
        # update reg view if visible
        if self.ui.stack.currentIndex() == 0:
            for reg, widgets in self.ui.register_widgets.items():
                for i, widget in enumerate(widgets):
                    old_value = widget.text()
                    new_value = self.registers[reg][i]
                    print("old_value = ", old_value, " new value = ", new_value)
                    widget.setText(new_value)
                    widget.setCursorPosition(0)
                    if self.qmp.running:
                        if old_value != new_value:
                            widget.setStyleSheet('color: blue')
                        else:
                            widget.setStyleSheet('')
                    widget.setCursorPosition(0)

    def get_info(self):
        """get cpu register info"""
        # execute hmp command over qmp and parse cpu registers
        self.info = self.qmp.hmp_command('info registers')['return']
        self.registers = self.parse_info()

    def parse_info(self):
        """parse register info from hmp plain text"""
        registers = {}
        values = []

        tokens = self.info.split("\r\n")
        for i in range(0, 3):
            grp = tokens[i].split()
            for tok in grp:
                if "=" in tok and tok.split("=")[0] and tok.split("=")[1]:
                    chars = tok.split("=")
                    registers[chars[0]] = chars[1]
        for i in range(3, 9):
            grp = tokens[i].split()
            registers[grp[0]] = grp[1].replace("=","") + grp[2] + grp[3] + grp[4] + grp[5] + grp[6]
        grp = tokens[9].split()
        registers[grp[0].split("=")[0]] = grp[0].split("=")[1] + grp[1] + grp[2] + grp[3] + grp[4] + grp[5]
        grp = tokens[10].split()
        registers[grp[0]] = grp[1].split("=")[1] + grp[2] + grp[3] + grp[4] + grp[5] + grp[6]
        for i in range(11, 13):
            grp = tokens[i].split()
            registers[grp[0].split("=")[0]] = grp[1] + grp[2]
        for i in range(13, 18):
            grp = tokens[i].split()
            for tok in grp:
                if "=" in tok and tok.split("=")[0] and tok.split("=")[1]:
                    chars = tok.split("=")
                    registers[chars[0]] = chars[1]
        for i in range(18, 22):
            grp = tokens[i].split()
            registers[grp[0].split("=")[0]] = grp[0].split("=")[1] + grp[1]
            registers[grp[2].split("=")[0]] = grp[2].split("=")[1] + grp[3]
        for i in range(22, 26):
            grp = tokens[i].split()
            registers[grp[0].split("=")[0]] = grp[0].split("=")[1]
            registers[grp[1].split("=")[0]] = grp[1].split("=")[1]

        return registers

    def closeEvent(self, event):
        """overridden close event"""
        self.timer.stop()
        event.accept()

if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication
    from itc_qemu_gui.qmpwrapper import QMP
    if len(sys.argv) != 3:
        sys.exit(f'usage: {sys.argv[0]} host port')
    host, port = sys.argv[1:]
    qmp = QMP()
    qmp.sock_connect(host, int(port))
    qmp.start()
    app = QApplication(sys.argv)
    win = CpuRegistersWindow(qmp)
    win.show()
    app.exec_()

