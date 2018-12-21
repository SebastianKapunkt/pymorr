from PyQt5 import QtCore, QtGui


def percentage_value(percentage, size):
    return (size * percentage) / 100


def set_image_to_widget(qtview, widget, image, height, width):
    pixmap = QtGui.QPixmap(image).scaled(
        percentage_value(width, qtview.width()),
        percentage_value(height, qtview.height()),
        QtCore.Qt.KeepAspectRatio
    )
    widget.setPixmap(pixmap)


def set_widget_height(qtview, widget, percentage):
    widget.setFixedHeight(
        percentage_value(percentage, qtview.height())
    )
