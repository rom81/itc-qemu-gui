#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from package import app
import signal
import sys

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL) # fixes ctrl+c
    sys.exit(app.run()) 
