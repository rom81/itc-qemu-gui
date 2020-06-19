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
        self.text.append(f'{data}\n')