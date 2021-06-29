# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'memdump.ui'
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


class Ui_memdump(object):
    def setupUi(self, memdump):
        if not memdump.objectName():
            memdump.setObjectName(u"memdump")
        memdump.resize(900, 600)
        self.verticalLayout_2 = QVBoxLayout(memdump)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_address = QLabel(memdump)
        self.label_address.setObjectName(u"label_address")

        self.horizontalLayout.addWidget(self.label_address)

        self.le_address = QLineEdit(memdump)
        self.le_address.setObjectName(u"le_address")
        self.le_address.setMinimumSize(QSize(120, 0))
        self.le_address.setMaximumSize(QSize(120, 16777215))

        self.horizontalLayout.addWidget(self.le_address)

        self.label_size = QLabel(memdump)
        self.label_size.setObjectName(u"label_size")

        self.horizontalLayout.addWidget(self.label_size)

        self.le_size = QLineEdit(memdump)
        self.le_size.setObjectName(u"le_size")
        self.le_size.setMinimumSize(QSize(120, 0))
        self.le_size.setMaximumSize(QSize(120, 16777215))

        self.horizontalLayout.addWidget(self.le_size)

        self.label_grouping = QLabel(memdump)
        self.label_grouping.setObjectName(u"label_grouping")

        self.horizontalLayout.addWidget(self.label_grouping)

        self.combo_grouping = QComboBox(memdump)
        self.combo_grouping.addItem("")
        self.combo_grouping.addItem("")
        self.combo_grouping.addItem("")
        self.combo_grouping.addItem("")
        self.combo_grouping.setObjectName(u"combo_grouping")

        self.horizontalLayout.addWidget(self.combo_grouping)

        self.btn_search = QPushButton(memdump)
        self.btn_search.setObjectName(u"btn_search")

        self.horizontalLayout.addWidget(self.btn_search)

        self.btn_refresh = QPushButton(memdump)
        self.btn_refresh.setObjectName(u"btn_refresh")

        self.horizontalLayout.addWidget(self.btn_refresh)

        self.btn_save = QPushButton(memdump)
        self.btn_save.setObjectName(u"btn_save")

        self.horizontalLayout.addWidget(self.btn_save)

        self.btn_autorefresh = QCheckBox(memdump)
        self.btn_autorefresh.setObjectName(u"btn_autorefresh")

        self.horizontalLayout.addWidget(self.btn_autorefresh)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.splitter = QSplitter(memdump)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.out_address = QTextEdit(self.splitter)
        self.out_address.setObjectName(u"out_address")
        self.out_address.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.out_address.setLineWrapMode(QTextEdit.NoWrap)
        self.out_address.setReadOnly(True)
        self.splitter.addWidget(self.out_address)
        self.out_memory = QTextEdit(self.splitter)
        self.out_memory.setObjectName(u"out_memory")
        self.out_memory.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.out_memory.setLineWrapMode(QTextEdit.NoWrap)
        self.out_memory.setReadOnly(True)
        self.splitter.addWidget(self.out_memory)
        self.out_char = QTextEdit(self.splitter)
        self.out_char.setObjectName(u"out_char")
        self.out_char.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.out_char.setLineWrapMode(QTextEdit.NoWrap)
        self.out_char.setReadOnly(True)
        self.splitter.addWidget(self.out_char)

        self.horizontalLayout_2.addWidget(self.splitter)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(memdump)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.btn_be = QRadioButton(self.groupBox)
        self.btn_be.setObjectName(u"btn_be")

        self.verticalLayout_3.addWidget(self.btn_be)

        self.btn_le = QRadioButton(self.groupBox)
        self.btn_le.setObjectName(u"btn_le")

        self.verticalLayout_3.addWidget(self.btn_le)


        self.verticalLayout.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.retranslateUi(memdump)

        QMetaObject.connectSlotsByName(memdump)
    # setupUi

    def retranslateUi(self, memdump):
        memdump.setWindowTitle(QCoreApplication.translate("memdump", u"Memory", None))
        self.label_address.setText(QCoreApplication.translate("memdump", u"Address:", None))
        self.label_size.setText(QCoreApplication.translate("memdump", u"Size:", None))
        self.label_grouping.setText(QCoreApplication.translate("memdump", u"Grouping:", None))
        self.combo_grouping.setItemText(0, QCoreApplication.translate("memdump", u"1", None))
        self.combo_grouping.setItemText(1, QCoreApplication.translate("memdump", u"2", None))
        self.combo_grouping.setItemText(2, QCoreApplication.translate("memdump", u"4", None))
        self.combo_grouping.setItemText(3, QCoreApplication.translate("memdump", u"8", None))

        self.btn_search.setText(QCoreApplication.translate("memdump", u"Search", None))
        self.btn_refresh.setText(QCoreApplication.translate("memdump", u"Refresh", None))
        self.btn_save.setText(QCoreApplication.translate("memdump", u"Save", None))
        self.btn_autorefresh.setText(QCoreApplication.translate("memdump", u"Auto Refresh", None))
        self.groupBox.setTitle(QCoreApplication.translate("memdump", u"Endian", None))
        self.btn_be.setText(QCoreApplication.translate("memdump", u"Big", None))
        self.btn_le.setText(QCoreApplication.translate("memdump", u"Little", None))
    # retranslateUi

