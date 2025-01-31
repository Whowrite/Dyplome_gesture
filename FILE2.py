import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

class VideoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.capture = cv2.VideoCapture(0)  # Відкриття камери
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Оновлення кадру кожні 30 мс

    def initUI(self):
        self.setWindowTitle("Відеопотік з OpenCV")
        self.setGeometry(100, 100, 800, 600)

        # Додавання QLabel для відображення відео
        self.video_label = QLabel(self)
        self.video_label.setFixedSize(800, 600)

        # Компоновка
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        self.setLayout(layout)

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Конвертуємо в RGB
            height, width, channel = frame.shape
            step = channel * width
            q_image = QImage(frame.data, width, height, step, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.video_label.setPixmap(pixmap)

    def closeEvent(self, event):
        # Закриття камери при закритті вікна
        self.capture.release()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = VideoApp()
    mainWin.show()
    sys.exit(app.exec_())
