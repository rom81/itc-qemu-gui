# QEMU GUI
A GUI written in Python meant to simplify [QEMU](https://github.com/qemu/qemu) usage and to provide extra functionality for interacting with simulations. Uses [QMP](https://wiki.qemu.org/Documentation/QMP#Examples) to interact with QEMU.
## Setup
To setup and test the GUI in a Python virtual enviormnent simply run the commands below
```
python3 -m venv venv 
source ./venv/bin/activate
pip3 install -r requirements.txt
python3 main.py
```
Alternatively, you can use the provided startup script to do this automatically.
```
source ./startup.sh
```
