# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pageNlwPtc.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_FileMgrTab(object):
    def setupUi(self, FileMgrTab):
        if not FileMgrTab.objectName():
            FileMgrTab.setObjectName(u"FileMgrTab")
        FileMgrTab.resize(725, 666)
        self.verticalLayout = QVBoxLayout(FileMgrTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.FileMgrChildTab = QTabWidget(FileMgrTab)
        self.FileMgrChildTab.setObjectName(u"FileMgrChildTab")
        self.FileMgrChildTab.setMovable(True)
        self.FlattenLayoyt = QWidget()
        self.FlattenLayoyt.setObjectName(u"FlattenLayoyt")
        self.verticalLayout_13 = QVBoxLayout(self.FlattenLayoyt)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.FlattenDir = QHBoxLayout()
        self.FlattenDir.setObjectName(u"FlattenDir")
        self.FlattenDirOpen = QPushButton(self.FlattenLayoyt)
        self.FlattenDirOpen.setObjectName(u"FlattenDirOpen")

        self.FlattenDir.addWidget(self.FlattenDirOpen)

        self.FlattenDirInput = QLineEdit(self.FlattenLayoyt)
        self.FlattenDirInput.setObjectName(u"FlattenDirInput")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FlattenDirInput.sizePolicy().hasHeightForWidth())
        self.FlattenDirInput.setSizePolicy(sizePolicy)
        self.FlattenDirInput.setClearButtonEnabled(True)

        self.FlattenDir.addWidget(self.FlattenDirInput)


        self.verticalLayout_13.addLayout(self.FlattenDir)

        self.FlattenBtns = QHBoxLayout()
        self.FlattenBtns.setObjectName(u"FlattenBtns")
        self.FlattenRun = QPushButton(self.FlattenLayoyt)
        self.FlattenRun.setObjectName(u"FlattenRun")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.FlattenRun.sizePolicy().hasHeightForWidth())
        self.FlattenRun.setSizePolicy(sizePolicy1)

        self.FlattenBtns.addWidget(self.FlattenRun)

        self.FlattenStop = QPushButton(self.FlattenLayoyt)
        self.FlattenStop.setObjectName(u"FlattenStop")
        self.FlattenStop.setEnabled(False)

        self.FlattenBtns.addWidget(self.FlattenStop)


        self.verticalLayout_13.addLayout(self.FlattenBtns)

        self.FlattenSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_13.addItem(self.FlattenSpacer)

        self.FileMgrChildTab.addTab(self.FlattenLayoyt, "")
        self.NewFlattenLayout = QWidget()
        self.NewFlattenLayout.setObjectName(u"NewFlattenLayout")
        self.verticalLayout_17 = QVBoxLayout(self.NewFlattenLayout)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.NewFlattenDir = QHBoxLayout()
        self.NewFlattenDir.setObjectName(u"NewFlattenDir")
        self.NewFlattenDirOpen = QPushButton(self.NewFlattenLayout)
        self.NewFlattenDirOpen.setObjectName(u"NewFlattenDirOpen")

        self.NewFlattenDir.addWidget(self.NewFlattenDirOpen)

        self.NewFlattenDirInput = QLineEdit(self.NewFlattenLayout)
        self.NewFlattenDirInput.setObjectName(u"NewFlattenDirInput")
        self.NewFlattenDirInput.setClearButtonEnabled(True)

        self.NewFlattenDir.addWidget(self.NewFlattenDirInput)


        self.verticalLayout_17.addLayout(self.NewFlattenDir)

        self.NewFlattenProgress = QProgressBar(self.NewFlattenLayout)
        self.NewFlattenProgress.setObjectName(u"NewFlattenProgress")
        self.NewFlattenProgress.setValue(0)
        self.NewFlattenProgress.setTextVisible(False)

        self.verticalLayout_17.addWidget(self.NewFlattenProgress)

        self.NewFlattenBtns = QHBoxLayout()
        self.NewFlattenBtns.setObjectName(u"NewFlattenBtns")
        self.NewFlattenRun = QPushButton(self.NewFlattenLayout)
        self.NewFlattenRun.setObjectName(u"NewFlattenRun")

        self.NewFlattenBtns.addWidget(self.NewFlattenRun)

        self.NewFlattenStop = QPushButton(self.NewFlattenLayout)
        self.NewFlattenStop.setObjectName(u"NewFlattenStop")
        self.NewFlattenStop.setEnabled(False)

        self.NewFlattenBtns.addWidget(self.NewFlattenStop)


        self.verticalLayout_17.addLayout(self.NewFlattenBtns)

        self.NewFlattenSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_17.addItem(self.NewFlattenSpacer)

        self.FileMgrChildTab.addTab(self.NewFlattenLayout, "")

        self.verticalLayout.addWidget(self.FileMgrChildTab)


        self.retranslateUi(FileMgrTab)

        self.FileMgrChildTab.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(FileMgrTab)
    # setupUi

    def retranslateUi(self, FileMgrTab):
        FileMgrTab.setWindowTitle(QCoreApplication.translate("FileMgrTab", u"Form", None))
        self.FlattenDirOpen.setText(QCoreApplication.translate("FileMgrTab", u"\u6253\u5f00", None))
        self.FlattenDirInput.setPlaceholderText(QCoreApplication.translate("FileMgrTab", u"\u4ece\u6b64\u5904\u5f00\u59cb\u67e5\u627e\u6587\u4ef6\u5939", None))
        self.FlattenRun.setText(QCoreApplication.translate("FileMgrTab", u"\u8fd0\u884c", None))
        self.FlattenStop.setText(QCoreApplication.translate("FileMgrTab", u"\u7ec8\u6b62", None))
        self.FileMgrChildTab.setTabText(self.FileMgrChildTab.indexOf(self.FlattenLayoyt), QCoreApplication.translate("FileMgrTab", u"\u5c55\u5e73", None))
