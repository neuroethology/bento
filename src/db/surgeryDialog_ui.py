# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'surgeryDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_SurgeryDialog(object):
    def setupUi(self, SurgeryDialog):
        if not SurgeryDialog.objectName():
            SurgeryDialog.setObjectName(u"SurgeryDialog")
        SurgeryDialog.resize(356, 250)
        self.verticalLayout = QVBoxLayout(SurgeryDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.dateHorizontalLayout = QHBoxLayout()
        self.dateHorizontalLayout.setObjectName(u"dateHorizontalLayout")
        self.dateLabel = QLabel(SurgeryDialog)
        self.dateLabel.setObjectName(u"dateLabel")

        self.dateHorizontalLayout.addWidget(self.dateLabel)

        self.dateEdit = QDateEdit(SurgeryDialog)
        self.dateEdit.setObjectName(u"dateEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateEdit.sizePolicy().hasHeightForWidth())
        self.dateEdit.setSizePolicy(sizePolicy)

        self.dateHorizontalLayout.addWidget(self.dateEdit)


        self.verticalLayout.addLayout(self.dateHorizontalLayout)

        self.implantHorizontalLayout = QHBoxLayout()
        self.implantHorizontalLayout.setObjectName(u"implantHorizontalLayout")
        self.implantLabel = QLabel(SurgeryDialog)
        self.implantLabel.setObjectName(u"implantLabel")
        self.implantLabel.setMinimumSize(QSize(58, 0))

        self.implantHorizontalLayout.addWidget(self.implantLabel)

        self.noneImplantRadioButton = QRadioButton(SurgeryDialog)
        self.implantButtonGroup = QButtonGroup(SurgeryDialog)
        self.implantButtonGroup.setObjectName(u"implantButtonGroup")
        self.implantButtonGroup.addButton(self.noneImplantRadioButton)
        self.noneImplantRadioButton.setObjectName(u"noneImplantRadioButton")
        self.noneImplantRadioButton.setChecked(True)

        self.implantHorizontalLayout.addWidget(self.noneImplantRadioButton)

        self.leftImplantRadioButton = QRadioButton(SurgeryDialog)
        self.implantButtonGroup.addButton(self.leftImplantRadioButton)
        self.leftImplantRadioButton.setObjectName(u"leftImplantRadioButton")

        self.implantHorizontalLayout.addWidget(self.leftImplantRadioButton)

        self.rightImplantRadioButton = QRadioButton(SurgeryDialog)
        self.implantButtonGroup.addButton(self.rightImplantRadioButton)
        self.rightImplantRadioButton.setObjectName(u"rightImplantRadioButton")

        self.implantHorizontalLayout.addWidget(self.rightImplantRadioButton)

        self.bilatImplantRadioButton = QRadioButton(SurgeryDialog)
        self.implantButtonGroup.addButton(self.bilatImplantRadioButton)
        self.bilatImplantRadioButton.setObjectName(u"bilatImplantRadioButton")

        self.implantHorizontalLayout.addWidget(self.bilatImplantRadioButton)


        self.verticalLayout.addLayout(self.implantHorizontalLayout)

        self.injectionHorizontalLayout = QHBoxLayout()
        self.injectionHorizontalLayout.setObjectName(u"injectionHorizontalLayout")
        self.injectionLabel = QLabel(SurgeryDialog)
        self.injectionLabel.setObjectName(u"injectionLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.injectionLabel.sizePolicy().hasHeightForWidth())
        self.injectionLabel.setSizePolicy(sizePolicy1)
        self.injectionLabel.setMinimumSize(QSize(58, 0))

        self.injectionHorizontalLayout.addWidget(self.injectionLabel)

        self.noneInjectionRadioButton = QRadioButton(SurgeryDialog)
        self.injectionButtonGroup = QButtonGroup(SurgeryDialog)
        self.injectionButtonGroup.setObjectName(u"injectionButtonGroup")
        self.injectionButtonGroup.addButton(self.noneInjectionRadioButton)
        self.noneInjectionRadioButton.setObjectName(u"noneInjectionRadioButton")
        self.noneInjectionRadioButton.setChecked(True)

        self.injectionHorizontalLayout.addWidget(self.noneInjectionRadioButton)

        self.leftInjectionRadioButton = QRadioButton(SurgeryDialog)
        self.injectionButtonGroup.addButton(self.leftInjectionRadioButton)
        self.leftInjectionRadioButton.setObjectName(u"leftInjectionRadioButton")

        self.injectionHorizontalLayout.addWidget(self.leftInjectionRadioButton)

        self.rightInjectionRadioButton = QRadioButton(SurgeryDialog)
        self.injectionButtonGroup.addButton(self.rightInjectionRadioButton)
        self.rightInjectionRadioButton.setObjectName(u"rightInjectionRadioButton")

        self.injectionHorizontalLayout.addWidget(self.rightInjectionRadioButton)

        self.bilatInjectionRadioButton = QRadioButton(SurgeryDialog)
        self.injectionButtonGroup.addButton(self.bilatInjectionRadioButton)
        self.bilatInjectionRadioButton.setObjectName(u"bilatInjectionRadioButton")

        self.injectionHorizontalLayout.addWidget(self.bilatInjectionRadioButton)


        self.verticalLayout.addLayout(self.injectionHorizontalLayout)

        self.procedureHorizontalLayout = QHBoxLayout()
        self.procedureHorizontalLayout.setObjectName(u"procedureHorizontalLayout")
        self.procedureLabel = QLabel(SurgeryDialog)
        self.procedureLabel.setObjectName(u"procedureLabel")

        self.procedureHorizontalLayout.addWidget(self.procedureLabel)

        self.procedureLineEdit = QLineEdit(SurgeryDialog)
        self.procedureLineEdit.setObjectName(u"procedureLineEdit")

        self.procedureHorizontalLayout.addWidget(self.procedureLineEdit)


        self.verticalLayout.addLayout(self.procedureHorizontalLayout)

        self.anesthesiaHorizontalLayout = QHBoxLayout()
        self.anesthesiaHorizontalLayout.setObjectName(u"anesthesiaHorizontalLayout")
        self.anesthesiaLabel = QLabel(SurgeryDialog)
        self.anesthesiaLabel.setObjectName(u"anesthesiaLabel")

        self.anesthesiaHorizontalLayout.addWidget(self.anesthesiaLabel)

        self.anesthesiaLineEdit = QLineEdit(SurgeryDialog)
        self.anesthesiaLineEdit.setObjectName(u"anesthesiaLineEdit")

        self.anesthesiaHorizontalLayout.addWidget(self.anesthesiaLineEdit)


        self.verticalLayout.addLayout(self.anesthesiaHorizontalLayout)

        self.followUpHorizontalLayout = QHBoxLayout()
        self.followUpHorizontalLayout.setObjectName(u"followUpHorizontalLayout")
        self.followUpLabel = QLabel(SurgeryDialog)
        self.followUpLabel.setObjectName(u"followUpLabel")

        self.followUpHorizontalLayout.addWidget(self.followUpLabel)

        self.followUpLineEdit = QLineEdit(SurgeryDialog)
        self.followUpLineEdit.setObjectName(u"followUpLineEdit")

        self.followUpHorizontalLayout.addWidget(self.followUpLineEdit)


        self.verticalLayout.addLayout(self.followUpHorizontalLayout)

        self.buttonBox = QDialogButtonBox(SurgeryDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(SurgeryDialog)
        self.buttonBox.accepted.connect(SurgeryDialog.accept)
        self.buttonBox.rejected.connect(SurgeryDialog.reject)

        QMetaObject.connectSlotsByName(SurgeryDialog)
    # setupUi

    def retranslateUi(self, SurgeryDialog):
        SurgeryDialog.setWindowTitle(QCoreApplication.translate("SurgeryDialog", u"Add Surgery", None))
        self.dateLabel.setText(QCoreApplication.translate("SurgeryDialog", u"Date: ", None))
        self.dateEdit.setDisplayFormat(QCoreApplication.translate("SurgeryDialog", u"yyyy-MM-dd", None))
        self.implantLabel.setText(QCoreApplication.translate("SurgeryDialog", u"Implant: ", None))
        self.noneImplantRadioButton.setText(QCoreApplication.translate("SurgeryDialog", u"None", None))
        self.leftImplantRadioButton.setText(QCoreApplication.translate("SurgeryDialog", u"Left", None))
        self.rightImplantRadioButton.setText(QCoreApplication.translate("SurgeryDialog", u"Right", None))
        self.bilatImplantRadioButton.setText(QCoreApplication.translate("SurgeryDialog", u"Bilateral", None))
        self.injectionLabel.setText(QCoreApplication.translate("SurgeryDialog", u"Injection: ", None))
        self.noneInjectionRadioButton.setText(QCoreApplication.translate("SurgeryDialog", u"None", None))
        self.leftInjectionRadioButton.setText(QCoreApplication.translate("SurgeryDialog", u"Left", None))
        self.rightInjectionRadioButton.setText(QCoreApplication.translate("SurgeryDialog", u"Right", None))
        self.bilatInjectionRadioButton.setText(QCoreApplication.translate("SurgeryDialog", u"Bilateral", None))
        self.procedureLabel.setText(QCoreApplication.translate("SurgeryDialog", u"Procedure:", None))
        self.anesthesiaLabel.setText(QCoreApplication.translate("SurgeryDialog", u"Anesthesia: ", None))
        self.followUpLabel.setText(QCoreApplication.translate("SurgeryDialog", u"Follow up care: ", None))
    # retranslateUi

