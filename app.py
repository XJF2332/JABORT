import os
import subprocess

import send2trash
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QLineEdit, QMessageBox

from Tools.TextProcessing import CropText, CalSimilarity, JsonSorter
from Tools.Utils import ui_utils
from Workers import *
from ui_app import Ui_Form

with open("Style\Blue Archive.qss", "r", encoding="utf-8") as f:
    stylesheet = f.read()


# UI
class MyWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet(stylesheet)
        self.ThemeDropdown.addItems([os.path.join("Style", item) for item in os.listdir("Style")])

        # 工作线程实例
        self.upscaler_worker = None
        self.noise_worker = None
        self.png2jpg_worker = None
        self.flatten_worker = None
        self.new_flatten_worker = None
        self.seq2pdf_worker = None

        # 展平信号
        self.FlattenRun.clicked.connect(self.flatten_run)
        self.FlattenStop.clicked.connect(lambda: self.flatten_worker.stop())
        self.FlattenDirOpen.clicked.connect(lambda: self.select_folder(self.FlattenDirInput))
        self.NewFlattenRun.clicked.connect(self.new_flatten_run)
        self.NewFlattenStop.clicked.connect(lambda: self.new_flatten_worker.stop())
        self.NewFlattenDirOpen.clicked.connect(lambda: self.select_folder(self.NewFlattenDirInput))
        # PNG转JPG信号
        self.PNG2JPGRun.clicked.connect(self.png2jpg_run)
        self.PNG2JPGStop.clicked.connect(lambda: self.png2jpg_worker.stop())
        self.PNG2JPGFindDir.clicked.connect(lambda: self.select_folder(self.PNG2JPGDirTxt))
        self.PNG2JPGQualitySlider.valueChanged.connect(lambda v: self.PNG2JPGQualityNum.setText(str(v)))
        # 图像序列转PDF信号
        self.Seq2PDFRun.clicked.connect(self.img2pdf_run)
        self.Seq2PDFStop.clicked.connect(lambda: self.seq2pdf_worker.stop())
        self.Seq2PDFPathOpen.clicked.connect(lambda: self.select_folder(self.Seq2PDFPathInput))
        # 放大信号
        self.UpsChooseImagePath.clicked.connect(lambda: self.select_folder(self.UpsImagePath))
        self.UpsSavePathOpen.clicked.connect(lambda: self.select_folder(self.UpsSavePath))
        self.UpsRun.clicked.connect(lambda: self.ups_run(mode="upscale"))
        self.UpsStop.clicked.connect(lambda: self.upscaler_worker.stop())
        self.UpsRefreshModel.clicked.connect(
            lambda: ui_utils.refresh_combobox(
                target_widget=self.UpsModelDropdown,
                path=self.UpsComfyUrl.text(),
                sub_url="/object_info/UpscaleModelLoader",
                scan_type="url", include_path=False,
                location=["UpscaleModelLoader", "input", "required", "model_name", 1, "options"],
                parent=self
            )
        )
        self.UpsListImg.clicked.connect(lambda: self.ups_run(mode="find"))
        self.UpsList.itemDoubleClicked.connect(
            lambda item: ui_utils.add_double_click_open(item, self, ["T ", "L ", "TL "], "prefix")
        )
        self.UpsList.customContextMenuRequested.connect(
            lambda pos: ui_utils.show_context_menu(
                self.UpsList, pos,
                [
                    ("删除选择项", lambda: ui_utils.remove_entry(
                        mode="delete_selected", parent=self, target_widget=self.UpsList,
                        substring=["T ", "L ", "TL "], remove_type="prefix"
                    )),
                    ("删除全部项", lambda: ui_utils.remove_entry(
                        mode="delete_all", parent=self, target_widget=self.UpsList,
                        substring=["T ", "L ", "TL "], remove_type="prefix"
                    )),
                    ("忽略选中项", lambda: ui_utils.remove_entry(
                        mode="remove_selected", parent=self, target_widget=self.UpsList
                    )),
                    ("忽略全部项", lambda: ui_utils.remove_entry(
                        mode="remove_all", parent=self, target_widget=self.UpsList
                    )),
                    ("忽略透明项", lambda: ui_utils.remove_entry(
                        mode="remove_matched", parent=self, target_widget=self.UpsList,
                        pattern=r"(T |TL ).*", substring=["T ", "L ", "TL "], remove_type="prefix"
                    ))
                ]
            )
        )
        # 噪声图像生成信号
        self.ImageSeqGenStart.clicked.connect(self.image_seq_gen_run)
        self.ImageSeqGenStop.clicked.connect(lambda: self.noise_worker.stop())
        self.ImageSeqPathOpen.clicked.connect(lambda: self.select_folder(self.ImageSeqPathInput))
        # 裁剪文本信号
        self.CropTextInPathOpen.clicked.connect(lambda: self.select_file(self.CropTextInPath))
        self.CropTextOutPathOpen.clicked.connect(lambda: self.select_file(self.CropTextOutPath))
        self.CroptextRun.clicked.connect(self.crop_text_run)
        # 设置页面信号
        self.ThemeConfirm.clicked.connect(self.set_stylesheet)
        self.ClearLog.clicked.connect(self.clear_log)
        # 计算相似度信号
        self.CalSimModelRefresh.clicked.connect(
            lambda: ui_utils.refresh_combobox(
                target_widget=self.CalSimModelDropdown,
                path="models", include_path=True, parent=self
            )
        )
        self.CalSimRun.clicked.connect(self.cal_similarity_run)
        # JSON排序信号
        self.JsonSorterInOpen.clicked.connect(lambda: self.select_file(self.JsonSorterInPath, "*.json"))
        self.JsonSorterRun.clicked.connect(self.json_sorter_run)
        # Qt内置图标相关信号
        self.QtIconsShow.clicked.connect(
            lambda: subprocess.run(["python", os.path.join("Tools", "TestTools", "QtIconExport.py")])
        )
        self.QtIconsExport.clicked.connect(
            lambda: subprocess.run(["python", os.path.join("Tools", "TestTools", "QtIconExport.py"), "--export"])
        )

    # 一些共用的函数
    def select_folder(self, target_widget: QLineEdit):
        path = QFileDialog.getExistingDirectory(self, "选择目录")
        if path:
            target_widget.setText(path)

    def select_file(self, target_widget: QLineEdit, file_type: str = ""):
        if not file_type:
            path = QFileDialog.getOpenFileName(self, caption="选择文件")
        else:
            path = QFileDialog.getOpenFileName(self, caption="选择文件", filter=file_type)
        if path:
            target_widget.setText(path[0])

    # 会开启新线程的函数
    def flatten_run(self):
        self.FlattenRun.setEnabled(False)
        self.FlattenStop.setEnabled(True)
        self.flatten_worker = FlattenWorker(self.FlattenDirInput.text())
        self.flatten_worker.worker_finished.connect(lambda: self.FlattenRun.setEnabled(True))
        self.flatten_worker.worker_finished.connect(lambda: self.FlattenStop.setEnabled(False))
        self.flatten_worker.worker_finished.connect(lambda t: ui_utils.show_message_box(self, t[0], t[1], t[2]))
        self.flatten_worker.start()

    def new_flatten_run(self):
        self.NewFlattenRun.setEnabled(False)
        self.NewFlattenStop.setEnabled(True)
        self.new_flatten_worker = NewFlattenWorker(self.NewFlattenDirInput.text())
        self.new_flatten_worker.progress_updated.connect(lambda v: self.NewFlattenProgress.setValue(v))
        self.new_flatten_worker.worker_finished.connect(lambda: self.NewFlattenRun.setEnabled(True))
        self.new_flatten_worker.worker_finished.connect(lambda: self.NewFlattenStop.setEnabled(False))
        self.new_flatten_worker.worker_finished.connect(lambda t: ui_utils.show_message_box(self, t[0], t[1], t[2]))
        self.new_flatten_worker.start()

    def png2jpg_run(self):
        self.PNG2JPGRun.setEnabled(False)
        self.PNG2JPGStop.setEnabled(True)
        self.png2jpg_worker = PNG2JPGWorker(
            image_dir=self.PNG2JPGDirTxt.text(),
            recursive=self.PNG2JPGWalk.isChecked(),
            quality=self.PNG2JPGQualitySlider.value(),
            ignore_transparency=self.PNG2JPGIngoreAlpha.isChecked(),
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
        self.seq2pdf_worker.run()

    def ups_run(self, mode: str = "upscale"):
        self.UpsRun.setEnabled(False)
        self.UpsListImg.setEnabled(False)
        self.UpsList.setEnabled(False)
        self.UpsStop.setEnabled(True)
        self.upscaler_worker = UpscalerWorker(
            model_name=self.UpsModelDropdown.currentText(),
            img_dir=self.UpsImagePath.text(),
            recursive_search=self.UpsRecursive.isChecked(),
            width_threshold=self.UpsWidthThresholdSpin.value(),
            height_threshold=self.UpsHeightThresholdSpin.value(),
            jpg_size_threshold=self.UpsJPGThresholdSpin.value(),
            post_downscale_scale=self.UpsDownscaleSpin.value(),
            url=self.UpsComfyUrl.text(),
            image_list=[self.UpsList.item(i).text() for i in range(self.UpsList.count())],
            save_dir=self.UpsSavePath.text(),
            mode=mode,
        )
        self.upscaler_worker.worker_finished.connect(lambda: self.UpsRun.setEnabled(True))
        self.upscaler_worker.worker_finished.connect(lambda: self.UpsListImg.setEnabled(True))
        self.upscaler_worker.worker_finished.connect(lambda: self.UpsList.setEnabled(True))
        self.upscaler_worker.worker_finished.connect(lambda: self.UpsStop.setEnabled(False))
        self.upscaler_worker.worker_finished.connect(lambda t: ui_utils.show_message_box(self, t[0], t[1], t[2]))
        self.upscaler_worker.progress_updated.connect(lambda v: self.UpsProgress.setValue(v))
        self.upscaler_worker.image_list_got.connect(lambda lst: ui_utils.set_widget_items(self.UpsList, lst))
        self.upscaler_worker.image_list_got.connect(lambda lst: setattr(self, 'ups_image_list', lst))
        self.upscaler_worker.start()

    def image_seq_gen_run(self):
        self.ImageSeqGenStop.setEnabled(True)
        self.ImageSeqGenStart.setEnabled(False)
        self.noise_worker = ImageSeqWorker(
            num_images=self.ImageSeqItemAmount.value(),
            output_folder=self.ImageSeqPathInput.text()
        )
        self.noise_worker.progress_updated.connect(lambda v: self.ImageSeqGenProgress.setValue(v))
        self.noise_worker.worker_finished.connect(lambda: self.ImageSeqGenStart.setEnabled(True))
        self.noise_worker.worker_finished.connect(lambda: self.ImageSeqGenStop.setEnabled(False))
        self.noise_worker.worker_finished.connect(lambda t: ui_utils.show_message_box(self, t[0], t[1], t[2]))
        self.noise_worker.start()

    # 在当前线程运行的函数
    def crop_text_run(self):
        res = CropText.crop_text_file(
            source_path=self.CropTextInPath.text(),
            output_path=self.CropTextOutPath.text(),
            percentage=self.CropTextRatioSpinbox.value(),
        )
        if res[0]:
            ui_utils.show_message_box(self, "错误", res[1], QMessageBox.Icon.Critical)
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
        similarity = CalSimilarity.main(
            str1=self.CalSimIn1.text(),
            str2=self.CalSimIn2.text(),
            model=self.CalSimModelDropdown.currentText(),
            persistent_model=self.CalSimPersistentModel.isChecked()
        )
        if similarity[0]:
            ui_utils.show_message_box(self, "错误", similarity[1], QMessageBox.Icon.Critical)
        else:
            ui_utils.show_message_box(self, "计算结果", f"输入内容的相似度为 {similarity[1]}",
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