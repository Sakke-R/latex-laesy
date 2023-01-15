import numpy as np
import threading

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
        #self.init_buttons()
        #self.init_sliders()
        self.selected_songs.addSong("Askiin")
        print(self.selected_songs.getWidgetNames())

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.pdf_viewer.repaint)
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
        
        self.search_bar = SearchBar(self, self.bookletizer)
        self.search_bar.setGeometry(0, 0, int(width/2), int(height/20))

        # Create and add a completer for the search bar
        self.completer = QtWidgets.QCompleter(self.bookletizer.getAllSongTitles(), self)
        self.completer.setCaseSensitivity(0)
        self.completer.setCompletionMode(QtWidgets.QCompleter.CompletionMode.PopupCompletion)
        self.search_bar.setCompleter(self.completer)
        
        # Finally add the search bar to the vertical layout
        left_vertical.addWidget(self.search_bar, 10)

        self.selected_songs = SongSelection(self)
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
        self.pdf_viewer.changePixmap("GUI/a4_half/{}.png".format(page))

    def generateNewView(self):
        self.bookletizer.generateTexFile(self.selected_songs.getWidgetNames())
        images = convert_from_path("a4_half_generated.pdf", thread_count=4, fmt="png")
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
        self.update_pdf_viewer(self.pdf_viewer.page_view)

    def newViewGenerationThread(self):
        thread = threading.Thread(target=self.generateNewView)
        thread.start()
        thread.join()

    def addSong(self, title):
        self.selected_songs.addSong(title)
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
        return super().keyPressEvent(a0)