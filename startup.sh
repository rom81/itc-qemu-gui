#!/bin/bash

green='\033[0;32m'
yellow='\033[0;33m'
red='\033[0;31m'
off='\033[0m'

if [ ! -d "./venv" ]; then
    echo -e "${yellow}[+]${off} Creating virtual enviornment"
    python3 -m venv venv
    pip3 install wheel
fi

if [ -z $VIRTUAL_ENV ]; then
    echo -e "${yellow}[+]${off} Running virtual enviornment"
    source ./venv/bin/activate 
fi

pip3 install -e .

echo -e "${green}[+]${off} Running GUI"
itc-qemu-gui

