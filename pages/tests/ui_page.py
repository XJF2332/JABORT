# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pageDOPYtJ.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QHBoxLayout, QLineEdit,
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QVBoxLayout, QWidget)

class Ui_TestTab(object):
    def setupUi(self, TestTab):
        if not TestTab.objectName():
            TestTab.setObjectName(u"TestTab")
        self.verticalLayout = QVBoxLayout(TestTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.TestChildTab = QTabWidget(TestTab)
        self.TestChildTab.setObjectName(u"TestChildTab")
        self.TestChildTab.setMovable(True)
        self.Seq = QWidget()
        self.Seq.setObjectName(u"Seq")
        self.verticalLayout_12 = QVBoxLayout(self.Seq)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.SeqItemAmount = QSpinBox(self.Seq)
        self.SeqItemAmount.setObjectName(u"SeqItemAmount")
        self.SeqItemAmount.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.SeqItemAmount.setMinimum(1)
        self.SeqItemAmount.setMaximum(500)

        self.verticalLayout_12.addWidget(self.SeqItemAmount)

        self.SeqPaths = QHBoxLayout()
        self.SeqPaths.setObjectName(u"SeqPaths")
        self.SeqPathOpen = QPushButton(self.Seq)
        self.SeqPathOpen.setObjectName(u"SeqPathOpen")

        self.SeqPaths.addWidget(self.SeqPathOpen)

        self.SeqPathInput = QLineEdit(self.Seq)
        self.SeqPathInput.setObjectName(u"SeqPathInput")
        self.SeqPathInput.setClearButtonEnabled(True)

        self.SeqPaths.addWidget(self.SeqPathInput)


        self.verticalLayout_12.addLayout(self.SeqPaths)

        self.SeqProgress = QProgressBar(self.Seq)
        self.SeqProgress.setObjectName(u"SeqProgress")
        self.SeqProgress.setValue(0)
        self.SeqProgress.setTextVisible(False)

        self.verticalLayout_12.addWidget(self.SeqProgress)

        self.SeqBtns = QHBoxLayout()
        self.SeqBtns.setObjectName(u"SeqBtns")
        self.SeqStart = QPushButton(self.Seq)
        self.SeqStart.setObjectName(u"SeqStart")

        self.SeqBtns.addWidget(self.SeqStart)

        self.SeqStop = QPushButton(self.Seq)
        self.SeqStop.setObjectName(u"SeqStop")
        self.SeqStop.setEnabled(False)

        self.SeqBtns.addWidget(self.SeqStop)


        self.verticalLayout_12.addLayout(self.SeqBtns)

        self.SeqSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_12.addItem(self.SeqSpacer)

        self.TestChildTab.addTab(self.Seq, "")
        self.IconLayout = QWidget()
        self.IconLayout.setObjectName(u"IconLayout")
        self.verticalLayout_16 = QVBoxLayout(self.IconLayout)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.IconOutputs = QHBoxLayout()
        self.IconOutputs.setObjectName(u"IconOutputs")
        self.IconOutputOpen = QPushButton(self.IconLayout)
        self.IconOutputOpen.setObjectName(u"IconOutputOpen")

        self.IconOutputs.addWidget(self.IconOutputOpen)

        self.IconOutputPath = QLineEdit(self.IconLayout)
        self.IconOutputPath.setObjectName(u"IconOutputPath")

        self.IconOutputs.addWidget(self.IconOutputPath)


        self.verticalLayout_16.addLayout(self.IconOutputs)

        self.IconExport = QPushButton(self.IconLayout)
        self.IconExport.setObjectName(u"IconExport")

        self.verticalLayout_16.addWidget(self.IconExport)

        self.IconSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_16.addItem(self.IconSpacer)

        self.TestChildTab.addTab(self.IconLayout, "")

        self.verticalLayout.addWidget(self.TestChildTab)


        self.retranslateUi(TestTab)

        self.TestChildTab.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(TestTab)
    # setupUi

    def retranslateUi(self, TestTab):
        TestTab.setWindowTitle(QCoreApplication.translate("TestTab", u"TestsTab", None))
        self.SeqItemAmount.setSuffix(QCoreApplication.translate("TestTab", u" \u5f20\u56fe\u7247", None))
        self.SeqItemAmount.setPrefix(QCoreApplication.translate("TestTab", u"\u751f\u6210 ", None))
        self.SeqPathOpen.setText(QCoreApplication.translate("TestTab", u"\u6253\u5f00", None))
        self.SeqPathInput.setPlaceholderText(QCoreApplication.translate("TestTab", u"\u5728\u6b64\u76ee\u5f55\u4e0b\u751f\u6210", None))
        self.SeqStart.setText(QCoreApplication.translate("TestTab", u"\u5f00\u59cb", None))
        self.SeqStop.setText(QCoreApplication.translate("TestTab", u"\u7ec8\u6b62", None))
        self.TestChildTab.setTabText(self.TestChildTab.indexOf(self.Seq), QCoreApplication.translate("TestTab", u"\u751f\u6210\u56fe\u50cf\u5e8f\u5217", None))
        self.IconOutputOpen.setText(QCoreApplication.translate("TestTab", u"\u6253\u5f00", None))
        self.IconOutputPath.setPlaceholderText(QCoreApplication.translate("TestTab", u"\u5bfc\u51fa\u5230\u6b64\u5904", None))
        self.IconExport.setText(QCoreApplication.translate("TestTab", u"\u5bfc\u51fa", None))
        self.TestChildTab.setTabText(self.TestChildTab.indexOf(self.IconLayout), QCoreApplication.translate("TestTab", u"Qt\u5185\u7f6e\u56fe\u6807", None))
    # retranslateUi

