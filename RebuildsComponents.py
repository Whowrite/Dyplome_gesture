from PyQt5.QtWidgets import QFrame, QDialog, QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt

class ClickableFrame(QFrame):
    clicked = pyqtSignal()  # створюємо власний сигнал

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()  # емітуємо сигнал при кліку

class ClickableLabel(QLabel):
    clicked = pyqtSignal()  # створюємо власний сигнал

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()  # емітуємо сигнал при кліку

class ModalWindow(QDialog):
    def __init__(self, x, y, lenght, height, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Модальне вікно")
        self.setGeometry(x, y, lenght, height)
        self.setStyleSheet("""
            QDialog {
                background-color: #F0F0F0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)