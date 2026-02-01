# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'appJSFEDf.ui'
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
    QDoubleSpinBox, QFormLayout, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPlainTextEdit, QProgressBar, QPushButton, QSizePolicy,
    QSlider, QSpacerItem, QSpinBox, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(666, 677)
        icon = QIcon()
        icon.addFile(u"Icons/SP_TitleBarMenuButton.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Form.setWindowIcon(icon)
        self.formLayout = QFormLayout(Form)
        self.formLayout.setObjectName(u"formLayout")
        self.MainPage = QTabWidget(Form)
        self.MainPage.setObjectName(u"MainPage")
        self.MainPage.setTabShape(QTabWidget.TabShape.Rounded)
        self.MainPage.setMovable(True)
        self.FileMgrLayout = QWidget()
        self.FileMgrLayout.setObjectName(u"FileMgrLayout")
        self.verticalLayout_2 = QVBoxLayout(self.FileMgrLayout)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.FileMgrChildTab = QTabWidget(self.FileMgrLayout)
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

        self.verticalLayout_2.addWidget(self.FileMgrChildTab)

        self.MainPage.addTab(self.FileMgrLayout, "")
        self.ConvertorLayout = QWidget()
        self.ConvertorLayout.setObjectName(u"ConvertorLayout")
        self.verticalLayout_3 = QVBoxLayout(self.ConvertorLayout)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.ConvertorChildTab = QTabWidget(self.ConvertorLayout)
        self.ConvertorChildTab.setObjectName(u"ConvertorChildTab")
        self.ConvertorChildTab.setMovable(True)
        self.PNG2JPG = QWidget()
        self.PNG2JPG.setObjectName(u"PNG2JPG")
        self.verticalLayout = QVBoxLayout(self.PNG2JPG)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.PNG2JPGDir = QHBoxLayout()
        self.PNG2JPGDir.setObjectName(u"PNG2JPGDir")
        self.PNG2JPGFindDir = QPushButton(self.PNG2JPG)
        self.PNG2JPGFindDir.setObjectName(u"PNG2JPGFindDir")
        sizePolicy1.setHeightForWidth(self.PNG2JPGFindDir.sizePolicy().hasHeightForWidth())
        self.PNG2JPGFindDir.setSizePolicy(sizePolicy1)

        self.PNG2JPGDir.addWidget(self.PNG2JPGFindDir)

        self.PNG2JPGDirTxt = QLineEdit(self.PNG2JPG)
        self.PNG2JPGDirTxt.setObjectName(u"PNG2JPGDirTxt")
        sizePolicy.setHeightForWidth(self.PNG2JPGDirTxt.sizePolicy().hasHeightForWidth())
        self.PNG2JPGDirTxt.setSizePolicy(sizePolicy)

        self.PNG2JPGDir.addWidget(self.PNG2JPGDirTxt)


        self.verticalLayout.addLayout(self.PNG2JPGDir)

        self.PNG2JPGOptions = QGridLayout()
        self.PNG2JPGOptions.setObjectName(u"PNG2JPGOptions")
        self.PNG2JPGDelOri = QPushButton(self.PNG2JPG)
        self.PNG2JPGDelOri.setObjectName(u"PNG2JPGDelOri")
        self.PNG2JPGDelOri.setCheckable(True)

        self.PNG2JPGOptions.addWidget(self.PNG2JPGDelOri, 0, 0, 1, 1)

        self.PNG2JPGPreverveMeta = QPushButton(self.PNG2JPG)
        self.PNG2JPGPreverveMeta.setObjectName(u"PNG2JPGPreverveMeta")
        self.PNG2JPGPreverveMeta.setCheckable(True)

        self.PNG2JPGOptions.addWidget(self.PNG2JPGPreverveMeta, 0, 2, 1, 1)

        self.PNG2JPGIngoreAlpha = QPushButton(self.PNG2JPG)
        self.PNG2JPGIngoreAlpha.setObjectName(u"PNG2JPGIngoreAlpha")
        self.PNG2JPGIngoreAlpha.setCheckable(True)

        self.PNG2JPGOptions.addWidget(self.PNG2JPGIngoreAlpha, 0, 1, 1, 1)

        self.PNG2JPGWalk = QPushButton(self.PNG2JPG)
        self.PNG2JPGWalk.setObjectName(u"PNG2JPGWalk")
        self.PNG2JPGWalk.setCheckable(True)

        self.PNG2JPGOptions.addWidget(self.PNG2JPGWalk, 1, 0, 1, 1)

        self.PNG2JPGDedup = QComboBox(self.PNG2JPG)
        self.PNG2JPGDedup.addItem("")
        self.PNG2JPGDedup.addItem("")
        self.PNG2JPGDedup.addItem("")
        self.PNG2JPGDedup.setObjectName(u"PNG2JPGDedup")

        self.PNG2JPGOptions.addWidget(self.PNG2JPGDedup, 1, 1, 1, 2)


        self.verticalLayout.addLayout(self.PNG2JPGOptions)

        self.PNG2JPGQuality = QHBoxLayout()
        self.PNG2JPGQuality.setObjectName(u"PNG2JPGQuality")
        self.PNG2JPGQualityTxt = QLabel(self.PNG2JPG)
        self.PNG2JPGQualityTxt.setObjectName(u"PNG2JPGQualityTxt")

        self.PNG2JPGQuality.addWidget(self.PNG2JPGQualityTxt)

        self.PNG2JPGQualitySlider = QSlider(self.PNG2JPG)
        self.PNG2JPGQualitySlider.setObjectName(u"PNG2JPGQualitySlider")
        self.PNG2JPGQualitySlider.setMinimum(1)
        self.PNG2JPGQualitySlider.setMaximum(100)
        self.PNG2JPGQualitySlider.setValue(80)
        self.PNG2JPGQualitySlider.setOrientation(Qt.Orientation.Horizontal)

        self.PNG2JPGQuality.addWidget(self.PNG2JPGQualitySlider)

        self.PNG2JPGQualityNum = QLabel(self.PNG2JPG)
        self.PNG2JPGQualityNum.setObjectName(u"PNG2JPGQualityNum")

        self.PNG2JPGQuality.addWidget(self.PNG2JPGQualityNum)


        self.verticalLayout.addLayout(self.PNG2JPGQuality)

        self.PNG2JPGProgress = QProgressBar(self.PNG2JPG)
        self.PNG2JPGProgress.setObjectName(u"PNG2JPGProgress")
        self.PNG2JPGProgress.setValue(0)
        self.PNG2JPGProgress.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.PNG2JPGProgress.setTextVisible(False)
        self.PNG2JPGProgress.setInvertedAppearance(False)

        self.verticalLayout.addWidget(self.PNG2JPGProgress)

        self.PNG2JPGBtns = QHBoxLayout()
        self.PNG2JPGBtns.setObjectName(u"PNG2JPGBtns")
        self.PNG2JPGRun = QPushButton(self.PNG2JPG)
        self.PNG2JPGRun.setObjectName(u"PNG2JPGRun")
        sizePolicy1.setHeightForWidth(self.PNG2JPGRun.sizePolicy().hasHeightForWidth())
        self.PNG2JPGRun.setSizePolicy(sizePolicy1)

        self.PNG2JPGBtns.addWidget(self.PNG2JPGRun)

        self.PNG2JPGStop = QPushButton(self.PNG2JPG)
        self.PNG2JPGStop.setObjectName(u"PNG2JPGStop")
        self.PNG2JPGStop.setEnabled(False)

        self.PNG2JPGBtns.addWidget(self.PNG2JPGStop)


        self.verticalLayout.addLayout(self.PNG2JPGBtns)

        self.PNG2JPGSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.PNG2JPGSpacer)

        self.ConvertorChildTab.addTab(self.PNG2JPG, "")
        self.Seq2PDF = QWidget()
        self.Seq2PDF.setObjectName(u"Seq2PDF")
        self.verticalLayout_18 = QVBoxLayout(self.Seq2PDF)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.Seq2PDFPath = QHBoxLayout()
        self.Seq2PDFPath.setObjectName(u"Seq2PDFPath")
        self.Seq2PDFPathOpen = QPushButton(self.Seq2PDF)
        self.Seq2PDFPathOpen.setObjectName(u"Seq2PDFPathOpen")

        self.Seq2PDFPath.addWidget(self.Seq2PDFPathOpen)

        self.Seq2PDFPathInput = QLineEdit(self.Seq2PDF)
        self.Seq2PDFPathInput.setObjectName(u"Seq2PDFPathInput")

        self.Seq2PDFPath.addWidget(self.Seq2PDFPathInput)


        self.verticalLayout_18.addLayout(self.Seq2PDFPath)

        self.Seq2PDOptions = QHBoxLayout()
        self.Seq2PDOptions.setObjectName(u"Seq2PDOptions")
        self.Seq2PDFDel = QPushButton(self.Seq2PDF)
        self.Seq2PDFDel.setObjectName(u"Seq2PDFDel")
        self.Seq2PDFDel.setCheckable(True)

        self.Seq2PDOptions.addWidget(self.Seq2PDFDel)

        self.Seq2PDFRecursive = QPushButton(self.Seq2PDF)
        self.Seq2PDFRecursive.setObjectName(u"Seq2PDFRecursive")
        self.Seq2PDFRecursive.setCheckable(True)

        self.Seq2PDOptions.addWidget(self.Seq2PDFRecursive)


        self.verticalLayout_18.addLayout(self.Seq2PDOptions)

        self.Seq2PDFProgress = QProgressBar(self.Seq2PDF)
        self.Seq2PDFProgress.setObjectName(u"Seq2PDFProgress")
        self.Seq2PDFProgress.setValue(0)
        self.Seq2PDFProgress.setTextVisible(False)

        self.verticalLayout_18.addWidget(self.Seq2PDFProgress)

        self.Seq2PDFBtns = QHBoxLayout()
        self.Seq2PDFBtns.setObjectName(u"Seq2PDFBtns")
        self.Seq2PDFRun = QPushButton(self.Seq2PDF)
        self.Seq2PDFRun.setObjectName(u"Seq2PDFRun")

        self.Seq2PDFBtns.addWidget(self.Seq2PDFRun)

        self.Seq2PDFStop = QPushButton(self.Seq2PDF)
        self.Seq2PDFStop.setObjectName(u"Seq2PDFStop")
        self.Seq2PDFStop.setEnabled(False)

        self.Seq2PDFBtns.addWidget(self.Seq2PDFStop)


        self.verticalLayout_18.addLayout(self.Seq2PDFBtns)

        self.Seq2PDFSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_18.addItem(self.Seq2PDFSpacer)

        self.ConvertorChildTab.addTab(self.Seq2PDF, "")

        self.verticalLayout_3.addWidget(self.ConvertorChildTab)

        self.MainPage.addTab(self.ConvertorLayout, "")
        self.ImgProcessingLayout = QWidget()
        self.ImgProcessingLayout.setObjectName(u"ImgProcessingLayout")
        self.verticalLayout_5 = QVBoxLayout(self.ImgProcessingLayout)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.ImgProcessingChildTab = QTabWidget(self.ImgProcessingLayout)
        self.ImgProcessingChildTab.setObjectName(u"ImgProcessingChildTab")
        self.ImgProcessingChildTab.setMovable(True)
        self.UpsLayout = QWidget()
        self.UpsLayout.setObjectName(u"UpsLayout")
        self.verticalLayout_4 = QVBoxLayout(self.UpsLayout)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.UpsComfyUrl = QLineEdit(self.UpsLayout)
        self.UpsComfyUrl.setObjectName(u"UpsComfyUrl")
        sizePolicy.setHeightForWidth(self.UpsComfyUrl.sizePolicy().hasHeightForWidth())
        self.UpsComfyUrl.setSizePolicy(sizePolicy)

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

        self.UpsImg.addWidget(self.UpsImagePath)

        self.UpsRecursive = QPushButton(self.UpsLayout)
        self.UpsRecursive.setObjectName(u"UpsRecursive")
        self.UpsRecursive.setCheckable(True)

        self.UpsImg.addWidget(self.UpsRecursive)


        self.verticalLayout_4.addLayout(self.UpsImg)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.UpsHeightThresholdSpin = QSpinBox(self.UpsLayout)
        self.UpsHeightThresholdSpin.setObjectName(u"UpsHeightThresholdSpin")
        sizePolicy.setHeightForWidth(self.UpsHeightThresholdSpin.sizePolicy().hasHeightForWidth())
        self.UpsHeightThresholdSpin.setSizePolicy(sizePolicy)
        self.UpsHeightThresholdSpin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.UpsHeightThresholdSpin.setMaximum(3000)
        self.UpsHeightThresholdSpin.setValue(1500)

        self.gridLayout_2.addWidget(self.UpsHeightThresholdSpin, 0, 0, 1, 1)

        self.UpsJPGThresholdSpin = QSpinBox(self.UpsLayout)
        self.UpsJPGThresholdSpin.setObjectName(u"UpsJPGThresholdSpin")
        sizePolicy.setHeightForWidth(self.UpsJPGThresholdSpin.sizePolicy().hasHeightForWidth())
        self.UpsJPGThresholdSpin.setSizePolicy(sizePolicy)
        self.UpsJPGThresholdSpin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.UpsJPGThresholdSpin.setMaximum(3000)
        self.UpsJPGThresholdSpin.setValue(500)

        self.gridLayout_2.addWidget(self.UpsJPGThresholdSpin, 1, 0, 1, 1)

        self.UpsWidthThresholdSpin = QSpinBox(self.UpsLayout)
        self.UpsWidthThresholdSpin.setObjectName(u"UpsWidthThresholdSpin")
        sizePolicy.setHeightForWidth(self.UpsWidthThresholdSpin.sizePolicy().hasHeightForWidth())
        self.UpsWidthThresholdSpin.setSizePolicy(sizePolicy)
        self.UpsWidthThresholdSpin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.UpsWidthThresholdSpin.setMaximum(3000)
        self.UpsWidthThresholdSpin.setValue(1500)

        self.gridLayout_2.addWidget(self.UpsWidthThresholdSpin, 0, 1, 1, 1)

        self.UpsCheckIntevalSpin = QDoubleSpinBox(self.UpsLayout)
        self.UpsCheckIntevalSpin.setObjectName(u"UpsCheckIntevalSpin")
        sizePolicy.setHeightForWidth(self.UpsCheckIntevalSpin.sizePolicy().hasHeightForWidth())
        self.UpsCheckIntevalSpin.setSizePolicy(sizePolicy)
        self.UpsCheckIntevalSpin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.UpsCheckIntevalSpin.setMinimum(0.100000000000000)
        self.UpsCheckIntevalSpin.setMaximum(3.000000000000000)
        self.UpsCheckIntevalSpin.setSingleStep(0.100000000000000)
        self.UpsCheckIntevalSpin.setValue(0.100000000000000)

        self.gridLayout_2.addWidget(self.UpsCheckIntevalSpin, 1, 1, 1, 1)

        self.UpsDownscaleSpin = QDoubleSpinBox(self.UpsLayout)
        self.UpsDownscaleSpin.setObjectName(u"UpsDownscaleSpin")
        sizePolicy1.setHeightForWidth(self.UpsDownscaleSpin.sizePolicy().hasHeightForWidth())
        self.UpsDownscaleSpin.setSizePolicy(sizePolicy1)
        self.UpsDownscaleSpin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.UpsDownscaleSpin.setMinimum(0.010000000000000)
        self.UpsDownscaleSpin.setMaximum(1.000000000000000)
        self.UpsDownscaleSpin.setSingleStep(0.010000000000000)
        self.UpsDownscaleSpin.setValue(1.000000000000000)

        self.gridLayout_2.addWidget(self.UpsDownscaleSpin, 2, 0, 1, 2)


        self.verticalLayout_4.addLayout(self.gridLayout_2)

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
        self.UpsList.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.UpsList.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.UpsList.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.UpsList)

        self.UpsSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.UpsSpacer)

        self.ImgProcessingChildTab.addTab(self.UpsLayout, "")

        self.verticalLayout_5.addWidget(self.ImgProcessingChildTab)

        self.MainPage.addTab(self.ImgProcessingLayout, "")
        self.TextProcessingLayout = QWidget()
        self.TextProcessingLayout.setObjectName(u"TextProcessingLayout")
        self.verticalLayout_11 = QVBoxLayout(self.TextProcessingLayout)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.TextProcChildTab = QTabWidget(self.TextProcessingLayout)
        self.TextProcChildTab.setObjectName(u"TextProcChildTab")
        self.TextProcChildTab.setMovable(True)
        self.CropText = QWidget()
        self.CropText.setObjectName(u"CropText")
        self.verticalLayout_6 = QVBoxLayout(self.CropText)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.CropTextInput = QHBoxLayout()
        self.CropTextInput.setObjectName(u"CropTextInput")
        self.CropTextInPathOpen = QPushButton(self.CropText)
        self.CropTextInPathOpen.setObjectName(u"CropTextInPathOpen")

        self.CropTextInput.addWidget(self.CropTextInPathOpen)

        self.CropTextInPath = QLineEdit(self.CropText)
        self.CropTextInPath.setObjectName(u"CropTextInPath")

        self.CropTextInput.addWidget(self.CropTextInPath)


        self.verticalLayout_6.addLayout(self.CropTextInput)

        self.CropTextRatioSpinbox = QSpinBox(self.CropText)
        self.CropTextRatioSpinbox.setObjectName(u"CropTextRatioSpinbox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.CropTextRatioSpinbox.sizePolicy().hasHeightForWidth())
        self.CropTextRatioSpinbox.setSizePolicy(sizePolicy2)
        self.CropTextRatioSpinbox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.CropTextRatioSpinbox.setMinimum(1)
        self.CropTextRatioSpinbox.setMaximum(100)

        self.verticalLayout_6.addWidget(self.CropTextRatioSpinbox)

        self.CropTextOutput = QHBoxLayout()
        self.CropTextOutput.setObjectName(u"CropTextOutput")
        self.CropTextOutPathOpen = QPushButton(self.CropText)
        self.CropTextOutPathOpen.setObjectName(u"CropTextOutPathOpen")

        self.CropTextOutput.addWidget(self.CropTextOutPathOpen)

        self.CropTextOutPath = QLineEdit(self.CropText)
        self.CropTextOutPath.setObjectName(u"CropTextOutPath")

        self.CropTextOutput.addWidget(self.CropTextOutPath)


        self.verticalLayout_6.addLayout(self.CropTextOutput)

        self.CroptextRun = QPushButton(self.CropText)
        self.CroptextRun.setObjectName(u"CroptextRun")

        self.verticalLayout_6.addWidget(self.CroptextRun)

        self.CropTextSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.CropTextSpacer)

        self.TextProcChildTab.addTab(self.CropText, "")
        self.CalSim = QWidget()
        self.CalSim.setObjectName(u"CalSim")
        self.verticalLayout_14 = QVBoxLayout(self.CalSim)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.CalSimModel = QHBoxLayout()
        self.CalSimModel.setObjectName(u"CalSimModel")
        self.CalSimModelDropdown = QComboBox(self.CalSim)
        self.CalSimModelDropdown.setObjectName(u"CalSimModelDropdown")
        sizePolicy2.setHeightForWidth(self.CalSimModelDropdown.sizePolicy().hasHeightForWidth())
        self.CalSimModelDropdown.setSizePolicy(sizePolicy2)

        self.CalSimModel.addWidget(self.CalSimModelDropdown)

        self.CalSimModelRefresh = QPushButton(self.CalSim)
        self.CalSimModelRefresh.setObjectName(u"CalSimModelRefresh")

        self.CalSimModel.addWidget(self.CalSimModelRefresh)

        self.CalSimPersistentModel = QPushButton(self.CalSim)
        self.CalSimPersistentModel.setObjectName(u"CalSimPersistentModel")
        self.CalSimPersistentModel.setCheckable(True)

        self.CalSimModel.addWidget(self.CalSimPersistentModel)


        self.verticalLayout_14.addLayout(self.CalSimModel)

        self.CalSimInput = QHBoxLayout()
        self.CalSimInput.setObjectName(u"CalSimInput")
        self.CalSimIn1 = QLineEdit(self.CalSim)
        self.CalSimIn1.setObjectName(u"CalSimIn1")

        self.CalSimInput.addWidget(self.CalSimIn1)

        self.CalSimIn2 = QLineEdit(self.CalSim)
        self.CalSimIn2.setObjectName(u"CalSimIn2")

        self.CalSimInput.addWidget(self.CalSimIn2)


        self.verticalLayout_14.addLayout(self.CalSimInput)

        self.CalSimRun = QPushButton(self.CalSim)
        self.CalSimRun.setObjectName(u"CalSimRun")

        self.verticalLayout_14.addWidget(self.CalSimRun)

        self.CalSimSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_14.addItem(self.CalSimSpacer)

        self.TextProcChildTab.addTab(self.CalSim, "")
        self.JsonSorter = QWidget()
        self.JsonSorter.setObjectName(u"JsonSorter")
        self.verticalLayout_15 = QVBoxLayout(self.JsonSorter)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.JsonSorterIn = QHBoxLayout()
        self.JsonSorterIn.setObjectName(u"JsonSorterIn")
        self.JsonSorterInOpen = QPushButton(self.JsonSorter)
        self.JsonSorterInOpen.setObjectName(u"JsonSorterInOpen")

        self.JsonSorterIn.addWidget(self.JsonSorterInOpen)

        self.JsonSorterInPath = QLineEdit(self.JsonSorter)
        self.JsonSorterInPath.setObjectName(u"JsonSorterInPath")

        self.JsonSorterIn.addWidget(self.JsonSorterInPath)


        self.verticalLayout_15.addLayout(self.JsonSorterIn)

        self.JsonSorterRun = QPushButton(self.JsonSorter)
        self.JsonSorterRun.setObjectName(u"JsonSorterRun")

        self.verticalLayout_15.addWidget(self.JsonSorterRun)

        self.JsonSorterSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_15.addItem(self.JsonSorterSpacer)

        self.TextProcChildTab.addTab(self.JsonSorter, "")

        self.verticalLayout_11.addWidget(self.TextProcChildTab)

        self.MainPage.addTab(self.TextProcessingLayout, "")
        self.TestingLayout = QWidget()
        self.TestingLayout.setObjectName(u"TestingLayout")
        self.verticalLayout_9 = QVBoxLayout(self.TestingLayout)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.TestChildTab = QTabWidget(self.TestingLayout)
        self.TestChildTab.setObjectName(u"TestChildTab")
        self.TestChildTab.setMovable(True)
        self.ImgSeqGen = QWidget()
        self.ImgSeqGen.setObjectName(u"ImgSeqGen")
        self.verticalLayout_12 = QVBoxLayout(self.ImgSeqGen)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.ImageSeqItemAmount = QSpinBox(self.ImgSeqGen)
        self.ImageSeqItemAmount.setObjectName(u"ImageSeqItemAmount")
        self.ImageSeqItemAmount.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.ImageSeqItemAmount.setMinimum(1)
        self.ImageSeqItemAmount.setMaximum(500)

        self.verticalLayout_12.addWidget(self.ImageSeqItemAmount)

        self.ImageSeqPaths = QHBoxLayout()
        self.ImageSeqPaths.setObjectName(u"ImageSeqPaths")
        self.ImageSeqPathOpen = QPushButton(self.ImgSeqGen)
        self.ImageSeqPathOpen.setObjectName(u"ImageSeqPathOpen")

        self.ImageSeqPaths.addWidget(self.ImageSeqPathOpen)

        self.ImageSeqPathInput = QLineEdit(self.ImgSeqGen)
        self.ImageSeqPathInput.setObjectName(u"ImageSeqPathInput")
        self.ImageSeqPathInput.setClearButtonEnabled(True)

        self.ImageSeqPaths.addWidget(self.ImageSeqPathInput)


        self.verticalLayout_12.addLayout(self.ImageSeqPaths)

        self.ImageSeqGenProgress = QProgressBar(self.ImgSeqGen)
        self.ImageSeqGenProgress.setObjectName(u"ImageSeqGenProgress")
        self.ImageSeqGenProgress.setValue(0)
        self.ImageSeqGenProgress.setTextVisible(False)

        self.verticalLayout_12.addWidget(self.ImageSeqGenProgress)

        self.ImageSeqGenBtns = QHBoxLayout()
        self.ImageSeqGenBtns.setObjectName(u"ImageSeqGenBtns")
        self.ImageSeqGenStart = QPushButton(self.ImgSeqGen)
        self.ImageSeqGenStart.setObjectName(u"ImageSeqGenStart")

        self.ImageSeqGenBtns.addWidget(self.ImageSeqGenStart)

        self.ImageSeqGenStop = QPushButton(self.ImgSeqGen)
        self.ImageSeqGenStop.setObjectName(u"ImageSeqGenStop")
        self.ImageSeqGenStop.setEnabled(False)

        self.ImageSeqGenBtns.addWidget(self.ImageSeqGenStop)


        self.verticalLayout_12.addLayout(self.ImageSeqGenBtns)

        self.ImageSeqGenSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_12.addItem(self.ImageSeqGenSpacer)

        self.TestChildTab.addTab(self.ImgSeqGen, "")
        self.QtIconsLayout = QWidget()
        self.QtIconsLayout.setObjectName(u"QtIconsLayout")
        self.verticalLayout_16 = QVBoxLayout(self.QtIconsLayout)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.QtIconsBtns = QHBoxLayout()
        self.QtIconsBtns.setObjectName(u"QtIconsBtns")
        self.QtIconsExport = QPushButton(self.QtIconsLayout)
        self.QtIconsExport.setObjectName(u"QtIconsExport")

        self.QtIconsBtns.addWidget(self.QtIconsExport)

        self.QtIconsShow = QPushButton(self.QtIconsLayout)
        self.QtIconsShow.setObjectName(u"QtIconsShow")

        self.QtIconsBtns.addWidget(self.QtIconsShow)


        self.verticalLayout_16.addLayout(self.QtIconsBtns)

        self.QtIconsSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_16.addItem(self.QtIconsSpacer)

        self.TestChildTab.addTab(self.QtIconsLayout, "")

        self.verticalLayout_9.addWidget(self.TestChildTab)

        self.MainPage.addTab(self.TestingLayout, "")
        self.SettingLayout = QWidget()
        self.SettingLayout.setObjectName(u"SettingLayout")
        self.verticalLayout_8 = QVBoxLayout(self.SettingLayout)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.ThemeLabel = QLabel(self.SettingLayout)
        self.ThemeLabel.setObjectName(u"ThemeLabel")

        self.verticalLayout_8.addWidget(self.ThemeLabel)

        self.ThemeChoose = QHBoxLayout()
        self.ThemeChoose.setObjectName(u"ThemeChoose")
        self.ThemeDropdown = QComboBox(self.SettingLayout)
        self.ThemeDropdown.setObjectName(u"ThemeDropdown")
        sizePolicy2.setHeightForWidth(self.ThemeDropdown.sizePolicy().hasHeightForWidth())
        self.ThemeDropdown.setSizePolicy(sizePolicy2)

        self.ThemeChoose.addWidget(self.ThemeDropdown)

        self.ThemeConfirm = QPushButton(self.SettingLayout)
        self.ThemeConfirm.setObjectName(u"ThemeConfirm")

        self.ThemeChoose.addWidget(self.ThemeConfirm)


        self.verticalLayout_8.addLayout(self.ThemeChoose)

        self.LogLabel = QLabel(self.SettingLayout)
        self.LogLabel.setObjectName(u"LogLabel")

        self.verticalLayout_8.addWidget(self.LogLabel)

        self.UniLog = QPlainTextEdit(self.SettingLayout)
        self.UniLog.setObjectName(u"UniLog")
        self.UniLog.setReadOnly(True)

        self.verticalLayout_8.addWidget(self.UniLog)

        self.SettingsSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.SettingsSpacer)

        self.MainPage.addTab(self.SettingLayout, "")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.SpanningRole, self.MainPage)


        self.retranslateUi(Form)

        self.MainPage.setCurrentIndex(0)
        self.FileMgrChildTab.setCurrentIndex(0)
        self.ConvertorChildTab.setCurrentIndex(0)
        self.PNG2JPGDedup.setCurrentIndex(2)
        self.ImgProcessingChildTab.setCurrentIndex(0)
        self.UpsModelDropdown.setCurrentIndex(-1)
        self.TextProcChildTab.setCurrentIndex(0)
        self.TestChildTab.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Toolbox", None))
        self.FlattenDirOpen.setText(QCoreApplication.translate("Form", u"\u6253\u5f00", None))
        self.FlattenDirInput.setPlaceholderText(QCoreApplication.translate("Form", u"\u4ece\u6b64\u5904\u5f00\u59cb\u67e5\u627e\u6587\u4ef6\u5939", None))
        self.FlattenRun.setText(QCoreApplication.translate("Form", u"\u8fd0\u884c", None))
        self.FlattenStop.setText(QCoreApplication.translate("Form", u"\u7ec8\u6b62", None))
        self.FileMgrChildTab.setTabText(self.FileMgrChildTab.indexOf(self.FlattenLayoyt), QCoreApplication.translate("Form", u"\u5c55\u5e73", None))
