# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'memtree.ui'
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


class Ui_memtree(object):
    def setupUi(self, memtree):
        if not memtree.objectName():
            memtree.setObjectName(u"memtree")
        memtree.resize(480, 320)
        memtree.setMinimumSize(QSize(480, 200))
        self.verticalLayout = QVBoxLayout(memtree)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_refresh = QPushButton(memtree)
        self.btn_refresh.setObjectName(u"btn_refresh")

        self.horizontalLayout.addWidget(self.btn_refresh)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tree_memory = QTreeWidget(memtree)
        self.tree_memory.setObjectName(u"tree_memory")
        self.tree_memory.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tree_memory.header().setMinimumSectionSize(150)
        self.tree_memory.header().setDefaultSectionSize(150)
        self.tree_memory.header().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.tree_memory)


        self.retranslateUi(memtree)

        QMetaObject.connectSlotsByName(memtree)
    # setupUi

    def retranslateUi(self, memtree):
        memtree.setWindowTitle(QCoreApplication.translate("memtree", u"Memory Tree", None))
        self.btn_refresh.setText(QCoreApplication.translate("memtree", u"Refresh", None))
        ___qtreewidgetitem = self.tree_memory.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("memtree", u"End Address", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("memtree", u"Start Address", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("memtree", u"Memory Region", None));
    # retranslateUi

