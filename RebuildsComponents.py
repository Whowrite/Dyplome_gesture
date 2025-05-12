from PyQt5.QtWidgets import QFrame, QDialog, QLabel, QMainWindow
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt, QTimer
import sys

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


class MainWindow(QMainWindow):
    def __init__(self, Music):
        super().__init__()
        self.music = Music
        self.widgetsColor = ["#9EFFA5", "#DAFFDF"]
        self.widgetsLanguage = 0

        self.session_time = 0
        self.session_timer = QTimer()
        self.session_timer.timeout.connect(self.update_session_time)
        self.session_timer.start(1000)

        self.setWindowTitle("ToTrainYourNeurons")
        self.setGeometry(250, 100, 1315, 917)

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.widgetsColor[1]}; /* Колір вікна */
            }}
        """)

    def closeEvent(self, event):
        """
        Перевизначаємо подію закриття вікна, щоб зберегти налаштування перед виходом.
        """
        # self.music.stop_music()
        self.saveSettings()
        self.saveSessionTime()
        self.music.stop_music()
        event.accept()  # Дозволяємо вікну закритися

    def saveSettings(self):
        print("Збереження налаштувань...")
        filename = "settings.txt"
        languages = {
            0: "ukrainian",
            1: "english"
        }

        try:
            current_language = languages[self.widgetsLanguage]
            current_colors = self.widgetsColor

            settings_content = f"Language: {current_language}\n"
            settings_content += f"Color: \"{current_colors[0]}\", \"{current_colors[1]}\""

            with open(filename, 'w', encoding='utf-8') as file:
                file.write(settings_content)

        except Exception as e:
            print(f"Помилка при збереженні налаштувань: {e}")

    def set_color(self, colors):
        self.widgetsColor = colors
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.widgetsColor[1]};
            }}
        """)

    def set_language(self, language):
        self.widgetsLanguage = language

    def update_session_time(self):
        self.session_time += 1

    def saveSessionTime(self):
        self.session_timer.stop()
        # Форматуємо час у зручний вигляд (години:хвилини:секунди)
        hours = self.session_time // 3600
        minutes = (self.session_time % 3600) // 60
        seconds = self.session_time % 60
        session_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        print(f"Ваша сесія тривала: {session_str}")