#if QT_CONFIG(tooltip)
        self.FileMgrChildTab.setTabToolTip(self.FileMgrChildTab.indexOf(self.FlattenLayoyt), QCoreApplication.translate("Form", u"\u5982\u679c\u4e00\u4e2a\u6587\u4ef6\u5939\u53ea\u6709\u4e00\u4e2a\u6587\u4ef6\uff0c\u90a3\u4e48\u628a\u8fd9\u4e2a\u6587\u4ef6\u79fb\u52a8\u5230\u5176\u7236\u7ea7\u6587\u4ef6\u5939\uff0c\u5e76\u91cd\u547d\u540d\u4e3a\u6e90\u6587\u4ef6\u5939\u7684\u540d\u79f0\uff0c\u91cd\u590d\u8fd0\u884c\u76f4\u5230\u6ca1\u6709\u53ef\u5904\u7406\u7684\u6587\u4ef6", None))
#endif // QT_CONFIG(tooltip)
        self.NewFlattenDirOpen.setText(QCoreApplication.translate("Form", u"\u6253\u5f00", None))
        self.NewFlattenDirInput.setPlaceholderText(QCoreApplication.translate("Form", u"\u4ece\u6b64\u5904\u5f00\u59cb\u67e5\u627e\u6587\u4ef6\u5939", None))
        self.NewFlattenRun.setText(QCoreApplication.translate("Form", u"\u8fd0\u884c", None))
        self.NewFlattenStop.setText(QCoreApplication.translate("Form", u"\u7ec8\u6b62", None))
        self.FileMgrChildTab.setTabText(self.FileMgrChildTab.indexOf(self.NewFlattenLayout), QCoreApplication.translate("Form", u"\u5c55\u5e73\uff08\u65b0\uff09", None))
