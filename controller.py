#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymorr
import main


class PymorrController(object):
    def __init__(self):
        self.morr = pymorr.Pymorr()
        self.morr.set_root('/Users/devbook/Downloads/Keep/')
        self.next_images = self.morr.get_image_paths_from_root()
        self.previous_images = self.morr.get_image_paths_from_log()

    def attach_view(self, view):
        self.view = view

    def request_content(self):
        self.view.update_images(
            self.next_images,
            self.previous_images
        )

    def get_path(self):
        self.morr.root

    def set_path(self, path):
        self.morr.set_root(path)
        self.update_image_paths()
        self.request_content()

    def update_image_paths(self):
        self.next_images = self.morr.get_image_paths_from_root()
        self.previous_images = self.morr.get_image_paths_from_log()

    def move_image(self, destination):
        if len(self.next_images) > 0:
            moved_path = self.morr.move_image(
                self.next_images[0],
                self.morr.prefered_folder[destination]
            )
            self.previous_images.append(moved_path)
            self.next_images.pop(0)
            self.view.update_images(self.next_images, self.previous_images)

    def undo_last_move(self):
        self.morr.undo_last_move()
        self.update_image_paths()
        self.request_content()
