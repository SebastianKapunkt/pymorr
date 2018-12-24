from PyQt5 import QtCore, QtGui


def percentage_value(percentage, size):
    return (size * percentage) / 100


def get_scale_pixmap(qtview, qt_image, height, width):
    return QtGui.QPixmap.fromImage(qt_image).scaled(
        percentage_value(width, qtview.width()),
        percentage_value(height, qtview.height()),
        QtCore.Qt.KeepAspectRatio
    )


def set_widget_height(qtview, widget, percentage):
    widget.setFixedHeight(
        percentage_value(percentage, qtview.height())
    )

def set_widget_width(qtview, widget, percentage):
    widget.setFixedWidth(
        percentage_value(percentage, qtview.width())
    )
