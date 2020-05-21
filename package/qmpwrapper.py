import socket
import json

'''
wrapper for qemu qmp interface

example usage:

>>> q = QMP('127.0.0.1', 55555)
>>> q.execute('stop')
{"timestamp": {"seconds": 1590021820, "microseconds": 61949}, "event": "STOP"}
>>> q.execute('cont')
{"return": {}}
'''

class QMP:

    def __init__(self, host, port):

        # Initialize QMP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.banner = self.sock.recv(256).decode().strip()

        # Put QMP into command mode
        self.execute('qmp_capabilities')

    def execute(self, cmd):

        # Send JSON encoded command to the socket and return response
        cmdstr = json.dumps({'execute': cmd})
        self.sock.sendall(cmdstr.encode()) 
        resp = self.sock.recv(256).decode().strip()
        return resp

    stop = lambda self : self.execute('stop')
    cont = lambda self : self.execute('cont')