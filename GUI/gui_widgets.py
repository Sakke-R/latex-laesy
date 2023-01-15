from PyQt5 import QtWidgets, QtGui, QtCore

    
class PdfViewer(QtWidgets.QLabel):
    def __init__(self, parent, img):
        super(PdfViewer, self).__init__()
        self.page_view = 0
        self.pages = 1
        self.gui = parent
        self.setFrameStyle(QtWidgets.QFrame.Shape.StyledPanel)
        self.pixmap = QtGui.QPixmap(img)

    def shiftViewRight(self):
        if self.page_view < self.pages - 1:
            self.page_view += 1
            self.gui.update_pdf_viewer(self.page_view)

    def shiftViewLeft(self):
        if self.page_view > 0:
            self.page_view -= 1
            self.gui.update_pdf_viewer(self.page_view)

    def updatePageNum(self, num):
        self.pages = num

    def paintEvent(self, event):
        """Courtesy of stackoverflow https://stackoverflow.com/questions/24106903/resizing-qpixmap-while-maintaining-aspect-ratio """
        size = self.size()
        painter = QtGui.QPainter(self)
        point = QtCore.QPoint(0,0)
        scaledPix = self.pixmap.scaled(size, aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                             transformMode= QtCore.Qt.TransformationMode.SmoothTransformation)
        # start painting the label from left upper corner
        point.setX(int((size.width() - scaledPix.width())/2))
        point.setY(int((size.height() - scaledPix.height())/2))
        painter.drawPixmap(point, scaledPix)

    def changePixmap(self, img):
        self.pixmap = QtGui.QPixmap(img)
        self.repaint() # repaint() will trigger the paintEvent(self, event), this way the new pixmap will be drawn on the label
    

class SearchBar(QtWidgets.QLineEdit):

    def __init__(self, parent, song_selector):
        super().__init__(parent)
        self.gui = parent
        self.song_selector = song_selector

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == QtCore.Qt.Key.Key_Return:
            if(self.song_selector.isMatch(self.displayText())):
                self.gui.add_song_title(self.displayText())
                self.setText("")
        elif a0.key() == QtCore.Qt.Key.Key_Left:
            self.gui.pdf_viewer.shiftViewLeft()
        elif a0.key() == QtCore.Qt.Key.Key_Right:
            self.gui.pdf_viewer.shiftViewRight()
        return super().keyPressEvent(a0)

class SongSelection(QtWidgets.QListWidget):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.gui = parent

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == QtCore.Qt.Key.Key_Delete:
            self.takeItem(self.currentRow())
        elif e.key() == QtCore.Qt.Key.Key_Up:
            row = self.currentRow()
            item = self.takeItem(row)
            self.insertItem(row - 1, item)
            self.setCurrentRow(row)
        elif e.key() == QtCore.Qt.Key.Key_Down:
            row = self.currentRow()
            item = self.takeItem(row)
            self.insertItem(row + 1, item)
            self.setCurrentRow(row)

        return super().keyPressEvent(e)

    def getSongTitles(self):
        return [self.item(x).text() for x in range(self.count())]