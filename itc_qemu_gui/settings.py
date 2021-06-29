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

from PySide2.QtWidgets import QApplication, QDialog, QVBoxLayout
from PySide2.QtGui import QPalette, QColor, QGuiApplication
from PySide2.QtCore import Qt, QObject

from itc_qemu_gui.ui.settings import Ui_settings_dialog

class SettingsDialog(QDialog):

    def __init__(self, parent, default_palette):
        super().__init__(parent)
        self.ui = Ui_settings_dialog()
        self.ui.setupUi(self)

        self.default_palette = default_palette
        if QGuiApplication.palette() != default_palette:
            self.ui.btn_darkmode.setChecked(True)
        self.ui.btn_darkmode.toggled.connect(self.on_dark_mode_toggle)

    def on_dark_mode_toggle(self, state):
        """dark mode checkbox callback"""
        if state:
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(25, 25, 25)) # 53 53 53
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(53, 53, 53)) # 25 25 25
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            QGuiApplication.setPalette(palette)
        else:
            QGuiApplication.setPalette(self.default_palette)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = SettingsDialog(None, QGuiApplication.palette())
    win.show()
    sys.exit(app.exec_())

