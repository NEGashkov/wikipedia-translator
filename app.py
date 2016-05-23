#!/usr/bin/python3
# -*- coding: utf-8 -*- #

# app.py
# Wikipedia Translator
# Created by Nick Gashkov on 22.04.16
# Copyright © 2016 Nick Gashkov. All rights reserved.

"""Wikipedia Translator

Following code is main file, used to execute the app.

"""

import sys

from gui import MainWindow

from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':

    application = QApplication(sys.argv)
    app = MainWindow()
    sys.exit(application.exec_())
