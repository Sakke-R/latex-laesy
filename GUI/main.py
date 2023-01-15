#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os

from PyQt5.QtWidgets import QApplication
from gui import GUI
from song_selector import Bookletizer


def main():
    booklet_format = None

    global app
    app = QApplication(sys.argv)
    song_selector = Bookletizer()

    gui = GUI(booklet_format, song_selector)


    sys.exit(app.exec_())


if __name__ == "__main__":
    main()