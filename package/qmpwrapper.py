from PySide2 import QtCore
import threading
import socket
import json

class QMP(threading.Thread, QtCore.QObject):

    stateChanged = QtCore.Signal(bool)
    emptyReturn = QtCore.Signal(bool)

    def __init__(self, host, port):

        QtCore.QObject.__init__(self)
        threading.Thread.__init__(self)
        
        # Kill thread when parent dies
        self.daemon = True 

        # Socket creation
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        # QMP setup
        self.command('qmp_capabilities')
        self.listen() # pluck empty return object
        self.command('query-status')
        self._running = None
        self._empty_return = None
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

    def listen(self):
        data = self.sock.recv(512).decode().split('\n')[0]
        data = json.loads(data)
        return data

    def command(self, cmd, args=None):
        qmpcmd = json.dumps({'execute': cmd})
        if args:
            qmpcmd = json.dumps({'execute': cmd, 'arguments': args})
        self.sock.sendall(qmpcmd.encode())


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
