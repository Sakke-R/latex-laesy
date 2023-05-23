import numpy as np
import threading
import os

from PyQt5 import QtWidgets, QtGui, QtCore
from pdf2image import convert_from_path
from PIL import Image

from gui_widgets import PdfViewer, SearchBar, SongSelection

class GUI(QtWidgets.QMainWindow):
        
    def __init__(self, booklet_format, bookletizer):
        super().__init__()
        self.format = booklet_format
        self.bookletizer = bookletizer

        self.setCentralWidget(QtWidgets.QWidget())
        self.horizontal = QtWidgets.QHBoxLayout()
        self.centralWidget().setLayout(self.horizontal)
        
        self.width, self.height = 1000, 700

        self.init_window()
        self.init_pdf_viewer()
        self.selected_songs.addSong("Kenompi Phuksi")
        self.selected_songs.addSong("Askiin")

        self.selected_songs.addPageBreak()
        self.selected_songs.addSong("Ikuisen Teekkarin Laulu", True)

        print(self.selected_songs.getWidgets())

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.pdf_viewer.repaint)
        self.timer.timeout.connect(self.bookletizer.initializeLibrary)
        self.timer.start(10)

    def init_window(self):
        """Sets initial geometry and visuals of window"""
        # Get geometry of desktop
        width, height = self.width, self.height
        desktopRect = QtWidgets.QApplication.desktop().availableGeometry(self)
        center_point = desktopRect.center()

        # Define offset to adjust center
        offset = QtCore.QPoint(int(width/2), int(height/2))
        
        windowRect = QtCore.QRect(center_point - offset, center_point + offset)
        self.setGeometry(windowRect)
        self.setWindowTitle('Läsy tunkki v1')

        # Create a layout for displaying the left side widgets
        left_vertical = QtWidgets.QVBoxLayout()
        
        # Add widgets for displaying search bar, selected songs and output page
        self.selected_songs = SongSelection(self)

    
        # Create and add a completer for the search bar
        completer = QtWidgets.QCompleter(self.bookletizer.getAllTitles(), self)
        completer.setCaseSensitivity(0)
        completer.setCompletionMode(QtWidgets.QCompleter.CompletionMode.PopupCompletion)
        
        self.search_bar = SearchBar(self, self.selected_songs, self.bookletizer, completer)
        self.search_bar.setGeometry(0, 0, int(width/2), int(height/20))
        
        # Finally add the search bar to the vertical layout
        left_vertical.addWidget(self.search_bar, 10)


        self.selected_songs.setGeometry(0, int(height/20), int(width/2), height - int(height/20))
        #self.selected_songs.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        left_vertical.addWidget(self.selected_songs, 85)

        self.generate_btn = QtWidgets.QPushButton("Generate pages", self)
        self.generate_btn.clicked.connect(self.generateNewView)
        left_vertical.addWidget(self.generate_btn)

        self.horizontal.addLayout(left_vertical, 30)
        #self.selected_songs.show()
        self.show()

    def init_pdf_viewer(self):
        self.pdf_viewer = PdfViewer(self, "GUI/placeholder.png")
        self.pdf_viewer.setGeometry(int(self.width/2), 0, int(self.width / 2), self.height)
        self.pdf_viewer.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)

        self.horizontal.addWidget(self.pdf_viewer, 70)
        self.pdf_viewer.show()

    def update_pdf_viewer(self, page):
        if os.path.exists("GUI/a4_half/{}.png".format(page)):
            self.pdf_viewer.changePixmap("GUI/a4_half/{}.png".format(page))
        else:
            self.generateNewView(page)

    def generateNewView(self, first_pg = None):
        self.bookletizer.generateTexFile(self.selected_songs.getWidgets())
        images = convert_from_path("a4_half_generated.pdf", thread_count=4, fmt="png", first_page = first_pg)
        if self.pdf_viewer.dual:
            print(len(images))
            
            new_images = [Image.fromarray(np.hstack([images[-1], images[0]]))]
            
            for i in range(1, int(len(images) / 2)): # There should always be at least 4 images
                combined_imgs = np.hstack([images[i*2 - 1], images[i*2]])
                new_images.append(Image.fromarray(combined_imgs))
            images = new_images

        self.pdf_viewer.updatePageNum(len(images))

        for i, img in enumerate(images):
            img.save("GUI/a4_half/{}.png".format(i), 'PNG')

        if os.path.exists("GUI/a4_half/{}.png".format(self.pdf_viewer.page_view)):
            self.pdf_viewer.changePixmap("GUI/a4_half/{}.png".format(self.pdf_viewer.page_view))
        #self.update_pdf_viewer(self.pdf_viewer.page_view)

    def newViewGenerationThread(self):
        thread = threading.Thread(target=self.generateNewView)
        thread.start()
        thread.join()

    def addSong(self, title, center = False):
        self.selected_songs.addSong(title, center)
        self.selected_songs.setFocus()

    def addImg(self, title):
        self.selected_songs.addImg(title)
        self.selected_songs.setFocus()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
        elif a0.key() == QtCore.Qt.Key.Key_Right:
            print("Right")
            self.pdf_viewer.shiftViewRight()
        elif a0.key() == QtCore.Qt.Key.Key_Left:
            print("Left")
            self.pdf_viewer.shiftViewLeft()
        else:
            return super().keyPressEvent(a0)
        return None
