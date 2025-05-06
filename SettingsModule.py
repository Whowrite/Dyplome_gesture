from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QFrame, QHBoxLayout, \
    QStyle, QMessageBox, QRadioButton, QButtonGroup
from PyQt5.QtGui import QImage, QPixmap, QFont, QIcon, QTransform
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt, QSize
from functools import partial
import random

class SettingsModule:
    def __init__(self):
        self.language = "UK"
        self.color = "green"

    def set_language(self, lang):
        if lang in ["UK", "EN"]:
            self.language = lang

    def set_color(self, color):
        if color in ["green", "purple", "orange", "pink"]:
            self.color = color

    # Функція-обробник кнопки для виклику меню налаштувань
    def show_settings(self, settings_frame, unvisible_frame, window):
        settings_frame.show()
        unvisible_frame.show()

        unvisible_frame.clicked.connect(partial(self.hide_settings, settings_frame, unvisible_frame))

        # Стиль для квадратних QRadioButton
        radio_button_style = """
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid black;
                border-radius: 5px;
            }
            QRadioButton::indicator:checked {
                background-color: #5dade2;
                border: 2px solid black;
            }
            QRadioButton::indicator:unchecked {
                background-color: white;
                border: 2px solid black;
            }
            QRadioButton {
                background-color: transparent;
            }
        """

        # ------------------------------------------------------------------------------------------------------------------Кнопка для закриття меню налаштувань

        button_closeSettings = QPushButton(settings_frame)
        button_closeSettings.setGeometry(350, 13, 50, 50)
        button_closeSettings.setText("X")
        button_closeSettings.show()

        font = QFont()
        font.setBold(True)
        font.setPointSize(15)
        button_closeSettings.setFont(font)

        button_closeSettings.setStyleSheet("""
                                QPushButton {
                                    background-color: #DAFFDF; /* Колір кнопки */
                                    color: #eb8934; /* Колір тексту */
                                    border-radius: 25px; /* Закруглення кутів */
                                }
                                QPushButton:hover {
                                    background-color: #5dade2; /* Колір кнопки при наведенні */
                                }
                                QPushButton:pressed {
                                    background-color: #1f618d; /* Колір кнопки при натисканні */
                                }
                            """)
        button_closeSettings.clicked.connect(partial(self.hide_settings, settings_frame, unvisible_frame))

        button_Statistics = QPushButton(settings_frame)
        button_Statistics.setGeometry(290, 13, 50, 50)
        # Завантажуємо іконку
        icon = QIcon("FingerImages/user.png")
        button_Statistics.setIcon(icon)
        button_Statistics.setIconSize(QSize(50, 50))  # Налаштовуємо розмір іконки (50x50 пікселів)
        button_Statistics.show()

        button_Statistics.setFont(font)

        button_Statistics.setStyleSheet("""
                                        QPushButton {
                                            background-color: #DAFFDF; /* Колір кнопки */
                                            color: #eb8934; /* Колір тексту */
                                            border-radius: 25px; /* Закруглення кутів */
                                        }
                                        QPushButton:hover {
                                            background-color: #5dade2; /* Колір кнопки при наведенні */
                                        }
                                        QPushButton:pressed {
                                            background-color: #1f618d; /* Колір кнопки при натисканні */
                                        }
                                    """)
        button_Statistics.clicked.connect(lambda: self.showUserStatistics(window))

        # ------------------------------------------------------------------------------------------------------------------Підпис "Мова застосунку"

        label_language = QLabel(settings_frame)
        label_language.setGeometry(80, 20, 150, 55)
        label_language.setText("Мова 🌐")
        label_language.setStyleSheet("background-color: transparent;")
        label_language.show()

        font = QFont()
        font.setBold(False)
        font.setPointSize(18)
        label_language.setFont(font)

        font2 = QFont()
        font2.setBold(False)
        font2.setPointSize(25)

        line1 = QLabel(settings_frame)
        line1.setGeometry(30, 30, 380, 55)
        line1.setText("_________________________________________")
        line1.setStyleSheet("background-color: transparent;")
        line1.show()
        line1.setFont(font2)

        # ------------------------------------------------------------------------------------------------------------------Вибір мови застосунку
        language_group = QButtonGroup(settings_frame)

        radio_ukrainian = QRadioButton(settings_frame)
        radio_ukrainian.setGeometry(40, 100, 180, 30)
        radio_ukrainian.setText("Українська")
        radio_ukrainian.setChecked(self.language == "UK")
        radio_ukrainian.toggled.connect(lambda: self.set_language("UK"))
        radio_ukrainian.setStyleSheet(radio_button_style)
        radio_ukrainian.show()
        radio_ukrainian.setFont(font)
        language_group.addButton(radio_ukrainian)

        radio_english = QRadioButton(settings_frame)
        radio_english.setGeometry(40, 150, 180, 30)
        radio_english.setText("Англійська")
        radio_english.setChecked(self.language == "EN")
        radio_english.toggled.connect(lambda: self.set_language("EN"))
        radio_english.setStyleSheet(radio_button_style)
        radio_english.show()
        radio_english.setFont(font)
        language_group.addButton(radio_english)

        # ------------------------------------------------------------------------------------------------------------------Підпис "Колірна схема"
        line2 = QLabel(settings_frame)
        line2.setGeometry(30, 160, 380, 55)
        line2.setText("_________________________________________")
        line2.setStyleSheet("background-color: transparent;")
        line2.show()
        line2.setFont(font2)

        label_color = QLabel(settings_frame)
        label_color.setGeometry(80, 210, 250, 55)
        label_color.setText("Колірна схема 🎨")
        label_color.setStyleSheet("background-color: transparent;")
        label_color.show()
        label_color.setFont(font)

        line3 = QLabel(settings_frame)
        line3.setGeometry(30, 220, 380, 55)
        line3.setText("_________________________________________")
        line3.setStyleSheet("background-color: transparent;")
        line3.show()
        line3.setFont(font2)

        # ------------------------------------------------------------------------------------------------------------------Вибір колірної схеми застосунку
        color_group = QButtonGroup(settings_frame)

        radio_green = QRadioButton(settings_frame)
        radio_green.setGeometry(40, 290, 230, 30)
        radio_green.setText("Зелена")
        radio_green.setChecked(self.color == "green")
        radio_green.toggled.connect(lambda: self.set_color("green"))
        radio_green.setStyleSheet(radio_button_style)
        radio_green.show()
        radio_green.setFont(font)
        color_group.addButton(radio_green)

        radio_purple = QRadioButton(settings_frame)
        radio_purple.setGeometry(40, 340, 230, 30)
        radio_purple.setText("Фіолетова")
        radio_purple.setStyleSheet(radio_button_style)
        radio_purple.setChecked(self.color == "purple")
        radio_purple.toggled.connect(lambda: self.set_color("purple"))
        radio_purple.show()
        radio_purple.setFont(font)
        color_group.addButton(radio_purple)

        radio_orange = QRadioButton(settings_frame)
        radio_orange.setGeometry(40, 390, 230, 30)
        radio_orange.setText("Помаранчева")
        radio_orange.setChecked(self.color == "orange")
        radio_orange.toggled.connect(lambda: self.set_color("orange"))
        radio_orange.setStyleSheet(radio_button_style)
        radio_orange.show()
        radio_orange.setFont(font)
        color_group.addButton(radio_orange)

        radio_pink = QRadioButton(settings_frame)
        radio_pink.setGeometry(40, 440, 230, 30)
        radio_pink.setText("Рожева")
        radio_pink.setChecked(self.color == "pink")
        radio_pink.toggled.connect(lambda: self.set_color("pink"))
        radio_pink.setStyleSheet(radio_button_style)
        radio_pink.show()
        radio_pink.setFont(font)
        color_group.addButton(radio_pink)

        line4 = QLabel(settings_frame)
        line4.setGeometry(30, 450, 380, 55)
        line4.setText("_________________________________________")
        line4.setStyleSheet("background-color: transparent;")
        line4.show()
        line4.setFont(font2)

        # ------------------------------------------------------------------------------------------------------------------Побажання
        wishes = [
            "Бажаю вам сил, спокою та якнайшвидшого одужання, щоб цей день приніс вам трохи світла й тепла.",
            "Нехай день буде сповнений радості та тепла!",
            "Бажаю успіху в усіх ваших починаннях!"
        ]

        font3 = QFont()
        font3.setBold(False)
        font3.setPointSize(13)

        wish_label = QLabel(settings_frame)
        wish_label.setGeometry(30, 440, 380, 200)
        wish_label.setText("💕 Твоє побажання на сьогодні: 💕")
        wish_label.setStyleSheet("background-color: transparent;")
        wish_label.show()
        wish_label.setFont(font3)

        wish_text = QLabel(settings_frame)
        wish_text.setGeometry(40, 515, 360, 200)
        wish_text.setText(f"{random.choice(wishes)}")
        wish_text.setWordWrap(True)
        wish_text.setAlignment(Qt.AlignCenter)
        wish_text.show()
        wish_text.setFont(font3)

        line5 = QLabel(settings_frame)
        line5.setGeometry(30, 640, 380, 55)
        line5.setText("_________________________________________")
        line5.setStyleSheet("background-color: transparent;")
        line5.show()
        line5.setFont(font2)

        # ------------------------------------------------------------------------------------------------------------------Кнопки для скидання налаштувань та виходу з додатку
        button_reset = QPushButton(settings_frame)
        button_reset.setGeometry(50, 720, 330, 50)
        button_reset.setText("Скинути налаштування")
        button_reset.show()
        button_reset.setFont(font3)
        button_reset.setStyleSheet("""
                    QPushButton {
                        background-color: #DAFFDF;
                        color: black;
                        border-radius: 10px;
                    }
                    QPushButton:hover {
                        background-color: #5dade2;
                    }
                    QPushButton:pressed {
                        background-color: #1f618d;
                    }
                """)

        button_exit = QPushButton(settings_frame)
        button_exit.setGeometry(50, 790, 330, 50)
        button_exit.setText("Вийти з програми")
        button_exit.show()
        button_exit.setFont(font3)
        button_exit.setStyleSheet("""
                    QPushButton {
                        background-color: #DAFFDF;
                        color: black;
                        border-radius: 10px;
                    }
                    QPushButton:hover {
                        background-color: #5dade2;
                    }
                    QPushButton:pressed {
                        background-color: #1f618d;
                    }
                """)

        # ------------------------------------------------------------------------------------------------------------------Зміна ієрархії елементів
        label_language.raise_()
        label_color.raise_()
        wish_label.raise_()
        radio_english.raise_()
        radio_pink.raise_()
        button_closeSettings.raise_()
        button_Statistics.raise_()

    def showUserStatistics(self, window):
        # ------------------------------------------------------------------------------------------------------------------Фрейм відображення статистики

        frame_UserStatistics = QFrame(window)
        frame_UserStatistics.setGeometry(0, 0, 1315, 917)
        frame_UserStatistics.show()
        frame_UserStatistics.setStyleSheet("""
                            QFrame {
                                background-color: #9EFFA5; /* Фон картки */
                                border-radius: 10px; /* Закруглені кути */
                            }
                        """)

        # ------------------------------------------------------------------------------------------------------------------Кнопка для повернення на головну сторінку

        button_return = QPushButton(frame_UserStatistics)
        button_return.setGeometry(48, 23, 60, 60)

        # Завантажуємо зображення в QPixmap
        pixmap = QPixmap("FingerImages/right-arrow.png")  # Вкажіть шлях до вашого зображення

        # Обертаємо зображення
        transform = QTransform().rotate(180)
        rotated_pixmap = pixmap.transformed(transform)

        # Завантажуємо іконку
        icon = QIcon(rotated_pixmap)
        button_return.setIcon(icon)
        button_return.setIconSize(QSize(50, 50))  # Налаштовуємо розмір іконки (50x50 пікселів)
        button_return.show()

        button_return.setStyleSheet("""
                                QPushButton {
                                    background-color: #DAFFDF; /* Колір кнопки */
                                    color: #eb8934; /* Колір тексту */
                                    border-radius: 30px; /* Закруглення кутів */
                                }
                                QPushButton:hover {
                                    background-color: #5dade2; /* Колір кнопки при наведенні */
                                }
                                QPushButton:pressed {
                                    background-color: #1f618d; /* Колір кнопки при натисканні */
                                }
                            """)
        button_return.clicked.connect(
            partial(self.hide_frame_UserStatistics, frame_UserStatistics))

        # ------------------------------------------------------------------------------------------------------------------Назва вікна

        title_window = QLabel(frame_UserStatistics)
        title_window.setGeometry(538, 23, 290, 55)
        title_window.setText("Статистика")
        title_window.show()

        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        title_window.setFont(font)

        title_window.setFrameShape(QLabel.StyledPanel)
        title_window.setFrameShadow(QLabel.Plain)
        title_window.setAlignment(Qt.AlignCenter)
        title_window.setStyleSheet("""
                    QLabel {
                        background-color: #DAFFDF; /* Колір фону */
                        color: black; /* Колір тексту */
                        border-radius: 10px; /* Закруглення кутів */
                    }
                """)

        # ------------------------------------------------------------------------------------------------------------------Кнопка Довідки

        button_help = QPushButton(frame_UserStatistics)
        button_help.setGeometry(1206, 18, 60, 60)
        button_help.setText("?")
        button_help.show()

        font2 = QFont()
        font2.setBold(True)
        font2.setPointSize(18)
        button_help.setFont(font2)

        button_help.setStyleSheet("""
                        QPushButton {
                            background-color: #DAFFDF; /* Колір кнопки */
                            color: #eb8934; /* Колір тексту */
                            border-radius: 30px; /* Закруглення кутів */
                        }
                        QPushButton:hover {
                            background-color: #5dade2; /* Колір кнопки при наведенні */
                        }
                        QPushButton:pressed {
                            background-color: #1f618d; /* Колір кнопки при натисканні */
                        }
                    """)



    def hide_frame_UserStatistics(self, frame_UserStatistics):
        print("close: frame_UserStatistics")
        frame_UserStatistics.hide()

    # Функція-обробник кнопки для закриття меню налаштувань
    def hide_settings(self, settings_frame, unvisible_frame):
        settings_frame.hide()
        unvisible_frame.hide()