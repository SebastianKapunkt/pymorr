#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget,
                             QFileDialog, QGridLayout, QLabel, QMainWindow,
                             QPushButton, QWidget)

import pymorr
from view_utils import percentage_value, set_image_to_widget, set_widget_height


class Pymorr_View(QMainWindow):

    def __init__(self):
        super().__init__()

        self.morr = pymorr.Pymorr()
        self.morr.set_root('/Users/devbook/Downloads/Keep/')
        self.initUI()
        self.show_current_image()

    def initUI(self):
        self.keep_btn = QPushButton('Keep', self)
        self.keep_btn.clicked.connect(self.move_image_to_keep)

        self.maybe_btn = QPushButton('Maybe', self)
        self.maybe_btn.clicked.connect(self.move_image_to_maybe)

        self.delete_btn = QPushButton('Delete', self)
        self.delete_btn.clicked.connect(self.move_image_to_delete)

        self.undo_btn = QPushButton('Undo', self)
        self.undo_btn.clicked.connect(self.undo_last_move)

        self.current_image = QLabel(self)
        self.current_image.setAlignment(QtCore.Qt.AlignCenter)
        self.previous_image_1 = QLabel(self)
        self.previous_image_2 = QLabel(self)
        self.next_image_1 = QLabel(self)
        self.next_image_1.setAlignment(QtCore.Qt.AlignCenter)
        self.next_image_2 = QLabel(self)
        self.next_image_2.setAlignment(QtCore.Qt.AlignCenter)

        grid = QGridLayout()
        grid.setSpacing(5)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.layout().setContentsMargins(0, 0, 0, 0)

        grid.addWidget(self.current_image, 0, 0, 1, 0)
        grid.addWidget(self.next_image_2, 1, 0)
        grid.addWidget(self.next_image_1, 1, 1)
        grid.addWidget(self.previous_image_1, 1, 3)
        grid.addWidget(self.previous_image_2, 1, 4)
        grid.addWidget(self.keep_btn, 2, 0)
        grid.addWidget(self.maybe_btn, 2, 1)
        grid.addWidget(self.delete_btn, 2, 2)
        grid.addWidget(self.undo_btn, 2, 4)

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
        self.setWindowTitle("pymorr {}".format(self.morr.root))
        self.show()

    def fit_widgets_to_window(self):
        set_widget_height(self, self.current_image, 70)
        set_widget_height(self, self.undo_btn, 5)
        set_widget_height(self, self.keep_btn, 5)
        set_widget_height(self, self.maybe_btn, 5)
        set_widget_height(self, self.delete_btn, 5)
        set_widget_height(self, self.next_image_2, 20)
        set_widget_height(self, self.next_image_1, 20)
        set_widget_height(self, self.previous_image_1, 20)
        set_widget_height(self, self.previous_image_2, 20)

    def on_directory_selected(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, 'Open Folder', '/')
        self.setWindowTitle("pymorr {}".format(folder_path))
        self.morr.set_root(folder_path)
        self.show_current_image()

    def show_current_image(self):
        pictures = self.morr.get_image_paths_from_root()
        if len(pictures) > 0:
            set_image_to_widget(self, self.current_image,
                                pictures[0], 70, 95)
        else:
            self.current_image.clear()

        if len(pictures) > 1:
            set_image_to_widget(self, self.next_image_1, pictures[1], 20, 20)
        else:
            self.next_image_1.clear()

        if len(pictures) > 2:
            set_image_to_widget(self, self.next_image_2, pictures[2], 20, 20)
        else:
            self.next_image_2.clear()

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

    def resizeEvent(self, event):
        self.show_current_image()
        self.fit_widgets_to_window()
        QMainWindow.resizeEvent(self, event)


def main():
    app = QApplication(sys.argv)
    pymorr = Pymorr_View()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
