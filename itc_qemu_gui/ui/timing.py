# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'timing.ui'
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


class Ui_timing(object):
    def setupUi(self, timing):
        if not timing.objectName():
            timing.setObjectName(u"timing")
        timing.resize(800, 600)
        self.verticalLayout_2 = QVBoxLayout(timing)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_rate = QLabel(timing)
        self.label_rate.setObjectName(u"label_rate")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_rate.setFont(font)
        self.label_rate.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_rate)

        self.spin_rate = QSpinBox(timing)
        self.spin_rate.setObjectName(u"spin_rate")
        self.spin_rate.setMinimum(1)
        self.spin_rate.setMaximum(1000)
        self.spin_rate.setValue(10)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.spin_rate)


        self.horizontalLayout.addLayout(self.formLayout)

        self.line = QFrame(timing)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_limit = QLabel(timing)
        self.label_limit.setObjectName(u"label_limit")
        self.label_limit.setFont(font)
        self.label_limit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_limit)

        self.spin_limit = QSpinBox(timing)
        self.spin_limit.setObjectName(u"spin_limit")
        self.spin_limit.setMinimum(1)
        self.spin_limit.setMaximum(1000)
        self.spin_limit.setValue(10)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.spin_limit)


        self.horizontalLayout.addLayout(self.formLayout_3)

        self.line_2 = QFrame(timing)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_2)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_window = QLabel(timing)
        self.label_window.setObjectName(u"label_window")
        self.label_window.setFont(font)
        self.label_window.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_window)

        self.spin_window = QSpinBox(timing)
        self.spin_window.setObjectName(u"spin_window")
        self.spin_window.setMinimum(1)
        self.spin_window.setMaximum(1000)
        self.spin_window.setValue(10)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.spin_window)


        self.horizontalLayout.addLayout(self.formLayout_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.horizontalLayout.setStretch(5, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.figure = QHBoxLayout()
        self.figure.setObjectName(u"figure")

        self.horizontalLayout_2.addLayout(self.figure)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(timing)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.out_min = QLabel(self.groupBox)
        self.out_min.setObjectName(u"out_min")
        self.out_min.setMinimumSize(QSize(50, 0))

        self.gridLayout.addWidget(self.out_min, 0, 1, 1, 1)

        self.out_max = QLabel(self.groupBox)
        self.out_max.setObjectName(u"out_max")
        self.out_max.setMinimumSize(QSize(50, 0))

        self.gridLayout.addWidget(self.out_max, 1, 1, 1, 1)

        self.label_min = QLabel(self.groupBox)
        self.label_min.setObjectName(u"label_min")
        self.label_min.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_min, 0, 0, 1, 1)

        self.label_max = QLabel(self.groupBox)
        self.label_max.setObjectName(u"label_max")
        self.label_max.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_max, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(timing)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.out_window_min = QLabel(self.groupBox_2)
        self.out_window_min.setObjectName(u"out_window_min")
        self.out_window_min.setMinimumSize(QSize(50, 0))

        self.gridLayout_2.addWidget(self.out_window_min, 0, 1, 1, 1)

        self.out_window_mean = QLabel(self.groupBox_2)
        self.out_window_mean.setObjectName(u"out_window_mean")
        self.out_window_mean.setMinimumSize(QSize(50, 0))

        self.gridLayout_2.addWidget(self.out_window_mean, 4, 1, 1, 1)

        self.label_window_median = QLabel(self.groupBox_2)
        self.label_window_median.setObjectName(u"label_window_median")
        self.label_window_median.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_window_median, 5, 0, 1, 1)

        self.label_window_min = QLabel(self.groupBox_2)
        self.label_window_min.setObjectName(u"label_window_min")
        self.label_window_min.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_window_min, 0, 0, 1, 1)

        self.label_window_max = QLabel(self.groupBox_2)
        self.label_window_max.setObjectName(u"label_window_max")
        self.label_window_max.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_window_max, 2, 0, 1, 1)

        self.label_window_mean = QLabel(self.groupBox_2)
        self.label_window_mean.setObjectName(u"label_window_mean")
        self.label_window_mean.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_window_mean, 4, 0, 1, 1)

        self.out_window_max = QLabel(self.groupBox_2)
        self.out_window_max.setObjectName(u"out_window_max")
        self.out_window_max.setMinimumSize(QSize(50, 0))

        self.gridLayout_2.addWidget(self.out_window_max, 2, 1, 1, 1)

        self.out_window_median = QLabel(self.groupBox_2)
        self.out_window_median.setObjectName(u"out_window_median")
        self.out_window_median.setMinimumSize(QSize(50, 0))

        self.gridLayout_2.addWidget(self.out_window_median, 5, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout_2.setStretch(0, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.retranslateUi(timing)

        QMetaObject.connectSlotsByName(timing)
    # setupUi

    def retranslateUi(self, timing):
        timing.setWindowTitle(QCoreApplication.translate("timing", u"Timing", None))
        self.label_rate.setText(QCoreApplication.translate("timing", u"Sample Rate (Hz):", None))
        self.label_limit.setText(QCoreApplication.translate("timing", u"Limit (s):", None))
        self.label_window.setText(QCoreApplication.translate("timing", u"Window:", None))
        self.groupBox.setTitle(QCoreApplication.translate("timing", u"Cumulative", None))
        self.out_min.setText(QCoreApplication.translate("timing", u"<font color=\"grey\">N/A<font>", None))
        self.out_max.setText(QCoreApplication.translate("timing", u"<font color=\"grey\">N/A<font>", None))
        self.label_min.setText(QCoreApplication.translate("timing", u"Min:", None))
        self.label_max.setText(QCoreApplication.translate("timing", u"Max:", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("timing", u"Window", None))
        self.out_window_min.setText(QCoreApplication.translate("timing", u"<font color=\"grey\">N/A<font>", None))
        self.out_window_mean.setText(QCoreApplication.translate("timing", u"<font color=\"grey\">N/A<font>", None))
        self.label_window_median.setText(QCoreApplication.translate("timing", u"Median:", None))
        self.label_window_min.setText(QCoreApplication.translate("timing", u"Min:", None))
        self.label_window_max.setText(QCoreApplication.translate("timing", u"Max:", None))
        self.label_window_mean.setText(QCoreApplication.translate("timing", u"Mean:", None))
        self.out_window_max.setText(QCoreApplication.translate("timing", u"<font color=\"grey\">N/A<font>", None))
        self.out_window_median.setText(QCoreApplication.translate("timing", u"<font color=\"grey\">N/A<font>", None))
    # retranslateUi

