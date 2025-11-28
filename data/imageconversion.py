from PyQt5.QtWidgets import QFileDialog

class ImageConversion():
    def __init__(self):
        pass

    def openImageFile(self):
        filePath, _ = QFileDialog.getOpenFileName(
            None,
            "Select an image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if filePath:
            return filePath

    def openFolder(self):
        folderPath = QFileDialog.getExistingDirectory(None, "Select Folder")
        if folderPath:
            return folderPath