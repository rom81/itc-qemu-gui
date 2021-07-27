# Copyright (C) 2009 - 2020 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
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

from PySide2 import QtCore
import threading
import socket
import json
import time

class QMP(threading.Thread, QtCore.QObject):

    stateChanged = QtCore.Signal(bool)
    pmem = QtCore.Signal(list)
    memoryMap = QtCore.Signal(list)
    timeUpdate = QtCore.Signal(tuple)
    memSizeInfo = QtCore.Signal(int)
    connectionChange = QtCore.Signal(bool)
    newData = QtCore.Signal(dict)
    timeMetric = QtCore.Signal(list)
    extraData = QtCore.Signal(dict)

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
    
        self.isValid = False
        self.sock_sem = QtCore.QSemaphore(1)

        self.banner = None

        # self.sock_connect(host, port)

        # QMP setup
        self._running = None
        self._p_mem = None
        self._time = None
        self._mem_size = None
        self._connected = False
        self._newdata = None
        self._metric = None

        self.ready = False

    def run(self):
        while self.ready:
            data = self.listen()
            if data == 'lost_conn':
                self.running = None
                break
            # Handle Async QMP Messages 
            if 'timestamp' in data:
                if data['event'] == 'STOP':
                    self.running = False
                elif data['event'] == 'RESUME': 
                    self.running = True
                elif data['event'] == 'SHUTDOWN':
                    self.sock_disconnect()
            # Handle Status Return Messages
            elif 'return' in data and 'running' in data['return'] and len(str(data['return'])) < 250:
                self.running = data['return']['running']
            elif 'return' in data and 'hash' in data['return'] and 'vals' in data['return']:
                self.p_mem = data['return']
            elif 'return' in data and type(data['return']) == list and len(data['return']) > 0 and 'name' in data['return'][0]:
                self.memorymap = data['return']
            elif 'return' in data and type(data['return']) == list and len(data['return']) == 2 and 'time_ns' in data['return'][0]:
                self.metric = data['return']
            elif 'return' in data and 'time_ns' in data['return']:
                self.time = data['return']['time_ns']
            elif 'return' in data and 'base-memory' in data['return']:
                self.mem_size = data['return']['base-memory']        
            else:
                self.extraData.emit(data)
            self.newdata = data           

    def listen(self):
        if self.isSockValid():
            total_data = bytearray() # handles large returns
            while self.connected:
                try:
                    data = self.sock.recv(4096)
                    print(data)
                except OSError:
                    return ''
                total_data.extend(data)
                if len(data) < 4095 and data[-3] == 125 and data[-2] == 13 and data[-1] == 10:
                    break
            data = total_data.decode().split('\n')[0]
            data = json.loads(data)
 
            if 'time_ns' not in str(data) and "{'return': \{\}}" not in str(data):
                self.responses.append(data)
            # {'return': {'status': 'running', 'singlestep': False, 'running': True}}
            if 'return' in data and 'running' in data['return'] and len(str(data)) < 250:
                self.running = data['return']['running']
                self.ready = True
            return data
        return ''


    def command(self, cmd, args=None):
        if self.isSockValid():
            qmpcmd = json.dumps({'execute': cmd})
            if args:
                qmpcmd = json.dumps({'execute': cmd, 'arguments': args})
            try:
                self.sock.sendall(qmpcmd.encode())
            except BrokenPipeError:
                print("BrokenPipeError in command()!")
                if self.isSockValid():
                    self.sock_disconnect()

    def hmp_command(self, cmd):
        if self.isSockValid():
            hmpcmd = json.dumps({'execute': 'human-monitor-command', 'arguments': {'command-line': cmd}})
            try:
                self.sock.sendall(hmpcmd.encode())
            except BrokenPipeError:
                print("BrokenPipeError in hmp_command()!")
                if self.isSockValid():
                    self.sock_disconnect()
                    return None
            time.sleep(0.05) # wait for listen to capture data and place it in responses dictionary
            data = self.responses[-1]
            return data
        return None

    def sock_disconnect(self):
        try:
            self.sock_sem.acquire()
            self.sock.close()
            self.sock = None
            self.isValid = False
            self.connected = False
            self.running = False
            self.ready = False
        except OSError as e:
            print(e)
        finally:
            self.sock_sem.release()

    def sock_connect(self, host, port):
        try:
            self.sock_sem.acquire()
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(1)
            self.sock.connect((host, port))
            self.isValid = True
            self.connected = True
            self.banner = json.loads(self.sock.recv(256))
        except (OSError, Exception) as e:
            print(e)
            self.isValid = False
            self.connected = False
            self.sock_sem.release()
            return e
        finally:
            self.sock_sem.release()

        self.command('qmp_capabilities')
        self.command('query-status')

        #if not self.isAlive():
        #    print(self.listen()) # pluck empty return object
        #    print(self.listen()) # grab running state

        while not self.ready:
            self.command('query-status')
            self.listen()

    def reconnect(self, host, port):
        self.sock_disconnect()
        self.sock_connect(host, port)

        while not self.ready:
            self.command('query-status')
            self.listen()
              
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
        #print('sent: ', value)
        #time.sleep(0.05) # fix race condition
        self._running = value
        self.stateChanged.emit(value)

    @property
    def p_mem(self):
        return self._p_mem

    @p_mem.setter
    def p_mem(self, value):
        self._p_mem = value
        self.pmem.emit(value)


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


    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, value):
        self._connected = value
        self.connectionChange.emit(value)


    @property
    def newdata(self):
        return self._newdata

    @newdata.setter
    def newdata(self, value):
        self._newdata = value
        self.newData.emit(value)

    
    @property
    def metric(self):
        return self._metric

    @metric.setter
    def metric(self, value):
        self._metric = value
        self.timeMetric.emit(value)