#if QT_CONFIG(tooltip)
        self.FileMgrChildTab.setTabToolTip(self.FileMgrChildTab.indexOf(self.NewFlattenLayout), QCoreApplication.translate("Form", u"\u57fa\u4e8e\u6811\u7684\u65b0\u5c55\u5e73\u65b9\u5f0f\uff0c\u4ee5\u5185\u5b58\u5360\u7528\u4e3a\u4ee3\u4ef7\uff0c\u63d0\u9ad8\u5c55\u5e73\u901f\u5ea6", None))
#endif // QT_CONFIG(tooltip)
        self.MainPage.setTabText(self.MainPage.indexOf(self.FileMgrLayout), QCoreApplication.translate("Form", u"\u6587\u4ef6\u7ba1\u7406", None))
        self.PNG2JPGFindDir.setText(QCoreApplication.translate("Form", u"\u6253\u5f00", None))
        self.PNG2JPGDirTxt.setPlaceholderText(QCoreApplication.translate("Form", u"\u4ece\u6b64\u5904\u5f00\u59cb\u67e5\u627e\u56fe\u50cf", None))
        self.PNG2JPGDelOri.setText(QCoreApplication.translate("Form", u"\u5220\u9664\u539f\u6587\u4ef6", None))
        self.PNG2JPGPreverveMeta.setText(QCoreApplication.translate("Form", u"\u4fdd\u7559\u5143\u6570\u636e", None))
        self.PNG2JPGIngoreAlpha.setText(QCoreApplication.translate("Form", u"\u65e0\u89c6\u900f\u660e\u5ea6", None))
        self.PNG2JPGWalk.setText(QCoreApplication.translate("Form", u"\u9012\u5f52\u67e5\u627e", None))
        self.PNG2JPGDedup.setItemText(0, QCoreApplication.translate("Form", u"\u91cd\u590d\u7684\u6587\u4ef6\uff1a\u8986\u76d6", None))
        self.PNG2JPGDedup.setItemText(1, QCoreApplication.translate("Form", u"\u91cd\u590d\u7684\u6587\u4ef6\uff1a\u8df3\u8fc7", None))
        self.PNG2JPGDedup.setItemText(2, QCoreApplication.translate("Form", u"\u91cd\u590d\u7684\u6587\u4ef6\uff1a\u589e\u52a0\u5e8f\u53f7", None))

        self.PNG2JPGDedup.setPlaceholderText(QCoreApplication.translate("Form", u"\u91cd\u590d\u7684\u6587\u4ef6", None))
        self.PNG2JPGQualityTxt.setText(QCoreApplication.translate("Form", u"\u8d28\u91cf", None))
        self.PNG2JPGQualityNum.setText(QCoreApplication.translate("Form", u"80", None))
        self.PNG2JPGProgress.setFormat(QCoreApplication.translate("Form", u"%p %", None))
        self.PNG2JPGRun.setText(QCoreApplication.translate("Form", u"\u8fd0\u884c", None))
        self.PNG2JPGStop.setText(QCoreApplication.translate("Form", u"\u7ec8\u6b62", None))
        self.ConvertorChildTab.setTabText(self.ConvertorChildTab.indexOf(self.PNG2JPG), QCoreApplication.translate("Form", u"PNG \u8f6c JPG", None))