#if QT_CONFIG(tooltip)
        self.FileMgrChildTab.setTabToolTip(self.FileMgrChildTab.indexOf(self.FlattenLayoyt), QCoreApplication.translate("FileMgrTab", u"\u5982\u679c\u4e00\u4e2a\u6587\u4ef6\u5939\u53ea\u6709\u4e00\u4e2a\u6587\u4ef6\uff0c\u90a3\u4e48\u628a\u8fd9\u4e2a\u6587\u4ef6\u79fb\u52a8\u5230\u5176\u7236\u7ea7\u6587\u4ef6\u5939\uff0c\u5e76\u91cd\u547d\u540d\u4e3a\u6e90\u6587\u4ef6\u5939\u7684\u540d\u79f0\uff0c\u91cd\u590d\u8fd0\u884c\u76f4\u5230\u6ca1\u6709\u53ef\u5904\u7406\u7684\u6587\u4ef6", None))
#endif // QT_CONFIG(tooltip)
        self.NewFlattenDirOpen.setText(QCoreApplication.translate("FileMgrTab", u"\u6253\u5f00", None))
        self.NewFlattenDirInput.setPlaceholderText(QCoreApplication.translate("FileMgrTab", u"\u4ece\u6b64\u5904\u5f00\u59cb\u67e5\u627e\u6587\u4ef6\u5939", None))
        self.NewFlattenRun.setText(QCoreApplication.translate("FileMgrTab", u"\u8fd0\u884c", None))
        self.NewFlattenStop.setText(QCoreApplication.translate("FileMgrTab", u"\u7ec8\u6b62", None))
        self.FileMgrChildTab.setTabText(self.FileMgrChildTab.indexOf(self.NewFlattenLayout), QCoreApplication.translate("FileMgrTab", u"\u5c55\u5e73\uff08\u65b0\uff09", None))
#if QT_CONFIG(tooltip)
        self.FileMgrChildTab.setTabToolTip(self.FileMgrChildTab.indexOf(self.NewFlattenLayout), QCoreApplication.translate("FileMgrTab", u"\u57fa\u4e8e\u6811\u7684\u65b0\u5c55\u5e73\u65b9\u5f0f\uff0c\u4ee5\u5185\u5b58\u5360\u7528\u4e3a\u4ee3\u4ef7\uff0c\u63d0\u9ad8\u5c55\u5e73\u901f\u5ea6", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

