from PyQt5.QtWidgets import QApplication
import sys

from data.mainwindow import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
window.showMaximized()
sys.exit(app.exec())