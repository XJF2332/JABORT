from PySide6.QtWidgets import QWidget

from Workers import FlattenWorker, NewFlattenWorker
from pages.file_mgr.ui_page import Ui_FileMgrTab
from modules.utils import ui_utils

class FileMgrWidget(QWidget, Ui_FileMgrTab):
    def __init__(self, make_designer_happy):
        super().__init__()
        self.new_flatten_worker = None
        self.flatten_worker = None
        self.setupUi(self)

        # 绑定信号
        self.FlattenRun.clicked.connect(self.flatten_run)
        self.FlattenStop.clicked.connect(lambda: self.flatten_worker.stop())
        self.FlattenDirOpen.clicked.connect(lambda: ui_utils.select_folder(self, self.FlattenDirInput))
        self.NewFlattenRun.clicked.connect(self.new_flatten_run)
        self.NewFlattenStop.clicked.connect(lambda: self.new_flatten_worker.stop())
        self.NewFlattenDirOpen.clicked.connect(lambda: ui_utils.select_folder(self, self.NewFlattenDirInput))

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