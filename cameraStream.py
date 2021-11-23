import PyQt5.QtCore, PyQt5.QtWidgets
from PyQt5.QtGui import QImage


import cv2


class ThreadClass(PyQt5.QtCore.QThread):
    any_signal = PyQt5.QtCore.pyqtSignal(QImage)

    def __init__(self, parent=None):
        super(ThreadClass, self).__init__(parent)
        self.is_running = True

    def run(self):
        cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)

        while True:
            ret, source_img = cap.read()

            if ret:
                crope_img = source_img[100:500, 300:900]
                img = cv2.cvtColor(crope_img, cv2.COLOR_BGR2RGB)
                height, width, channel = img.shape
                step = channel * width
                qImg = QImage(img.data, width, height, step, QImage.Format_RGB888)
                self.any_signal.emit(qImg)

    def stop(self):
        self.is_running = False
        self.terminate()