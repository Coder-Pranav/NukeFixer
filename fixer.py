import os
import sys
from PySide2.QtWidgets import*

nuke_path = sys.executable
python_file = 'disable_all.py'
python_file = os.path.join(os.path.dirname(__file__),python_file)

class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.label = QLabel()
        self.button = QPushButton('Disable')
        master_lay = QVBoxLayout()
        master_lay.addWidget(self.label)
        master_lay.addWidget(self.button)

        self.setAcceptDrops(True)
        self.setLayout(master_lay)
        self.setMinimumSize(500,250)
        self.setWindowTitle('Nuke Fixer')
        self.button.clicked.connect(self.execute)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        for url in e.mimeData().urls():
            file_name = url.toLocalFile()
            self.label.setText(file_name)
            print("Dropped file: " + file_name)

    def execute(self):
        wrk_file_path = self.label.text()
        if wrk_file_path.endswith('nk'):
            os.system('start /wait cmd /k "{}" -it {} {}'.format(nuke_path, python_file, wrk_file_path))
        else:
            msgBox = QMessageBox()
            msgBox.setText("Please Drag a nuke file")
            msgBox.exec_()


def run():
    run.window = MainWindow()
    run.window.show()




