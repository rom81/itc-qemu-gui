# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qemu.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_qemu(object):
    def setupUi(self, qemu):
        if not qemu.objectName():
            qemu.setObjectName(u"qemu")
        qemu.resize(420, 250)
        self.action_file_exit = QAction(qemu)
        self.action_file_exit.setObjectName(u"action_file_exit")
        self.action_help_about = QAction(qemu)
        self.action_help_about.setObjectName(u"action_help_about")
        self.action_Preferences = QAction(qemu)
        self.action_Preferences.setObjectName(u"action_Preferences")
        self.action_run_play = QAction(qemu)
        self.action_run_play.setObjectName(u"action_run_play")
        self.action_run_stop = QAction(qemu)
        self.action_run_stop.setObjectName(u"action_run_stop")
        self.action_file_settings = QAction(qemu)
        self.action_file_settings.setObjectName(u"action_file_settings")
        self.action_tools_memdump = QAction(qemu)
        self.action_tools_memdump.setObjectName(u"action_tools_memdump")
        self.action_tools_memtree = QAction(qemu)
        self.action_tools_memtree.setObjectName(u"action_tools_memtree")
        self.action_tools_cpuregs = QAction(qemu)
        self.action_tools_cpuregs.setObjectName(u"action_tools_cpuregs")
        self.action_tools_asm = QAction(qemu)
        self.action_tools_asm.setObjectName(u"action_tools_asm")
        self.action_tools_logging = QAction(qemu)
        self.action_tools_logging.setObjectName(u"action_tools_logging")
        self.action_tools_timing = QAction(qemu)
        self.action_tools_timing.setObjectName(u"action_tools_timing")
        self.action_plugin_qmp = QAction(qemu)
        self.action_plugin_qmp.setObjectName(u"action_plugin_qmp")
        self.actionPlugins_2 = QAction(qemu)
        self.actionPlugins_2.setObjectName(u"actionPlugins_2")
        self.centralwidget = QWidget(qemu)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.le_qmp_ip = QLineEdit(self.groupBox)
        self.le_qmp_ip.setObjectName(u"le_qmp_ip")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_qmp_ip.sizePolicy().hasHeightForWidth())
        self.le_qmp_ip.setSizePolicy(sizePolicy)
        self.le_qmp_ip.setMinimumSize(QSize(120, 0))
        self.le_qmp_ip.setMaximumSize(QSize(120, 16777215))

        self.horizontalLayout_4.addWidget(self.le_qmp_ip)

        self.le_qmp_port = QLineEdit(self.groupBox)
        self.le_qmp_port.setObjectName(u"le_qmp_port")
        sizePolicy.setHeightForWidth(self.le_qmp_port.sizePolicy().hasHeightForWidth())
        self.le_qmp_port.setSizePolicy(sizePolicy)
        self.le_qmp_port.setMinimumSize(QSize(120, 0))
        self.le_qmp_port.setMaximumSize(QSize(120, 16777215))

        self.horizontalLayout_4.addWidget(self.le_qmp_port)

        self.btn_qmp_connect = QPushButton(self.groupBox)
        self.btn_qmp_connect.setObjectName(u"btn_qmp_connect")

        self.horizontalLayout_4.addWidget(self.btn_qmp_connect)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.horizontalLayout_4.setStretch(3, 1)

        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(16)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_logo = QLabel(self.centralwidget)
        self.label_logo.setObjectName(u"label_logo")
        self.label_logo.setMinimumSize(QSize(75, 75))

        self.horizontalLayout_2.addWidget(self.label_logo)

        self.btn_simstate = QToolButton(self.centralwidget)
        self.btn_simstate.setObjectName(u"btn_simstate")
        self.btn_simstate.setMinimumSize(QSize(50, 50))

        self.horizontalLayout_2.addWidget(self.btn_simstate)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_simstate = QLabel(self.groupBox_2)
        self.label_simstate.setObjectName(u"label_simstate")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_simstate)

        self.label_time = QLabel(self.groupBox_2)
        self.label_time.setObjectName(u"label_time")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_time)

        self.out_simstate = QLabel(self.groupBox_2)
        self.out_simstate.setObjectName(u"out_simstate")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.out_simstate)

        self.out_time = QLabel(self.groupBox_2)
        self.out_time.setObjectName(u"out_time")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.out_time)

        self.label_version = QLabel(self.groupBox_2)
        self.label_version.setObjectName(u"label_version")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_version)

        self.out_version = QLabel(self.groupBox_2)
        self.out_version.setObjectName(u"out_version")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.out_version)


        self.horizontalLayout.addLayout(self.formLayout)


        self.horizontalLayout_3.addWidget(self.groupBox_2)

        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        qemu.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(qemu)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 420, 22))
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_help = QMenu(self.menubar)
        self.menu_help.setObjectName(u"menu_help")
        self.menu_run = QMenu(self.menubar)
        self.menu_run.setObjectName(u"menu_run")
        self.menu_tools = QMenu(self.menubar)
        self.menu_tools.setObjectName(u"menu_tools")
        self.menu_plugins = QMenu(self.menubar)
        self.menu_plugins.setObjectName(u"menu_plugins")
        qemu.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(qemu)
        self.statusbar.setObjectName(u"statusbar")
        qemu.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_run.menuAction())
        self.menubar.addAction(self.menu_tools.menuAction())
        self.menubar.addAction(self.menu_plugins.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menu_file.addAction(self.action_file_settings)
        self.menu_file.addAction(self.action_file_exit)
        self.menu_help.addAction(self.action_help_about)
        self.menu_run.addAction(self.action_run_play)
        self.menu_run.addAction(self.action_run_stop)
        self.menu_tools.addAction(self.action_tools_memdump)
        self.menu_tools.addAction(self.action_tools_memtree)
        self.menu_tools.addAction(self.action_tools_cpuregs)
        self.menu_tools.addAction(self.action_tools_asm)
        self.menu_tools.addAction(self.action_tools_logging)
        self.menu_tools.addAction(self.action_tools_timing)

        self.retranslateUi(qemu)

        QMetaObject.connectSlotsByName(qemu)
    # setupUi

    def retranslateUi(self, qemu):
        qemu.setWindowTitle(QCoreApplication.translate("qemu", u"QEMU", None))
        self.action_file_exit.setText(QCoreApplication.translate("qemu", u"E&xit", None))
        self.action_help_about.setText(QCoreApplication.translate("qemu", u"&About", None))
        self.action_Preferences.setText(QCoreApplication.translate("qemu", u"&Preferences", None))
        self.action_run_play.setText(QCoreApplication.translate("qemu", u"Play", None))
        self.action_run_stop.setText(QCoreApplication.translate("qemu", u"&Stop", None))
        self.action_file_settings.setText(QCoreApplication.translate("qemu", u"&Settings", None))
        self.action_tools_memdump.setText(QCoreApplication.translate("qemu", u"Memory Dump", None))
        self.action_tools_memtree.setText(QCoreApplication.translate("qemu", u"Memory Tree", None))
        self.action_tools_cpuregs.setText(QCoreApplication.translate("qemu", u"CPU Registers", None))
        self.action_tools_asm.setText(QCoreApplication.translate("qemu", u"Assembly", None))
        self.action_tools_logging.setText(QCoreApplication.translate("qemu", u"Logging", None))
        self.action_tools_timing.setText(QCoreApplication.translate("qemu", u"Timing", None))
        self.action_plugin_qmp.setText(QCoreApplication.translate("qemu", u"QMP Debug", None))
        self.actionPlugins_2.setText(QCoreApplication.translate("qemu", u"Plugins", None))
        self.groupBox.setTitle(QCoreApplication.translate("qemu", u"QMP", None))
        self.le_qmp_ip.setPlaceholderText(QCoreApplication.translate("qemu", u"IP", None))
        self.le_qmp_port.setPlaceholderText(QCoreApplication.translate("qemu", u"Port", None))
        self.btn_qmp_connect.setText(QCoreApplication.translate("qemu", u"Connect", None))
        self.label_logo.setText("")
        self.btn_simstate.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("qemu", u"Status", None))
        self.label_simstate.setText(QCoreApplication.translate("qemu", u"State:", None))
        self.label_time.setText(QCoreApplication.translate("qemu", u"Time:", None))
        self.out_simstate.setText(QCoreApplication.translate("qemu", u"<font color=\"grey\">N/A<font>", None))
        self.out_time.setText(QCoreApplication.translate("qemu", u"<font color=\"grey\">N/A<font>", None))
        self.label_version.setText(QCoreApplication.translate("qemu", u"Version:", None))
        self.out_version.setText(QCoreApplication.translate("qemu", u"<font color=\"grey\">N/A<font>", None))
        self.menu_file.setTitle(QCoreApplication.translate("qemu", u"&File", None))
        self.menu_help.setTitle(QCoreApplication.translate("qemu", u"&Help", None))
        self.menu_run.setTitle(QCoreApplication.translate("qemu", u"&Run", None))
        self.menu_tools.setTitle(QCoreApplication.translate("qemu", u"&Tools", None))
        self.menu_plugins.setTitle(QCoreApplication.translate("qemu", u"&Plugins", None))
    # retranslateUi

