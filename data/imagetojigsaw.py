from PyQt5.QtWidgets import (
    QGraphicsScene, QGraphicsPixmapItem, QMessageBox
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image
import random

class JigsawPiece(QGraphicsPixmapItem):

    number = 0

    def __init__(self, pixmap, correctPos):
        super().__init__()
        self.setPixmap(pixmap)
        self.correctPos = correctPos
        self.setFlags(
            QGraphicsPixmapItem.ItemIsMovable |
            QGraphicsPixmapItem.ItemIsSelectable
        )
        self.setPos(0, 0)
        JigsawPiece.number += 1
        self.number = JigsawPiece.number
        self.cluster = {self}

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.pos()
            print(event.pos(), self.correctPos, " ", self.number)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.dragPosition:
            delta = self.mapToParent(event.pos()) - self.dragPosition - self.pos()
            for piece in self.cluster:
                piece.setPos(piece.pos() + delta)
    

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            firstRow = 0
            lastRow = (PuzzleWindow.getRows)
            print(firstRow, lastRow)
            if (self.number):
                None


class PuzzleWindow(QGraphicsScene):
    def __init__(self, filePath, rows, cols):
        super().__init__()
        self.filePath = filePath
        self.rows = rows
        print(self.rows-1)
        self.cols = cols
        print(self.cols-1)
        if (filePath != None):

            self.createPuzzle(rows, cols)

    def createPuzzle(self, rows, cols):
        image = Image.open(self.filePath)
        w, h = image.size
        pieceW, pieceH = w // cols, h // rows

        

        if (w >= 800 and h >= 800):
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Only image below the height 800 and width 800 are supported\n"
                        f"Current image width: {w}\n"
                        f"Current image height: {h}")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
        else:
                    

            for i in range(rows):
                for j in range(cols):

                    box = (j*pieceW, i*pieceH, (j+1)*pieceW, (i+1)*pieceH)
                    pieceImg = image.crop(box)
                    width, height = pieceImg.width, pieceImg.height
                    data = pieceImg.tobytes("raw", "RGB")
                    qimage = QImage(data, width, height, 3 * width, QImage.Format_RGB888)  
                    pixmap = QPixmap.fromImage(qimage)
                    piece = JigsawPiece(pixmap, (j*pieceW, i*pieceH))
                    print(f"Piecenumber: {piece.number} | Row: {i} Col: {j} | H: {pieceImg.height} W: {pieceImg.width}")

                    piece.setPos(random.randint(0, w-pieceW), random.randint(0, h-pieceH))                    
                    self.addItem(piece)
                    piece.setPos(random.randint(0, int(self.width()-pieceW)), random.randint(0, int(self.height()-pieceH)))
                    print("1111")
    
    def getRows(self):
        return self.rows
    
    def getCols(self):
        return self.cols
                