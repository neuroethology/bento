# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'animalDialog.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_AnimalDialog(object):
    def setupUi(self, AnimalDialog):
        if AnimalDialog.objectName():
            AnimalDialog.setObjectName(u"AnimalDialog")
        AnimalDialog.resize(429, 409)
        self.verticalLayout = QVBoxLayout(AnimalDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.investigatorHorizontalLayout = QHBoxLayout()
        self.investigatorHorizontalLayout.setObjectName(u"investigatorHorizontalLayout")
        self.investigatorLabel = QLabel(AnimalDialog)
        self.investigatorLabel.setObjectName(u"investigatorLabel")

        self.investigatorHorizontalLayout.addWidget(self.investigatorLabel)

        self.investigatorComboBox = QComboBox(AnimalDialog)
        self.investigatorComboBox.setObjectName(u"investigatorComboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.investigatorComboBox.sizePolicy().hasHeightForWidth())
        self.investigatorComboBox.setSizePolicy(sizePolicy)

        self.investigatorHorizontalLayout.addWidget(self.investigatorComboBox)


        self.verticalLayout.addLayout(self.investigatorHorizontalLayout)

        self.asiHorizontalLayout = QHBoxLayout()
        self.asiHorizontalLayout.setObjectName(u"asiHorizontalLayout")
        self.asiLabel = QLabel(AnimalDialog)
        self.asiLabel.setObjectName(u"asiLabel")

        self.asiHorizontalLayout.addWidget(self.asiLabel)

        self.asiLineEdit = QLineEdit(AnimalDialog)
        self.asiLineEdit.setObjectName(u"asiLineEdit")

        self.asiHorizontalLayout.addWidget(self.asiLineEdit)


        self.verticalLayout.addLayout(self.asiHorizontalLayout)

        self.dobHorizontalLayout = QHBoxLayout()
        self.dobHorizontalLayout.setObjectName(u"dobHorizontalLayout")
        self.label_4 = QLabel(AnimalDialog)
        self.label_4.setObjectName(u"label_4")

        self.dobHorizontalLayout.addWidget(self.label_4)

        self.dateEdit = QDateEdit(AnimalDialog)
        self.dateEdit.setObjectName(u"dateEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.dateEdit.sizePolicy().hasHeightForWidth())
        self.dateEdit.setSizePolicy(sizePolicy1)

        self.dobHorizontalLayout.addWidget(self.dateEdit)


        self.verticalLayout.addLayout(self.dobHorizontalLayout)

        self.sexHorizontalLayout = QHBoxLayout()
        self.sexHorizontalLayout.setObjectName(u"sexHorizontalLayout")
        self.sexLabel = QLabel(AnimalDialog)
        self.sexLabel.setObjectName(u"sexLabel")

        self.sexHorizontalLayout.addWidget(self.sexLabel)

        self.maleRadioButton = QRadioButton(AnimalDialog)
        self.maleRadioButton.setObjectName(u"maleRadioButton")
        sizePolicy1.setHeightForWidth(self.maleRadioButton.sizePolicy().hasHeightForWidth())
        self.maleRadioButton.setSizePolicy(sizePolicy1)

        self.sexHorizontalLayout.addWidget(self.maleRadioButton)

        self.femaleRadioButton = QRadioButton(AnimalDialog)
        self.femaleRadioButton.setObjectName(u"femaleRadioButton")
        sizePolicy1.setHeightForWidth(self.femaleRadioButton.sizePolicy().hasHeightForWidth())
        self.femaleRadioButton.setSizePolicy(sizePolicy1)

        self.sexHorizontalLayout.addWidget(self.femaleRadioButton)

        self.unknownRadioButton = QRadioButton(AnimalDialog)
        self.unknownRadioButton.setObjectName(u"unknownRadioButton")
        sizePolicy1.setHeightForWidth(self.unknownRadioButton.sizePolicy().hasHeightForWidth())
        self.unknownRadioButton.setSizePolicy(sizePolicy1)

        self.sexHorizontalLayout.addWidget(self.unknownRadioButton)


        self.verticalLayout.addLayout(self.sexHorizontalLayout)

        self.genotypeHorizontalLayout = QHBoxLayout()
        self.genotypeHorizontalLayout.setObjectName(u"genotypeHorizontalLayout")
        self.genotypeLabel = QLabel(AnimalDialog)
        self.genotypeLabel.setObjectName(u"genotypeLabel")

        self.genotypeHorizontalLayout.addWidget(self.genotypeLabel)

        self.genotypeLineEdit = QLineEdit(AnimalDialog)
        self.genotypeLineEdit.setObjectName(u"genotypeLineEdit")

        self.genotypeHorizontalLayout.addWidget(self.genotypeLineEdit)


        self.verticalLayout.addLayout(self.genotypeHorizontalLayout)

        self.nicknameHorizontalLayout = QHBoxLayout()
        self.nicknameHorizontalLayout.setObjectName(u"nicknameHorizontalLayout")
        self.nicknameLabel = QLabel(AnimalDialog)
        self.nicknameLabel.setObjectName(u"nicknameLabel")

        self.nicknameHorizontalLayout.addWidget(self.nicknameLabel)

        self.nicknameLineEdit = QLineEdit(AnimalDialog)
        self.nicknameLineEdit.setObjectName(u"nicknameLineEdit")

        self.nicknameHorizontalLayout.addWidget(self.nicknameLineEdit)


        self.verticalLayout.addLayout(self.nicknameHorizontalLayout)

        self.surgeryHorizontalLayout = QHBoxLayout()
        self.surgeryHorizontalLayout.setObjectName(u"surgeryHorizontalLayout")
        self.surgeryVerticalLayout = QVBoxLayout()
        self.surgeryVerticalLayout.setObjectName(u"surgeryVerticalLayout")
        self.label = QLabel(AnimalDialog)
        self.label.setObjectName(u"label")

        self.surgeryVerticalLayout.addWidget(self.label)

        self.pushButton = QPushButton(AnimalDialog)
        self.pushButton.setObjectName(u"pushButton")

        self.surgeryVerticalLayout.addWidget(self.pushButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.surgeryVerticalLayout.addItem(self.verticalSpacer)


        self.surgeryHorizontalLayout.addLayout(self.surgeryVerticalLayout)

        self.tableView = QTableView(AnimalDialog)
        self.tableView.setObjectName(u"tableView")

        self.surgeryHorizontalLayout.addWidget(self.tableView)


        self.verticalLayout.addLayout(self.surgeryHorizontalLayout)

        self.buttonBox = QDialogButtonBox(AnimalDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Apply|QDialogButtonBox.Discard|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AnimalDialog)
        self.buttonBox.accepted.connect(AnimalDialog.accept)
        self.buttonBox.rejected.connect(AnimalDialog.reject)
        self.buttonBox.clicked.connect(AnimalDialog.update)

        QMetaObject.connectSlotsByName(AnimalDialog)
    # setupUi

    def retranslateUi(self, AnimalDialog):
        AnimalDialog.setWindowTitle(QCoreApplication.translate("AnimalDialog", u"Animal", None))
        self.investigatorLabel.setText(QCoreApplication.translate("AnimalDialog", u"Investigator: ", None))
        self.asiLabel.setText(QCoreApplication.translate("AnimalDialog", u"Animal Services ID: ", None))
        self.label_4.setText(QCoreApplication.translate("AnimalDialog", u"Date of Birth: ", None))
        self.sexLabel.setText(QCoreApplication.translate("AnimalDialog", u"Sex: ", None))
        self.maleRadioButton.setText(QCoreApplication.translate("AnimalDialog", u"Male", None))
        self.femaleRadioButton.setText(QCoreApplication.translate("AnimalDialog", u"Female", None))
        self.unknownRadioButton.setText(QCoreApplication.translate("AnimalDialog", u"Unknown", None))
        self.genotypeLabel.setText(QCoreApplication.translate("AnimalDialog", u"Genotype: ", None))
        self.nicknameLabel.setText(QCoreApplication.translate("AnimalDialog", u"Nickname: ", None))
        self.label.setText(QCoreApplication.translate("AnimalDialog", u"Surgical Log: ", None))
        self.pushButton.setText(QCoreApplication.translate("AnimalDialog", u"Add ...", None))
    # retranslateUi