#if QT_CONFIG(tooltip)
        self.ConvertorChildTab.setTabToolTip(self.ConvertorChildTab.indexOf(self.PNG2JPG), QCoreApplication.translate("Form", u"\u6279\u91cf\u7684\u5c06 PNG \u56fe\u50cf\u8f6c\u6362\u4e3a JPG \u56fe\u50cf", None))
#endif // QT_CONFIG(tooltip)
        self.Seq2PDFPathOpen.setText(QCoreApplication.translate("Form", u"\u6253\u5f00", None))
        self.Seq2PDFPathInput.setPlaceholderText(QCoreApplication.translate("Form", u"\u4ece\u6b64\u5904\u5f00\u59cb\u67e5\u627e\u56fe\u50cf", None))
        self.Seq2PDFDel.setText(QCoreApplication.translate("Form", u"\u5220\u9664\u539f\u6587\u4ef6", None))
        self.Seq2PDFRecursive.setText(QCoreApplication.translate("Form", u"\u9012\u5f52\u67e5\u627e", None))
        self.Seq2PDFRun.setText(QCoreApplication.translate("Form", u"\u8fd0\u884c", None))
        self.Seq2PDFStop.setText(QCoreApplication.translate("Form", u"\u7ec8\u6b62", None))
        self.ConvertorChildTab.setTabText(self.ConvertorChildTab.indexOf(self.Seq2PDF), QCoreApplication.translate("Form", u"\u56fe\u50cf\u5e8f\u5217\u8f6c PDF", None))
