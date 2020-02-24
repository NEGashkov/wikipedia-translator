#!/usr/bin/python3
# -*- coding: utf-8 -*- #

# gui.py
# Wikipedia Translator
# Created by Nick Gashkov on 22.04.16
# Copyright © 2016 Nick Gashkov. All rights reserved.

"""Wikipedia Translator

Following code implements graphical user interface of the app.

"""

import os.path

from core import Translator

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QMainWindow

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__style__ = open(os.path.join(__location__, 'style_file.qss')).read()

class MainWindow(QMainWindow):

    """Main Window Class

    Following class contains several public functions to implement GUI of the app.

    """

    def __init__(self):

        """Initialize Function

        Following function creates main window and executes all other initialization functions.

        Args:
            QMainWindow object: main window of the app.

        Returns:
            None

        """

        super().__init__()

        self.resize(600, 200)
        self.init_ui()
        self.setStyleSheet(__style__)

        self.show()

    def init_ui(self):

        """Initialize User Interface Function

        Following function executes all other initialization functions, defining whole look of the app.

        Args:
            QMainWindow object: main window of the app.

        Returns:
            None

        """

        self.init_combo_box()
        self.init_text_edit()
        self.init_push_button()

    def init_combo_box(self):

        """Initialize Combo Boxes Function

        Following function defines all of the combo boxes of the app.

        Args:
            QMainWindow object: main window of the app.

        Returns:
            None

        """

        self.adjust_query = QComboBox(self)
        self.adjust_query.resize(200, 40)
        self.adjust_query.move(150, 140)

    def init_text_edit(self):

        """Initialize Text Edits Function

        Following function defines all of the text edits of the app.

        Args:
            QMainWindow object: main window of the app.

        Returns:
            None

        """

        self.russian_text_edit = QTextEdit(self)
        self.russian_text_edit.setPlaceholderText('Введите термин')
        self.russian_text_edit.setStyleSheet(__style__)
        self.russian_text_edit.resize(250, 100)
        self.russian_text_edit.move(20, 20)

        self.english_text_edit = QTextEdit(self)
        self.english_text_edit.setPlaceholderText('Enter term')
        self.english_text_edit.setStyleSheet(__style__)
        self.english_text_edit.resize(250, 100)
        self.english_text_edit.move(330, 20)

    def init_push_button(self):

        """Initialize Buttons Function

        Following function defines all of the buttons of the app.

        Args:
            QMainWindow object: main window of the app.

        Returns:
            None

        """

        self.translate_to_english_button = QPushButton('>', self)
        self.translate_to_english_button.clicked.connect(self.translate_to_english_button_clicked)
        self.translate_to_english_button.resize(20, 20)
        self.translate_to_english_button.move(290, 40)

        self.translate_to_russian_button = QPushButton('<', self)
        self.translate_to_russian_button.clicked.connect(self.translate_to_russian_button_clicked)
        self.translate_to_russian_button.resize(20, 20)
        self.translate_to_russian_button.move(290, 80)

        self.adjust_query_button = QPushButton('Adjust query', self)
        self.adjust_query_button.clicked.connect(self.adjust_query_button_clicked)
        self.adjust_query_button.resize(100, 30)
        self.adjust_query_button.move(370, 140)

    def translate_to_english_button_clicked(self):

        """Translate to English Button Clicked Function

        Following function implements logic, executing when user wants to translate term into English.

        Args:
            QMainWindow object: main window of the app.

        Returns:
            None

        """

        term = self.russian_text_edit.toPlainText()
        self.language = 'ru'
        search_result = Translator.search_user_term(term, self.language)

        if Translator.translate_user_term(term, self.language)[0] == '0':
            self.adjust_query.clear()
            for item in search_result:
                self.adjust_query.addItem(item)
            term = self.adjust_query.currentText()
            self.english_text_edit.setText(
                Translator.translate_user_term(term, self.language)[1:]
            )
        else:
            QMessageBox.warning(
                self,
                'Error',
                Translator.translate_user_term(term, self.language)[1:],
                QMessageBox.Ok,
            )

    def translate_to_russian_button_clicked(self):

        """Translate to Russian Button Clicked Function

        Following function implements logic, executing when user wants to translate term into Russian.

        Args:
            QMainWindow object: main window of the app.

        Returns:
            None

        """

        term = self.english_text_edit.toPlainText()
        self.language = 'en'
        search_result = Translator.search_user_term(term, self.language)

        if Translator.translate_user_term(term, self.language)[0] == '0':
            self.adjust_query.clear()
            for item in search_result:
                self.adjust_query.addItem(item)
            term = self.adjust_query.currentText()
            self.russian_text_edit.setText(
                Translator.translate_user_term(term, self.language)[1:]
            )
        else:
            QMessageBox.warning(
                self,
                'Error',
                Translator.translate_user_term(term, self.language)[1:],
                QMessageBox.Ok,
            )

    def adjust_query_button_clicked(self):

        """Adjust Query Button Clicked Function

        Following function implements logic, executing when user wants to adjust query.

        Args:
            QMainWindow object: main window of the app.

        Returns:
            None

        """

        try:
            term = self.adjust_query.currentText()
            adjust_language = self.language
            search_result = Translator.search_user_term(term, adjust_language)

            if Translator.translate_user_term(term, adjust_language)[0] == '0':
                if adjust_language == 'en':
                    self.russian_text_edit.setText(Translator.translate_user_term(term, adjust_language)[1:])
                else:
                    self.english_text_edit.setText(Translator.translate_user_term(term, adjust_language)[1:])
            else:
                QMessageBox.warning(self, 'Error', Translator.translate_user_term(term, adjust_language)[1:], QMessageBox.Ok)
        except UnboundLocalError:
            QMessageBox.warning(self, 'Error', 'Input term to translate first', QMessageBox.Ok)
