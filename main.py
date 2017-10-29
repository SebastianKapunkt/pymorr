#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QMainWindow, QLabel,
                             QAction, QFileDialog,
                             QApplication, QGridLayout,
                             QWidget, QPushButton,
                             QDesktopWidget)
from PyQt5 import (QtGui, QtCore)
import pymorr
import sys


class Pymorr_View(QMainWindow):

    def __init__(self):
        super().__init__()

        self.morr = pymorr.Pymorr()
        self.morr.set_root('/Users/devbook/Downloads/Keep/')
        self.initUI()
        self.show_current_image()

    def initUI(self):

        self.directory_label_content = QLabel(self.morr.root)

        self.keep_btn = QPushButton('Keep', self)
        self.keep_btn.clicked.connect(self.move_image_to_keep)

        self.maybe_btn = QPushButton('Maybe', self)
        self.maybe_btn.clicked.connect(self.move_image_to_maybe)

        self.delete_btn = QPushButton('Delete', self)
        self.delete_btn.clicked.connect(self.move_image_to_delete)

        self.undo_btn = QPushButton('Undo', self)
        self.undo_btn.clicked.connect(self.undo_last_move)

        self.pic = QLabel(self)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.directory_label_content, 0, 0)
        grid.addWidget(self.undo_btn, 0, 1)

        grid.addWidget(self.pic, 1, 0, 1, 3)
        grid.addWidget(self.keep_btn, 2, 0)
        grid.addWidget(self.maybe_btn, 2, 1)
        grid.addWidget(self.delete_btn, 2, 2)

        widget = QWidget(self)
        self.setCentralWidget(widget)
        widget.setLayout(grid)

        openDirectory = QAction('Open', self)
        openDirectory.setShortcut('Ctrl+O')
        openDirectory.setStatusTip('Open Folder')
        openDirectory.triggered.connect(self.on_directory_selected)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(openDirectory)

        self.screenShape = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, self.screenShape.width(),
                         self.screenShape.height())
        self.setWindowTitle('File dialog')
        self.show()

    def on_directory_selected(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, 'Open Folder', '/')
        self.directory_label_content.setText(folder_path)
        self.morr.set_root(folder_path)
        self.show_current_image()

    def show_current_image(self):
        pictures = self.morr.get_image_paths_from_root()
        if len(pictures) > 0:
            next_image = pictures[0]
            self.image = QtGui.QPixmap(next_image).scaled(
                self.screenShape.width() / 1.05, self.screenShape.height() / 1.2, QtCore.Qt.KeepAspectRatio)
            self.pic.setPixmap(self.image)
        else:
            self.pic.clear()

    def move_image_to_keep(self):
        self.move_image(self.morr.prefered_folder['Keep'])

    def move_image_to_maybe(self):
        self.move_image(self.morr.prefered_folder['Maybe'])

    def move_image_to_delete(self):
        self.move_image(self.morr.prefered_folder['Delete'])

    def move_image(self, destination):
        pictures = self.morr.get_image_paths_from_root()
        if len(pictures) > 0:
            self.morr.move_image(
                pictures[0], destination)
            self.show_current_image()

    def undo_last_move(self):
        self.morr.undo_last_move()
        self.show_current_image()

def main():
    app = QApplication(sys.argv)
    pymorr = Pymorr_View()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