#if QT_CONFIG(tooltip)
        self.ConvertorChildTab.setTabToolTip(self.ConvertorChildTab.indexOf(self.Seq2PDF), QCoreApplication.translate("Form", u"\u5c06\u4e00\u4e2a\u6587\u4ef6\u5939\u4e2d\u7684\u56fe\u50cf\u5e8f\u5217\u8f6c\u6362\u4e3a\u5355\u4e2a PDF \u6587\u4ef6\uff0c\u4ee5\u7236\u6587\u4ef6\u5939\u547d\u540d\uff0c\u4fdd\u5b58\u5728\u56fe\u50cf\u5e8f\u5217\u6240\u5728\u7684\u4e0a\u4e00\u7ea7\u6587\u4ef6\u5939", None))
#endif // QT_CONFIG(tooltip)
        self.MainPage.setTabText(self.MainPage.indexOf(self.ConvertorLayout), QCoreApplication.translate("Form", u"\u8f6c\u6362\u5de5\u5177", None))
        self.UpsComfyUrl.setText(QCoreApplication.translate("Form", u"http://127.0.0.1:8188", None))
        self.UpsModelDropdown.setCurrentText("")
        self.UpsModelDropdown.setPlaceholderText(QCoreApplication.translate("Form", u"\u8f93\u5165URL\u6216\u5237\u65b0\u5217\u8868", None))
        self.UpsRefreshModel.setText(QCoreApplication.translate("Form", u"\u5237\u65b0", None))
        self.UpsChooseImagePath.setText(QCoreApplication.translate("Form", u"\u6253\u5f00", None))
        self.UpsImagePath.setPlaceholderText(QCoreApplication.translate("Form", u"\u4ece\u6b64\u5904\u5f00\u59cb\u67e5\u627e\u56fe\u50cf", None))
        self.UpsRecursive.setText(QCoreApplication.translate("Form", u"\u9012\u5f52\u67e5\u627e", None))
        self.UpsHeightThresholdSpin.setSuffix(QCoreApplication.translate("Form", u" \u50cf\u7d20", None))
        self.UpsHeightThresholdSpin.setPrefix(QCoreApplication.translate("Form", u"\u9ad8\u5ea6\u9608\u503c\uff1a", None))
        self.UpsJPGThresholdSpin.setSuffix(QCoreApplication.translate("Form", u" KB", None))
        self.UpsJPGThresholdSpin.setPrefix(QCoreApplication.translate("Form", u"\u5927\u5c0f\u9608\u503c\uff1a", None))
        self.UpsWidthThresholdSpin.setSuffix(QCoreApplication.translate("Form", u" \u50cf\u7d20", None))
        self.UpsWidthThresholdSpin.setPrefix(QCoreApplication.translate("Form", u"\u5bbd\u5ea6\u9608\u503c\uff1a", None))
        self.UpsCheckIntevalSpin.setPrefix(QCoreApplication.translate("Form", u"\u6bcf ", None))
        self.UpsCheckIntevalSpin.setSuffix(QCoreApplication.translate("Form", u" \u79d2\u67e5\u8be2\u961f\u5217\u72b6\u6001", None))
        self.UpsDownscaleSpin.setPrefix(QCoreApplication.translate("Form", u"\u56fe\u50cf\u7f29\u653e\u4e3a\uff1a", None))
        self.UpsDownscaleSpin.setSuffix(QCoreApplication.translate("Form", u" \u500d", None))
        self.UpsRun.setText(QCoreApplication.translate("Form", u"\u8fd0\u884c", None))
        self.UpsListImg.setText(QCoreApplication.translate("Form", u"\u67e5\u627e\u56fe\u50cf", None))
        self.UpsStop.setText(QCoreApplication.translate("Form", u"\u7ec8\u6b62", None))
        self.ImgProcessingChildTab.setTabText(self.ImgProcessingChildTab.indexOf(self.UpsLayout), QCoreApplication.translate("Form", u"ComfyUI \u56fe\u50cf\u653e\u5927", None))
