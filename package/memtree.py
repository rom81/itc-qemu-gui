from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QPushButton, QTreeWidget, QTreeWidgetItem
from package.qmpwrapper import QMP
from package.constants import constants
from PySide2.QtCore import QSemaphore
import time
class MemTree(QWidget):
	def __init__(self, qmp):
		super().__init__()
		self.qmp = qmp
		self.qmp.memoryMap.connect(self.update_tree)

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
		self.tree.itemClicked.connect(self.expand_item)
		self.tree.itemCollapsed.connect(self.collapse_item)
		self.tree.setColumnCount(3)
		self.vbox.addWidget(self.tree)

		self.setLayout(self.vbox)
		self.show()

	def expand_item(self, item, column):
		if not item.isExpanded():
			name = '?' + item.text(0)
			parent = item.parent()
			while parent: 
				name = '?' + parent.text(0) + name
				parent = parent.parent()
			self.get_subregion(name)
		else:
			print(item.text(0))
			self.collapse_item(item)
			item.setExpanded(False)

	def collapse_item(self, item):
		for i in range(item.childCount()):
			item.removeChild(item.child(i))

	def get_map(self):
		self.tree.clear()
		self.get_subregion('?')

	def get_subregion(self, name):
		self.qmp.command('mtree', args={'name': name})

	# finds item with name 'name' in self.tree
	# self.tree_sem must be acquired before use
	def find(self, name):
		root = self.tree.invisibleRootItem()
		names = name.split('?')[1:]
		for n in names:
			found = False
			print(root.childCount())
			for i in range(root.childCount()):
				child = root.child(i)
				if child.text(0) == n:
					found = True
					root = child
					break
			if not found:
				return None
		return root

	def update_tree(self, value):
		parent = value['parent']
		region = value['memorymap']
		if region != None:
			self.tree_sem.acquire()
			parent_node = self.tree
			if parent != '?':
				parent_node = self.find(parent)
			for r in region:
				node = QTreeWidgetItem(parent_node)
				node.setText(0, r['name'])
				node.setText(1, 'start: '  + str(r['start']))
				node.setText(2, 'end: ' + str(r['end']))
			if type(parent) is QTreeWidgetItem and not parent_node.isExpanded():
					parent_node.setExpanded(True)
			self.tree_sem.release()