# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'eventTriggeredAverage.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *


class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.resize(945, 869)
        self.verticalLayoutWidget = QWidget(Frame)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(9, 9, 291, 851))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.comboBox = QComboBox(self.verticalLayoutWidget)
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout.addWidget(self.comboBox)

        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.comboBox_2 = QComboBox(self.verticalLayoutWidget)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.verticalLayout.addWidget(self.comboBox_2)

        self.radioButton = QRadioButton(self.verticalLayoutWidget)
        self.radioButton.setObjectName(u"radioButton")

        self.verticalLayout.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.verticalLayout.addWidget(self.radioButton_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_4 = QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)

        self.label_5 = QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 1, 2, 1, 1)

        self.label_6 = QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)

        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.textEdit_2 = QTextEdit(self.verticalLayoutWidget)
        self.textEdit_2.setObjectName(u"textEdit_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_2.sizePolicy().hasHeightForWidth())
        self.textEdit_2.setSizePolicy(sizePolicy)
        self.textEdit_2.setMaximumSize(QSize(40, 30))

        self.gridLayout.addWidget(self.textEdit_2, 1, 1, 1, 1)

        self.textEdit = QTextEdit(self.verticalLayoutWidget)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setMaximumSize(QSize(40, 30))

        self.gridLayout.addWidget(self.textEdit, 0, 1, 1, 1)

        self.label_7 = QLabel(self.verticalLayoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 2, 2, 1, 1)

        self.textEdit_3 = QTextEdit(self.verticalLayoutWidget)
        self.textEdit_3.setObjectName(u"textEdit_3")
        sizePolicy.setHeightForWidth(self.textEdit_3.sizePolicy().hasHeightForWidth())
        self.textEdit_3.setSizePolicy(sizePolicy)
        self.textEdit_3.setMaximumSize(QSize(40, 30))

        self.gridLayout.addWidget(self.textEdit_3, 2, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 3, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.textEdit_4 = QTextEdit(self.verticalLayoutWidget)
        self.textEdit_4.setObjectName(u"textEdit_4")
        sizePolicy.setHeightForWidth(self.textEdit_4.sizePolicy().hasHeightForWidth())
        self.textEdit_4.setSizePolicy(sizePolicy)
        self.textEdit_4.setMaximumSize(QSize(40, 30))

        self.gridLayout_2.addWidget(self.textEdit_4, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)

        self.label_8 = QLabel(self.verticalLayoutWidget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 0, 0, 1, 1)

        self.label_9 = QLabel(self.verticalLayoutWidget)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 0, 2, 1, 1)

        self.textEdit_5 = QTextEdit(self.verticalLayoutWidget)
        self.textEdit_5.setObjectName(u"textEdit_5")
        sizePolicy.setHeightForWidth(self.textEdit_5.sizePolicy().hasHeightForWidth())
        self.textEdit_5.setSizePolicy(sizePolicy)
        self.textEdit_5.setMaximumSize(QSize(40, 30))

        self.gridLayout_2.addWidget(self.textEdit_5, 1, 1, 1, 1)

        self.label_10 = QLabel(self.verticalLayoutWidget)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_2.addWidget(self.label_10, 1, 2, 1, 1)

        self.label_11 = QLabel(self.verticalLayoutWidget)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_2.addWidget(self.label_11, 1, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        self.label_12 = QLabel(self.verticalLayoutWidget)
        self.label_12.setObjectName(u"label_12")

        self.verticalLayout.addWidget(self.label_12)

        self.comboBox_3 = QComboBox(self.verticalLayoutWidget)
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.verticalLayout.addWidget(self.comboBox_3)

        self.label_13 = QLabel(self.verticalLayoutWidget)
        self.label_13.setObjectName(u"label_13")

        self.verticalLayout.addWidget(self.label_13)

        self.listView = QListView(self.verticalLayoutWidget)
        self.listView.setObjectName(u"listView")
        sizePolicy.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
        self.listView.setSizePolicy(sizePolicy)
        self.listView.setMaximumSize(QSize(16777215, 60))

        self.verticalLayout.addWidget(self.listView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_14 = QLabel(self.verticalLayoutWidget)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout.addWidget(self.label_14)

        self.checkBox = QCheckBox(self.verticalLayoutWidget)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout.addWidget(self.checkBox)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label_15 = QLabel(self.verticalLayoutWidget)
        self.label_15.setObjectName(u"label_15")

        self.verticalLayout.addWidget(self.label_15)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")

        self.verticalLayout.addLayout(self.gridLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton = QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_2.addWidget(self.pushButton_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.verticalLayoutWidget_2 = QWidget(Frame)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(316, 9, 611, 851))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(50, 0, 0, 0)

        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.label.setText(QCoreApplication.translate("Frame", u"Behavior trigger :", None))
        self.label_2.setText(QCoreApplication.translate("Frame", u"in channel :", None))
        self.radioButton.setText(QCoreApplication.translate("Frame", u"Align at start", None))
        self.radioButton_2.setText(QCoreApplication.translate("Frame", u"Align at end", None))
        self.label_4.setText(QCoreApplication.translate("Frame", u"sec before", None))
        self.label_5.setText(QCoreApplication.translate("Frame", u"sec after", None))
        self.label_6.setText(QCoreApplication.translate("Frame", u"Bin size :", None))
        self.label_3.setText(QCoreApplication.translate("Frame", u"Window : ", None))
        self.label_7.setText(QCoreApplication.translate("Frame", u"seconds", None))
        self.label_8.setText(QCoreApplication.translate("Frame", u"Discards bouts under", None))
        self.label_9.setText(QCoreApplication.translate("Frame", u"sec long", None))
        self.label_10.setText(QCoreApplication.translate("Frame", u"sec apart", None))
        self.label_11.setText(QCoreApplication.translate("Frame", u"Merge bouts under", None))
        self.label_12.setText(QCoreApplication.translate("Frame", u"Element to analyze :", None))
        self.label_13.setText(QCoreApplication.translate("Frame", u"in channels(s) :", None))
        self.label_14.setText(QCoreApplication.translate("Frame", u"Z-score traces : ", None))
        self.checkBox.setText("")
        self.label_15.setText(QCoreApplication.translate("Frame", u"Behaviors to show :", None))
        self.pushButton.setText(QCoreApplication.translate("Frame", u"PushButton", None))
        self.pushButton_2.setText(QCoreApplication.translate("Frame", u"PushButton", None))
    # retranslateUi