#if QT_CONFIG(tooltip)
        self.ImgProcessingChildTab.setTabToolTip(self.ImgProcessingChildTab.indexOf(self.UpsLayout), QCoreApplication.translate("Form", u"\u4f7f\u7528 ComfyUI API \u6279\u91cf\u653e\u5927\u56fe\u7247\n"
"\u56fe\u50cf\u8def\u5f84\u524d\u7684 T \u4ee3\u8868\u8fd9\u4e2a\u56fe\u7247\u5305\u542b\u900f\u660e\u901a\u9053\uff0cL \u4ee3\u8868\u8fd9\u4e2a\u56fe\u7247\u7684\u957f\u5bbd\u6bd4\u6709\u4e9b\u5947\u602a\uff0c\u53ef\u80fd\u662f\u957f\u622a\u56fe\u6216\u5168\u666f\u56fe", None))
#endif // QT_CONFIG(tooltip)
        self.MainPage.setTabText(self.MainPage.indexOf(self.ImgProcessingLayout), QCoreApplication.translate("Form", u"\u5a92\u4f53\u5904\u7406", None))
        self.CropTextInPathOpen.setText(QCoreApplication.translate("Form", u"\u6253\u5f00", None))
        self.CropTextInPath.setPlaceholderText(QCoreApplication.translate("Form", u"\u8f93\u5165\u6587\u4ef6\u8def\u5f84", None))
        self.CropTextRatioSpinbox.setSuffix(QCoreApplication.translate("Form", u" %", None))
        self.CropTextRatioSpinbox.setPrefix(QCoreApplication.translate("Form", u"\u622a\u53d6\u6587\u672c\u7684\u540e ", None))
        self.CropTextOutPathOpen.setText(QCoreApplication.translate("Form", u"\u6253\u5f00", None))
        self.CropTextOutPath.setPlaceholderText(QCoreApplication.translate("Form", u"\u8f93\u51fa\u6587\u4ef6\u8def\u5f84\uff08\u7559\u7a7a\u4ee5\u4fdd\u5b58\u5230\u6e90\u6587\u4ef6\u5939\uff09", None))
        self.CroptextRun.setText(QCoreApplication.translate("Form", u"\u8fd0\u884c", None))
        self.TextProcChildTab.setTabText(self.TextProcChildTab.indexOf(self.CropText), QCoreApplication.translate("Form", u"\u622a\u53d6\u6587\u672c", None))
