import os

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget

from Workers import TrimmerWorker, UpscalerWorker
from modules.utils import ui_utils
from pages.media_proc.ui_page import Ui_MediaProcTab


class MediaProcWidget(QWidget, Ui_MediaProcTab):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

        # 工作线程
        self.upscaler_worker = None
        self.trimmer_worker = None

        # Actions
        self.del_selected = QAction("移除选中项并删除文件")
        self.remove_selected = QAction("移除选中项并保留文件")
        self.remove_trans = QAction("移除透明项并保留文件")
        self.del_all = QAction("清空列表并删除原文件")
        self.remove_all = QAction("清空列表")

        # 连接信号
        self.VidTrimRun.clicked.connect(self.vid_trim_run)
        self.VidTrimInputOpen.clicked.connect(lambda: ui_utils.select_file(
            self, self.VidTrimInputPath, "Video (*.mp4 *.avi *.mov *.mkv)"
        ))
        self.VidTrimOutputOpen.clicked.connect(lambda: ui_utils.select_savefile(
            self, self.VidTrimOutputPath, "Video (*.mp4)"
        ))
        self.VidTrimInputPlay.clicked.connect(lambda: ui_utils.open_file(self, self.VidTrimInputPath.text()))
        self.UpsChooseImagePath.clicked.connect(lambda: ui_utils.select_folder(self, self.UpsImagePath))
        self.UpsSavePathOpen.clicked.connect(lambda: ui_utils.select_folder(self, self.UpsSavePath))
        self.UpsRun.clicked.connect(lambda: self.ups_run(mode="upscale"))
        self.UpsStop.clicked.connect(lambda: self.upscaler_worker.stop())
        self.UpsRefreshModel.clicked.connect(lambda: ui_utils.refresh_combobox(
            target_widget=self.UpsModelDropdown, path=self.UpsComfyUrl.text(),
            sub_url="/object_info/UpscaleModelLoader", scan_type="url", include_path=False,
            location=["UpscaleModelLoader", "input", "required", "model_name", 1, "options"], parent=self
        ))
        self.UpsListImg.clicked.connect(lambda: self.ups_run(mode="find"))
        self.UpsList.itemDoubleClicked.connect(
            lambda item: ui_utils.add_double_click_open(item, self, ["T ", "L ", "TL "], "prefix")
        )

        self.add_context_menu()

    def add_context_menu(self):
        self.del_selected.triggered.connect(lambda: ui_utils.remove_entry(
            mode="delete_selected", parent=self, target_widget=self.UpsList, substring=["T ", "L ", "TL "],
            remove_type="prefix"
        ))
        self.remove_selected.triggered.connect(lambda: ui_utils.remove_entry(
            mode="remove_selected", parent=self, target_widget=self.UpsList
        ))
        self.remove_trans.triggered.connect(lambda: ui_utils.remove_entry(
            mode="remove_matched", parent=self, target_widget=self.UpsList, pattern=r"(T |TL ).*",
            substring=["T ", "L ", "TL "], remove_type="prefix"
        ))
        self.del_all.triggered.connect(lambda: ui_utils.remove_entry(
            mode="delete_all", parent=self, target_widget=self.UpsList, substring=["T ", "L ", "TL "],
            remove_type="prefix"
        ))
        self.remove_all.triggered.connect(lambda: ui_utils.remove_entry(
            mode="remove_all", parent=self, target_widget=self.UpsList
        ))

        self.UpsList.addAction(self.del_selected)
        self.UpsList.addAction(self.remove_selected)
        self.UpsList.addAction(self.remove_trans)
        self.UpsList.addAction(self.del_all)
        self.UpsList.addAction(self.remove_all)

    def vid_trim_run(self):
        self.VidTrimRun.setEnabled(False)
        self.VidTrimRun.setText("正在运行")
        self.trimmer_worker = TrimmerWorker(
            input_path=self.VidTrimInputPath.text(),
            input_time=self.VidTrimTime.time(),
            output_path=self.VidTrimOutputPath.text(),
            preserve=self.VidTrimMode.currentIndex()
        )
        self.trimmer_worker.worker_finished.connect(lambda: self.VidTrimRun.setEnabled(True))
        self.trimmer_worker.worker_finished.connect(lambda: self.VidTrimRun.setText("运行"))
        self.trimmer_worker.worker_finished.connect(lambda t: ui_utils.show_message_box(self, t[0], t[1], t[2]))
        self.trimmer_worker.start()

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
        self.upscaler_worker.output_path_updated.connect(lambda t: self.UpsSavePath.setText(os.path.normpath(t)))
        self.upscaler_worker.start()
