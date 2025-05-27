from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QFrame, QHBoxLayout, \
    QStyle, QMessageBox, QRadioButton, QButtonGroup, QProgressBar
from PyQt5.QtGui import QImage, QPixmap, QFont, QIcon, QTransform
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt, QSize
from functools import partial
import random

class SettingsModule:
    def __init__(self, main, level_counting, music):
        self.widgetsLanguage = 0
        self.widgetsColor = ["#9EFFA5", "#DAFFDF"]
        self.connection = None
        self.main_window = main
        self.level_counting = level_counting
        self.Music = music
        # self.Music.play_music()  # Початок відтворення
        self.button_Music_Checked = True
        self.widgetsText = {
            "label_language": ['Мова 🌐', 'Language 🌐'],
            "radio_ukrainian": ['Українська', 'Ukrainian'],
            "radio_english": ['Англійська', 'English'],
            "label_color": ['Колірна схема 🎨', 'Color scheme 🎨'],
            "radio_green": ['Зелений', 'Green'],
            "radio_purple": ['Фіолетовий', 'Purple'],
            "radio_orange": ['Помаранчевий', 'Orange'],
            "radio_pink": ['Рожевий', 'Pink'],
            "wish_label": ['💕 Твоє побажання на сьогодні: 💕', '💕 Your wish for today: 💕'],
            "button_reset": ['Скинути налаштування', 'Reset the settings'],
            "button_exit": ['Вийти з програми', 'Exit the program'],
            "title_window": ['Статистика', 'Statistics'],
            "title_facts": ['Цікаві факти', 'Interesting facts'],
            "title_correctGestures": ['Найбільше правильних жестів', 'The most correct gestures'],
            "label_mode": ['Улюблений режим:', 'Favorite mode:'],
            "label_numberSessionsLastMonth": ['За останній місяць:', 'Over the past month:'],
            "label_AverageTimeSessions": ['Середній час сеансу (хв.):', 'Average session time (minutes):'],
            "title_outDeveloper": ['Порада від розробника: “Іноді лінь, може підштовхнути вас до здійснення мрій!',
                                   'A tip from the developer: "Sometimes being lazy can make you realize your dreams!'],
            "button_help_statistics": ["Допоміжний текст 4!!!", "Help text 4!!!"]
        }
        self.wishes = {
            0: [
                "Бажаю вам сил, спокою та якнайшвидшого одужання, щоб цей день приніс вам трохи світла й тепла.",
                "Нехай день буде сповнений радості та тепла!",
                "Бажаю успіху в усіх ваших починаннях!"
            ],
            1: [
                "I wish you strength, peace of mind and a speedy recovery so that this day brings you some light and warmth.",
                "May the day be full of joy and warmth!",
                "I wish you success in all your endeavors!"
            ]
        }
        self.select_wish = random.choice([0, 1, 2])
        # Компоненти, що залежні від налаштувань додатку
        self.label_language = None
        self.radio_ukrainian = None
        self.radio_english = None
        self.label_color = None
        self.radio_green = None
        self.radio_purple = None
        self.radio_orange = None
        self.radio_pink = None
        self.wish_label = None
        self.wish_text = None
        self.button_reset = None
        self.button_exit = None
        self.button_closeSettings = None
        self.button_Statistics = None
        self.button_Music = None

    # Функція для зміни мови додатку
    def set_language(self, lang):
        if lang in [0, 1]:
            self.widgetsLanguage = lang
            # print(f"def set_language(self, lang): {lang}")
            self.main_window.setLanguage(lang)
            self.level_counting.setLanguage(lang)
            self.update_ui()

    # Функція для зміни кольору додатку
    def set_color(self, color):
        if color[0] in ["9EFFA5", "CA9EFF", "FFCD9E", "FF9EBB"] and color[1] in ["DAFFDF", "F9DAFF", "FFEBDA", "FFDAEC"]:
            self.widgetsColor[0] = f'#{color[0]}'
            self.widgetsColor[1] = f'#{color[1]}'
            self.main_window.setColor(self.widgetsColor)
            self.level_counting.setColor(self.widgetsColor)
            self.update_ui()

    # Встановлення підключення до бд
    def set_connect_ToBD(self, con):
        self.connection = con
        print("Підлючення встановлено: SettingsModule")

    # Функція для оновлення візуалу компонентів вікна
    def update_ui(self):
        if self.label_language:
            self.label_language.setText(self.widgetsText["label_language"][self.widgetsLanguage])
            self.label_language.setStyleSheet(f"background-color: {self.widgetsColor[0]};")
        if self.label_color:
            self.label_color.setText(self.widgetsText["label_color"][self.widgetsLanguage])
            self.label_color.setStyleSheet(f"background-color: {self.widgetsColor[0]};")
        if self.wish_label:
            self.wish_label.setText(self.widgetsText["wish_label"][self.widgetsLanguage])
            self.wish_label.setStyleSheet(f"background-color: {self.widgetsColor[0]};")
        if self.wish_text:
            self.wish_text.setText(self.wishes[self.widgetsLanguage][self.select_wish])
            self.wish_text.setStyleSheet(f"background-color: {self.widgetsColor[0]};")
        button_style = f"""
                    QPushButton {{
                        background-color: {self.widgetsColor[1]};
                        color: black;
                        border-radius: 10px;
                    }}
                    QPushButton:hover {{
                        background-color: #5dade2;
                    }}
                    QPushButton:pressed {{
                        background-color: #1f618d;
                    }}
                """
        button_style2 = f"""
                                QPushButton {{
                                    background-color: {self.widgetsColor[1]}; /* Колір кнопки */
                                    color: #eb8934; /* Колір тексту */
                                    border-radius: 25px; /* Закруглення кутів */
                                }}
                                QPushButton:hover {{
                                    background-color: #5dade2; /* Колір кнопки при наведенні */
                                }}
                                QPushButton:pressed {{
                                    background-color: #1f618d; /* Колір кнопки при натисканні */
                                }}
                            """
        if self.button_reset:
            self.button_reset.setText(self.widgetsText["button_reset"][self.widgetsLanguage])
            self.button_reset.setStyleSheet(button_style)
        if self.button_exit:
            self.button_exit.setText(self.widgetsText["button_exit"][self.widgetsLanguage])
            self.button_exit.setStyleSheet(button_style)
        if self.button_closeSettings:
            self.button_closeSettings.setStyleSheet(button_style2)
        if self.button_Statistics:
            self.button_Statistics.setStyleSheet(button_style2)
        if self.button_Music:
            self.button_Music.setStyleSheet(button_style2)

        # Стиль для квадратних QRadioButton
        radio_button_style = f"""
                    QRadioButton::indicator {{
                        width: 20px;
                        height: 20px;
                        border: 2px solid black;
                        border-radius: 5px;
                    }}
                    QRadioButton::indicator:checked {{
                        background-color: #5dade2;
                        border: 2px solid black;
                    }}
                    QRadioButton::indicator:unchecked {{
                        background-color: white;
                        border: 2px solid black;
                    }}
                    QRadioButton {{
                        background-color: {self.widgetsColor[0]};
                    }}
                """
        if self.radio_ukrainian:
            self.radio_ukrainian.setText(self.widgetsText["radio_ukrainian"][self.widgetsLanguage])
            self.radio_ukrainian.setStyleSheet(radio_button_style)
        if self.radio_english:
            self.radio_english.setText(self.widgetsText["radio_english"][self.widgetsLanguage])
            self.radio_english.setStyleSheet(radio_button_style)
        if self.radio_green:
            self.radio_green.setText(self.widgetsText["radio_green"][self.widgetsLanguage])
            self.radio_green.setStyleSheet(radio_button_style)
        if self.radio_purple:
            self.radio_purple.setText(self.widgetsText["radio_purple"][self.widgetsLanguage])
            self.radio_purple.setStyleSheet(radio_button_style)
        if self.radio_orange:
            self.radio_orange.setText(self.widgetsText["radio_orange"][self.widgetsLanguage])
            self.radio_orange.setStyleSheet(radio_button_style)
        if self.radio_pink:
            self.radio_pink.setText(self.widgetsText["radio_pink"][self.widgetsLanguage])
            self.radio_pink.setStyleSheet(radio_button_style)

    # Функція-обробник кнопки для виклику меню налаштувань
    def show_settings(self, settings_frame, unvisible_frame, window):
        settings_frame.show()
        unvisible_frame.show()

        unvisible_frame.clicked.connect(partial(self.hide_settings, settings_frame, unvisible_frame))

        # Стиль для квадратних QRadioButton
        radio_button_style = f"""
            QRadioButton::indicator {{
                width: 20px;
                height: 20px;
                border: 2px solid black;
                border-radius: 5px;
            }}
            QRadioButton::indicator:checked {{
                background-color: #5dade2;
                border: 2px solid black;
            }}
            QRadioButton::indicator:unchecked {{
                background-color: white;
                border: 2px solid black;
            }}
            QRadioButton {{
                background-color: {self.widgetsColor[0]};
            }}
        """

        self.button_Music = QPushButton(settings_frame)
        self.button_Music.setGeometry(230, 13, 50, 50)
        if self.button_Music_Checked:
            # Завантажуємо іконку
            icon = QIcon("FingerImages/musicMute.png")
            self.button_Music.setIcon(icon)
        else:
            # Завантажуємо іконку
            icon = QIcon("FingerImages/musicPlay.png")
            self.button_Music.setIcon(icon)
        self.button_Music.setIconSize(QSize(40, 40))  # Налаштовуємо розмір іконки (50x50 пікселів)
        self.button_Music.show()

        self.button_Music.setStyleSheet(f"""
                                        QPushButton {{
                                            background-color: {self.widgetsColor[1]}; /* Колір кнопки */
                                            color: #eb8934; /* Колір тексту */
                                            border-radius: 25px; /* Закруглення кутів */
                                        }}
                                        QPushButton:hover {{
                                            background-color: #5dade2; /* Колір кнопки при наведенні */
                                        }}
                                        QPushButton:pressed {{
                                            background-color: #1f618d; /* Колір кнопки при натисканні */
                                        }}
                                    """)
        self.button_Music.clicked.connect(partial(self.musicCatcher))

        # ------------------------------------------------------------------------------------------------------------------Кнопка для закриття меню налаштувань

        self.button_closeSettings = QPushButton(settings_frame)
        self.button_closeSettings.setGeometry(350, 13, 50, 50)
        self.button_closeSettings.setText("X")
        self.button_closeSettings.show()

        font = QFont()
        font.setBold(True)
        font.setPointSize(15)
        self.button_closeSettings.setFont(font)

        self.button_closeSettings.setStyleSheet(f"""
                                QPushButton {{
                                    background-color: {self.widgetsColor[1]}; /* Колір кнопки */
                                    color: #eb8934; /* Колір тексту */
                                    border-radius: 25px; /* Закруглення кутів */
                                }}
                                QPushButton:hover {{
                                    background-color: #5dade2; /* Колір кнопки при наведенні */
                                }}
                                QPushButton:pressed {{
                                    background-color: #1f618d; /* Колір кнопки при натисканні */
                                }}
                            """)
        self.button_closeSettings.clicked.connect(partial(self.hide_settings, settings_frame, unvisible_frame))

        self.button_Statistics = QPushButton(settings_frame)
        self.button_Statistics.setGeometry(290, 13, 50, 50)
        # Завантажуємо іконку
        icon = QIcon("FingerImages/user.png")
        self.button_Statistics.setIcon(icon)
        self.button_Statistics.setIconSize(QSize(50, 50))  # Налаштовуємо розмір іконки (50x50 пікселів)
        self.button_Statistics.show()

        self.button_Statistics.setFont(font)

        self.button_Statistics.setStyleSheet(f"""
                                QPushButton {{
                                    background-color: {self.widgetsColor[1]}; /* Колір кнопки */
                                    color: #eb8934; /* Колір тексту */
                                    border-radius: 25px; /* Закруглення кутів */
                                }}
                                QPushButton:hover {{
                                    background-color: #5dade2; /* Колір кнопки при наведенні */
                                }}
                                QPushButton:pressed {{
                                    background-color: #1f618d; /* Колір кнопки при натисканні */
                                }}
                            """)
        self.button_Statistics.clicked.connect(lambda: self.showUserStatistics(window))

        # ------------------------------------------------------------------------------------------------------------------Підпис "Мова застосунку"

        self.label_language = QLabel(settings_frame)
        self.label_language.setGeometry(80, 20, 180, 55)
        self.label_language.setText(self.widgetsText["label_language"][self.widgetsLanguage])
        self.label_language.setStyleSheet(f"background-color: {self.widgetsColor[0]};")
        self.label_language.show()

        font = QFont()
        font.setBold(False)
        font.setPointSize(18)
        self.label_language.setFont(font)

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

        self.radio_ukrainian = QRadioButton(settings_frame)
        self.radio_ukrainian.setGeometry(40, 100, 180, 30)
        self.radio_ukrainian.setText(self.widgetsText["radio_ukrainian"][self.widgetsLanguage])
        self.radio_ukrainian.setChecked(self.widgetsLanguage == 0)
        self.radio_ukrainian.toggled.connect(lambda: self.set_language(0))
        self.radio_ukrainian.setStyleSheet(radio_button_style)
        self.radio_ukrainian.show()
        self.radio_ukrainian.setFont(font)
        language_group.addButton(self.radio_ukrainian)

        self.radio_english = QRadioButton(settings_frame)
        self.radio_english.setGeometry(40, 150, 180, 40)
        self.radio_english.setText(self.widgetsText["radio_english"][self.widgetsLanguage])
        self.radio_english.setChecked(self.widgetsLanguage == 1)
        self.radio_english.toggled.connect(lambda: self.set_language(1))
        self.radio_english.setStyleSheet(radio_button_style)
        self.radio_english.show()
        self.radio_english.setFont(font)
        language_group.addButton(self.radio_english)

        # ------------------------------------------------------------------------------------------------------------------Підпис "Колірна схема"
        line2 = QLabel(settings_frame)
        line2.setGeometry(30, 160, 380, 55)
        line2.setText("_________________________________________")
        line2.setStyleSheet("background-color: transparent;")
        line2.show()
        line2.setFont(font2)

        self.label_color = QLabel(settings_frame)
        self.label_color.setGeometry(80, 210, 250, 55)
        self.label_color.setText(self.widgetsText["label_color"][self.widgetsLanguage])
        self.label_color.setStyleSheet(f"background-color: {self.widgetsColor[0]};")
        self.label_color.show()
        self.label_color.setFont(font)

        line3 = QLabel(settings_frame)
        line3.setGeometry(30, 220, 380, 55)
        line3.setText("_________________________________________")
        line3.setStyleSheet("background-color: transparent;")
        line3.show()
        line3.setFont(font2)

        # ------------------------------------------------------------------------------------------------------------------Вибір колірної схеми застосунку
        color_group = QButtonGroup(settings_frame)

        self.radio_green = QRadioButton(settings_frame)
        self.radio_green.setGeometry(40, 290, 230, 40)
        self.radio_green.setText(self.widgetsText["radio_green"][self.widgetsLanguage])
        self.radio_green.setChecked(self.widgetsColor[0] == "#9EFFA5")
        self.radio_green.toggled.connect(lambda: self.set_color(["9EFFA5", "DAFFDF"]))
        self.radio_green.setStyleSheet(radio_button_style)
        self.radio_green.show()
        self.radio_green.setFont(font)
        color_group.addButton(self.radio_green)

        self.radio_purple = QRadioButton(settings_frame)
        self.radio_purple.setGeometry(40, 340, 230, 40)
        self.radio_purple.setText(self.widgetsText["radio_purple"][self.widgetsLanguage])
        self.radio_purple.setStyleSheet(radio_button_style)
        self.radio_purple.setChecked(self.widgetsColor[0] == "#CA9EFF")
        self.radio_purple.toggled.connect(lambda: self.set_color(["CA9EFF", "F9DAFF"]))
        self.radio_purple.show()
        self.radio_purple.setFont(font)
        color_group.addButton(self.radio_purple)

        self.radio_orange = QRadioButton(settings_frame)
        self.radio_orange.setGeometry(40, 390, 230, 40)
        self.radio_orange.setText(self.widgetsText["radio_orange"][self.widgetsLanguage])
        self.radio_orange.setChecked(self.widgetsColor[0] == "#FFCD9E")
        self.radio_orange.toggled.connect(lambda: self.set_color(["FFCD9E", "FFEBDA"]))
        self.radio_orange.setStyleSheet(radio_button_style)
        self.radio_orange.show()
        self.radio_orange.setFont(font)
        color_group.addButton(self.radio_orange)

        self.radio_pink = QRadioButton(settings_frame)
        self.radio_pink.setGeometry(40, 440, 230, 40)
        self.radio_pink.setText(self.widgetsText["radio_pink"][self.widgetsLanguage])
        self.radio_pink.setChecked(self.widgetsColor[0] == "#FF9EBB")
        self.radio_pink.toggled.connect(lambda: self.set_color(["FF9EBB", "FFDAEC"]))
        self.radio_pink.setStyleSheet(radio_button_style)
        self.radio_pink.show()
        self.radio_pink.setFont(font)
        color_group.addButton(self.radio_pink)

        line4 = QLabel(settings_frame)
        line4.setGeometry(30, 450, 380, 55)
        line4.setText("_________________________________________")
        line4.setStyleSheet("background-color: transparent;")
        line4.show()
        line4.setFont(font2)

        # ------------------------------------------------------------------------------------------------------------------Побажання
        font3 = QFont()
        font3.setBold(False)
        font3.setPointSize(13)

        self.wish_label = QLabel(settings_frame)
        self.wish_label.setGeometry(30, 440, 380, 200)
        self.wish_label.setText(self.widgetsText["wish_label"][self.widgetsLanguage])
        self.wish_label.setStyleSheet(f"background-color: {self.widgetsColor[0]};")
        self.wish_label.setFrameShape(QLabel.StyledPanel)
        self.wish_label.setFrameShadow(QLabel.Plain)
        self.wish_label.setAlignment(Qt.AlignCenter)
        self.wish_label.show()
        self.wish_label.setFont(font3)

        self.wish_text = QLabel(settings_frame)
        self.wish_text.setGeometry(40, 565, 360, 110)
        self.wish_text.setText(self.wishes[self.widgetsLanguage][self.select_wish])
        self.wish_text.setWordWrap(True)
        self.wish_text.setStyleSheet(f"background-color: {self.widgetsColor[0]};")
        self.wish_text.setAlignment(Qt.AlignCenter)
        self.wish_text.show()
        self.wish_text.setFont(font3)

        line5 = QLabel(settings_frame)
        line5.setGeometry(30, 640, 380, 55)
        line5.setText("_________________________________________")
        line5.setStyleSheet("background-color: transparent;")
        line5.show()
        line5.setFont(font2)

        # ------------------------------------------------------------------------------------------------------------------Кнопки для скидання налаштувань та виходу з додатку
        self.button_reset = QPushButton(settings_frame)
        self.button_reset.setGeometry(50, 720, 330, 50)
        self.button_reset.setText(self.widgetsText["button_reset"][self.widgetsLanguage])
        self.button_reset.show()
        self.button_reset.setFont(font3)
        self.button_reset.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {self.widgetsColor[1]};
                        color: black;
                        border-radius: 10px;
                    }}
                    QPushButton:hover {{
                        background-color: #5dade2;
                    }}
                    QPushButton:pressed {{
                        background-color: #1f618d;
                    }}
                """)
        self.button_reset.clicked.connect(partial(self.set_defaultSettings))

        self.button_exit = QPushButton(settings_frame)
        self.button_exit.setGeometry(50, 790, 330, 50)
        self.button_exit.setText(self.widgetsText["button_exit"][self.widgetsLanguage])
        self.button_exit.show()
        self.button_exit.setFont(font3)
        self.button_exit.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {self.widgetsColor[1]};
                        color: black;
                        border-radius: 10px;
                    }}
                    QPushButton:hover {{
                        background-color: #5dade2;
                    }}
                    QPushButton:pressed {{
                        background-color: #1f618d;
                    }}
                """)
        self.button_exit.clicked.connect(partial(self.exitProgram))

        # ------------------------------------------------------------------------------------------------------------------Зміна ієрархії елементів
        self.label_language.raise_()
        self.label_color.raise_()
        self.radio_english.raise_()
        line4.raise_()
        self.radio_pink.raise_()
        self.wish_text.raise_()
        line5.raise_()
        self.button_closeSettings.raise_()
        self.button_Statistics.raise_()
        self.button_Music.raise_()

    # Функція-обробник для демонстрації фрейму зі статисткою користувача
    def showUserStatistics(self, window):
        # ------------------------------------------------------------------------------------------------------------------Фрейм відображення статистики

        frame_UserStatistics = QFrame(window)
        frame_UserStatistics.setGeometry(0, 0, 1315, 917)
        frame_UserStatistics.show()
        frame_UserStatistics.setStyleSheet(f"""
                            QFrame {{
                                background-color: {self.widgetsColor[0]}; /* Фон картки */
                                border-radius: 10px; /* Закруглені кути */
                            }}
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

        button_return.setStyleSheet(f"""
                                QPushButton {{
                                    background-color: {self.widgetsColor[1]}; /* Колір кнопки */
                                    color: #eb8934; /* Колір тексту */
                                    border-radius: 30px; /* Закруглення кутів */
                                }}
                                QPushButton:hover {{
                                    background-color: #5dade2; /* Колір кнопки при наведенні */
                                }}
                                QPushButton:pressed {{
                                    background-color: #1f618d; /* Колір кнопки при натисканні */
                                }}
                            """)
        button_return.clicked.connect(
            partial(self.hide_frame_UserStatistics, frame_UserStatistics))

        # ------------------------------------------------------------------------------------------------------------------Назва вікна

        title_window = QLabel(frame_UserStatistics)
        title_window.setGeometry(488, 23, 335, 55)
        title_window.setText(self.widgetsText["title_window"][self.widgetsLanguage])
        title_window.show()

        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        title_window.setFont(font)

        title_window.setFrameShape(QLabel.StyledPanel)
        title_window.setFrameShadow(QLabel.Plain)
        title_window.setAlignment(Qt.AlignCenter)
        title_window.setStyleSheet(f"""
                    QLabel {{
                        background-color: {self.widgetsColor[1]}; /* Колір фону */
                        color: black; /* Колір тексту */
                        border-radius: 10px; /* Закруглення кутів */
                    }}
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

        button_help.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {self.widgetsColor[1]}; /* Колір кнопки */
                            color: #eb8934; /* Колір тексту */
                            border-radius: 30px; /* Закруглення кутів */
                        }}
                        QPushButton:hover {{
                            background-color: #5dade2; /* Колір кнопки при наведенні */
                        }}
                        QPushButton:pressed {{
                            background-color: #1f618d; /* Колір кнопки при натисканні */
                        }}
                    """)

        # Підключення сигналу "clicked" до обробника
        button_help.clicked.connect(
            partial(self.main_window.showHelpWindow, self.widgetsText["button_help_statistics"][self.widgetsLanguage],
                    "FingerImages/Записування з екрана 2025-04-16 112136.gif"))

        # ------------------------------------------------------------------------------------------------------------------Заголовки

        title_facts = QLabel(frame_UserStatistics)
        title_facts.setGeometry(48, 135, 470, 55)
        title_facts.setText(self.widgetsText["title_facts"][self.widgetsLanguage])
        title_facts.show()

        font3 = QFont()
        font3.setBold(True)
        font3.setPointSize(15)
        title_facts.setFont(font3)

        title_facts.setFrameShape(QLabel.StyledPanel)
        title_facts.setFrameShadow(QLabel.Plain)
        title_facts.setAlignment(Qt.AlignCenter)
        title_facts.setStyleSheet(f"""
                            QLabel {{
                                background-color: {self.widgetsColor[1]}; /* Колір фону */
                                color: black; /* Колір тексту */
                                border-radius: 10px; /* Закруглення кутів */
                            }}
                        """)

        title_correctGestures = QLabel(frame_UserStatistics)
        title_correctGestures.setGeometry(796, 135, 470, 55)
        title_correctGestures.setText(self.widgetsText["title_correctGestures"][self.widgetsLanguage])
        title_correctGestures.show()

        title_correctGestures.setFont(font3)

        title_correctGestures.setFrameShape(QLabel.StyledPanel)
        title_correctGestures.setFrameShadow(QLabel.Plain)
        title_correctGestures.setAlignment(Qt.AlignCenter)
        title_correctGestures.setStyleSheet(f"""
                                    QLabel {{
                                        background-color: {self.widgetsColor[1]}; /* Колір фону */
                                        color: black; /* Колір тексту */
                                        border-radius: 10px; /* Закруглення кутів */
                                    }}
                                """)

        # ------------------------------------------------------------------------------------------------------------------Фрейм цікавих фактів

        frame_facts = QFrame(frame_UserStatistics)
        frame_facts.setGeometry(48, 210, 470, 450)
        frame_facts.show()
        frame_facts.setStyleSheet(f"""
                                    QFrame {{
                                        background-color: {self.widgetsColor[1]}; /* Фон картки */
                                        border-radius: 10px; /* Закруглені кути */
                                        border: 5 solid black;
                                    }}
                                """)

        label_mode = QLabel(frame_facts)
        label_mode.setGeometry(30, 30, 300, 55)
        label_mode.setText(self.widgetsText["label_mode"][self.widgetsLanguage])
        label_mode.show()

        font4 = QFont()
        font4.setBold(False)
        font4.setPointSize(15)
        label_mode.setFont(font4)

        label_mode.setStyleSheet(f"""
                                    QLabel {{
                                        background-color: {self.widgetsColor[1]}; /* Колір фону */
                                        color: black; /* Колір тексту */
                                        border: none;
                                    }}
                                """)

        UserModes = {
            0: ["Жести однією рукою", "Жести двума руками", "Користувацький рівень"],
            1: ["Gestures with one hand", "Gestures with two hand", "User level"]
        }

        userMode = (lambda: self.get_userLikeMode())()

        label_modeAnswer = QLabel(frame_facts)
        label_modeAnswer.setGeometry(30, 95, 410, 55)

        label_modeAnswer.setText(UserModes[self.widgetsLanguage][userMode])
        label_modeAnswer.show()

        label_modeAnswer.setFont(font3)
        label_modeAnswer.setFrameShape(QLabel.StyledPanel)
        label_modeAnswer.setFrameShadow(QLabel.Plain)
        label_modeAnswer.setAlignment(Qt.AlignCenter)

        label_modeAnswer.setStyleSheet(f"""
                                            QLabel {{
                                                background-color: {self.widgetsColor[1]}; /* Колір фону */
                                                color: black; /* Колір тексту */
                                                border: none;
                                            }}
                                        """)
        # --------------------------------------------------
        label_numberSessionsLastMonth = QLabel(frame_facts)
        label_numberSessionsLastMonth.setGeometry(30, 170, 300, 55)
        label_numberSessionsLastMonth.setText(self.widgetsText["label_numberSessionsLastMonth"][self.widgetsLanguage])
        label_numberSessionsLastMonth.show()

        label_numberSessionsLastMonth.setFont(font4)

        label_numberSessionsLastMonth.setStyleSheet(f"""
                                                    QLabel {{
                                                        background-color: {self.widgetsColor[1]}; /* Колір фону */
                                                        color: black; /* Колір тексту */
                                                        border: none;
                                                    }}
                                                """)

        label_numberSessionsLastMonthAnswer = QLabel(frame_facts)
        label_numberSessionsLastMonthAnswer.setGeometry(30, 235, 410, 55)
        label_numberSessionsLastMonthAnswer.setText(self.get_NumberSessionLastMonth())
        label_numberSessionsLastMonthAnswer.show()

        label_numberSessionsLastMonthAnswer.setFont(font3)
        label_numberSessionsLastMonthAnswer.setFrameShape(QLabel.StyledPanel)
        label_numberSessionsLastMonthAnswer.setFrameShadow(QLabel.Plain)
        label_numberSessionsLastMonthAnswer.setAlignment(Qt.AlignCenter)

        label_numberSessionsLastMonthAnswer.setStyleSheet("""
                                                            QLabel {
                                                                background-color: none; /* Колір фону */
                                                                color: black; /* Колір тексту */
                                                                border: none;
                                                            }
                                                        """)

        # --------------------------------------------------
        label_AverageTimeSessions = QLabel(frame_facts)
        label_AverageTimeSessions.setGeometry(30, 305, 370, 55)
        label_AverageTimeSessions.setText(self.widgetsText["label_AverageTimeSessions"][self.widgetsLanguage])
        label_AverageTimeSessions.show()

        label_AverageTimeSessions.setFont(font4)

        label_AverageTimeSessions.setStyleSheet(f"""
                                                    QLabel {{
                                                        background-color: {self.widgetsColor[1]}; /* Колір фону */
                                                        color: black; /* Колір тексту */
                                                        border: none;
                                                    }}
                                                """)

        label_AverageTimeSessionsAnswer = QLabel(frame_facts)
        label_AverageTimeSessionsAnswer.setGeometry(30, 365, 410, 55)
        label_AverageTimeSessionsAnswer.setText(self.get_AverageTimeSession())
        label_AverageTimeSessionsAnswer.show()

        label_AverageTimeSessionsAnswer.setFont(font3)
        label_AverageTimeSessionsAnswer.setFrameShape(QLabel.StyledPanel)
        label_AverageTimeSessionsAnswer.setFrameShadow(QLabel.Plain)
        label_AverageTimeSessionsAnswer.setAlignment(Qt.AlignCenter)

        label_AverageTimeSessionsAnswer.setStyleSheet("""
                                                                    QLabel {
                                                                        background-color: none; /* Колір фону */
                                                                        color: black; /* Колір тексту */
                                                                        border: none;
                                                                    }
                                                                """)

        # ------------------------------------------------------------------------------------------------------------------Фрейм правильних жестів

        frame_correctGestures = QFrame(frame_UserStatistics)
        frame_correctGestures.setGeometry(796, 210, 470, 450)
        frame_correctGestures.show()
        frame_correctGestures.setStyleSheet(f"""
                                            QFrame {{
                                                background-color: {self.widgetsColor[1]}; /* Фон картки */
                                                border-radius: 10px; /* Закруглені кути */
                                                border: 5 solid black;
                                            }}
                                        """)
        y = 0
        # Прогрес-бари та підписи
        for item in (lambda: self.get_correctGestures())():
            image, value, maxvalue = item
            # Зображення
            image_label = QLabel(frame_correctGestures)
            image_label.setGeometry(30, 30 + y, 100, 100)
            pixmap = QPixmap(image)
            image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            image_label.setStyleSheet("""
                                                            QLabel {
                                                                background-color: none; /* Колір фону */
                                                                border: none;
                                                            }
                                                        """)
            image_label.show()

            # Прогрес-бар
            progress_bar = QProgressBar(frame_correctGestures)
            progress_bar.setGeometry(150, 55 + y, 300, 50)
            progress_bar.setMinimum(0)
            progress_bar.setMaximum(maxvalue)
            progress_bar.setValue(value)
            progress_bar.setFormat("%v/%m")  # Показує поточне значення / максимум (наприклад, 7/10)
            progress_bar.setAlignment(Qt.AlignCenter)  # Вирівнювання тексту по центру
            progress_bar.setStyleSheet("""
                QProgressBar {
                    border: none;
                    border-radius: 15px;
                    background-color: #FFF5E6;  /* Колір фону */
                }
                QProgressBar::chunk {
                    background-color: #FF69B4;  /* Колір заповнення */
                    border-radius: 15px;
                }
            """)
            progress_bar.show()
            y += 140

        # ------------------------------------------------------------------------------------------------------------------Пасхалка від розробника

        title_outDeveloper = QLabel(frame_UserStatistics)
        title_outDeveloper.setGeometry(160, 850, 980, 35)
        title_outDeveloper.setText(self.widgetsText["title_outDeveloper"][self.widgetsLanguage])
        title_outDeveloper.show()

        font5 = QFont()
        font5.setBold(True)
        font5.setPointSize(10)
        title_outDeveloper.setFont(font5)

        title_outDeveloper.setFrameShape(QLabel.StyledPanel)
        title_outDeveloper.setFrameShadow(QLabel.Plain)
        title_outDeveloper.setAlignment(Qt.AlignCenter)
        title_outDeveloper.setStyleSheet(f"""
                                    QLabel {{
                                        background-color: {self.widgetsColor[1]}; /* Колір фону */
                                        color: black; /* Колір тексту */
                                        border-radius: 10px; /* Закруглення кутів */
                                    }}
                                """)

    # Функція для повернення значення улюбленого режиму гри користувача
    def get_userLikeMode(self):
        userModes = {
            "Жести однією рукою": 0,
            "Жести двума руками": 1,
            "Користувацький рівень": 2
        }
        # Додати запит до бд
        result = "Жести однією рукою"
        return userModes[result]

    # Функція для повернення значення середньої кількості сесій користувача за місяць
    def get_NumberSessionLastMonth(self):
        # Додати запит до бд
        result = 15
        return str(result)

    # Функція для повернення значення середньої часу сесій користувача за місяць
    def get_AverageTimeSession(self):
        # Додати запит до бд
        result = 26
        return str(result)

    # Функція для повернення значення найбільш правильних жестів користувача
    def get_correctGestures(self):
        # Додати запит до бд
        result = [["FingerImages/both_gesture_heart.jpg", 7, 10], ["FingerImages/gesture_oke.jpg", 5, 10], ["FingerImages/both_gesture_uwu.jpg", 2, 10]]
        return result

    # Функція-обробник для того, щоб сховати фрейм статистки користувача
    def hide_frame_UserStatistics(self, frame_UserStatistics):
        print("close: frame_UserStatistics")
        frame_UserStatistics.hide()

    # Функція-обробник кнопки для закриття меню налаштувань
    def hide_settings(self, settings_frame, unvisible_frame):
        settings_frame.hide()
        unvisible_frame.hide()

    # Функція-обробник для встановлення початкових значень налаштувань
    def set_defaultSettings(self):
        self.set_color(["9EFFA5", "DAFFDF"])
        self.radio_green.setChecked(True)
        self.set_language(0)
        self.radio_ukrainian.setChecked(True)

    # Функція-обробник для виходу зі застосунку
    def exitProgram(self):
        self.saveSettings()
        self.main_window.window.saveSessionTime()
        self.Music.stop_music()
        QApplication.quit()

    # Функція-обробник для опрацювання музики
    def musicCatcher(self):
        if not self.button_Music_Checked:
            # Завантажуємо іконку
            icon = QIcon("FingerImages/musicMute.png")
            self.button_Music.setIcon(icon)
            self.Music.stop_music()
            self.button_Music_Checked = True
        else:
            # Завантажуємо іконку
            icon = QIcon("FingerImages/musicPlay.png")
            self.button_Music.setIcon(icon)
            self.Music.play_music()
            self.button_Music_Checked = False

    # Функція для підвантаження налаштувань в застосунок
    def uploadSettings(self):
        filename = "settings.txt"
        languages = {
            "ukrainian": 0,
            "english": 1
        }
        default_colors = ["#9EFFA5", "#DAFFDF"]
        color = default_colors.copy()  # Ініціалізуємо значення за замовчуванням
        language = "ukrainian"  # Значення за замовчуванням для мови

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line:  # Пропускаємо порожні рядки
                        continue
                    if line.startswith("Language:"):
                        language = line.split(":", 1)[1].strip().lower()
                    elif line.startswith("Color:"):
                        # Отримуємо частину після "Color:" і прибираємо пробіли
                        color_str = line.split(":", 1)[1].strip()
                        # Розбиваємо на кольори, прибираємо лапки та '#'
                        colors = [c.strip().strip('"').lstrip('#') for c in color_str.split(",")]
                        # Перевіряємо, чи отримали два кольори
                        if len(colors) == 2 and all(c for c in colors):
                            color = colors
                        else:
                            print("Некоректний формат кольорів. Використовуються значення за замовчуванням.")
                            color = default_colors

            # Встановлюємо значення
            self.set_color(color)
            self.set_language(languages.get(language, 0))  # 0 як значення за замовчуванням

        except FileNotFoundError:
            print(f"Файл {filename} не знайдено. Використовуються налаштування за замовчуванням.")
            self.set_color(["9EFFA5", "DAFFDF"])
            self.set_language(languages["ukrainian"])
        except Exception as e:
            print(f"Помилка при читанні файлу налаштувань: {e}")
            self.set_color(["9EFFA5", "DAFFDF"])
            self.set_language(languages["ukrainian"])

    # Функція для збереження налаштувань застосунку
    def saveSettings(self):
        filename = "settings.txt"
        # Словник для зворотного перетворення числового ідентифікатора мови у назву
        languages = {
            0: "ukrainian",
            1: "english"
        }

        try:
            # Отримуємо поточні налаштування з об'єкта
            current_language = languages[(self.widgetsLanguage)]
            current_colors = self.widgetsColor

            # Формуємо вміст файлу
            settings_content = f"Language: {current_language}\n"
            settings_content += f"Color: \"{current_colors[0]}\", \"{current_colors[1]}\""

            # Записуємо у файл
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(settings_content)

        except Exception as e:
            print(f"Помилка при збереженні налаштувань: {e}")