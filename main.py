#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget,
                             QFileDialog, QGridLayout, QLabel, QMainWindow,
                             QPushButton, QWidget)

import controller
from view_utils import percentage_value, set_image_to_widget, set_widget_height


class Pymorr_View(QMainWindow):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.create_view_elements()
        self.set_event_listners()
        self.setup_layout()
        # attach view
        self.controller.attach_view(self)
        # finally show UI
        self.initUI()

    def create_view_elements(self):
        # create buttons
        self.keep_btn = QPushButton('Keep', self)
        self.maybe_btn = QPushButton('Maybe', self)
        self.delete_btn = QPushButton('Delete', self)
        self.undo_btn = QPushButton('Undo', self)

        # create image previews
        self.current_image = QLabel(self)
        self.current_image.setAlignment(QtCore.Qt.AlignCenter)
        self.previous_image_1 = QLabel(self)
        self.previous_image_1.setAlignment(QtCore.Qt.AlignCenter)
        self.previous_image_2 = QLabel(self)
        self.previous_image_2.setAlignment(QtCore.Qt.AlignCenter)
        self.next_image_1 = QLabel(self)
        self.next_image_1.setAlignment(QtCore.Qt.AlignCenter)
        self.next_image_2 = QLabel(self)
        self.next_image_2.setAlignment(QtCore.Qt.AlignCenter)

        # create layout
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.layout().setContentsMargins(0, 0, 0, 0)

    def setup_layout(self):
        grid = self.grid

        grid.addWidget(self.current_image, 1, 0, 1, 0)
        grid.addWidget(self.next_image_2, 0, 0)
        grid.addWidget(self.next_image_1, 0, 1)
        grid.addWidget(self.previous_image_1, 0, 3)
        grid.addWidget(self.previous_image_2, 0, 4)
        grid.addWidget(self.keep_btn, 2, 0)
        grid.addWidget(self.maybe_btn, 2, 1)
        grid.addWidget(self.delete_btn, 2, 2)
        grid.addWidget(self.undo_btn, 2, 4)

        widget = QWidget(self)
        self.setCentralWidget(widget)
        widget.setLayout(grid)

    def set_event_listners(self):
        # Button event listners
        self.keep_btn.clicked.connect(self.move_image_to_keep)
        self.maybe_btn.clicked.connect(self.move_image_to_maybe)
        self.delete_btn.clicked.connect(self.move_image_to_delete)
        self.undo_btn.clicked.connect(self.undo_last_move)

    def setup_menubar(self):
        openDirectory = QAction('Open', self)
        openDirectory.setShortcut('Ctrl+O')
        openDirectory.setStatusTip('Open Folder')
        openDirectory.triggered.connect(self.on_directory_selected)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(openDirectory)

    def initUI(self):
        self.screenShape = QDesktopWidget().screenGeometry()
        self.setGeometry(
            0,
            0,
            self.screenShape.width(),
            self.screenShape.height()
        )
        self.setWindowTitle("pymorr {}".format(self.controller.get_path()))
        self.show()

    def on_directory_selected(self):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            'Open Folder',
            '/'
        )
        self.setWindowTitle("pymorr {}".format(folder_path))
        self.controller.set_path(folder_path)

    def update_images(self, next_images, previous_images):
        # central image
        if len(next_images) > 0:
            set_image_to_widget(
                self,
                self.current_image,
                next_images[0], 70, 95
            )
        else:
            self.current_image.clear()

        # next upcoming picture
        if len(next_images) > 1:
            set_image_to_widget(
                self,
                self.next_image_1,
                next_images[1], 20, 19
            )
        else:
            self.next_image_1.clear()

        # second next upcoming picture
        if len(next_images) > 2:
            set_image_to_widget(
                self,
                self.next_image_2,
                next_images[2], 20, 19
            )
        else:
            self.next_image_2.clear()

        # prevoius image
        if len(previous_images) > 0:
            set_image_to_widget(
                self,
                self.previous_image_1,
                previous_images[len(previous_images) - 1], 20, 19
            )
        else:
            self.previous_image_1.clear()

        # second prevoius image
        if len(previous_images) > 1:
            set_image_to_widget(
                self,
                self.previous_image_2,
                previous_images[len(previous_images) - 2], 20, 19
            )
        else:
            self.previous_image_2.clear()

    def move_image_to_keep(self):
        self.controller.move_image('Keep')

    def move_image_to_maybe(self):
        self.controller.move_image('Maybe')

    def move_image_to_delete(self):
        self.controller.move_image('Delete')

    def undo_last_move(self):
        self.controller.undo_last_move()

    def fit_widgets_height_to_window(self):
        set_widget_height(self, self.current_image, 70)
        set_widget_height(self, self.undo_btn, 5)
        set_widget_height(self, self.keep_btn, 5)
        set_widget_height(self, self.maybe_btn, 5)
        set_widget_height(self, self.delete_btn, 5)
        set_widget_height(self, self.next_image_2, 20)
        set_widget_height(self, self.next_image_1, 20)
        set_widget_height(self, self.previous_image_1, 20)
        set_widget_height(self, self.previous_image_2, 20)

    def resizeEvent(self, event):
        self.controller.request_content()
        self.fit_widgets_height_to_window()
        QMainWindow.resizeEvent(self, event)


def main():
    app = QApplication(sys.argv)
    pymorr_controller = controller.PymorrController()
    Pymorr_View(pymorr_controller)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
