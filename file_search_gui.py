#!/usr/bin/env python3


"""
This is a simple gui app made with PyQt5 for file searching.

Author: P SURYA TEJA
Last Modified: 10122017 IST
"""


import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class FileSearch(QMainWindow):
    def __init__(self, parent=None):
        super(FileSearch, self).__init__(parent)

        directory_label = QLabel("Select or Enter Directory Path")
        search_term_label = QLabel("Enter Part Of The Filename.")

        self.directory_input = QLineEdit()
        self.directory_input.setPlaceholderText("Enter the directory path or select it. [ESC to clear]")
        self.directory_input.setToolTip("Folder to Search")
        self.directory_input.returnPressed.connect(self.verifyInput)

        directory_selection_button = QPushButton('Select Folder')
        directory_selection_button.clicked.connect(self.selectFolder)

        self.search_term_input = QLineEdit()
        self.search_term_input.setPlaceholderText("Enter the search term and press Enter to search.  [ESC to clear]")
        self.search_term_input.setToolTip("Part of the filename you are searching for.")
        self.search_term_input.returnPressed.connect(self.verifyInput)

        search_button = QPushButton('Search')
        search_button.clicked.connect(self.verifyInput)

        self.result_box = QTextBrowser()
        self.result_box.setFocusPolicy(Qt.NoFocus)
        self.directory_input.setText("/home/suri")
        self.search_term_input.setText("abcd")
        # self.result_box.setStyleSheet("QTextBrowser {line-height: 10px;}")

        main_layout = QGridLayout()
        main_layout.addWidget(directory_label, 0, 0)
        main_layout.addWidget(self.directory_input, 0, 1)
        main_layout.addWidget(directory_selection_button, 0, 2)
        main_layout.addWidget(search_term_label, 1, 0)
        main_layout.addWidget(self.search_term_input, 1, 1)
        main_layout.addWidget(search_button, 1, 2)
        main_layout.addWidget(self.result_box, 2, 0, 1, 3)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        # creating status bar
        self.status = self.statusBar()
        self.status.setSizeGripEnabled(False)
        self.status.showMessage("Ready", 5000)

        self.setCentralWidget(central_widget)
        self.setMinimumSize(900, 600)
        self.setFont(QFont('Ubuntu', pointSize=11, weight=-3, italic=False))
        self.setWindowTitle("File Search")
        self.show()

    def keyPressEvent(self, e):
        # pressing Esc when in any of the two lineedits clears the contents
        if e.key() == Qt.Key_Escape:
            if self.directory_input.hasFocus():
                self.directory_input.clear()
            elif self.search_term_input.hasFocus():
                self.search_term_input.clear()

    def verifyInput(self):
        directory = self.directory_input.text()
        search_term = self.search_term_input.text()
        self.files_found = 0
        self.directories_found = 0
        # shows an error tooltip if directory is invalid or empty
        if not os.path.isdir(directory):
            QToolTip.showText(self.directory_input.mapToGlobal(QPoint(0, 5)), "Enter a Valid Directory")
            return
        # shows an error tooltip if search term is empty
        elif not search_term:
            QToolTip.showText(self.search_term_input.mapToGlobal(QPoint(0, 5)), "Enter Something")
        else:
            self.status.showMessage("Searching...")
            self.searchFiles(directory, True)
            self.updateStatusBar(still_searching=False)


    def selectFolder(self):
        """this method opens a file selection dialog that lets the user select a directory.
        """
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        folder = dialog.getExistingDirectory(self, "Select Directory")
        self.directory_input.setText(folder)

    def searchFiles(self, directory, user_called):
        """this is a recursive method.
        this method checks the entire directory for matching files.
        if there are any files that contain the search term they will be appended to result box.
        if there are any directories in the current searching directory, then the function will
        be called recursively with the new directory path.
        """
        # if this method is called as a result of user interaction like pressing enter,
        # result box will be cleared as it is a new search
        if user_called:
            self.result_box.clear()
        search_term = self.search_term_input.text().lower()
        try:
            # looping all files in the directory
            for each_file in os.listdir(directory):
                # converting filename to full path
                full_path = os.path.join(directory, each_file)
                # if it is a directory and not a sym link
                if os.path.isdir(full_path) and not os.path.islink(full_path):
                    # if the directory name contains the search term
                    if search_term in each_file.lower():
                        self.directories_found += 1
                        self.updateStatusBar(True)
                        each_file = each_file.lower().replace(search_term, '<b>' + search_term + '</b>')
                        self.result_box.append("directory: {}".format(os.path.join(directory, each_file)))
                    self.searchFiles(full_path, False)
                # if it is a file and search term matches
                elif os.path.isfile(full_path) and ( search_term in each_file.lower() ):
                    self.files_found += 1
                    each_file = each_file.lower().replace(search_term, '<b>' + search_term + '</b>')
                    self.result_box.append("File: {}".format(os.path.join(directory, each_file)))
        # if the program is denied access
        except PermissionError as e:
            e = str(e)
            # extracting the path of the directory the program is denied access from error message
            error_path = e[e.index("'") + 1 : len(e) - 1]
            self.result_box.append("<b>Denied access to {}.</b>".format(error_path))

    def updateStatusBar(self, still_searching=True):
        if still_searching:
            message_beginning = 'Searching...'
        else:
            message_beginning = 'Search Complete.'
        self.status.showMessage("{}  Files Found: {}"
                                "  Directories Found: {}".format(message_beginning,
                                                                 self.files_found,
                                                                 self.directories_found))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = FileSearch()
    app.exec_()
