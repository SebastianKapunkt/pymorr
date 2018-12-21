from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage


class ImageDataHolder:
    image: QImage
    height: int
    width: int
    widget_name: str


class ImageWorkerSignals(QObject):
    result = pyqtSignal(object)


class ImageWorker(QRunnable):
    def __init__(self, image_path, widget_name, width, height):
        super(ImageWorker, self).__init__()

        self.image_path = image_path
        self.widget_name = widget_name
        self.signals = ImageWorkerSignals()
        self.height = height
        self.width = width

    @pyqtSlot()
    def run(self):
        holder = ImageDataHolder()
        holder.image = QImage(self.image_path)
        holder.widget_name = self.widget_name
        holder.height = self.height
        holder.width = self.width

        self.signals.result.emit(holder)
