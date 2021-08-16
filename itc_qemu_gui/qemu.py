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

import time
import datetime
import os.path
import threading

from PySide2.QtWidgets import QMainWindow, QLabel, QMessageBox, QAction, QGraphicsView, QGraphicsScene
from PySide2.QtGui import QGuiApplication, QIcon, QPixmap, QRegExpValidator, QIntValidator
from PySide2.QtCore import Signal, Qt, Slot

from itc_qemu_gui import __version__
from itc_qemu_gui.common import RESOURCE_ROOT, PLUGIN_ROOT
from itc_qemu_gui.qmpwrapper import QMP
from itc_qemu_gui.ui.qemu import Ui_qemu
from itc_qemu_gui.settings import SettingsDialog
from itc_qemu_gui.timing import TimingWindow
from itc_qemu_gui.memdump import MemoryDumpWindow
from itc_qemu_gui.memtree import MemoryTreeWindow
from itc_qemu_gui.cpuregs import CpuRegistersWindow
from itc_qemu_gui.logging import LoggingWindow
from itc_qemu_gui.assembly import AssemblyWindow

from yapsy.PluginManager import PluginManager

class QemuWindow(QMainWindow):

    kill_thread = Signal()

    def __init__(self, app):

        self.app = app
 
        # self.qmp = QMP('localhost', 55555)
        self.qmp = QMP()

        self.qmp.stateChanged.connect(self.handle_pause_button)
        self.qmp.connectionChange.connect(self.handle_connect_button)

        self.paused = False

        super().__init__()
        self.init_ui()

        self.qmp.timeUpdate.connect(self.update_time)
        self.t = TimeThread(self.qmp)

        self.window = []

        self.default_theme = QGuiApplication.palette()

    def init_ui(self):
        """init ui"""
        # load ui file
        self.ui = Ui_qemu()
        self.ui.setupUi(self)
        # set main window icon
        icon = QIcon(os.path.join(RESOURCE_ROOT, 'qemu-official.png'))
        self.setWindowIcon(icon)
        # menus
        self.ui.action_file_settings.triggered.connect(self.open_settings_dialog)
        self.ui.action_file_exit.triggered.connect(self.app.closeAllWindows)
        self.ui.action_run_stop.triggered.connect(lambda: self.qmp.command('stop'))
        self.ui.action_run_play.triggered.connect(lambda: self.qmp.command('cont'))
        self.ui.action_tools_memdump.triggered.connect(lambda: self.open_new_window(MemoryDumpWindow))
        self.ui.action_tools_memtree.triggered.connect(lambda: self.open_new_window(MemoryTreeWindow))
        self.ui.action_tools_cpuregs.triggered.connect(lambda: self.open_new_window(CpuRegistersWindow))
        self.ui.action_tools_asm.triggered.connect(lambda: self.open_new_window(AssemblyWindow))
        self.ui.action_tools_logging.triggered.connect(lambda: self.open_new_window(LoggingWindow))
        self.ui.action_tools_timing.triggered.connect(lambda: self.open_new_window(TimingWindow))
        self.ui.action_help_about.triggered.connect(self.show_about_splash)
        # widgets
        validator = QRegExpValidator('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', self.ui.le_qmp_ip)
        self.ui.le_qmp_ip.setValidator(validator)
        validator = QIntValidator(0, 65535, self.ui.le_qmp_port)
        self.ui.le_qmp_port.setValidator(validator)
        self.ui.btn_simstate.setText('■')
        self.ui.btn_simstate.clicked.connect(lambda: self.stop_sim() if not self.paused else self.cont_sim())
        self.ui.btn_simstate.setEnabled(False)
        logo = QPixmap(os.path.join(RESOURCE_ROOT, 'qemu-official.png'))
        logo = logo.scaled(64, 64, Qt.KeepAspectRatio)
        self.ui.label_logo.setPixmap(logo)
        self.ui.btn_qmp_connect.clicked.connect(self.qmp_start)
        self.ui.label_status = QLabel("Disconnected")
        self.ui.statusbar.addPermanentWidget(self.ui.label_status)
        # plugins
        plugin_mgr = PluginManager()
        plugin_mgr.setPluginPlaces([PLUGIN_ROOT])
        plugin_mgr.locatePlugins()
        plugin_mgr.loadPlugins()
        for plugin in plugin_mgr.getAllPlugins():
            self.ui.menu_plugins.addAction(QAction(plugin.name, self, triggered=(lambda: plugin.plugin_object.display(self.qmp))))

    def show_about_splash(self):
        """about menu handler"""
        about_dialog = QMessageBox(self)
        about_dialog.setWindowTitle("ITC QEMU GUI")
        about_dialog.setIconPixmap(QPixmap(os.path.join(RESOURCE_ROOT, 'nasa.png')))
        about_dialog.setTextFormat(Qt.RichText)
        about_dialog.setText("<b>ITC QEMU GUI</b><br>"
                             "Version: <em>" + __version__ + "</em><br><br>"
                             "Copyright (C) 2020 National Aeronautics and Space Administration. "
                             "All Foreign Rights are Reserved to the U.S. Government.")
        about_dialog.exec_()

    def open_settings_dialog(self):
        """open settings dialog"""
        dialog = SettingsDialog(self, self.default_theme)
        dialog.exec_()

    def cont_sim(self):
        print("sending cont command")
        self.ui.btn_simstate.setText('■')
        self.ui.out_simstate.setText('<font color="green">Running</font>')
        self.qmp.command('cont')

    def stop_sim(self):
        print("sending stop command")
        self.ui.btn_simstate.setText('▶')
        self.ui.out_simstate.setText('<font color="red">Paused</font>')
        self.qmp.command('stop')

    def throwError(self):
        msgBox = QMessageBox(self)
        msgBox.setText('Lost Connection to QMP!')
        msgBox.show()

    @Slot(bool)
    def handle_pause_button(self, value):
        # Catches signals from QMPWrapper
        #print('recieved: ', value)
        # time.sleep(0.05) # fix race condition
        if value:
            self.paused = False
            self.ui.btn_simstate.setText('■')
            self.ui.out_simstate.setText('<font color="green">Running</font>')
        elif not value and value is not None:
            self.paused = True 
            self.ui.btn_simstate.setText('▶')
            self.ui.out_simstate.setText('<font color="red">Paused</font>')

    def handle_connect_button(self, value):
        self.ui.btn_qmp_connect.setChecked(value)
        self.ui.le_qmp_ip.setReadOnly(value)
        self.ui.le_qmp_port.setReadOnly(value)

    def open_new_window(self, window_class):
        if self.qmp.isSockValid():
            #win = window_class(self.qmp, parent=self)
            win = window_class(self.qmp)
            win.show()
            self.window.append(win)

    def update_time(self, time):
        date = datetime.datetime.fromtimestamp(time / 1000000000, datetime.timezone.utc)
        self.ui.out_time.setText(f'{date.day - 1:02}:{date.hour:02}:{date.minute:02}:{date.second:02}') # -1 for day because it starts from 1

    def qmp_start(self):
        if not self.ui.le_qmp_port.hasAcceptableInput():
            return
        if self.qmp.isSockValid():
            self.qmp.sock_disconnect()
            self.kill_thread.emit()
            self.ui.btn_simstate.setText('■')
            self.ui.out_simstate.setText('<font color="grey">Inactive</font>')
            self.ui.btn_simstate.setEnabled(False)
            return
        else:
            host = self.ui.le_qmp_ip.text()
            port = self.ui.le_qmp_port.text()
            if port.isnumeric():
                status = self.qmp.sock_connect(host, int(port))
                if self.qmp.isSockValid():
                    self.ui.label_status.setText("Connected")
                    self.ui.out_version.setText(str(self.qmp.banner['QMP']['version']['package']))
                    self.ui.btn_simstate.setEnabled(True)

                    # check if running initially
                    if self.qmp.running:
                        self.paused = False
                        self.ui.btn_simstate.setText('■')
                        self.ui.out_simstate.setText('<font color="green">Running</font>')
                    else:
                        self.paused = True
                        self.ui.btn_simstate.setText('▶')
                        self.ui.out_simstate.setText('<font color="red">Paused</font>')
                    if not self.qmp.isAlive():
                        self.qmp.start()
                    if not self.t.isAlive():
                        self.t.start()
                else:
                    self.ui.label_status.setText("Failed to connect: " + str(status))

    def closeEvent(self, event):
        self.kill_thread.emit()
        event.accept()

class TimeThread(threading.Thread):

    def __init__(self, qmp):
        super().__init__()
        self.daemon = True
        self.qmp = qmp

    def run(self):
        while True:
            if self.qmp.running:
                time.sleep(.5)
                args = {'clock': 'virtual'}
                self.qmp.command('itc-sim-time', args=args)
