#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os

from PyQt5.QtWidgets import QApplication
from gui import GUI
from bookletizer import Bookletizer


def main():
    booklet_format = None
    if(not os.path.exists("GUI/a4_half")):
        os.mkdir("GUI/a4_half")

    global app
    app = QApplication(sys.argv)
    song_selector = Bookletizer()

    gui = GUI(booklet_format, song_selector)

    exit_code = app.exec_()
    for img in os.listdir("GUI/a4_half"):
       os.remove("GUI/a4_half/{}".format(img))

    sys.exit(exit_code)


if __name__ == "__main__":
    main()