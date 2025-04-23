from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt

class ClickableFrame(QFrame):
    clicked = pyqtSignal()  # створюємо власний сигнал

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()  # емитимо сигнал при кліку