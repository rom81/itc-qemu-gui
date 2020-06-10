from PySide2.QtCore import QSize, Slot, Qt, QSemaphore, QThread, Signal
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QTextEdit, QPushButton, QRadioButton, QCheckBox
from package.qmpwrapper import QMP
from PySide2.QtGui import QFont, QTextCharFormat, QTextCursor
from enum import Enum
from package.constants import constants
import time

def char_convert(byte):
    if byte in range(127):
        if byte == 0:
            return '\\0'
        elif byte == 9:
            return '\\t'
        elif byte == 10:
            return '\\n'
        elif byte >= 32:
            return chr(byte)
    return '.'

class MemDumpWindow(QWidget):

    kill_signal = Signal(bool)

    def __init__(self, qmp, ):
        super().__init__()
        self.init_ui()

        self.baseAddress = 0
        self.maxAddress = 0
        
        self.delta = 4 # adds a small buffer area for scrolling action to happen

        self.sem = QSemaphore(1) # semaphore for controlling access to the enabling / disabling of the scroll listening
        self.pos = self.chr_display.verticalScrollBar().value()

        self.highlight_sem = QSemaphore(1) # semaphore for controlling access to highlighting state
        self.is_highlighted = False
        self.highlight_addr = 0

        self.endian = Endian.little
        self.endian_sem = QSemaphore(1)

        self.qmp = qmp
        
        self.qmp.emptyReturn.connect(self.update_text)
        self.grab_data()

        self.t = MyThread(self)
        self.t.timing_signal.connect(lambda:self.grab_data(val=self.baseAddress, size=self.maxAddress-self.baseAddress, refresh=True))
        self.qmp.stateChanged.connect(self.t.halt)
        self.t.running = self.qmp.running
        self.t.start()
        self.show() 


    def init_ui(self):   
        self.hbox = QHBoxLayout() # holds widgets for refresh button, desired address, and size to grab
        self.vbox = QVBoxLayout() # main container
        self.lower_hbox = QHBoxLayout() # holds memory views
        self.lower_hbox.setSpacing(0)
        self.endian_vbox = QVBoxLayout()

        self.hbox.addWidget(QLabel('Address:'))
        self.address = QLineEdit()
        self.hbox.addWidget(self.address)

        self.hbox.addWidget(QLabel('Size:'))
        self.size = QLineEdit()
        self.hbox.addWidget(self.size)

        self.search = QPushButton('Search')
        self.search.clicked.connect(lambda:self.find(self.address.text(), constants['block_size']))
        self.hbox.addWidget(self.search)

        self.refresh = QPushButton('Refresh')
        self.refresh.clicked.connect(lambda:self.grab_data(val=self.address.text(), size=self.size.text(), refresh=True))
        self.hbox.addWidget(self.refresh)

        self.auto_refresh = QCheckBox('Auto Refresh')
        self.auto_refresh.setCheckState(Qt.CheckState.Checked)
        self.auto_refresh.stateChanged.connect(self.auto_refresh_check)
        self.hbox.addWidget(self.auto_refresh)

        self.vbox.addLayout(self.hbox)
        
        # textbox for addresses
        self.addresses = QTextEdit()
        self.addresses.setReadOnly(True)
        self.addresses.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.addresses.setLineWrapMode(QTextEdit.NoWrap)
        self.addresses.setCurrentFont(QFont('Courier New'))
        self.lower_hbox.addWidget(self.addresses)

        # textbox for hex display of memory
        self.mem_display = QTextEdit()
        self.mem_display.setReadOnly(True)
        self.mem_display.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.mem_display.setLineWrapMode(QTextEdit.NoWrap)
        self.mem_display.setCurrentFont(QFont('Courier New'))
        self.lower_hbox.addWidget(self.mem_display)
      
        # textbox for char display of memory
        self.chr_display = QTextEdit()
        self.chr_display.setReadOnly(True)
        self.chr_display.setLineWrapMode(QTextEdit.NoWrap)
        self.chr_display.setCurrentFont(QFont('Courier New'))
        self.lower_hbox.addWidget(self.chr_display)

        self.mem_display.verticalScrollBar().valueChanged.connect(self.addresses.verticalScrollBar().setValue) #synchronizes addresses's scroll bar to mem_display's 
        self.addresses.verticalScrollBar().valueChanged.connect(self.mem_display.verticalScrollBar().setValue) #synchronizes mem_display's scroll to addresses's, allowing for searching for addresses to scrol mem_display to the desired point 
        self.chr_display.verticalScrollBar().valueChanged.connect(self.mem_display.verticalScrollBar().setValue)  
        self.mem_display.verticalScrollBar().valueChanged.connect(self.chr_display.verticalScrollBar().setValue)  

        self.chr_display.verticalScrollBar().valueChanged.connect(self.handle_scroll)

        # setting up endiannes selection buttons
        self.little = QRadioButton("Little Endian")
        self.little.click()
        self.little.clicked.connect(lambda:self.change_endian(Endian.little))
        self.big = QRadioButton("Big Endian")
        self.big.clicked.connect(lambda:self.change_endian(Endian.big))
        self.endian_vbox.addWidget(self.little)
        self.endian_vbox.addWidget(self.big)

        self.lower_hbox.addLayout(self.endian_vbox)

        self.vbox.addLayout(self.lower_hbox)

        self.setLayout(self.vbox)
        self.setWindowTitle("Memory Dump")
        self.setGeometry(100, 100, 1550, 500)

 


    def auto_refresh_check(self, value):
        if self.auto_refresh.checkState() == Qt.CheckState.Checked and not self.t.isRunning():
            self.t = MyThread(self)
            self.t.timing_signal.connect(lambda:self.grab_data(val=self.baseAddress, size=self.maxAddress-self.baseAddress, refresh=True))
            self.t.start()
        elif self.auto_refresh.checkState() == Qt.CheckState.Unchecked:
            self.kill_signal.emit(True)

    def closeEvent(self, event):
        self.kill_signal.emit(True)
        self.qmp.emptyReturn.disconnect(self.update_text)
        event.accept()

    def update_text(self, value):
        f = None
        try: 
            f = open('/tmp/QEMUGUI-memdump', 'rb')
            byte = f.read()
            f.close()
        except Exception as e: # possibly an empty return for another function
            if f:
                f.close()
        s = '' # hex representation of memory
        addresses =  '' # addresses
        count = self.baseAddress # keeps track of each 16 addresses
        if self.pos == self.chr_display.verticalScrollBar().maximum():  # scrolling down
            count = self.maxAddress 
        self.maxAddress = count + len(byte)
        first = True
        chars = '' # char represenation of memor

        line_s = '' # single line in s
        line_c = '' # single line in chars
        self.endian_sem.acquire()
        for b in byte:
            if count % 16 == 0:
                if first:
                    addresses += f'0x{count:08x}' 
                    first = False
                else:
                    addresses += f'\n0x{count:08x}' 
                    s += line_s + '\n'
                    chars += line_c + '\n'
                    line_s = ''
                    line_c = ''
            count += 1
            if self.endian == Endian.big:
                line_s += f'0x{b:02x} ' 
                line_c += f'{char_convert(b):3}'
            elif self.endian == Endian.little:
                line_s = f'0x{b:02x} ' + line_s
                line_c = f'{char_convert(b):3}' + line_c
        self.endian_sem.release()

        scroll_goto = self.pos

        if self.pos >= self.max - self.delta:  # scrolling down
            self.addresses.append(addresses)
            self.mem_display.append(s[:-1])
            self.chr_display.append(chars[:-1])
            scroll_goto = self.max

        elif self.pos < self.min + self.delta:    # scrolling  up
            addr_cur = self.addresses.textCursor()
            mem_cur = self.mem_display.textCursor()
            chr_cur = self.chr_display.textCursor()

            addr_cur.setPosition(0)
            mem_cur.setPosition(0)
            chr_cur.setPosition(0)

            self.addresses.setTextCursor(addr_cur)
            self.mem_display.setTextCursor(mem_cur)
            self.chr_display.setTextCursor(chr_cur)

            self.addresses.insertPlainText(addresses + '\n')
            self.mem_display.insertPlainText(s)
            self.chr_display.insertPlainText(chars)

            scroll_goto = self.chr_display.verticalScrollBar().maximum() - self.max
        else:
            self.addresses.setPlainText(addresses)
            self.mem_display.setPlainText(s[:-1])
            self.chr_display.setPlainText(chars[:-1])

        self.highlight_sem.acquire()
        if self.is_highlighted:
            self.highlight_sem.release()
            self.highlight(self.highlight_addr)
        else:
            self.highlight_sem.release()

        self.chr_display.verticalScrollBar().setValue(scroll_goto)
        self.chr_display.verticalScrollBar().valueChanged.connect(self.handle_scroll)
        self.sem.release()
            


    def grab_data(self, val=0, size=constants['block_size'], refresh=False):
        if not self.sem.tryAcquire(1, 3000): # assume lost due to error
            self.chr_display.verticalScrollBar().valueChanged.connect(self.handle_scroll)
            val = 0
            size = constants['block_size']
            
        if val == None:
            val = 0
        if size == None:
            size = 1024

        if type(val) == str:
            try:
                val = int(val, 0)
            except Exception:
                val = 0
        
        if type(size) == str:
            try:
                size = int(size, 0)
            except Exception:
                size = constants['block_size']

        if val < 0:
            val = 0
        if size < 0:
            size = constants['block_size']
    
        val = val - (val % 16)
        if val < self.baseAddress or refresh:
            self.baseAddress = val

        self.chr_display.verticalScrollBar().valueChanged.disconnect(self.handle_scroll)
        self.pos = self.chr_display.verticalScrollBar().value()
        self.max = self.chr_display.verticalScrollBar().maximum()
        self.min = self.chr_display.verticalScrollBar().minimum()
        if refresh:
            self.clear_highlight()
            self.addresses.clear()  # clearing to refresh data, other regions will be refilled through scrolling
            self.mem_display.clear()
            self.chr_display.clear() 
            self.maxAddress = self.baseAddress

            self.highlight_sem.acquire()
            if self.is_highlighted and self.highlight_addr not in range(val, val + size):
                self.is_highlighted = False
                self.pos = 0
            self.highlight_sem.release()
        print(type(val))
        args = {
                'val': val,
                'size': size,
                'filename': '/tmp/QEMUGUI-memdump'
                }
        self.qmp.command('pmemsave', args=args)


    def find(self, addr, size):
        try:
            addr = int(addr, 0)
        except ValueError as e:
            print(e)
            return
        if self.baseAddress <= addr and addr <= self.maxAddress:
            self.highlight(addr)
            
        else:
            self.highlight_sem.acquire()
            self.is_highlighted = True
            self.highlight_addr = addr
            self.highlight_sem.release()
            self.grab_data(val=addr, size=size, refresh=True )
            
        self.sem.acquire()
        self.chr_display.verticalScrollBar().valueChanged.disconnect(self.handle_scroll)
        self.chr_display.ensureCursorVisible()
        self.chr_display.verticalScrollBar().valueChanged.connect(self.handle_scroll)
        self.sem.release()



    def clear_highlight(self):
        fmt = QTextCharFormat()
        fmt.setFont('Courier New')
        # clearing past highlights
        addr_cur = self.addresses.textCursor()  # getting cursors
        mem_cur = self.mem_display.textCursor()
        chr_cur = self.chr_display.textCursor()

        addr_cur.select(QTextCursor.Document)   # selecting entire document
        mem_cur.select(QTextCursor.Document)
        chr_cur.select(QTextCursor.Document)
        
        addr_cur.setCharFormat(fmt) # adding format
        mem_cur.setCharFormat(fmt)
        chr_cur.setCharFormat(fmt)


    def highlight(self, addr):
        self.clear_highlight()
        
        # adding new highlights
        fmt = QTextCharFormat()
        fmt.setBackground(Qt.cyan)
        fmt.setFont('Courier New')

        addr_block = self.addresses.document().findBlockByLineNumber((addr - self.baseAddress) // 16) # gets linenos 
        mem_block = self.mem_display.document().findBlockByLineNumber((addr - self.baseAddress) // 16)
        chr_block = self.chr_display.document().findBlockByLineNumber((addr - self.baseAddress) // 16)

        addr_cur = self.addresses.textCursor()  # getting cursors
        mem_cur = self.mem_display.textCursor()
        chr_cur = self.chr_display.textCursor()


        char_offset = 0
        char_from_anchor = 0
        mem_offset = 0
        self.endian_sem.acquire()
        if self.endian == Endian.big:
            mem_offset = (addr % 16) * 5
            char_offset = (addr % 16) * 3
        elif self.endian == Endian.little:
            mem_offset = (15*5) - ((addr % 16) * 5)
            char_offset = (15*3) - ((addr % 16)*3)
        self.endian_sem.release()
        addr_cur.setPosition(addr_block.position()) # getting positions
        mem_cur.setPosition(mem_block.position() + mem_offset) # gives character offset within 16 byte line
        chr_cur.setPosition(chr_block.position() + char_offset) # sets position of char

        chr_text = self.chr_display.toPlainText()
        if chr_text[chr_cur.position()] == '\\' and chr_cur.position() + 1 < len(chr_text) and chr_text[chr_cur.position() + 1] in ['0', 'n', 't']:
            chr_cur.setPosition(chr_cur.position() + 2, mode=QTextCursor.KeepAnchor) 
        else:
            chr_cur.setPosition(chr_cur.position() + 1, mode=QTextCursor.KeepAnchor) 


        addr_cur.select(QTextCursor.LineUnderCursor)    # selects whole line
        mem_cur.select(QTextCursor.WordUnderCursor)     # selects just one word

        addr_cur.setCharFormat(fmt) # setting format
        mem_cur.setCharFormat(fmt)
        chr_cur.setCharFormat(fmt)

        self.addresses.setTextCursor(addr_cur)
        self.mem_display.setTextCursor(mem_cur)
        self.chr_display.setTextCursor(chr_cur)
        
        self.highlight_sem.acquire()
        self.is_highlighted = True
        self.highlight_addr = addr
        self.highlight_sem.release()

    def handle_scroll(self):
        if self.chr_display.verticalScrollBar().value() >= self.chr_display.verticalScrollBar().maximum() - self.delta:
            self.grab_data(val=self.maxAddress)
        elif self.baseAddress > 0 and self.chr_display.verticalScrollBar().value() < self.chr_display.verticalScrollBar().minimum() + self.delta:
            size = constants['block_size']
            if self.baseAddress < size:
                size = self.baseAddress
            self.grab_data(val=self.baseAddress-size, size=size)
      
    def change_endian(self, endian):
        self.endian_sem.acquire()
        if endian == Endian.little:
            self.endian = endian
        elif endian == Endian.big:
            self.endian = endian
        self.endian_sem.release()


class MyThread(QThread):
    timing_signal = Signal(bool) 

    def __init__(self, mem):
        super().__init__()
        mem.kill_signal.connect(self.end)    
        self.sem = QSemaphore() 
        self.running = True
    def run(self):
        while True:
            if self.sem.tryAcquire(1, 1000): # try to acquire and wait 1s to try to acquire
                break
            if self.running:
                self.timing_signal.emit(True)

    def end(self, b):
        self.sem.release()

    def halt(self, running):
        self.running = running


class Endian(Enum):
    little = 1
    big = 2
