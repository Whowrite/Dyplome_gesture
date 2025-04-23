from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QFrame, QHBoxLayout, \
    QStyle, QMessageBox
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from functools import partial

class SettingsModule:
    def __init__(self):
        language = "UK"
        color = "green"

    # Функція-обробник кнопки для виклику меню налаштувань
    def show_settings(self, settings_frame, unvisible_frame):
        settings_frame.show()
        unvisible_frame.show()

        unvisible_frame.clicked.connect(partial(self.hide_settings, settings_frame, unvisible_frame))

        # ------------------------------------------------------------------------------------------------------------------Кнопка для закриття меню налаштувань

        button_closeSettings = QPushButton(settings_frame)
        button_closeSettings.setGeometry(48, 13, 60, 60)
        button_closeSettings.setText("X")
        button_closeSettings.show()

        font = QFont()
        font.setBold(True)
        font.setPointSize(18)
        button_closeSettings.setFont(font)

        button_closeSettings.setStyleSheet("""
                                QPushButton {
                                    background-color: #DAFFDF; /* Колір кнопки */
                                    color: black; /* Колір тексту */
                                    border-radius: 30px; /* Закруглення кутів */
                                }
                                QPushButton:hover {
                                    background-color: #5dade2; /* Колір кнопки при наведенні */
                                }
                                QPushButton:pressed {
                                    background-color: #1f618d; /* Колір кнопки при натисканні */
                                }
                            """)
        button_closeSettings.clicked.connect(partial(self.hide_settings, settings_frame, unvisible_frame))

        # ------------------------------------------------------------------------------------------------------------------Назва програми

        label_language = QLabel(settings_frame)
        label_language.setGeometry(50, 80, 150, 55)
        label_language.setText("Мова 🌐")
        label_language.show()

        font = QFont()
        font.setBold(False)
        font.setPointSize(18)
        label_language.setFont(font)

        font2 = QFont()
        font2.setBold(False)
        font2.setPointSize(25)

        line1 = QLabel(settings_frame)
        line1.setGeometry(50, 100, 330, 55)
        line1.setText("_________________________________________")
        line1.show()
        line1.setFont(font2)

        # ------------------------------------------------------------------------------------------------------------------Зміна ієрархії елементів
        label_language.raise_()

    # Функція-обробник кнопки для закриття меню налаштувань
    def hide_settings(self, settings_frame, unvisible_frame):
        settings_frame.hide()
        unvisible_frame.hide()