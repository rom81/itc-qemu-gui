from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QPushButton, QTreeWidget, QTreeWidgetItem, QHeaderView
from package.qmpwrapper import QMP
from package.constants import constants
from PySide2.QtCore import QSemaphore, QSize
from PySide2.QtGui import QFont
from package.memdumpwindow import MemDumpWindow

class MemTree(QWidget):
	def __init__(self, qmp, parent):
		super().__init__()
		self.qmp = qmp
		self.qmp.memoryMap.connect(self.update_tree)

		self.parent = parent

		self.tree_sem = QSemaphore(1)
		self.sending_sem = QSemaphore(1) # used to prevent sending too many requests at once

		self.init_ui()
		self.get_map()

	def init_ui(self):
		self.vbox = QVBoxLayout()

		self.refresh = QPushButton('Refresh')
		self.refresh.clicked.connect(lambda:self.get_map())
		self.vbox.addWidget(self.refresh)

		self.tree = QTreeWidget()
		self.tree.itemDoubleClicked.connect(self.open_region)
		self.tree.setColumnCount(3)
		self.tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)
		self.tree.header().setStretchLastSection(False)
		self.tree.setHeaderLabels(['Memory Region', 'Start Address', 'End Address'])
		self.vbox.addWidget(self.tree)

		self.setLayout(self.vbox)
		self.setGeometry(100, 100, 600, 325)
		self.setWindowTitle("Memory Tree")
		self.show()

	def get_map(self):
		self.tree.clear()
		self.qmp.command('mtree')		

	# finds item with name 'name' in self.tree
	# self.tree_sem must be acquired before use
	def find(self, name, node):
		if node.text(0) == name:
			return node
		else:
			for i in range(node.childCount()):
				result = self.find(name, node.child(i))
				if result:
					return result
			return None


	def update_tree(self, value):
		if value != None:
			self.tree_sem.acquire()
			current_addr_space = ''

			for region in value:
				parent_node = self.tree
				parent = region['parent']

				if parent != '':
					root = self.tree.invisibleRootItem()
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
		self.parent.open_new_window(MemDumpWindow(self.qmp, base=int(node.text(1), 16), max=int(node.text(2), 16)))