#if QT_CONFIG(tooltip)
        self.TextProcChildTab.setTabToolTip(self.TextProcChildTab.indexOf(self.CropText), QCoreApplication.translate("Form", u"\u622a\u53d6\u6587\u672c\u7684\u5c3e\u90e8\n"
"\u901a\u5e38\u7528\u4e8e\u91cd\u8981\u5185\u5bb9\u5728\u6587\u672c\u5c3e\u90e8\u7684\u60c5\u51b5\uff0c\u5982\u62a5\u9519\u65f6\u7684\u65e5\u5fd7", None))
#endif // QT_CONFIG(tooltip)
        self.CalSimModelDropdown.setPlaceholderText(QCoreApplication.translate("Form", u"\u9700\u8981\u5237\u65b0", None))
        self.CalSimModelRefresh.setText(QCoreApplication.translate("Form", u"\u5237\u65b0", None))
        self.CalSimPersistentModel.setText(QCoreApplication.translate("Form", u"\u6301\u4e45\u6a21\u578b", None))
        self.CalSimIn1.setPlaceholderText(QCoreApplication.translate("Form", u"\u8f93\u5165\u6587\u672c 1", None))
        self.CalSimIn2.setPlaceholderText(QCoreApplication.translate("Form", u"\u8f93\u5165\u6587\u672c 2", None))
        self.CalSimRun.setText(QCoreApplication.translate("Form", u"\u8ba1\u7b97", None))
        self.TextProcChildTab.setTabText(self.TextProcChildTab.indexOf(self.CalSim), QCoreApplication.translate("Form", u"\u8ba1\u7b97\u76f8\u4f3c\u5ea6", None))
