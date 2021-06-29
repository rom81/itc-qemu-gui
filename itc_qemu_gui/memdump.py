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

import math
import os.path
from random import randint
from enum import Enum

from PySide2.QtWidgets import QWidget, QFileDialog
from PySide2.QtGui import QIcon, QTextCursor, QTextCharFormat, QFont
from PySide2.QtCore import Qt, Signal, QThread, QSemaphore

from itc_qemu_gui.common import RESOURCE_ROOT
from itc_qemu_gui.constants import constants
from itc_qemu_gui.ui.memdump import Ui_memdump

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

class MemoryDumpWindow(QWidget):

    kill_signal = Signal(bool)

    def __init__(self, qmp, base=0, max=constants['block_size'], parent=None):
        super().__init__(parent)
       
        print("base = ", hex(base), " max = ", hex(max)) 
        self.flag = False
        self.threshold = 2048 # number of resident bytes

        self.qmp = qmp
        self.init_ui()

        self.baseAddress = base
        #self.maxAddress = self.baseAddress
        self.maxAddress = max
 
        print("self.baseAddress = ", hex(self.baseAddress), " self.maxAddress = ", hex(self.maxAddress)) 
        self.delta = 4 # adds a small buffer area for scrolling action to happen

        self.sem = QSemaphore(1) # semaphore for controlling access to the enabling / disabling of the scroll listening
        self.pos = self.ui.out_char.verticalScrollBar().value()

        self.highlight_sem = QSemaphore(1) # semaphore for controlling access to highlighting state
        self.is_highlighted = False
        self.highlight_addr = 0

        self.endian = Endian.little
        self.endian_sem = QSemaphore(1)

        self.hash = randint(0, 0xfffffffffffffff)

        icon = QIcon(os.path.join(RESOURCE_ROOT, 'nasa.png'))
        self.setWindowIcon(icon)

        self.max_size = 0xfffffffffffffff

        self.qmp.pmem.connect(self.update_text)
        self.grab_data(val=self.baseAddress, size=min(max, constants['block_size'] + base)-self.baseAddress)

        self.t = MyThread(self)
        self.t.timing_signal.connect(lambda:self.grab_data(val=self.baseAddress, size=self.maxAddress-self.baseAddress, grouping=self.ui.combo_grouping.currentText(), refresh=True))
        self.qmp.stateChanged.connect(self.t.halt)
        self.t.running = self.qmp.running
        self.t.start()

    def init_ui(self):   
        self.ui = Ui_memdump()
        self.ui.setupUi(self)

        self.ui.btn_search.clicked.connect(lambda:self.find(self.ui.le_address.text(), constants['block_size']))
        self.ui.btn_refresh.clicked.connect(lambda:self.grab_data(val=self.ui.le_address.text(), size=self.ui.le_size.text(), grouping=self.ui.combo_grouping.currentText(), refresh=True))
        self.ui.btn_save.clicked.connect(lambda: self.save_to_file())
        self.disable_save(self.qmp.running)
        self.qmp.stateChanged.connect(self.disable_save)
        self.ui.btn_autorefresh.stateChanged.connect(self.auto_refresh_check)
        
        self.ui.out_address.setCurrentFont(QFont('Courier New'))
        self.ui.out_address.setGeometry(0,0,150,500)
        self.ui.out_memory.setCurrentFont(QFont('Courier New'))
        self.ui.out_memory.setGeometry(0,0,600,500)
        self.ui.out_char.setCurrentFont(QFont('Courier New'))
        self.ui.out_char.setGeometry(0,0,400,500)

        self.ui.out_memory.verticalScrollBar().valueChanged.connect(self.ui.out_address.verticalScrollBar().setValue) #synchronizes addresses's scroll bar to mem_display's 
        self.ui.out_address.verticalScrollBar().valueChanged.connect(self.ui.out_memory.verticalScrollBar().setValue) #synchronizes mem_display's scroll to addresses's, allowing for searching for addresses to scrol mem_display to the desired point 
        self.ui.out_char.verticalScrollBar().valueChanged.connect(self.ui.out_memory.verticalScrollBar().setValue)  
        self.ui.out_memory.verticalScrollBar().valueChanged.connect(self.ui.out_char.verticalScrollBar().setValue)  

        self.ui.out_char.verticalScrollBar().valueChanged.connect(self.handle_scroll) # allows us to do scrolling

        # setting up endiannes selection buttons
        self.ui.btn_le.clicked.connect(lambda:self.change_endian(Endian.little))
        self.ui.btn_be.clicked.connect(lambda:self.change_endian(Endian.big))

        self.ui.splitter.setSizes([100, 200, 200])

    def disable_save(self, val):
        self.ui.btn_save.setEnabled(not val)

    def save_to_file(self):
        try:
            filename = QFileDialog().getSaveFileName(self, 'Save', '.', options=QFileDialog.DontUseNativeDialog)
        except Exception as e:
            return

        if filename[0] == '':
            return

        args = {
            'val': self.baseAddress,
            'size': self.maxAddress - self.baseAddress,
            'filename': filename[0]
        }

        self.qmp.command('pmemsave', args=args)

    def auto_refresh_check(self, value):
        if self.ui.btn_autorefresh.checkState() == Qt.CheckState.Checked and not self.t.isRunning():
            self.t = MyThread(self)
            self.t.timing_signal.connect(lambda:self.grab_data(val=self.baseAddress, size=self.maxAddress-self.baseAddress, grouping=self.ui.combo_grouping.currentText(), refresh=True))
            self.t.start()
        elif self.ui.btn_autorefresh.checkState() == Qt.CheckState.Unchecked:
            self.kill_signal.emit(True)

    def closeEvent(self, event):
        self.kill_signal.emit(True)
        self.qmp.pmem.disconnect(self.update_text)
        while True:
            if self.sem.tryAcquire(1, 1):
                break
            self.sem.release(10)
        event.accept()

    def update_text(self, value):
        if not value or value['hash'] != self.hash: # semaphore must be held before entering this function
            return
        byte = value['vals']
        if self.refresh:
            self.clear_highlight()
            self.ui.out_address.clear()  # clearing to refresh data, other regions will be refilled through scrolling
            self.ui.out_memory.clear()
            self.ui.out_char.clear()
            
        s = [''] * math.ceil((len(byte) / (16))) # hex representation of memory
        addresses =  '' # addresses
        count = self.baseAddress # keeps track of each 16 addresses
        if self.pos == self.max:  # scrolling down
            count = self.maxAddress 

        self.maxAddress = max(count + (len(byte)), self.maxAddress)

        first = True
        chars = [''] * len(s) # char represenation of memory
        index = 0
        self.endian_sem.acquire()
        nums = ''
        for tup in byte:
            b = tup['val']
            if count % 16 == 0:
                if first:
                    addresses += f'0x{count:08x}' 
                    first = False
                else:
                    addresses += f'\n0x{count:08x}' 

                    index += 1
            count += 1
             
            if self.endian == Endian.big:
                if tup['ismapped']:
                    nums = f'{b:02x}' + nums
                    chars[index] += f'{char_convert(b):3}'
                else:
                    nums = '**' + nums
                    chars[index] += f'{".":3}'

            elif self.endian == Endian.little:  
                if tup['ismapped']:     
                    nums += f'{b:02x}'      
                    chars[index] = f'{char_convert(b):3}' + chars[index]
                else:
                    nums = '**' + nums
                    chars[index] = f'{".":3}' + chars[index]

            if count % self.group == 0:
                if self.endian == Endian.big:
                    s[index] += nums + ' '
                elif self.endian == Endian.little:
                     s[index] = nums + ' ' + s[index]
                nums = ''
                #print(f'"{s[index]}"')
        self.endian_sem.release()

        s = '\n'.join(s)
        chars = '\n'.join(chars)

        scroll_goto = self.pos
        
        if self.pos > self.max - self.delta:  # scrolling down
            self.ui.out_address.append(addresses)
            self.ui.out_memory.append(s)
            self.ui.out_char.append(chars)
            if self.flag:
                self.flag = False
                scroll_goto = (1 - constants['block_size'] / self.threshold) * self.max
            else:
                scroll_goto = self.max

        elif self.pos < self.min + self.delta:    # scrolling  up
            addr_cur = self.ui.out_address.textCursor()
            mem_cur = self.ui.out_memory.textCursor()
            chr_cur = self.ui.out_char.textCursor()

            addr_cur.setPosition(0)
            mem_cur.setPosition(0)
            chr_cur.setPosition(0)

            self.ui.out_address.setTextCursor(addr_cur)
            self.ui.out_memory.setTextCursor(mem_cur)
            self.ui.out_char.setTextCursor(chr_cur)

            self.ui.out_address.insertPlainText(addresses + '\n')
            self.ui.out_memory.insertPlainText(s + '\n')
            self.ui.out_char.insertPlainText(chars + '\n')
            
            if self.flag:
                self.flag = False
                scroll_goto = (constants['block_size'] / self.threshold) * self.max
            else:
                scroll_goto = self.ui.out_char.verticalScrollBar().maximum() - self.max

        else:
            self.ui.out_address.setPlainText(addresses)
            self.ui.out_memory.setPlainText(s)
            self.ui.out_char.setPlainText(chars)

        self.highlight_sem.acquire()
        if self.is_highlighted:
            self.highlight_sem.release()
            self.highlight(self.highlight_addr, self.group)
        else:
            self.highlight_sem.release()

        self.ui.out_char.verticalScrollBar().setValue(scroll_goto)
        self.ui.out_char.verticalScrollBar().valueChanged.connect(self.handle_scroll)
        self.sem.release()

    def grab_data(self, val=0, size=constants['block_size'], grouping=1, refresh=False):       
        print("in grab_data: base address = ", hex(val), " size = ", size) 
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

        if type(grouping) == str:
            try:
                grouping = int(grouping, 0)
            except:
                grouping = 1

        if grouping not in [1, 2, 4, 8]:
            grouping = 1

        if val < 0:
            val = 0
        if val >= self.max_size:
            return
        if size < 0:
            size = constants['block_size']
        if size > self.threshold:
            size = self.threshold
        

        self.sem.acquire()

        val = val - (val % 16)
        if val < self.baseAddress or refresh:
            self.baseAddress = val
        if size % 16 != 0:
            size = size + (16 - (size % 16))
        if val + size > self.max_size:
            size = self.max_size - val
        
        try:
            self.ui.out_char.verticalScrollBar().valueChanged.disconnect(self.handle_scroll)
        except:
            pass
        self.pos = self.ui.out_char.verticalScrollBar().value()
        self.max = self.ui.out_char.verticalScrollBar().maximum()
        self.min = self.ui.out_char.verticalScrollBar().minimum()
        self.group = grouping

        self.refresh = refresh
        if refresh: 
            self.maxAddress = self.baseAddress
            
            self.highlight_sem.acquire()
            if self.is_highlighted and self.highlight_addr not in range(val, val + size):
                self.is_highlighted = False
                self.pos = 0
            self.highlight_sem.release()

        args = {
                'addr': val,
                'size': size,
                'hash': self.hash,
                'grouping': 1
                }
        self.qmp.command('itc-pmem', args=args)


    def find(self, addr, size):
        try:
            addr = int(addr, 0)
        except ValueError as e:
            print(e)
            return
        if self.baseAddress <= addr and addr <= self.maxAddress:
            group = self.ui.combo_grouping.currentText()
            try:
                group = int(group, 0)
                if group not in [1, 2, 4, 8]:
                    group = 1
            except:
                group = 1
            self.highlight(addr, group)
            
        else:
            self.highlight_sem.acquire()
            self.is_highlighted = True
            self.highlight_addr = addr
            self.highlight_sem.release()
            self.grab_data(val=addr, size=size, refresh=True )


    def clear_highlight(self):
        fmt = QTextCharFormat()
        fmt.setFont('Courier New')
        # clearing past highlights
        addr_cur = self.ui.out_address.textCursor()  # getting cursors
        mem_cur = self.ui.out_memory.textCursor()
        chr_cur = self.ui.out_char.textCursor()

        addr_cur.select(QTextCursor.Document)   # selecting entire document
        mem_cur.select(QTextCursor.Document)
        chr_cur.select(QTextCursor.Document)
        
        addr_cur.setCharFormat(fmt) # adding format
        mem_cur.setCharFormat(fmt)
        chr_cur.setCharFormat(fmt)


    def highlight(self, addr, group):
        self.clear_highlight()
        
        # adding new highlights
        fmt = QTextCharFormat()
        fmt.setBackground(Qt.cyan)
        fmt.setFont('Courier New')

        addr_block = self.ui.out_address.document().findBlockByLineNumber((addr - self.baseAddress) // 16) # gets linenos 
        mem_block = self.ui.out_memory.document().findBlockByLineNumber((addr - self.baseAddress) // 16)
        chr_block = self.ui.out_char.document().findBlockByLineNumber((addr - self.baseAddress) // 16)

        addr_cur = self.ui.out_address.textCursor()  # getting cursors
        mem_cur = self.ui.out_memory.textCursor()
        chr_cur = self.ui.out_char.textCursor()

        char_offset = 0
        mem_offset = 0
        self.endian_sem.acquire()
        if self.endian == Endian.big:
            mem_offset = ((addr % 16) // group) * (2 * group + 1)
            char_offset = (addr % 16) * 3
        elif self.endian == Endian.little:
            mem_offset = (((16 / group) - 1 )* (2 * group + 1)) - ((addr % 16) // group) * (2 * group + 1)
            char_offset = (15*3) - ((addr % 16) * 3)
        self.endian_sem.release()
        addr_cur.setPosition(addr_block.position()) # getting positions
        mem_cur.setPosition(mem_block.position() + mem_offset) # gives character offset within 16 byte line
        chr_cur.setPosition(chr_block.position() + char_offset) # sets position of char

        chr_text = self.ui.out_char.toPlainText()
        if chr_text[chr_cur.position()] == '\\' and chr_cur.position() + 1 < len(chr_text) and chr_text[chr_cur.position() + 1] in ['0', 'n', 't']:
            chr_cur.setPosition(chr_cur.position() + 2, mode=QTextCursor.KeepAnchor) 
        else:
            chr_cur.setPosition(chr_cur.position() + 1, mode=QTextCursor.KeepAnchor) 


        addr_cur.select(QTextCursor.LineUnderCursor)    # selects whole line
        mem_cur.select(QTextCursor.WordUnderCursor)     # selects just one word

        addr_cur.setCharFormat(fmt) # setting format
        mem_cur.setCharFormat(fmt)
        chr_cur.setCharFormat(fmt)

        self.ui.out_address.setTextCursor(addr_cur)
        self.ui.out_memory.setTextCursor(mem_cur)
        self.ui.out_char.setTextCursor(chr_cur)
        
        self.highlight_sem.acquire()
        self.is_highlighted = True
        self.highlight_addr = addr
        self.highlight_sem.release()


    def handle_scroll(self):
        if self.baseAddress > 0 and self.ui.out_char.verticalScrollBar().value() < self.ui.out_char.verticalScrollBar().minimum() + self.delta:
            size = constants['block_size']
            if self.maxAddress - self.baseAddress >= self.threshold:
                self.flag = True
                self.grab_data(val=self.baseAddress - constants['block_size'], size=self.threshold, refresh=True, grouping=self.ui.combo_grouping.currentText())
                return
            if self.baseAddress < size:
                size = self.baseAddress
            self.grab_data(val=self.baseAddress-size, size=size, grouping=self.ui.combo_grouping.currentText())
        elif self.ui.out_char.verticalScrollBar().value() > self.ui.out_char.verticalScrollBar().maximum() - self.delta and self.maxAddress <= self.max_size:
            if self.maxAddress - self.baseAddress >= self.threshold:
                self.flag = True
                self.grab_data(val=self.baseAddress + constants['block_size'], size=self.threshold, refresh=True, grouping=self.ui.combo_grouping.currentText())
            else:
                self.grab_data(val=self.maxAddress, grouping=self.ui.combo_grouping.currentText())

    def change_endian(self, endian):
        self.endian_sem.acquire()
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
    win = MemoryDumpWindow(qmp)
    win.show()
    app.exec_()

