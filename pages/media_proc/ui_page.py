# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pagenpnrLc.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractSpinBox, QApplication, QComboBox,
    QDoubleSpinBox, QGridLayout, QHBoxLayout, QLineEdit,
    QListWidget, QListWidgetItem, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QTabWidget,
    QTimeEdit, QVBoxLayout, QWidget)

class Ui_MediaProcTab(object):
    def setupUi(self, MediaProcTab):
        if not MediaProcTab.objectName():
            MediaProcTab.setObjectName(u"MediaProcTab")
        MediaProcTab.resize(603, 653)
        self.verticalLayout = QVBoxLayout(MediaProcTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.MediaProcessingChildTab = QTabWidget(MediaProcTab)
        self.MediaProcessingChildTab.setObjectName(u"MediaProcessingChildTab")
        self.MediaProcessingChildTab.setMovable(True)
        self.UpsLayout = QWidget()
        self.UpsLayout.setObjectName(u"UpsLayout")
        self.verticalLayout_4 = QVBoxLayout(self.UpsLayout)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.UpsComfyUrl = QLineEdit(self.UpsLayout)
        self.UpsComfyUrl.setObjectName(u"UpsComfyUrl")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.UpsComfyUrl.sizePolicy().hasHeightForWidth())
        self.UpsComfyUrl.setSizePolicy(sizePolicy)
        self.UpsComfyUrl.setClearButtonEnabled(True)

        self.verticalLayout_4.addWidget(self.UpsComfyUrl)

        self.UpsModel = QHBoxLayout()
        self.UpsModel.setObjectName(u"UpsModel")
        self.UpsModelDropdown = QComboBox(self.UpsLayout)
        self.UpsModelDropdown.setObjectName(u"UpsModelDropdown")
        sizePolicy.setHeightForWidth(self.UpsModelDropdown.sizePolicy().hasHeightForWidth())
        self.UpsModelDropdown.setSizePolicy(sizePolicy)
        self.UpsModelDropdown.setFrame(True)

        self.UpsModel.addWidget(self.UpsModelDropdown)

        self.UpsRefreshModel = QPushButton(self.UpsLayout)
        self.UpsRefreshModel.setObjectName(u"UpsRefreshModel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.UpsRefreshModel.sizePolicy().hasHeightForWidth())
        self.UpsRefreshModel.setSizePolicy(sizePolicy1)

        self.UpsModel.addWidget(self.UpsRefreshModel)


        self.verticalLayout_4.addLayout(self.UpsModel)

        self.UpsImg = QHBoxLayout()
        self.UpsImg.setObjectName(u"UpsImg")
        self.UpsChooseImagePath = QPushButton(self.UpsLayout)
        self.UpsChooseImagePath.setObjectName(u"UpsChooseImagePath")
        sizePolicy1.setHeightForWidth(self.UpsChooseImagePath.sizePolicy().hasHeightForWidth())
        self.UpsChooseImagePath.setSizePolicy(sizePolicy1)

        self.UpsImg.addWidget(self.UpsChooseImagePath)

        self.UpsImagePath = QLineEdit(self.UpsLayout)
        self.UpsImagePath.setObjectName(u"UpsImagePath")
        sizePolicy.setHeightForWidth(self.UpsImagePath.sizePolicy().hasHeightForWidth())
        self.UpsImagePath.setSizePolicy(sizePolicy)
        self.UpsImagePath.setClearButtonEnabled(True)

        self.UpsImg.addWidget(self.UpsImagePath)

        self.UpsRecursive = QPushButton(self.UpsLayout)
        self.UpsRecursive.setObjectName(u"UpsRecursive")
        self.UpsRecursive.setCheckable(True)

        self.UpsImg.addWidget(self.UpsRecursive)


        self.verticalLayout_4.addLayout(self.UpsImg)

        self.UpsSaves = QHBoxLayout()
        self.UpsSaves.setObjectName(u"UpsSaves")
        self.UpsSavePathOpen = QPushButton(self.UpsLayout)
        self.UpsSavePathOpen.setObjectName(u"UpsSavePathOpen")

        self.UpsSaves.addWidget(self.UpsSavePathOpen)

        self.UpsSavePath = QLineEdit(self.UpsLayout)
        self.UpsSavePath.setObjectName(u"UpsSavePath")
        self.UpsSavePath.setClearButtonEnabled(True)

        self.UpsSaves.addWidget(self.UpsSavePath)


        self.verticalLayout_4.addLayout(self.UpsSaves)

        self.UpsOptions = QGridLayout()
        self.UpsOptions.setObjectName(u"UpsOptions")
        self.UpsHeightThresholdSpin = QSpinBox(self.UpsLayout)
        self.UpsHeightThresholdSpin.setObjectName(u"UpsHeightThresholdSpin")
        sizePolicy.setHeightForWidth(self.UpsHeightThresholdSpin.sizePolicy().hasHeightForWidth())
        self.UpsHeightThresholdSpin.setSizePolicy(sizePolicy)
        self.UpsHeightThresholdSpin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.UpsHeightThresholdSpin.setMaximum(3000)
        self.UpsHeightThresholdSpin.setValue(1500)

        self.UpsOptions.addWidget(self.UpsHeightThresholdSpin, 0, 0, 1, 1)

        self.UpsJPGThresholdSpin = QSpinBox(self.UpsLayout)
        self.UpsJPGThresholdSpin.setObjectName(u"UpsJPGThresholdSpin")
        sizePolicy.setHeightForWidth(self.UpsJPGThresholdSpin.sizePolicy().hasHeightForWidth())
        self.UpsJPGThresholdSpin.setSizePolicy(sizePolicy)
        self.UpsJPGThresholdSpin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.UpsJPGThresholdSpin.setMaximum(3000)
        self.UpsJPGThresholdSpin.setValue(500)

        self.UpsOptions.addWidget(self.UpsJPGThresholdSpin, 1, 0, 1, 1)

        self.UpsWidthThresholdSpin = QSpinBox(self.UpsLayout)
        self.UpsWidthThresholdSpin.setObjectName(u"UpsWidthThresholdSpin")
        sizePolicy.setHeightForWidth(self.UpsWidthThresholdSpin.sizePolicy().hasHeightForWidth())
        self.UpsWidthThresholdSpin.setSizePolicy(sizePolicy)
        self.UpsWidthThresholdSpin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.UpsWidthThresholdSpin.setMaximum(3000)
        self.UpsWidthThresholdSpin.setValue(1500)

        self.UpsOptions.addWidget(self.UpsWidthThresholdSpin, 0, 1, 1, 1)

        self.UpsDownscaleSpin = QDoubleSpinBox(self.UpsLayout)
        self.UpsDownscaleSpin.setObjectName(u"UpsDownscaleSpin")
        sizePolicy1.setHeightForWidth(self.UpsDownscaleSpin.sizePolicy().hasHeightForWidth())
        self.UpsDownscaleSpin.setSizePolicy(sizePolicy1)
        self.UpsDownscaleSpin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.UpsDownscaleSpin.setMinimum(0.010000000000000)
        self.UpsDownscaleSpin.setMaximum(1.000000000000000)
        self.UpsDownscaleSpin.setSingleStep(0.010000000000000)
        self.UpsDownscaleSpin.setValue(1.000000000000000)

        self.UpsOptions.addWidget(self.UpsDownscaleSpin, 1, 1, 1, 1)


        self.verticalLayout_4.addLayout(self.UpsOptions)

        self.UpsProgress = QProgressBar(self.UpsLayout)
        self.UpsProgress.setObjectName(u"UpsProgress")
        self.UpsProgress.setValue(0)
        self.UpsProgress.setTextVisible(False)

        self.verticalLayout_4.addWidget(self.UpsProgress)

        self.UpsBtns = QHBoxLayout()
        self.UpsBtns.setObjectName(u"UpsBtns")
        self.UpsRun = QPushButton(self.UpsLayout)
        self.UpsRun.setObjectName(u"UpsRun")
        sizePolicy1.setHeightForWidth(self.UpsRun.sizePolicy().hasHeightForWidth())
        self.UpsRun.setSizePolicy(sizePolicy1)

        self.UpsBtns.addWidget(self.UpsRun)

        self.UpsListImg = QPushButton(self.UpsLayout)
        self.UpsListImg.setObjectName(u"UpsListImg")

        self.UpsBtns.addWidget(self.UpsListImg)

        self.UpsStop = QPushButton(self.UpsLayout)
        self.UpsStop.setObjectName(u"UpsStop")
        self.UpsStop.setEnabled(False)

        self.UpsBtns.addWidget(self.UpsStop)


        self.verticalLayout_4.addLayout(self.UpsBtns)

        self.UpsList = QListWidget(self.UpsLayout)
        self.UpsList.setObjectName(u"UpsList")
        self.UpsList.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.UpsList.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.UpsList.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.UpsList)

        self.UpsSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.UpsSpacer)

        self.MediaProcessingChildTab.addTab(self.UpsLayout, "")
        self.VidTrimLayout = QWidget()
        self.VidTrimLayout.setObjectName(u"VidTrimLayout")
        self.verticalLayout_7 = QVBoxLayout(self.VidTrimLayout)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.VidTrimInputs = QHBoxLayout()
        self.VidTrimInputs.setObjectName(u"VidTrimInputs")
        self.VidTrimInputOpen = QPushButton(self.VidTrimLayout)
        self.VidTrimInputOpen.setObjectName(u"VidTrimInputOpen")

        self.VidTrimInputs.addWidget(self.VidTrimInputOpen)

        self.VidTrimInputPath = QLineEdit(self.VidTrimLayout)
        self.VidTrimInputPath.setObjectName(u"VidTrimInputPath")
        self.VidTrimInputPath.setClearButtonEnabled(True)

        self.VidTrimInputs.addWidget(self.VidTrimInputPath)

        self.VidTrimInputPlay = QPushButton(self.VidTrimLayout)
        self.VidTrimInputPlay.setObjectName(u"VidTrimInputPlay")

        self.VidTrimInputs.addWidget(self.VidTrimInputPlay)


        self.verticalLayout_7.addLayout(self.VidTrimInputs)

        self.VidTrimOutputs = QHBoxLayout()
        self.VidTrimOutputs.setObjectName(u"VidTrimOutputs")
        self.VidTrimOutputOpen = QPushButton(self.VidTrimLayout)
        self.VidTrimOutputOpen.setObjectName(u"VidTrimOutputOpen")

        self.VidTrimOutputs.addWidget(self.VidTrimOutputOpen)

        self.VidTrimOutputPath = QLineEdit(self.VidTrimLayout)
        self.VidTrimOutputPath.setObjectName(u"VidTrimOutputPath")
        self.VidTrimOutputPath.setReadOnly(True)

        self.VidTrimOutputs.addWidget(self.VidTrimOutputPath)


        self.verticalLayout_7.addLayout(self.VidTrimOutputs)

        self.VidTrimOptions = QHBoxLayout()
        self.VidTrimOptions.setObjectName(u"VidTrimOptions")
        self.VidTrimMode = QComboBox(self.VidTrimLayout)
        self.VidTrimMode.addItem("")
        self.VidTrimMode.addItem("")
        self.VidTrimMode.setObjectName(u"VidTrimMode")

        self.VidTrimOptions.addWidget(self.VidTrimMode)

        self.VidTrimTime = QTimeEdit(self.VidTrimLayout)
        self.VidTrimTime.setObjectName(u"VidTrimTime")
        self.VidTrimTime.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.VidTrimOptions.addWidget(self.VidTrimTime)


        self.verticalLayout_7.addLayout(self.VidTrimOptions)

        self.VidTrimRun = QPushButton(self.VidTrimLayout)
        self.VidTrimRun.setObjectName(u"VidTrimRun")

        self.verticalLayout_7.addWidget(self.VidTrimRun)

        self.VidTrimSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.VidTrimSpacer)

        self.MediaProcessingChildTab.addTab(self.VidTrimLayout, "")

        self.verticalLayout.addWidget(self.MediaProcessingChildTab)


        self.retranslateUi(MediaProcTab)

        self.MediaProcessingChildTab.setCurrentIndex(0)
        self.UpsModelDropdown.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MediaProcTab)
    # setupUi

    def retranslateUi(self, MediaProcTab):
        MediaProcTab.setWindowTitle(QCoreApplication.translate("MediaProcTab", u"Form", None))
        self.UpsComfyUrl.setText(QCoreApplication.translate("MediaProcTab", u"http://127.0.0.1:8188", None))
        self.UpsModelDropdown.setCurrentText("")
        self.UpsModelDropdown.setPlaceholderText(QCoreApplication.translate("MediaProcTab", u"\u9700\u8981\u5237\u65b0", None))
        self.UpsRefreshModel.setText(QCoreApplication.translate("MediaProcTab", u"\u5237\u65b0", None))
        self.UpsChooseImagePath.setText(QCoreApplication.translate("MediaProcTab", u"\u6253\u5f00", None))
        self.UpsImagePath.setPlaceholderText(QCoreApplication.translate("MediaProcTab", u"\u4ece\u6b64\u5904\u5f00\u59cb\u67e5\u627e\u56fe\u50cf", None))
        self.UpsRecursive.setText(QCoreApplication.translate("MediaProcTab", u"\u9012\u5f52\u67e5\u627e", None))
        self.UpsSavePathOpen.setText(QCoreApplication.translate("MediaProcTab", u"\u6253\u5f00", None))
        self.UpsSavePath.setPlaceholderText(QCoreApplication.translate("MediaProcTab", u"\u5c06\u56fe\u50cf\u4fdd\u5b58\u5230\u6b64\u5904", None))
        self.UpsHeightThresholdSpin.setSuffix(QCoreApplication.translate("MediaProcTab", u" \u50cf\u7d20", None))
        self.UpsHeightThresholdSpin.setPrefix(QCoreApplication.translate("MediaProcTab", u"\u9ad8\u5ea6\u9608\u503c\uff1a", None))
        self.UpsJPGThresholdSpin.setSuffix(QCoreApplication.translate("MediaProcTab", u" KB", None))
        self.UpsJPGThresholdSpin.setPrefix(QCoreApplication.translate("MediaProcTab", u"\u5927\u5c0f\u9608\u503c\uff1a", None))
        self.UpsWidthThresholdSpin.setSuffix(QCoreApplication.translate("MediaProcTab", u" \u50cf\u7d20", None))
        self.UpsWidthThresholdSpin.setPrefix(QCoreApplication.translate("MediaProcTab", u"\u5bbd\u5ea6\u9608\u503c\uff1a", None))
        self.UpsDownscaleSpin.setPrefix(QCoreApplication.translate("MediaProcTab", u"\u56fe\u50cf\u7f29\u653e\u4e3a\uff1a", None))
        self.UpsDownscaleSpin.setSuffix(QCoreApplication.translate("MediaProcTab", u" \u500d", None))
        self.UpsRun.setText(QCoreApplication.translate("MediaProcTab", u"\u8fd0\u884c", None))
        self.UpsListImg.setText(QCoreApplication.translate("MediaProcTab", u"\u67e5\u627e\u56fe\u50cf", None))
        self.UpsStop.setText(QCoreApplication.translate("MediaProcTab", u"\u7ec8\u6b62", None))
        self.MediaProcessingChildTab.setTabText(self.MediaProcessingChildTab.indexOf(self.UpsLayout), QCoreApplication.translate("MediaProcTab", u"ComfyUI \u56fe\u50cf\u653e\u5927", None))
