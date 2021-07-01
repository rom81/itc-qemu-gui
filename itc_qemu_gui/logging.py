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

from PySide2.QtWidgets import QWidget, QTreeWidgetItem, QCheckBox, QFileDialog, QCompleter
from PySide2.QtGui import Qt, QTextCursor
from PySide2.QtCore import QFileSystemWatcher

from itc_qemu_gui.ui.logging import Ui_logging

DEFAULT_LOGFILE = os.path.join(os.path.expanduser("~"), "qemu.log")
MAX_LINES = 1000

# TODO write custom qmp command to get log masks
LOG_MASKS = (
    "out_asm",
    "in_asm",
    "op",
    "op_opt",
    "op_ind",
    "int",
    "exec",
    "cpu",
    "fpu",
    "mmu",
    "pcall",
    "cpu_reset",
    "unimp",
    "guest_errors",
    "page",
    "nochain",
)

class LoggingWindow(QWidget):
    """qemu logging window"""

    def __init__(self, qmp, parent=None):
        """init window"""
        super().__init__(parent)
        # qmp connection
        self.qmp = qmp
        # input logfile and file change watcher
        self.fin = None
        self.watcher = None
        # current active log masks and trace events used to restore state on exit
        self.active_masks = []
        self.active_tevents = []
        # init gui
        self.init_ui()

    def init_ui(self):
        """init user interface"""
        # init ui
        self.ui = Ui_logging()
        self.ui.setupUi(self)

        # configure logfile widgets
        self.ui.le_logfile.setText(DEFAULT_LOGFILE)
        self.ui.btn_logfile.clicked.connect(self.on_select_logfile)
        self.ui.btn_start.clicked.connect(self.on_start_logging)
        self.ui.btn_stop.clicked.connect(self.on_stop_logging)

        # configure splitters
        self.ui.splitter_outlog.setStretchFactor(1, 1)

        # retrieve and iterate all available trace events via qmp and dynamically populate tree widget
        raw_tevent_data = self.qmp.hmp_command('info trace-events').get('return', '')
        #print("raw_tevent_data = " + str(raw_tevent_data)) 
        tevent_regex = re.compile(r'\s*:\s*state\s*')
        tevent_categories = []
        tevent_widgets = []
        for line in sorted(raw_tevent_data.splitlines()):
            # parse raw trace event line to get event name and current state
            # note: command is actually hmp over qmp so result returned as string instead of nice json format
            tokens = tevent_regex.split(line)
            tevent = tokens[0]
            state = bool(int(tokens[1]))
            # attempt to categorize trace event
            category = tevent.split('_')[0]
            if category not in tevent_categories:
                # add trace event category
                tevent_categories.append(category)
                # create top level parent tree widget item for category
                item = QTreeWidgetItem(self.ui.tree_tevents)
                item.setText(0, category)
                tevent_widgets.append(item)
            # create trace event tree widget category child item
            subitem = QTreeWidgetItem(item)
            btn_tevent = QCheckBox(tevent)
            btn_tevent.setChecked(state)
            if state:
                self.active_tevents.append(tevent)
            btn_tevent.stateChanged.connect(self.on_tevent_enable)
            self.ui.tree_tevents.setItemWidget(subitem, 0, btn_tevent)

        # custom trace event category completion engine
        self.completer = QCompleter(tevent_categories, self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.le_search.setCompleter(self.completer)

        # trace event search
        self.ui.le_search.returnPressed.connect(self.ui.btn_search.click)
        self.ui.btn_search.clicked.connect(self.on_tevent_search)

        # trace event tree expand/collapse
        self.ui.btn_expand.clicked.connect(self.ui.tree_tevents.expandAll)
        self.ui.btn_collapse.clicked.connect(self.ui.tree_tevents.collapseAll)

        # dynamically populate log mask widgets
        for mask in LOG_MASKS:
            btn_mask = QCheckBox(mask)
            btn_mask.stateChanged.connect(self.on_mask_enable)
            self.ui.scroll_contents.layout().addWidget(btn_mask)
        self.ui.scroll_contents.layout().addStretch()

        # set maximum log lines and configure scrolling
        self.ui.out_log.setMaximumBlockCount(MAX_LINES + 1)
        self.ui.out_log.centerOnScroll()

    def on_select_logfile(self):
        """select logfile callback"""
        logfile = QFileDialog.getSaveFileName(self, "QEMU Log File", os.path.expanduser("~"))[0]
        if logfile:
            self.ui.le_logfile.setText(logfile)

    def on_start_logging(self):
        """start logging to logfile callback"""
        # get logfile name from widget
        logfile = self.ui.le_logfile.text()
        # enable logfile output via qmp
        self.qmp.hmp_command(f'logfile "{logfile}"')
        # open logfile and seek to end
        self.fin = open(logfile, 'r')
        self.fin.seek(0, 2)
        # create file watcher for efficient async change notifications
        self.watcher = None
        self.watcher = QFileSystemWatcher([logfile], parent=self)
        self.watcher.fileChanged.connect(self.on_log_change)

    def on_stop_logging(self):
        """stop logging"""
        # disable all trace events
        for tevent in self.active_tevents:
            self.qmp.hmp_command(f'trace-event {tevent} off')
        # disable all log masks on window close
        self.qmp.hmp_command('log none')
   
    def on_log_change(self, fname):
        """logfile change callback"""
        if self.fin:
            # read and insert new lines
            lines = self.fin.readlines()
            if lines:
                self.ui.out_log.textCursor().insertText("".join(lines))
                self.ui.out_log.textCursor().movePosition(QTextCursor.End, QTextCursor.MoveAnchor, 0)

    def on_tevent_search(self):
        """trace event search callback"""
        # find trace event widget item match and set as current tree item
        tevent = self.ui.le_search.text()
        items = self.ui.tree_tevents.findItems(tevent, Qt.MatchContains, 0)
        if items:
            self.ui.tree_tevents.setCurrentItem(items[0])

    def on_tevent_enable(self, state):
        """trace event change callback"""
        # widget emitting signal
        widget = self.sender()
        # enable/disable trace event based on widget state
        tevent = widget.text().strip()
        if state:
            self.qmp.hmp_command(f'trace-event {tevent} on')
            self.active_tevents.append(tevent)
        else:
            self.qmp.hmp_command(f'trace-event {tevent} off')
            self.active_tevents.remove(tevent)

    def on_mask_enable(self, state):
        """log mask enable callback"""
        # widget emitting signal
        widget = self.sender()
        # enable/disable log mask based on widget state
        mask = widget.text().strip()
        if state:
            self.active_masks.append(mask)
        else:
            self.active_masks.remove(mask)
        # first disable all log masks and then enable selections due to qemu limitations
        masks = ",".join(self.active_masks)
        self.qmp.hmp_command('log none')
        self.qmp.hmp_command(f'log {masks}')

    def closeEvent(self, event):
        """overridden close event"""
        # disable all trace events on window close
        for tevent in self.active_tevents:
            self.qmp.hmp_command(f'trace-event {tevent} off')
        # disable all log masks on window close
        self.qmp.hmp_command('log none')
        # close logfile
        if self.fin:
            self.fin.close()
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
    print("host = " + host)
    print("port = " + port) 
    qmp.start()
    app = QApplication(sys.argv)
    win = LoggingWindow(qmp)
    win.show()
    app.exec_()

