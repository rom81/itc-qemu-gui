#!/bin/bash

declare -A locations

locations=(
	["./modified-qemu/cpus.c"]="../qemu/cpus.c"
	["./modified-qemu/itc-added-command.h"]="../qemu/include/itc-added-command.h"
	["./modified-qemu/memory.c"]="../qemu/memory.c"
	["./modified-qemu/misc.json"]="../qemu/qapi/misc.json"
	["./modified-qemu/qmp-cmds.c"]="../qemu/monitor/qmp-cmds.c"
	["./modified-qemu/helper.c"]="../qemu/target/i386/helper.c"
	["./modified-qemu/cpu.h"]="../qemu/target/i386/cpu.h"
	["./modified-qemu/include/hw/core/cpu.h"]="../qemu/include/hw/core/cpu.h"
	["./modified-qemu/hw/core/cpu.c"]="../qemu/hw/core/cpu.c"
	["./modified-qemu/target/i386/cpu.c"]="../qemu/target/i386/cpu.c"
)

if ! command -v git &> /dev/null
then
    echo "git not found; installing"
    sudo apt-get install git -y
fi

git clone https://github.com/qemu/qemu.git ../qemu

cd ../qemu/
git checkout b0ca999a43a22b38158a222233d3f5881648bb4f

cd -

for modified in "${!locations[@]}"; do	
    echo "[+] Copying $modified to ${locations[$modified]}"
    cp $modified ${locations[$modified]}
done

cd ../qemu/
./configure --target-list=i386-softmmu
make

