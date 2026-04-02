import os

import send2trash
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox

from modules.text_proc import JsonSorter, CalSimilarity, CropText
from modules.utils import ui_utils
from Workers import *
from ui_app import Ui_Form

with open(r"styles\Blue Archive.qss", "r", encoding="utf-8") as f:
    stylesheet = f.read()


# UI
class MyWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet(stylesheet)
        self.ThemeDropdown.addItems([os.path.join("styles", item) for item in os.listdir("styles")])

        # 工作线程实例
        self.upscaler_worker = None
        self.png2jpg_worker = None
        self.seq2pdf_worker = None
        self.trimmer_worker = None

        # PNG转JPG信号
        self.PNG2JPGRun.clicked.connect(self.png2jpg_run)
        self.PNG2JPGStop.clicked.connect(lambda: self.png2jpg_worker.stop())
        self.PNG2JPGFindDir.clicked.connect(lambda: ui_utils.select_folder(self, self.PNG2JPGDirTxt))
        self.PNG2JPGQualitySlider.valueChanged.connect(lambda v: self.PNG2JPGQualityNum.setText(str(v)))
        # 图像序列转PDF信号
        self.Seq2PDFRun.clicked.connect(self.img2pdf_run)
        self.Seq2PDFStop.clicked.connect(lambda: self.seq2pdf_worker.stop())
        self.Seq2PDFPathOpen.clicked.connect(lambda: ui_utils.select_folder(self, self.Seq2PDFPathInput))
        # 裁剪文本信号
        self.CropTextInPathOpen.clicked.connect(lambda: ui_utils.select_file(self, self.CropTextInPath))
        self.CropTextOutPathOpen.clicked.connect(lambda: ui_utils.select_savefile(self, self.CropTextOutPath))
        self.CroptextRun.clicked.connect(self.crop_text_run)
        # 设置页面信号
        self.ThemeConfirm.clicked.connect(self.set_stylesheet)
        self.ClearLog.clicked.connect(self.clear_log)
        # 计算相似度信号
        self.CalSimModelRefresh.clicked.connect(lambda: ui_utils.refresh_combobox(
            target_widget=self.CalSimModelDropdown, path="resources/models/embeddings", include_path=False, parent=self
        ))
        self.CalSimUnload.clicked.connect(lambda: ui_utils.show_message_box(
            self, content=CalSimilarity.unload_model(), icon=QMessageBox.Icon.Information
        ))
        self.CalSimRun.clicked.connect(self.cal_similarity_run)
        # JSON排序信号
        self.JsonSorterInOpen.clicked.connect(lambda: ui_utils.select_file(
            self, self.JsonSorterInPath, "*.json"
        ))
        self.JsonSorterRun.clicked.connect(self.json_sorter_run)


    # 会开启新线程的函数
    def png2jpg_run(self):
        self.PNG2JPGRun.setEnabled(False)
        self.PNG2JPGStop.setEnabled(True)
        self.png2jpg_worker = PNG2JPGWorker(
            image_dir=self.PNG2JPGDirTxt.text(),
            recursive=self.PNG2JPGWalk.isChecked(),
            quality=self.PNG2JPGQualitySlider.value(),
            skip_transparency=self.PNG2JPGSkipAlpha.isChecked(),
            preserve_metadata=self.PNG2JPGPreverveMeta.isChecked(),
            delete_origin=self.PNG2JPGDelOri.isChecked(),
            deduplicate=self.PNG2JPGDedup.currentIndex()
        )
        self.png2jpg_worker.progress_updated.connect(lambda v: self.PNG2JPGProgress.setValue(int(v)))
        self.png2jpg_worker.worker_finished.connect(lambda: self.PNG2JPGRun.setEnabled(True))
        self.png2jpg_worker.worker_finished.connect(lambda: self.PNG2JPGStop.setEnabled(False))
        self.png2jpg_worker.worker_finished.connect(lambda t: ui_utils.show_message_box(self, t[0], t[1], t[2]))
        self.png2jpg_worker.start()

    def img2pdf_run(self):
        self.Seq2PDFRun.setEnabled(False)
        self.Seq2PDFStop.setEnabled(True)
        self.seq2pdf_worker = ImgSeq2PDFWorker(
            folder=self.Seq2PDFPathInput.text(),
            recursive=self.Seq2PDFRecursive.isChecked(),
            send2trash=self.Seq2PDFDel.isChecked()
        )
        self.seq2pdf_worker.worker_finished.connect(lambda: self.Seq2PDFRun.setEnabled(True))
        self.seq2pdf_worker.worker_finished.connect(lambda: self.Seq2PDFStop.setEnabled(False))
        self.seq2pdf_worker.worker_finished.connect(lambda t: ui_utils.show_message_box(self, t[0], t[1], t[2]))
        self.seq2pdf_worker.progress_updated.connect(lambda v: self.Seq2PDFProgress.setValue(v))
        self.seq2pdf_worker.start()

    # 在当前线程运行的函数
    def crop_text_run(self):
        res = CropText.crop_text_file(
            input_path=self.CropTextInPath.text(),
            output_path=self.CropTextOutPath.text(),
            percentage=self.CropTextRatioSpinbox.value(),
            deduplicate=self.CropTextDedup.currentIndex()
        )
        if res[0].code:
            ui_utils.show_message_box(self, "错误", res[0].generic, QMessageBox.Icon.Critical)
        else:
            ui_utils.show_message_box(self, "成功", f"裁剪后的文本已保存到 {res[1]}",
                                      QMessageBox.Icon.Information)

    def set_stylesheet(self):
        with open(self.ThemeDropdown.currentText(), "r", encoding="utf-8") as style:
            style = style.read()
        self.setStyleSheet(style)

    def clear_log(self):
        try:
            logs = [os.path.join("logs", file) for file in os.listdir("logs") if file.endswith(".zip")]
            if logs:
                send2trash.send2trash(logs)
                ui_utils.show_message_box(self, "成功", "日志文件已删除", QMessageBox.Icon.Information)
            else:
                ui_utils.show_message_box(self, "错误", "没有日志文件", QMessageBox.Icon.Warning)
        except Exception as e:
            ui_utils.show_message_box(self, "错误", f"无法删除日志：{e}", QMessageBox.Icon.Critical)

    def cal_similarity_run(self):
        res = CalSimilarity.main(
            str1=self.CalSimIn1.text(), str2=self.CalSimIn2.text(),
            model=os.path.join("resources", "models", "embeddings", self.CalSimModelDropdown.currentText()),
            persistent_model=self.CalSimPersistentModel.isChecked()
        )
        if res[0].code:
            ui_utils.show_message_box(self, "错误", res[0].generic, QMessageBox.Icon.Critical)
        else:
            ui_utils.show_message_box(self, "计算结果", f"输入内容的相似度为 {res[1]}",
                                      QMessageBox.Icon.Information)

    def json_sorter_run(self):
        res = JsonSorter.main(self.JsonSorterInPath.text())
        if res[0]:
            ui_utils.show_message_box(self, "错误", res[1], QMessageBox.Icon.Critical)
        else:
            ui_utils.show_message_box(self, "信息", "排序已完成，结果已保存到原文件",
                                      QMessageBox.Icon.Information)


if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()