from PyQt5.QtWidgets import (
    QGraphicsScene, QGraphicsPixmapItem, QMessageBox
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image
import random
from data.settingswindow import SettingsWindow

class JigsawPiece(QGraphicsPixmapItem):

    number = 0
    allPieces = []


    def __init__(self, pixmap, startPos, resultRow, resultCol):
        super().__init__()

        self.setPixmap(pixmap)

        if(startPos != (0,0)):
            self.startPos = startPos
        else:
            self.startPos = (1,1)
        self.setFlags(
            QGraphicsPixmapItem.ItemIsMovable |
            QGraphicsPixmapItem.ItemIsSelectable
        )

        JigsawPiece.number += 1
        self.number = JigsawPiece.number

        self.width = self.pixmap().width()
        self.height = self.pixmap().height()

        self.row = resultRow
        self.col = resultCol
        self.cluster = {self}


        JigsawPiece.allPieces.append(self)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.pos():
            delta = self.mapToParent(event.pos()) - self.pos()
            for self in self.cluster:
                self.setPos(self.pos() + delta)
    

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.checkPieceCluster()

    def getPositionX(self):
        return self.pos().x() 
    
    def getPositionY(self):
        return self.pos().y() 
    
    def getNeighbors(self):
        neighbors = []
        for piece in JigsawPiece.allPieces:
            if piece == self:
                continue
            if((piece.row - self.row) == 0 and (piece.col - self.col) == 1):
                neighbors.append((piece, "right"))
            if((piece.row - self.row) == 1 and (piece.col - self.col) == 0):
                neighbors.append((piece, "down"))
            if((piece.row - self.row) == 0 and (piece.col - self.col) == -1):
                neighbors.append((piece, "left"))
            if((piece.row - self.row) == -1 and (piece.col - self.col) == 0):
                neighbors.append((piece, "up"))
        return neighbors

    def getDistanceToNeighborPieces(self):
        neighbors = self.getNeighbors()
        
        neighborDistances = [[neighbor, neighbor.getPositionX() - self.getPositionX(), neighbor.getPositionY() - self.getPositionY(), direction] for neighbor, direction in neighbors]
        return neighborDistances

    def checkPieceCluster(self):
        snapTolerance = 10
        distanceCheck = self.getDistanceToNeighborPieces()
        for neighbor, dx, dy, direction in distanceCheck:
            if direction == "right":
                if abs(dx - self.width) <= snapTolerance and abs(dy) <= snapTolerance:
                    self.setPieceCluster(neighbor)
            elif direction == "left":
                if abs(dx + self.width) <= snapTolerance and abs(dy) <= snapTolerance:
                    self.setPieceCluster(neighbor)
            elif direction == "down":
                if abs(dy - self.height) <= snapTolerance and abs(dx) <= snapTolerance:
                    self.setPieceCluster(neighbor)
            elif direction == "up":
                if abs(dy + self.height) <= snapTolerance and abs(dx) <= snapTolerance:
                    self.setPieceCluster(neighbor)
            

    def setPieceCluster(self, neighbor):   
        newCluster = self.cluster | neighbor.cluster
        for cluster in newCluster:
            cluster.cluster = newCluster 
    
class PuzzleWindow(QGraphicsScene):
    def __init__(self, filePath, rows, cols):
        super().__init__()

        for piece in JigsawPiece.allPieces:
            if piece.scene() is not None:
                piece.scene().removeItem(piece)
        JigsawPiece.allPieces.clear()
        JigsawPiece.number = 0

        self.filePath = filePath
        self.rows = rows
        self.cols = cols
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
                    

            for i in range(self.rows):
                for j in range(cols):

                    box = (j*pieceW, i*pieceH, (j+1)*pieceW, (i+1)*pieceH)
                    pieceImg = image.crop(box)
                    width, height = pieceImg.width, pieceImg.height
                    data = pieceImg.tobytes("raw", "RGB")
                    qimage = QImage(data, width, height, 3 * width, QImage.Format_RGB888)  
                    pixmap = QPixmap.fromImage(qimage)
                    piece = JigsawPiece(pixmap, (j*pieceW, i*pieceH), i, j)
                    piece.setPos(random.randint(0, w-pieceW), random.randint(0, h-pieceH))                    
                    self.addItem(piece)
                    piece.setPos(random.randint(1, int(self.width()-pieceW)), random.randint(1, int(self.height()-pieceH)))
                