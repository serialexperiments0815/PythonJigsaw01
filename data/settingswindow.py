from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDialog, QComboBox, QSlider
)
from PyQt5.QtCore import Qt, pyqtSignal
import json, math

from data.jsonhandler import JSONHandling

class SettingsWindow(QDialog):

    settingsChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.settings = JSONHandling()
        self.setWindowTitle("Settings")
        self.resize(400,200)
        layout = QVBoxLayout()
        
 
        layout.addWidget(QLabel("Select Color Theme:"))
        self.colorBox = QComboBox()
        self.colorBox.addItems(["Blue", "Red", "Green", "Yellow", "Purple", "Gray"])

        self.colorBox.setCurrentText(self.settings.getData("color"))
        layout.addWidget(self.colorBox)

        layout.addWidget(QLabel("Warning, due to the nature of the calculations. The exact number may not be used to fill the grid."))
        layout.addWidget(QLabel("Number of Puzzle Pieces:"))
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(12)
        self.slider.setMaximum(64)
        self.slider.setSingleStep(2)
        self.slider.setPageStep(2)
        self.slider.setValue(int(self.settings.getData("puzzlePieces")))
        self.slider.valueChanged.connect(self.updateSliderValue)
        self.sliderText = QLabel("Number of puzzle pieces: " + f"{self.settings.getData("puzzlePieces")}")
        
        layout.addWidget(self.slider)
        layout.addWidget(self.sliderText)


        buttonLayout = QHBoxLayout()
        saveBtn = QPushButton("Save")
        cancelBtn = QPushButton("Cancel")
        buttonLayout.addWidget(saveBtn)
        buttonLayout.addWidget(cancelBtn)
        layout.addLayout(buttonLayout)

        saveBtn.clicked.connect(self.saveSettings)
        cancelBtn.clicked.connect(self.reject)

        self.setLayout(layout)


    def updateSliderValue(self, value):
        snapped = 2 * round(value / 2)
        self.sliderText.setText(f"Number of puzzle pieces: {snapped}")


    def saveSettings(self):
        data = {
            "color": self.colorBox.currentText(),
            "puzzlePieces": self.slider.value()
        }
        with open (self.settings.getFileLocation(), "w") as f:
            json.dump(data, f, indent=4)
        self.accept()
        self.settingsChanged.emit()

    def piecesToGrid(self, totalPieces):
        cols = math.ceil(math.sqrt(totalPieces))
        rows = math.ceil(totalPieces / cols)
        return rows, cols
    
    def getGridRows(self):
        return self.piecesToGrid(self.settings.getData("puzzlePieces"))[0]

    def getGridCols(self):
        return self.piecesToGrid(self.settings.getData("puzzlePieces"))[1]