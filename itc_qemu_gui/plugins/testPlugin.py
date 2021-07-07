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

from PySide2.QtWidgets import QWidget, QTextEdit, QHBoxLayout
from yapsy.IPlugin import IPlugin

class TestPlugin(QWidget, IPlugin):
    name = 'QMP Displayer'

    def display(self, qmp):
        self.init_ui()
        self.qmp = qmp
        self.qmp.newData.connect(self.handle_data)
        self.show()

    def init_ui(self):
        self.layout = QHBoxLayout()
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.layout.addWidget(self.text)

        self.setLayout(self.layout)

    def handle_data(self, data):
        if data:
            self.text.append(f'{data}\n')
