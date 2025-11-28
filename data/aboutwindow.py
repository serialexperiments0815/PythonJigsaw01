from PyQt5.QtWidgets import QVBoxLayout, QLabel, QDialog

class AboutWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("About this application."))
        self.setLayout(layout)
