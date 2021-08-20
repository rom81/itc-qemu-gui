# Copyright (C) 2009 - 2020 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
#
# This software is provided "as is" without any warranty of any, kind either express, implied, or statutory, including, but not
# limited to, any warranty that the software will conform to, specifications any implied warranties of merchantability, fitness
# for a particular purpose, and freedom from infringement, and any warranty that the documentation will conform to the program, or
# any warranty that the software will be error free.
#
# In no event shall NASA be liable for any damages, including, but not limited to direct, indirect, special or consequential damages,
# arising out of, resulting from, or in any way connected with the software or its documentation.  Whether or not based upon warranty,
#
# contract, tort or otherwise, and whether or not loss was sustained from, or arose out of the results of, or use of, the software,
# documentation or services provided hereunder
#
# ITC Team
# NASA IV&V
# ivv-itc@lists.nasa.gov

import itc_qemu_gui
import setuptools

setuptools.setup(
    name="itc_qemu_gui",
    version=itc_qemu_gui.__version__,
    description="ITC QEMU GUI",
    author="ITC",
    author_email="ivv-itc@lists.nasa.gov",
    url="https://jstarbuild.ivv.nasa.gov/itc/qemu/itc-qemu-gui",
    packages=setuptools.find_packages(),
    package_data={
        "itc_qemu_gui": [
            "icons/*",
            "plugins/*.yapsy-plugin"
        ],
    },
    setup_requires=['wheel'],
    entry_points={
        "gui_scripts": [
            "itc-qemu-gui = itc_qemu_gui.app:run",
        ]
    },
    install_requires=[
        "wheel",
        "pyside2 == 5.14.2.1",
        "yapsy == 1.12.2",
        "pygdbmi == 0.9.0.3",
        "matplotlib == 3.2.2",
        "dataclasses == 0.6"
    ],
    python_requires=">=3.4",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Qt",
        "Topic :: System :: Emulators"
    ]
)

