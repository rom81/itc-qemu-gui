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

from PySide2.QtWidgets import QWidget, QHeaderView, QTreeWidgetItem
from PySide2.QtGui import QFont
from PySide2.QtCore import QSemaphore

from itc_qemu_gui.constants import constants
from itc_qemu_gui.ui.memtree import Ui_memtree
from itc_qemu_gui.memdump import MemoryDumpWindow

class MemoryTreeWindow(QWidget):
    """memory tree window"""
    def __init__(self, qmp, parent=None):
        """init memory tree window"""
        super().__init__(parent)
        self.qmp = qmp
        self.qmp.memoryMap.connect(self.update_tree)

        self.tree_sem = QSemaphore(1)
        self.sending_sem = QSemaphore(1) # used to prevent sending too many requests at once

        self.init_ui()
        self.get_mmap()

    def init_ui(self):
        """init user interface"""
        self.ui = Ui_memtree()
        self.ui.setupUi(self)
        self.ui.btn_refresh.clicked.connect(self.get_mmap)

        self.ui.tree_memory.itemDoubleClicked.connect(self.open_region)
        self.ui.tree_memory.header().setSectionsMovable(False)
        self.ui.tree_memory.header().setSectionResizeMode(0, QHeaderView.Stretch)

    def get_mmap(self):
        """get memory map"""
        self.ui.tree_memory.clear()
        self.qmp.command('itc-mtree')

    def find(self, name, node):
        """find items with name in tree"""
        # must acquire semaphore before use
        if node.text(0) == name:
            return node
        else:
            for i in range(node.childCount()):
                result = self.find(name, node.child(i))
                if result:
                    return result
                return None

    def update_tree(self, value):
        """update memory tree"""
        if value != None:
            self.tree_sem.acquire()
            current_addr_space = ''

            for region in value:
                parent_node = self.ui.tree_memory
                parent = region['parent']
                if parent != '':
                    root = self.ui.tree_memory.invisibleRootItem()
                    for i in range(root.childCount()):
                        if root.child(i).text(0) == current_addr_space:
                            root = root.child(i)
                            break
                    parent_node = self.find(parent, root)
                else:
                    current_addr_space = region['name']

                node = QTreeWidgetItem(parent_node)
                node.setText(0, region['name'])
                start = region['start']
                end = region['end']
                if start < 0:
                    start = start + (1 << constants['bits'])
                if end < 0:
                    end = end + (1 << constants['bits'])
                node.setText(1, f'{start:016x}')
                node.setText(2, f'{end:016x}')
                node.setFont(0, QFont('Courier New'))
                node.setFont(1, QFont('Courier New'))
                node.setFont(2, QFont('Courier New'))

            self.tree_sem.release()

    def open_region(self, node, col):
        """open memory dump window for region"""
        win = MemoryDumpWindow(self.qmp, base=int(node.text(1), 16), max=int(node.text(2), 16))
        win.show()

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
    win = MemoryTreeWindow(qmp, None)
    win.show()
    app.exec_()