#if QT_CONFIG(tooltip)
        self.TextProcChildTab.setTabToolTip(self.TextProcChildTab.indexOf(self.CalSim), QCoreApplication.translate("Form", u"\u4f7f\u7528\u5d4c\u5165\u6a21\u578b\u8ba1\u7b97\u4e24\u4e2a\u5b57\u7b26\u4e32\u7684\u8bed\u4e49\u76f8\u4f3c\u5ea6", None))
#endif // QT_CONFIG(tooltip)
        self.JsonSorterInOpen.setText(QCoreApplication.translate("Form", u"\u6253\u5f00", None))
        self.JsonSorterInPath.setPlaceholderText(QCoreApplication.translate("Form", u"\u8f93\u5165\u6587\u4ef6\u8def\u5f84", None))
        self.JsonSorterRun.setText(QCoreApplication.translate("Form", u"\u8fd0\u884c", None))
        self.TextProcChildTab.setTabText(self.TextProcChildTab.indexOf(self.JsonSorter), QCoreApplication.translate("Form", u"JSON \u6392\u5e8f", None))
#if QT_CONFIG(tooltip)
        self.TextProcChildTab.setTabToolTip(self.TextProcChildTab.indexOf(self.JsonSorter), QCoreApplication.translate("Form", u"\u5c06JSON\u7684\u952e\u503c\u5bf9\u6309\u952e\u7684\u987a\u5e8f\u6392\u5e8f", None))
#endif // QT_CONFIG(tooltip)
        self.MainPage.setTabText(self.MainPage.indexOf(self.TextProcessingLayout), QCoreApplication.translate("Form", u"\u6587\u672c\u5904\u7406", None))
        self.ImageSeqItemAmount.setSuffix(QCoreApplication.translate("Form", u" \u5f20\u56fe\u7247", None))
        self.ImageSeqItemAmount.setPrefix(QCoreApplication.translate("Form", u"\u751f\u6210 ", None))
        self.ImageSeqPathOpen.setText(QCoreApplication.translate("Form", u"\u6253\u5f00", None))
        self.ImageSeqPathInput.setPlaceholderText(QCoreApplication.translate("Form", u"\u5728\u6b64\u76ee\u5f55\u4e0b\u751f\u6210", None))
        self.ImageSeqGenStart.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb", None))
        self.ImageSeqGenStop.setText(QCoreApplication.translate("Form", u"\u7ec8\u6b62", None))
        self.TestChildTab.setTabText(self.TestChildTab.indexOf(self.ImgSeqGen), QCoreApplication.translate("Form", u"\u751f\u6210\u56fe\u50cf\u5e8f\u5217", None))
        self.QtIconsExport.setText(QCoreApplication.translate("Form", u"\u76f4\u63a5\u5bfc\u51fa", None))
        self.QtIconsShow.setText(QCoreApplication.translate("Form", u"\u6253\u5f00 GUI", None))
        self.TestChildTab.setTabText(self.TestChildTab.indexOf(self.QtIconsLayout), QCoreApplication.translate("Form", u"Qt\u5185\u7f6e\u56fe\u6807", None))
        self.MainPage.setTabText(self.MainPage.indexOf(self.TestingLayout), QCoreApplication.translate("Form", u"\u6d4b\u8bd5\u7528", None))
        self.ThemeLabel.setText(QCoreApplication.translate("Form", u"\u9009\u62e9\u4e3b\u9898\uff08\u4e3b\u9898\u8def\u5f84\uff1a./Style\uff09", None))
        self.ThemeConfirm.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.LogLabel.setText(QCoreApplication.translate("Form", u"\u8be6\u7ec6\u4fe1\u606f", None))
        self.MainPage.setTabText(self.MainPage.indexOf(self.SettingLayout), QCoreApplication.translate("Form", u"\u8bbe\u7f6e", None))
    # retranslateUi

