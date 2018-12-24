#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget,
                             QFileDialog, QGridLayout, QLabel, QMainWindow,
                             QPushButton, QWidget, QHBoxLayout)

import controller
from image_loader import ImageWorker
from view_utils import set_widget_height, get_scale_pixmap, set_widget_width


class Pymorr_View(QMainWindow):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.create_view_elements()
        self.set_event_listners()
        self.setup_menubar()
        self.setup_layout()
        # create threadpool
        self.threadpool = QThreadPool()
        # attach view
        self.controller.attach_view(self)
        # finally show UI
        self.initUI()
        # hide compare view
        self.hide_compare_widget()

    def create_view_elements(self):
        # create buttons
        self.keep_btn = QPushButton('Behalten', self)
        self.maybe_btn = QPushButton('Vielleicht', self)
        self.delete_btn = QPushButton('Löschen', self)
        self.undo_btn = QPushButton('Zurück', self)
        self.close_compare_btn = QPushButton('Close Compare', self)

        # create image previews
        self.current_image = QLabel(self)
        self.current_image.setAlignment(Qt.AlignCenter)
        self.compare_image = QLabel(self)
        self.compare_image.setAlignment(Qt.AlignCenter)
        self.previous_image_1 = QLabel(self)
        self.previous_image_1.setAlignment(Qt.AlignCenter)
        self.previous_image_2 = QLabel(self)
        self.previous_image_2.setAlignment(Qt.AlignCenter)
        self.next_image_1 = QLabel(self)
        self.next_image_1.setAlignment(Qt.AlignCenter)
        self.next_image_2 = QLabel(self)
        self.next_image_2.setAlignment(Qt.AlignCenter)

        # create layout
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.layout().setContentsMargins(0, 0, 0, 0)

        # compare h-box
        self.compare_box = QHBoxLayout()
        self.compare_box.setAlignment(Qt.AlignCenter)
        self.compare_box.setContentsMargins(0, 0, 0, 0)
        self.compare_box.layout().setContentsMargins(0, 0, 0, 0)

        # close compare h-box
        self.compare_close_box = QHBoxLayout()
        self.compare_close_box.setContentsMargins(0, 0, 0, 0)
        self.compare_close_box.layout().setContentsMargins(0, 0, 0, 0)

    def setup_layout(self):
        grid = self.grid

        self.compare_box.addStretch()
        self.compare_box.addWidget(self.current_image)
        self.compare_box.addWidget(self.compare_image)
        self.compare_box.addStretch()
        self.compare_close_box.addStretch()
        self.compare_close_box.addWidget(self.close_compare_btn)
        grid.addWidget(self.next_image_2, 0, 0)
        grid.addWidget(self.next_image_1, 0, 1)
        grid.addWidget(self.previous_image_1, 0, 3)
        grid.addWidget(self.previous_image_2, 0, 4)
        grid.addLayout(self.compare_close_box, 1, 0, 1, 0)
        grid.addLayout(self.compare_box, 2, 0, 1, 0)
        grid.addWidget(self.keep_btn, 3, 0)
        grid.addWidget(self.maybe_btn, 3, 1)
        grid.addWidget(self.delete_btn, 3, 2)
        grid.addWidget(self.undo_btn, 3, 4)

        widget = QWidget(self)
        self.setCentralWidget(widget)
        widget.setLayout(grid)

    def set_event_listners(self):
        # Button event listners
        self.keep_btn.clicked.connect(self.move_image_to_keep)
        self.maybe_btn.clicked.connect(self.move_image_to_maybe)
        self.delete_btn.clicked.connect(self.move_image_to_delete)
        self.undo_btn.clicked.connect(self.undo_last_move)
        self.close_compare_btn.clicked.connect(self.close_compare_clicked)
        self.previous_image_1.mouseReleaseEvent = self.previous_image_1_clicked
        self.previous_image_2.mouseReleaseEvent = self.previous_image_2_clicked
        self.next_image_1.mouseReleaseEvent = self.next_image_1_clicked
        self.next_image_2.mouseReleaseEvent = self.next_image_2_clicked

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
        print("show UI")
        self.show()

    def on_directory_selected(self):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            'Open Folder',
            '/'
        )
        self.setWindowTitle("pymorr {}".format(folder_path))
        self.controller.set_path(folder_path)

    def previous_image_1_clicked(self, event):
        self.show_compare_widget(
            self.previous_image_1.image_path
        )

    def previous_image_2_clicked(self, event):
        self.show_compare_widget(
            self.previous_image_2.image_path
        )

    def next_image_1_clicked(self, event):
        self.show_compare_widget(
            self.next_image_1.image_path
        )

    def next_image_2_clicked(self, event):
        self.show_compare_widget(
            self.next_image_2.image_path
        )

    def close_compare_clicked(self):
        self.hide_compare_widget()
        self.controller.request_content()

    def hide_compare_widget(self):
        self.close_compare_btn.setHidden(True)
        self.compare_image.setHidden(True)

    def show_compare_widget(self, path):
        set_widget_width(self, self.current_image, 46)
        self.close_compare_btn.setHidden(False)
        self.compare_image.setHidden(False)
        self.compare_image.image_path = path
        self.controller.request_content()

    def start_image_worker(self, path, widget_name, width, height):
        worker = ImageWorker(
            path,
            widget_name,
            width,
            height
        )
        worker.signals.result.connect(self.set_image)
        self.threadpool.start(worker)

    def update_images(self, next_images, previous_images):
        # central image
        if len(next_images) > 0:
            if self.close_compare_btn.isHidden():
                set_widget_width(self, self.current_image, 90)
                self.start_image_worker(
                    next_images[0],
                    'current_image',
                    90,
                    69
                )
            else:
                set_widget_width(self, self.current_image, 46)
                self.start_image_worker(
                    next_images[0],
                    'current_image',
                    46,
                    69
                )
                set_widget_width(self, self.compare_image, 46)
                if hasattr(self.compare_image, 'image_path'):
                    self.start_image_worker(
                        self.compare_image.image_path,
                        'compare_image',
                        46,
                        69
                    )
            self.current_image.image_path = next_images[0]
        else:
            self.current_image.clear()

        # next upcoming picture
        if len(next_images) > 1:
            self.start_image_worker(
                next_images[1],
                "next_image_1",
                19,
                20
            )
            self.next_image_1.image_path = next_images[1]
        else:
            self.next_image_1.clear()

        # second next upcoming picture
        if len(next_images) > 2:
            self.start_image_worker(
                next_images[2],
                "next_image_2",
                19,
                20
            )
            self.next_image_2.image_path = next_images[2]
        else:
            self.next_image_2.clear()

        # prevoius image
        if len(previous_images) > 0:
            self.start_image_worker(
                previous_images[len(previous_images) - 1],
                "previous_image_1",
                19,
                20
            )
            self.previous_image_1.image_path = previous_images[
                len(previous_images) - 1
            ]
        else:
            self.previous_image_1.clear()

        # second prevoius image
        if len(previous_images) > 1:
            self.start_image_worker(
                previous_images[len(previous_images) - 2],
                "previous_image_2",
                19,
                20
            )
            self.previous_image_2.image_path = previous_images[
                len(previous_images) - 2
            ]
        else:
            self.previous_image_2.clear()

    def set_image(self, holder):
        pixmap = get_scale_pixmap(
            self, holder.image, holder.height, holder.width
        )

        if holder.widget_name == 'current_image':
            self.current_image.setPixmap(pixmap)
        if holder.widget_name == 'compare_image':
            self.compare_image.setPixmap(pixmap)
        if holder.widget_name == 'previous_image_1':
            self.previous_image_1.setPixmap(pixmap)
        if holder.widget_name == 'previous_image_2':
            self.previous_image_2.setPixmap(pixmap)
        if holder.widget_name == 'next_image_1':
            self.next_image_1.setPixmap(pixmap)
        if holder.widget_name == 'next_image_2':
            self.next_image_2.setPixmap(pixmap)

    def move_image_to_keep(self):
        self.controller.move_image('Keep')

    def move_image_to_maybe(self):
        self.controller.move_image('Maybe')

    def move_image_to_delete(self):
        self.controller.move_image('Delete')

    def undo_last_move(self):
        self.controller.undo_last_move()

    def fit_widgets_height_to_window(self):
        set_widget_height(self, self.current_image, 69)
        set_widget_height(self, self.undo_btn, 5)
        set_widget_height(self, self.keep_btn, 5)
        set_widget_height(self, self.maybe_btn, 5)
        set_widget_height(self, self.delete_btn, 5)
        set_widget_height(self, self.close_compare_btn, 5)
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
