# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cpuregs.ui'
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


class Ui_cpuregs(object):
    def setupUi(self, cpuregs):
        if not cpuregs.objectName():
            cpuregs.setObjectName(u"cpuregs")
        cpuregs.resize(700, 400)
        self.action_file_save = QAction(cpuregs)
        self.action_file_save.setObjectName(u"action_file_save")
        self.action_options_autorefresh = QAction(cpuregs)
        self.action_options_autorefresh.setObjectName(u"action_options_autorefresh")
        self.action_options_autorefresh.setCheckable(True)
        self.action_options_autorefresh.setChecked(True)
        self.action_options_textview = QAction(cpuregs)
        self.action_options_textview.setObjectName(u"action_options_textview")
        self.action_options_textview.setCheckable(True)
        self.verticalLayout = QVBoxLayout(cpuregs)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.menubar = QMenuBar(cpuregs)
        self.menubar.setObjectName(u"menubar")
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_options = QMenu(self.menubar)
        self.menu_options.setObjectName(u"menu_options")

        self.verticalLayout.addWidget(self.menubar)

        self.stack = QStackedWidget(cpuregs)
        self.stack.setObjectName(u"stack")
        self.page_regs = QWidget()
        self.page_regs.setObjectName(u"page_regs")
        self.stack.addWidget(self.page_regs)
        self.page_text = QWidget()
        self.page_text.setObjectName(u"page_text")
        self.verticalLayout_2 = QVBoxLayout(self.page_text)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.out_cpuregs = QTextEdit(self.page_text)
        self.out_cpuregs.setObjectName(u"out_cpuregs")
        font = QFont()
        font.setFamily(u"Monospace")
        self.out_cpuregs.setFont(font)
        self.out_cpuregs.setLineWrapMode(QTextEdit.NoWrap)
        self.out_cpuregs.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.out_cpuregs)

        self.stack.addWidget(self.page_text)

        self.verticalLayout.addWidget(self.stack)


        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_options.menuAction())
        self.menu_file.addAction(self.action_file_save)
        self.menu_options.addAction(self.action_options_autorefresh)
        self.menu_options.addAction(self.action_options_textview)

        self.retranslateUi(cpuregs)

        self.stack.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(cpuregs)
    # setupUi

    def retranslateUi(self, cpuregs):
        cpuregs.setWindowTitle(QCoreApplication.translate("cpuregs", u"CPU Registers", None))
        self.action_file_save.setText(QCoreApplication.translate("cpuregs", u"&Save", None))
        self.action_options_autorefresh.setText(QCoreApplication.translate("cpuregs", u"Auto Refresh", None))
        self.action_options_textview.setText(QCoreApplication.translate("cpuregs", u"Text View", None))
        self.menu_file.setTitle(QCoreApplication.translate("cpuregs", u"&File", None))
        self.menu_options.setTitle(QCoreApplication.translate("cpuregs", u"&Options", None))
    # retranslateUi

