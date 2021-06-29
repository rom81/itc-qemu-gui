# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'logging.ui'
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


class Ui_logging(object):
    def setupUi(self, logging):
        if not logging.objectName():
            logging.setObjectName(u"logging")
        logging.resize(800, 800)
        logging.setMinimumSize(QSize(600, 200))
        self.verticalLayout_4 = QVBoxLayout(logging)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.le_logfile = QLineEdit(logging)
        self.le_logfile.setObjectName(u"le_logfile")
        self.le_logfile.setReadOnly(True)

        self.horizontalLayout_4.addWidget(self.le_logfile)

        self.btn_logfile = QPushButton(logging)
        self.btn_logfile.setObjectName(u"btn_logfile")
        self.btn_logfile.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_4.addWidget(self.btn_logfile)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)

        self.btn_start = QPushButton(logging)
        self.btn_start.setObjectName(u"btn_start")

        self.horizontalLayout_5.addWidget(self.btn_start)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.splitter_outlog = QSplitter(logging)
        self.splitter_outlog.setObjectName(u"splitter_outlog")
        self.splitter_outlog.setOrientation(Qt.Horizontal)
        self.splitter_outlog.setChildrenCollapsible(False)
        self.splitter_logitems = QSplitter(self.splitter_outlog)
        self.splitter_logitems.setObjectName(u"splitter_logitems")
        self.splitter_logitems.setOrientation(Qt.Vertical)
        self.splitter_logitems.setChildrenCollapsible(False)
        self.groupBox = QGroupBox(self.splitter_logitems)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.le_search = QLineEdit(self.groupBox)
        self.le_search.setObjectName(u"le_search")
        self.le_search.setMinimumSize(QSize(100, 0))
        self.le_search.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.le_search)

        self.btn_search = QPushButton(self.groupBox)
        self.btn_search.setObjectName(u"btn_search")
        self.btn_search.setMaximumSize(QSize(80, 16777215))
        self.btn_search.setIconSize(QSize(16, 16))

        self.horizontalLayout.addWidget(self.btn_search)


        self.horizontalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btn_expand = QPushButton(self.groupBox)
        self.btn_expand.setObjectName(u"btn_expand")
        self.btn_expand.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_2.addWidget(self.btn_expand)

        self.btn_collapse = QPushButton(self.groupBox)
        self.btn_collapse.setObjectName(u"btn_collapse")
        self.btn_collapse.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_2.addWidget(self.btn_collapse)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.tree_tevents = QTreeWidget(self.groupBox)
        self.tree_tevents.setObjectName(u"tree_tevents")
        self.tree_tevents.setMinimumSize(QSize(150, 0))
        self.tree_tevents.setHeaderHidden(True)

        self.verticalLayout_2.addWidget(self.tree_tevents)

        self.splitter_logitems.addWidget(self.groupBox)
        self.groupBox_2 = QGroupBox(self.splitter_logitems)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea = QScrollArea(self.groupBox_2)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(125, 0))
        self.scrollArea.setWidgetResizable(True)
        self.scroll_contents = QWidget()
        self.scroll_contents.setObjectName(u"scroll_contents")
        self.scroll_contents.setGeometry(QRect(0, 0, 405, 179))
        self.verticalLayout = QVBoxLayout(self.scroll_contents)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea.setWidget(self.scroll_contents)

        self.verticalLayout_3.addWidget(self.scrollArea)

        self.splitter_logitems.addWidget(self.groupBox_2)
        self.splitter_outlog.addWidget(self.splitter_logitems)
        self.out_log = QPlainTextEdit(self.splitter_outlog)
        self.out_log.setObjectName(u"out_log")
        font = QFont()
        font.setFamily(u"Monospace")
        self.out_log.setFont(font)
        self.out_log.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.out_log.setReadOnly(True)
        self.out_log.setMaximumBlockCount(1000)
        self.out_log.setCenterOnScroll(True)
        self.splitter_outlog.addWidget(self.out_log)

        self.verticalLayout_4.addWidget(self.splitter_outlog)

        self.verticalLayout_4.setStretch(1, 1)

        self.retranslateUi(logging)

        QMetaObject.connectSlotsByName(logging)
    # setupUi

    def retranslateUi(self, logging):
        logging.setWindowTitle(QCoreApplication.translate("logging", u"Logging", None))
        self.le_logfile.setPlaceholderText(QCoreApplication.translate("logging", u"Log File", None))
        self.btn_logfile.setText(QCoreApplication.translate("logging", u"...", None))
        self.btn_start.setText(QCoreApplication.translate("logging", u"Start", None))
        self.groupBox.setTitle(QCoreApplication.translate("logging", u"Trace Events:", None))
        self.btn_search.setText(QCoreApplication.translate("logging", u"Search", None))
        self.btn_expand.setText(QCoreApplication.translate("logging", u"\u25bc", None))
        self.btn_collapse.setText(QCoreApplication.translate("logging", u"\u25b2", None))
        ___qtreewidgetitem = self.tree_tevents.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("logging", u"Trace Events", None));
        self.groupBox_2.setTitle(QCoreApplication.translate("logging", u"Log Masks:", None))
    # retranslateUi

