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

        self.row = resultRow
        self.col = resultCol
        self.cluster = {self}


        JigsawPiece.allPieces.append(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            
            print("Momentane Position: {", self.getPositionX() , " - ", self.getPositionY(), "} Piece number: ", self.number, " Row: ", self.row, " Col: ", self.col, " Starting pos:", self.startPos)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.pos():
            delta = self.mapToParent(event.pos()) - self.pos()
            for self in self.cluster:
                self.setPos(self.pos() + delta)
    

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            neighbors = self.getDistanceToNeighborPieces()
            print(len(JigsawPiece.allPieces))
            for item in neighbors:
                print(f"Neighbor {item[0]} {item[3]}: distance x{item[1]}. y{item[2]}")
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
        distanceCheck = self.getDistanceToNeighborPieces()
        for neighbor, dx, dy, direction in distanceCheck:
            if direction == "right" and dx <= 150 and dx >= 110 and dy >= -5 and dy <= 5:
                self.setPieceCluster(neighbor)
            if(direction == "down" and dy <= 165 and dy >= 150 and dx >= -5 and dx <= 5):
                self.setPieceCluster(neighbor)
            if(direction == "left" and dx >= -125 and dx <= -100 and dy >= -5 and dy <= 5):
                self.setPieceCluster(neighbor)
            if(direction == "up" and dy <= -150 and dy >= -160 and dx >= -5 and dx <= 5):
                self.setPieceCluster(neighbor)
            

    def setPieceCluster(self, neighbor):   
        newCluster = self.cluster | neighbor.cluster
        for cluster in newCluster:
            cluster.cluster = newCluster 
    
class PuzzleWindow(QGraphicsScene):
    def __init__(self, filePath, rows, cols):
        super().__init__()
        self.filePath = filePath
        self.rows = rows
        print("ROWS: ", self.rows-1)
        self.cols = cols
        print("COLS: ", self.cols-1)
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
                    print(f"Piecenumber: {piece.number} | Row: {i} Col: {j} | H: {pieceImg.height} W: {pieceImg.width}")

                    piece.setPos(random.randint(0, w-pieceW), random.randint(0, h-pieceH))                    
                    self.addItem(piece)
                    piece.setPos(random.randint(1, int(self.width()-pieceW)), random.randint(1, int(self.height()-pieceH)))
                