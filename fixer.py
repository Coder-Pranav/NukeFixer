import os
import re
import sys

from PySide2.QtCore import QProcess
from PySide2.QtWidgets import *

nuke_path = sys.executable
python_file = 'disable_all.py'
python_file = os.path.join(os.path.dirname(__file__), python_file)
progress_re = re.compile("Total complete: (\d+)%")


def simple_percent_parser(output):
    m = progress_re.search(output)
    if m:
        pc_complete = m.group(1)
        return int(pc_complete)


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.label = QLabel()
        self.label.setText('Drag and drop nk file')
        self.button = QPushButton('Disable')
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 100)
        self.text_area = QPlainTextEdit()
        self.text_area.setReadOnly(True)
        master_lay = QVBoxLayout()
        master_lay.addWidget(self.label)
        master_lay.addWidget(self.progressBar)
        master_lay.addWidget(self.text_area)
        master_lay.addWidget(self.button)
        self.process = None

        self.setAcceptDrops(True)
        self.setLayout(master_lay)
        self.setMinimumSize(500, 250)
        self.setWindowTitle('Nuke Disable')
        self.button.clicked.connect(self.execute)

    def message(self, s):
        self.text_area.appendPlainText(s)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        for url in e.mimeData().urls():
            file_name = url.toLocalFile()
            self.label.setText(file_name)
            print("Dropped file: " + file_name)

    def execute(self):
        if self.process is None:
            self.process = QProcess()
            self.process.readyReadStandardOutput.connect(self.handle_stdout)
            self.process.readyReadStandardError.connect(self.handle_stderr)
            self.process.stateChanged.connect(self.handle_state)
            self.process.finished.connect(self.process_finished)
            wrk_file_path = self.label.text()
            if wrk_file_path.endswith('nk'):
                self.process.start('"{}" -it {} {}'.format(nuke_path, python_file, wrk_file_path))
            else:
                msgBox = QMessageBox()
                msgBox.setText("Please Drag a nuke file")
                msgBox.exec_()

    def handle_stderr(self):
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        # Extract progress if it is in the data.
        progress = simple_percent_parser(stderr)
        if progress:
            self.progressBar.setStyleSheet("QProgressBar::chunk"
                                           "{"
                                           "background-color: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0,"
                                           "stop: 0 #FF4E50,"
                                           "stop: 1 #F9D423);"
                                           "}")
            self.progressBar.setValue(progress)
        self.message(stderr)

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode()
        self.message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.message("State changed: {}".format(state_name))

    def process_finished(self):
        self.message("Process finished.")
        self.process = None


def run():
    run.window = MainWindow()
    run.window.show()
