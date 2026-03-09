from PySide6.QtWidgets import QWidget, QMessageBox

from Workers import ImageSeqWorker
from modules.tests.QtIconExport import export_all_icons
from modules.utils import ui_utils
from pages.tests.ui_page import Ui_TestTab


class TestsWidget(QWidget, Ui_TestTab):
    def __init__(self, make_designer_happy):
        super().__init__()
        self.setupUi(self)

        # 绑定信号
        self.IconExport.clicked.connect(self.export_icons)
        self.IconOutputOpen.clicked.connect(lambda: ui_utils.select_folder(self, self.IconOutputPath))
        self.SeqStart.clicked.connect(self.image_seq_gen_run)
        self.SeqStop.clicked.connect(lambda: self.seq_worker.stop())
        self.SeqPathOpen.clicked.connect(lambda: ui_utils.select_folder(self, self.SeqPathInput))

    def image_seq_gen_run(self):
        self.SeqStop.setEnabled(True)
        self.SeqStart.setEnabled(False)
        self.seq_worker = ImageSeqWorker(
            num_images=self.SeqItemAmount.value(),
            output_folder=self.SeqPathInput.text()
        )
        self.seq_worker.progress_updated.connect(lambda v: self.SeqProgress.setValue(v))
        self.seq_worker.worker_finished.connect(lambda: self.SeqStart.setEnabled(True))
        self.seq_worker.worker_finished.connect(lambda: self.SeqStop.setEnabled(False))
        self.seq_worker.worker_finished.connect(lambda t: ui_utils.show_message_box(self, t[0], t[1], t[2]))
        self.seq_worker.start()

    def export_icons(self):
        res = export_all_icons(self.IconOutputPath.text())
        if res[1]:
            ui_utils.show_message_box(self, content=f"导出已完成\n成功 {res[0]}\n失败 {res[1]}",
                                      icon=QMessageBox.Icon.Warning)
        else:
            ui_utils.show_message_box(self, content=f"导出已完成\n成功 {res[0]}\n失败 {res[1]}",
                                      icon=QMessageBox.Icon.Information)
