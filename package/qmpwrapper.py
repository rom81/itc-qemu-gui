from PySide2 import QtCore
import threading
import socket
import json
import time

class QMP(threading.Thread, QtCore.QObject):

    stateChanged = QtCore.Signal(bool)
    emptyReturn = QtCore.Signal(bool)
    memoryMap = QtCore.Signal(list)
    timeUpdate = QtCore.Signal(tuple)
    memSizeInfo = QtCore.Signal(int)

    def __init__(self):

        QtCore.QObject.__init__(self)
        threading.Thread.__init__(self)
        
        # Kill thread when parent dies
        self.daemon = True 

        # Socket creation
        self.sock = None
        self.isValid = False
        self.sock_sem = QtCore.QSemaphore(1)

        self.responses = []

        # QMP setup
        self._running = False
        self._empty_return = None
        self._time = None
        self._mem_size = None
        
    def run(self):
        while True:
            data = self.listen()
            # Handle Async QMP Messages 
            if 'timestamp' in data:
                if data['event'] == 'STOP':
                    self.running = False
                elif data['event'] == 'RESUME': 
                    self.running = True
            # Handle Status Return Messages
            elif 'return' in data and 'running' in data['return']:
                self.running = data['return']['running']
            elif 'return' in data and len(data['return']) == 0:
                self.empty_return = True
            elif 'return' in data and 'memorymap' in data['return']:
                self.memorymap = data['return']
            elif 'return' in data and 'time_ns' in data['return']:
                self.time = data['return']['time_ns']
            elif 'return' in data and 'base-memory' in data['return']:
                self.mem_size = data['return']['base-memory']


    def listen(self):
        if self.isSockValid():
            total_data = bytearray() # handles large returns
            while True:
                data = self.sock.recv(1024)
                total_data.extend(data)
                if len(data) < 1024:
                    break

            data = total_data.decode().split('\n')[0]
            data = json.loads(data)
            self.responses.append(data)
            return data
        return ''


    def command(self, cmd, args=None):
        if self.isSockValid():
            qmpcmd = json.dumps({'execute': cmd})
            if args:
                qmpcmd = json.dumps({'execute': cmd, 'arguments': args})
            self.sock.sendall(qmpcmd.encode())

    def hmp_command(self, cmd):
        if self.isSockValid():
            hmpcmd = json.dumps({'execute': 'human-monitor-command', 'arguments': {'command-line': cmd}})
            self.sock.sendall(hmpcmd.encode())
            time.sleep(0.1) # wait for listen to capture data and place it in responses dictionary
            data = self.responses.pop(-1)
            return data
        return None

    def reconnect(self, host, port):
        try:
            self.sock.close()
            self.sock_sem.acquire()
            self.isValid = False
            self.sock_sem.release()
        except:
            pass
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))

            self.sock_sem.acquire()
            self.isValid = True
            self.sock_sem.release()

            self.command('qmp_capabilities')
            self.listen() # pluck empty return object
            self.command('query-status')
        except Exception as e:
            print(e)
        
    def isSockValid(self):
        self.sock_sem.acquire()
        ret = self.isValid
        self.sock_sem.release()
        return ret

    @property
    def running(self):
        return self._running
    
    @running.setter
    def running(self, value):
        self._running = value
        self.stateChanged.emit(value)
        

    @property
    def empty_return(self):
        return self._empty_return

    @empty_return.setter
    def empty_return(self, value):
        self._empty_return = value
        self.emptyReturn.emit(value)


    @property
    def memorymap(self):
        return self._memorymap

    @memorymap.setter
    def memorymap(self, value):
        self._memorymap = value
        self.memoryMap.emit(value)


    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value
        self.timeUpdate.emit(value)


    @property
    def mem_size(self):
        return self._mem_size

    @mem_size.setter
    def mem_size(self, value):
        self._mem_size = value
        self.memSizeInfo.emit(value)