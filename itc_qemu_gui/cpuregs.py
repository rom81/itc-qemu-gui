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
        self.qmp.cpuRegInfo.connect(self.on_cpuRegInfo)
        ret = self.qmp.command("itc-cpureg")
        # init gui
        self.register_widgets = {}
        self.ui_inited = False

    def init_ui(self):
        """init user interface"""
        # init ui
        self.ui = Ui_cpuregs()
        self.ui.setupUi(self)
        # menu
        self.ui.action_file_save.triggered.connect(self.on_save)
        self.ui.action_options_autorefresh.triggered.connect(self.on_autorefresh)
        self.ui.action_options_autorefresh.setChecked(True)
        self.on_autorefresh(True)
        self.ui.action_options_textview.triggered.connect(self.on_textview)
        # dynamically populate register widgets
        self.ui.register_widgets = {}
        grid = QGridLayout()
        self.ui.page_regs.setLayout(grid)

        # set up register/value grid
        regs = []
        vals = []
        for reg in self.registers:
            regs.append(reg['reg'])
            vals.append(reg['val'])

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
                self.ui.register_widgets.setdefault(regs[k], le_val)

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

    def on_cpuRegInfo(self, data):
        """populate registers dictionary"""
        self.registers = json.loads(str(data['vals']).replace("\'", "\""))

        """populate self.info for text view"""
        self.info = ""
        for reg in self.registers:
            self.info += reg['reg'] + ": " + reg['val']
            self.info += "\n"

        if not self.ui_inited:
            self.init_ui()
            self.ui_inited = True

    def update(self):
        # """update gui info"""
        self.qmp.command("itc-cpureg")

        # update plain text view
        self.ui.out_cpuregs.setPlainText(self.info)

        # update reg view if visible
        i = 0
        if self.ui.stack.currentIndex() == 0:
            for reg, widgets in self.ui.register_widgets.items():
                old_value = widgets.text()
        
                # register = next(item for item in self.registers if item["reg"] == reg)
                register = None 
                for item in self.registers:
                    if item["reg"] == reg:
                        register = item
                new_value = register['val']
                i = i+1
                widgets.setText(new_value)
                widgets.setCursorPosition(0)
                if self.qmp.running:
                    if old_value != new_value:
                        widgets.setStyleSheet('color: blue')
                    else:
                        widgets.setStyleSheet('')
                widgets.setCursorPosition(0)

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

