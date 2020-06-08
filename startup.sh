#!/bin/bash

if [ ! -d "./venv" ]; then
    echo "[+] Creating virtual enviornment"
    python3 -m venv venv
fi

if [ -z $VIRTUAL_ENV ]; then
    echo "[+] Running virtual enviornment"
    source ./venv/bin/activate 
fi

installed=$(pip3 list 2>/dev/null)

for package in $(awk -F "==" '{print $1}' ./requirements.txt); do
    echo $installed | grep $package >/dev/null
    if [ $? -eq 1 ]; then
        echo "[+] Installing required package $package"
        pip3 install $(grep $package ./requirements.txt)
    fi
done

echo "[+] Running GUI"
python3 ./main.py
