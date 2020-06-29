#!/bin/bash

declare -A locations

locations=(
	["./modified-qemu/cpus.c"]="../qemu/cpus.c"
	["./modified-qemu/itc-added-command.h"]="../qemu/include/itc-added-command.h"
	["./modified-qemu/memory.c"]="../qemu/memory.c"
	["./modified-qemu/misc.json"]="../qemu/qapi/misc.json"
	["./modified-qemu/qmp-cmds.c"]="../qemu/monitor/qmp-cmds.c"
)

git clone https://github.com/qemu/qemu.git ../qemu

cd ../qemu/
git checkout b0ca999a43a22b38158a222233d3f5881648bb4f

cd -

for modified in "${!locations[@]}"; do	
    echo "[+] Copying $modified to ${locations[$modified]}"
    cp $modified ${locations[$modified]}
done

cd ../qemu/
./configure
make

