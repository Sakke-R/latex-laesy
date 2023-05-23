from PyQt5 import QtWidgets, QtGui, QtCore
    
class PdfViewer(QtWidgets.QLabel):
    def __init__(self, parent, img, dual=True):
        super(PdfViewer, self).__init__()
        self.page_view = 0
        self.pages = 4
        self.gui = parent
        self.dual = dual

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

    def __init__(self, gui, parent, bookletizer, completer):
        super().__init__(parent)
        self.gui = gui
        self.song_selector = parent
        self.bookletizer = bookletizer
        self.setCompleter(completer)
        self.completer().activated.connect(self.onEnter)

    def onEnter(self):
        QtCore.QTimer.singleShot(0, self.clear)

    def updateCompleter(self):
        completer = QtWidgets.QCompleter(self.bookletizer.getAllTitles(), self.gui)
        completer.setCaseSensitivity(0)
        completer.setCompletionMode(QtWidgets.QCompleter.CompletionMode.PopupCompletion)
        self.setCompleter(completer)
        self.completer().activated.connect(self.onEnter)


    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == QtCore.Qt.Key.Key_Return:
            if(self.bookletizer.isMatch(self.displayText())):
                self.song_selector.addWidget(self.displayText())
                self.onEnter()
                self.gui.selected_songs.setFocus()
        elif a0.key() == QtCore.Qt.Key.Key_Left:
            self.gui.pdf_viewer.shiftViewLeft()
        elif a0.key() == QtCore.Qt.Key.Key_Right:
            self.gui.pdf_viewer.shiftViewRight()
        else:
            return super().keyPressEvent(a0)
        return None


class SongSelection(QtWidgets.QListWidget):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.gui = parent

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        
        row = self.currentRow()
        key = e.key()
        if key == QtCore.Qt.Key.Key_Return:
            self.addPageBreak()
        elif key == QtCore.Qt.Key.Key_Delete:
            item = self.takeItem(row)
        elif key == QtCore.Qt.Key.Key_Up:
            item = self.takeItem(row)
            self.insertItem(row - 1, item)
        elif key == QtCore.Qt.Key.Key_Down:
            item = self.takeItem(row)
            self.insertItem(row + 1, item)
        elif key == QtCore.Qt.Key.Key_Plus:
            item = self.takeItem(row)
            if item.getType() == "image":
                self.insertItem(row, item.addScale(0.05))
            else:
                self.insertItem(row, item)
                self.addVspace(0.15)
        elif key == QtCore.Qt.Key.Key_Minus:
            item = self.takeItem(row)
            if item.getType() == "image":
                self.insertItem(row, item.addScale(-0.05))
            else:
                self.insertItem(row, item)
                self.addVspace(-0.15)
        elif key == QtCore.Qt.Key.Key_Right:
            item = self.takeItem(row)
            if item.getType() == "image":
                self.insertItem(row, item.addOffset(0.15))
                self.setCurrentRow(row)
                return None
            else:
                self.insertItem(row, item)
        elif key == QtCore.Qt.Key.Key_Left:
            item = self.takeItem(row)
            if item.getType() == "image":
                self.insertItem(row, item.addOffset(-0.15))
                self.setCurrentRow(row)
                return None
            else:
                self.insertItem(row, item)


        self.setCurrentRow(row)

        return super().keyPressEvent(e)

    def addWidget(self, name):
        if ".jpg" in name or ".png" in name:
            return self.addImg(name)
        return self.addSong(name)

    def addSong(self, title, centered = False):
        if title not in self.getSongWidgetNames():
            self.insertItem(self.currentRow() + 1, SongWidget(title, centered))
            self.setCurrentRow(self.currentRow() + 1)
            return True
        return False

    def addImg(self, title):
        self.insertItem(self.currentRow() + 1, GraphicalWidget(title))
        self.setCurrentRow(self.currentRow() + 1)

    def getSongWidgetNames(self):
        return list([widget.text() for widget in self.getWidgets() if widget.widget_type == "song"])

    def getWidgetNames(self):
        return list(map(lambda x: x.text(), self.getWidgets()))
    
    def getWidgets(self):
        return list([self.item(x) for x in range(self.count())])

    def addVspace(self, amount):
        def handleRow(row):
            row_item = self.takeItem(row)
            if isinstance(row_item, VspaceWidget):
                new_vspace = row_item + amount
                if new_vspace: # Not none
                    self.insertItem(row, new_vspace)
                self.setCurrentRow(row)
                return True
            self.insertItem(row, row_item)
            return False

        row = self.currentRow()
        if(row < 1):
            return False

        # Add to selected vspacewidget or one above current song title
        if handleRow(row) or handleRow(row - 1):
            return True

        # If there isn't a vspacewidget already then create one
        self.insertItem(row, VspaceWidget(amount))
        self.setCurrentRow(row + 1)
        return True

    def addPageBreak(self):
        self.insertItem(self.currentRow() + 1, PagebreakWidget())
        self.setCurrentRow(self.currentRow() + 1)


class GuiListWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, name, widget_type, centering = False):
        super().__init__(name)
        self.widget_type = widget_type
        self.centering = centering
    
    def getType(self):
        return self.widget_type
    
    def getCentering(self):
        return self.centering

class SongWidget(GuiListWidgetItem):
    def __init__(self, title, centered = False):
        super().__init__(title, "song", centered)
        self.title = title

    def getTitle(self):
        return self.title

class VspaceWidget(GuiListWidgetItem):

    def __init__(self, size: float):
        super().__init__("Vert space: {}".format(size), "vspace")
        self.size = size

    def getSize(self):
        return self.size
    
    def __add__(self, amount: float):
        self.size += amount
        if self.size == 0:
            return None
        return VspaceWidget(round(self.size, 2))


class GraphicalWidget(GuiListWidgetItem):

    def __init__(self, graphic_name, scale = 0.8, horizontal_offset = 0.):
        display_name = graphic_name
        if scale != 0.8:
            display_name += f", sc: {scale}"
        if horizontal_offset != 0:
            display_name += f", hspace: {horizontal_offset}"
        super().__init__(display_name, "image")
        self.name = graphic_name
        self.scale = scale
        self.horizontal_offset = horizontal_offset

    def getScale(self):
        return self.scale
    
    def getTitle(self):
        return self.name
    
    def getOffset(self):
        return self.horizontal_offset


    def addScale(self, amount):
        return GraphicalWidget(self.name, round(self.scale + amount, 3), self.horizontal_offset)

    def addOffset(self, offset):
        return GraphicalWidget(self.name, self.scale, round(self.horizontal_offset + offset, 3))


class PagebreakWidget(GuiListWidgetItem):

    def __init__(self):
        super().__init__("Page break", "pagebreak")
