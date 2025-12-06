from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGraphicsView, QToolBar, QAction, QMenu
from PyQt5.QtGui import QIcon

from data.settingswindow import SettingsWindow
from data.jsonhandler import JSONHandling
from data.imagetojigsaw import JigsawPiece, PuzzleWindow
from data.imageconversion import ImageConversion

class MainWindow(QMainWindow):
    def __init__(self):
        self.settings = JSONHandling()
        self.settingsWindow = SettingsWindow()
        self.imageConversion = ImageConversion()

        super().__init__()
        self.setWindowTitle("Jigsaw")
        self.resize(1024, 768)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)

        leftSide = QWidget()
        leftLayout = QVBoxLayout(leftSide)
        leftLayout.setContentsMargins(0, 0, 0, 0)
        leftLayout.setSpacing(5)

        self.scene = PuzzleWindow(None, self.settingsWindow.getGridRows(), self.settingsWindow.getGridCols())
        self.view = QGraphicsView(self.scene)
        self.view.setStyleSheet(f"background-color: {self.settings.getData("color")}; border: 1px solid black;")
        leftLayout.addWidget(self.view)

        topSide = QToolBar("Main Toolbar")
        self.addToolBar(topSide)
    
        settingsAction = QAction("Settings", self)
        settingsMenu = QMenu()
        settingsMenu.addAction("Settings", self.settingsWindow.show)
        settingsAction.setMenu(settingsMenu)
        self.settingsWindow.settingsChanged.connect(self.reloadSettings)

        aboutAction = QAction(QIcon(), "About", self)
        aboutMenu = QMenu()
        aboutMenu.addAction("About App")
        aboutAction.setMenu(aboutMenu)

      

        puzzleAction = QAction(QIcon(), "Puzzle", self)
        puzzleMenu = QMenu()
        addImageAction = puzzleMenu.addAction("Add Image")
        selectedImage = addImageAction.triggered.connect(lambda: self.handlerInput("image"))
        
        #addFolderAction = puzzleMenu.addAction("Add Folder")
        #selectedFolder = addFolderAction.triggered.connect(lambda: self.handlerInput("folder"))
        
        puzzleAction.setMenu(puzzleMenu)
        
        topSide.addAction(puzzleAction)
        topSide.addAction(settingsAction)
        topSide.addAction(aboutAction)

        layout.addWidget(leftSide, stretch=3)

    def reloadSettings(self):
        self.view.setStyleSheet(f"background-color: {self.settings.getData("color")}; border: 1px solid #ccc;")
        JigsawPiece.number = 0

    def handlerInput(self, typeInput):
        if typeInput == "image":
            selectedImage = self.imageConversion.openImageFile()
            if selectedImage:
                self.constructPuzzle(selectedImage)
        #elif typeInput == "folder":
        #    selectedFolder = self.imageConversion.openFolder()
        #    if selectedFolder:
        #        self.constructPuzzle(selectedFolder)

    def constructPuzzle(self, input):
        self.scene = PuzzleWindow(input, self.settingsWindow.getGridRows(), self.settingsWindow.getGridCols())
        self.view.setScene(self.scene)
    