#if QT_CONFIG(tooltip)
        self.MediaProcessingChildTab.setTabToolTip(self.MediaProcessingChildTab.indexOf(self.UpsLayout), QCoreApplication.translate("MediaProcTab", u"\u4f7f\u7528 ComfyUI API \u6279\u91cf\u653e\u5927\u56fe\u7247\n"
"\u56fe\u50cf\u8def\u5f84\u524d\u7684 T \u4ee3\u8868\u8fd9\u4e2a\u56fe\u7247\u5305\u542b\u900f\u660e\u901a\u9053\uff0cL \u4ee3\u8868\u8fd9\u4e2a\u56fe\u7247\u7684\u957f\u5bbd\u6bd4\u6709\u4e9b\u5947\u602a\uff0c\u53ef\u80fd\u662f\u957f\u622a\u56fe\u6216\u5168\u666f\u56fe", None))
#endif // QT_CONFIG(tooltip)
        self.VidTrimInputOpen.setText(QCoreApplication.translate("MediaProcTab", u"\u6253\u5f00", None))
        self.VidTrimInputPath.setPlaceholderText(QCoreApplication.translate("MediaProcTab", u"\u8981\u526a\u5207\u7684\u89c6\u9891\u8def\u5f84", None))
        self.VidTrimInputPlay.setText(QCoreApplication.translate("MediaProcTab", u"\u64ad\u653e", None))
        self.VidTrimOutputOpen.setText(QCoreApplication.translate("MediaProcTab", u"\u6253\u5f00", None))
        self.VidTrimOutputPath.setPlaceholderText(QCoreApplication.translate("MediaProcTab", u"\u8f93\u51fa\u89c6\u9891\u8def\u5f84\uff08\u7559\u7a7a\u4ee5\u4fdd\u5b58\u5230\u8f93\u5165\u6587\u4ef6\u5939\uff09", None))
        self.VidTrimMode.setItemText(0, QCoreApplication.translate("MediaProcTab", u"\u622a\u6b62\u4e8e", None))
        self.VidTrimMode.setItemText(1, QCoreApplication.translate("MediaProcTab", u"\u5f00\u59cb\u4e8e", None))

        self.VidTrimTime.setDisplayFormat(QCoreApplication.translate("MediaProcTab", u"HH:mm:ss.zzz", None))
        self.VidTrimRun.setText(QCoreApplication.translate("MediaProcTab", u"\u8fd0\u884c", None))
        self.MediaProcessingChildTab.setTabText(self.MediaProcessingChildTab.indexOf(self.VidTrimLayout), QCoreApplication.translate("MediaProcTab", u"\u89c6\u9891\u526a\u5207", None))
#if QT_CONFIG(tooltip)
        self.MediaProcessingChildTab.setTabToolTip(self.MediaProcessingChildTab.indexOf(self.VidTrimLayout), QCoreApplication.translate("MediaProcTab", u"\u4e22\u5f03\u4e00\u4e2a\u89c6\u9891\u524d\u6216\u540e\u4e00\u5b9a\u65f6\u95f4\u7684\u90e8\u5206\uff0c\u4e0d\u635f\u5931\u753b\u8d28\n"
"\u901a\u5e38\u7528\u4e8e\u4e00\u4e9b\u88ab\u586b\u5145\u4e86\u65e0\u5173\u5185\u5bb9\u7684\u89c6\u9891\uff0c\u6bd4\u5982B\u7ad9\u7684\u8d44\u6e90", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

