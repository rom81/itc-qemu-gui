from PySide2.QtCore import QSize, Slot, Qt, QSemaphore, QThread, Signal
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QTextEdit, QPushButton
from package.qmpwrapper import QMP
from PySide2.QtGui import QFont, QTextCharFormat, QTextCursor
from time import sleep

block_size = 1024 # size of each requested block of memory in bytes

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

    def __init__(self, qmp):
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

        self.qmp = qmp
        self.grab_data()

        self.qmp.emptyReturn.connect(self.update_text)
        
        self.t = MyThread(self)
        self.t.timing_signal.connect(lambda:self.grab_data(val=self.baseAddress, size=self.maxAddress-self.baseAddress, refresh=True))
        self.t.start()

        self.show()
       

    def init_ui(self):   
        self.hbox = QHBoxLayout() # holds widgets for refresh button, desired address, and size to grab
        self.vbox = QVBoxLayout()
        self.lower_hbox = QHBoxLayout()
        self.lower_hbox.setSpacing(0)

        self.hbox.addWidget(QLabel('Address:'))
        self.address = QLineEdit()
        self.hbox.addWidget(self.address)

        self.hbox.addWidget(QLabel('Size:'))
        self.size = QLineEdit()
        self.hbox.addWidget(self.size)

        self.search = QPushButton('Search')
        self.search.clicked.connect(lambda:self.find(self.address.text(), block_size))
        self.hbox.addWidget(self.search)

        self.refresh = QPushButton('Refresh')
        self.refresh.clicked.connect(lambda:self.grab_data(val=self.address.text(), size=self.size.text(), refresh=True))
        self.hbox.addWidget(self.refresh)

        self.vbox.addLayout(self.hbox)
        
        # textbox for addresses
        self.addresses = QTextEdit()
        self.addresses.setReadOnly(True)
        self.addresses.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.addresses.setMinimumWidth(150)
        self.addresses.setCurrentFont(QFont('Courier New'))
        self.lower_hbox.addWidget(self.addresses)

        # textbox for hex display of memory
        self.mem_display = QTextEdit()
        self.mem_display.setReadOnly(True)
        self.mem_display.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.mem_display.setMinimumWidth(800)
        self.mem_display.setCurrentFont(QFont('Courier New'))
        self.lower_hbox.addWidget(self.mem_display)
      
        # textbox for char display of memory
        self.chr_display = QTextEdit()
        self.chr_display.setReadOnly(True)
        self.chr_display.setMinimumWidth(400)
        self.chr_display.setCurrentFont(QFont('Courier New'))
        self.lower_hbox.addWidget(self.chr_display)

        self.mem_display.verticalScrollBar().valueChanged.connect(self.addresses.verticalScrollBar().setValue) #synchronizes addresses's scroll bar to mem_display's 
        self.addresses.verticalScrollBar().valueChanged.connect(self.mem_display.verticalScrollBar().setValue) #synchronizes mem_display's scroll to addresses's, allowing for searching for addresses to scrol mem_display to the desired point 
        self.chr_display.verticalScrollBar().valueChanged.connect(self.mem_display.verticalScrollBar().setValue)  
        self.mem_display.verticalScrollBar().valueChanged.connect(self.chr_display.verticalScrollBar().setValue)  

        self.chr_display.verticalScrollBar().valueChanged.connect(self.handle_scroll)

        self.vbox.addLayout(self.lower_hbox)

        self.setLayout(self.vbox)
        self.setWindowTitle("Memory Dump")

    def closeEvent(self, event):
        self.kill_signal.emit(True)
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
        s = ''
        addresses =  ''
        count = self.baseAddress
        if self.chr_display.verticalScrollBar().value() == self.chr_display.verticalScrollBar().maximum():  # scrolling down
            count = self.maxAddress 

        first = True
        chars = ''
        for b in byte:
            if count % 16 == 0:
                if first:
                    addresses += f'0x{count:08x}' 
                    first = False
                else:
                    addresses += f'\n0x{count:08x}' 
                    s += '\n'
                    chars += '\n'
            count += 1
            s += f'0x{b:02x} ' 
            chars += f'{char_convert(b)}'

        if self.pos >= self.chr_display.verticalScrollBar().maximum() - self.delta:  # scrolling down
            self.addresses.append(addresses)
            self.mem_display.append(s)
            self.chr_display.append(chars)
            self.maxAddress += len(byte)

        elif self.pos < self.chr_display.verticalScrollBar().minimum() + self.delta:    # scrolling  up
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
            self.mem_display.insertPlainText(s + '\n')
            self.chr_display.insertPlainText(chars + '\n')

        else:
            self.addresses.setPlainText(addresses)
            self.mem_display.setPlainText(s)
            self.chr_display.setPlainText(chars)
            

        self.highlight_sem.acquire()
        if self.is_highlighted:
            self.highlight_sem.release()
            self.highlight(self.highlight_addr)
        else:
            self.highlight_sem.release()
       
        print('load: ' + str(self.pos))
        self.chr_display.verticalScrollBar().setValue(self.pos)
        self.chr_display.verticalScrollBar().valueChanged.connect(self.handle_scroll)
        self.sem.release()
            


    def grab_data(self, val=0, size=block_size, refresh=False):
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
                size = block_size

        if val < 0:
            val = 0
        if size < 0:
            size = block_size

        val = val - (val % 16)
        if val < self.baseAddress or refresh:
            self.baseAddress = val
        
        self.sem.acquire()
        self.chr_display.verticalScrollBar().valueChanged.disconnect(self.handle_scroll)
        self.pos = self.chr_display.verticalScrollBar().value()

        if refresh:
            self.addresses.clear()  # clearing to refresh data, other regions will be refilled through scrolling
            self.mem_display.clear()
            self.chr_display.clear() 
            self.maxAddress = self.baseAddress

            self.highlight_sem.acquire()
            if self.highlight_addr not in range(val, val + size):
                self.is_highlighted = False
            self.highlight_sem.release()


        print('grab: ' + str(self.pos))
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
            self.grab_data(val=addr, size=size, refresh=True )
            self.highlight(addr)
            
        self.sem.acquire()
        self.chr_display.verticalScrollBar().valueChanged.disconnect(self.handle_scroll)
        self.chr_display.ensureCursorVisible()
        self.chr_display.verticalScrollBar().valueChanged.connect(self.handle_scroll)
        self.sem.release()


    def highlight(self, addr):
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

        
        addr_cur.setPosition(addr_block.position()) # getting positions
        mem_cur.setPosition(mem_block.position() + (addr % 16) * 5) # gives character offset within 16 byte line
        chr_cur.setPosition(chr_block.position() + (addr % 16)) # sets start of selection to just before char
        chr_cur.setPosition(chr_block.position() + (addr % 16) + 1, mode=QTextCursor.KeepAnchor) # sets end of election to just after char

        addr_cur.select(QTextCursor.LineUnderCursor)    # selects whole line
        mem_cur.select(QTextCursor.WordUnderCursor)     # selects just one word
                                                        # chr_cur made selection by setting anchor and pos

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
            size = block_size
            if self.baseAddress < size:
                size = self.baseAddress
            self.grab_data(val=self.baseAddress-size, size=size)
      

class MyThread(QThread):
    timing_signal = Signal(bool) 

    def __init__(self, mem):
        super().__init__()
        mem.kill_signal.connect(self.end)    
        self.sem = QSemaphore() 

    def run(self):
        while True:
            if self.sem.tryAcquire(1, 1000): # try to acquire and wait 1s to try to acquire
                break
            self.timing_signal.emit(True)

    def end(self, b):
        self.sem.release()
        
