import sys
import mediapipe as mp
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QPushButton, QScrollArea, QFrame, QHBoxLayout, \
    QGraphicsOpacityEffect, QMessageBox
from PyQt5.QtGui import QImage, QPixmap, QFont, QIcon, QTransform, QMovie
from PyQt5.QtCore import QTimer, Qt, QSize
from functools import partial
import LelelCounting, SettingsModule, RebuildsComponents, UserLevelsModule, Music
import requests
from packaging import version

class MainWindow():
    def __init__(self):
        self.current_game_level = "Undefined123"
        self.widgetsColor = ["#9EFFA5", "#DAFFDF"]
        self.widgetsLanguage = 0
        self.widgetsText = {
            "title_window": ['Потренуємо ваші нейрони', 'ToTrainYourNeurons'],
            "button_start": ['Спробувати', 'Try it'],
            "msg_box": [ ['Повідомлення', 'Вибачте, але рівень ще в стадії розробки😅'], ['Message', 'Sorry, but the level is still under development😅']],
            "best_try_level": ['Найкращий результат: ', 'The best result: '],
            "number_try_level": ['Кількість спроб: ', 'Count of attempts: '],
            "start_level_button": ['Почати', 'Start'],
            "textForLevels": ['Рівень ', 'Level '],
            "button_help": ["Допоміжний текст!!!", "Help text!!!"],
            "button_help_select_level": ["Допоміжний текст 2!!!", "Help text 2!!!"],
            "button_help_ForUserLevels": ["Допоміжний текст 3!!!", "Help text 3!!!"]
        }
        # Компоненти, що залежні від налаштувань додатку
        self.window = None
        self.title_window = None
        self.level_checking = None
        self.select_Level = None
        self.button_help = None
        self.settings_frame = None
        self.button_settings = None

        # Оголошення зв'язків з модулями застосунку
        self.levelCounting = LelelCounting.CreateLevel()
        self.MainWindowLink = None
        self.settingsModule = None
        self.Music = Music.Music()

    # Функція для ініціалізації зв'язку з модулем налаштувань
    def setMainWindowLink(self, MainWindowLink):
        self.check_for_updates()
        self.MainWindowLink = MainWindowLink
        self.settingsModule = SettingsModule.SettingsModule(self.MainWindowLink, self.levelCounting, self.Music)
        # self.settingsModule = SettingsModule.SettingsModule(self.MainWindowLink, self.levelCounting)
        self.settingsModule.uploadSettings()
        self.addUserVisits()

    # Функція для зміни мови додатку
    def setLanguage(self, Language):
        self.widgetsLanguage = Language
        # print(f"class MainWindow(): def setLanguage(self, Language): {Language}")
        self.update_ui()

    # Функція для зміни мови додатку
    def setColor(self, color):
        self.widgetsColor = color
        # print(f"class MainWindow(): def setColor(self, color): {color}")
        self.update_ui()

    # Функція для оновлення візуалу компонентів вікна
    def update_ui(self):
        frame_style = f"""
                        QFrame {{
                                background-color: {self.widgetsColor[0]}; /* Фон картки #9EFFA5; */
                                border-radius: 10px; /* Закруглені кути */
                            }}
                        """
        button_style = f"""
                        QPushButton {{
                            background-color: {self.widgetsColor[0]}; /* Колір кнопки */
                            color: #eb8934; /* Колір тексту */
                            border-radius: 30px; /* Закруглення кутів */
                        }}
                        QPushButton:hover {{
                            background-color: #5dade2; /* Колір кнопки при наведенні */
                        }}
                        QPushButton:pressed {{
                            background-color: #1f618d; /* Колір кнопки при натисканні */
                        }}
                    """
        if self.title_window:
            self.title_window.setText(self.widgetsText["title_window"][self.widgetsLanguage])
            self.title_window.setStyleSheet(f"""
                            QLabel {{
                                background-color: {self.widgetsColor[0]}; /* Колір фону */
                                color: black; /* Колір тексту */
                                border-radius: 10px; /* Закруглення кутів */
                            }}
                        """)
        self.fill_frame_level_checking()
        self.settings_frame.setStyleSheet(frame_style)
        self.button_settings.setStyleSheet(button_style)
        self.button_help.setStyleSheet(button_style)
        self.select_Level.setStyleSheet(frame_style)
        self.window.set_color(self.widgetsColor)
        self.window.set_language(self.widgetsLanguage)

    # Головна функція
    def mainWindow(self, Main):
        # Головне вікно застосунку
        # self.window = RebuildsComponents.MainWindow(self.Music)
        self.window = RebuildsComponents.MainWindow(self.Music)

        # ------------------------------------------------------------------------------------------------------------------Фрейм Налаштувань

        self.settings_frame = QFrame(self.window)
        self.settings_frame.setGeometry(0, 0, 438, 863)
        self.settings_frame.hide()
        self.settings_frame.setStyleSheet(f"""
                        QFrame {{
                            background-color: {self.widgetsColor[0]}; /* Фон картки #9EFFA5; */
                            border-radius: 10px; /* Закруглені кути */
                        }}
                    """)

        # ------------------------------------------------------------------------------------------------------------------Фрейм Прозорий

        unvisible_frame = RebuildsComponents.ClickableFrame(self.window)
        unvisible_frame.setGeometry(0, 0, 1315, 917)
        unvisible_frame.hide()
        unvisible_frame.setStyleSheet("""
                            QFrame {
                                background-color: #8A8A8A; /* Фон картки #9EFFA5; */
                                border-radius: 10px; /* Закруглені кути */
                            }
                        """)
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.4)

        unvisible_frame.setGraphicsEffect(opacity_effect)

        # ------------------------------------------------------------------------------------------------------------------Кнопка Налаштувань

        self.button_settings = QPushButton(self.window)
        self.button_settings.setGeometry(48, 23, 60, 60)
        # Завантажуємо іконку
        icon = QIcon("FingerImages/settings.png")
        self.button_settings.setIcon(icon)
        self.button_settings.setIconSize(QSize(50, 50))  # Налаштовуємо розмір іконки (50x50 пікселів)

        font = QFont()
        font.setBold(True)
        font.setPointSize(14)
        self.button_settings.setFont(font)

        self.button_settings.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.widgetsColor[0]}; /* Колір кнопки */
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
        self.button_settings.clicked.connect(lambda: self.settingsModule.show_settings(self.settings_frame, unvisible_frame, self.window))

        # ------------------------------------------------------------------------------------------------------------------Назва програми

        self.title_window = QLabel(self.window)
        self.title_window.setGeometry(468, 23, 380, 55)
        self.title_window.setText(self.widgetsText["title_window"][self.widgetsLanguage])

        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        self.title_window.setFont(font)

        self.title_window.setFrameShape(QLabel.StyledPanel)
        self.title_window.setFrameShadow(QLabel.Plain)
        self.title_window.setAlignment(Qt.AlignCenter)
        self.title_window.setStyleSheet(f"""
                QLabel {{
                    background-color: {self.widgetsColor[0]}; /* Колір фону */
                    color: black; /* Колір тексту */
                    border-radius: 10px; /* Закруглення кутів */
                }}
            """)

        # ------------------------------------------------------------------------------------------------------------------Кнопка Довідки

        self.button_help = QPushButton(self.window)
        self.button_help.setGeometry(1206, 18, 60, 60)
        self.button_help.setText("?")

        font = QFont()
        font.setBold(True)
        font.setPointSize(18)
        self.button_help.setFont(font)

        self.button_help.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.widgetsColor[0]}; /* Колір кнопки */
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
        self.button_help.clicked.connect(partial(self.showHelpWindow, self.widgetsText["button_help"][self.widgetsLanguage], "FingerImages/Записування з екрана 2025-04-16 112136.gif"))

        # ------------------------------------------------------------------------------------------------------------------Фрейм вибірки рівня

        self.select_Level = QFrame(self.window)
        self.select_Level.setGeometry(0, 0, 1315, 917)
        self.select_Level.hide()
        self.select_Level.setStyleSheet(f"""
                    QFrame {{
                        background-color: {self.widgetsColor[0]}; /* Фон картки */
                        border-radius: 10px; /* Закруглені кути */
                    }}
                """)

        # ------------------------------------------------------------------------------------------------------------------Фрейм з картками для вибору режиму тренування

        self.level_checking = QScrollArea(self.window)
        self.level_checking.setGeometry(48, 90, 1216, 800)

        self.level_checking.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # Горизонтальна прокрутка
        self.level_checking.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Відключення вертикальної прокрутки

        self.fill_frame_level_checking()

        self.level_checking.setStyleSheet("""
        QScrollArea {
            border: none; /* Забрати рамку, якщо потрібне чисте тло */
            background-color: #DAFFDF; /* Колір фону */
        }
        """)

        # ------------------------------------------------------------------------------------------------------------------Кінець Фрейм з картками для вибору режиму тренування

        # Підняття елементів на інші поверхи
        self.select_Level.raise_()
        self.title_window.raise_()
        self.button_help.raise_()
        unvisible_frame.raise_()
        self.settings_frame.raise_()

        # ------------------------------------------------------------------------------------------------------------------Закриття програми
        self.window.show()
        self.setMainWindowLink(Main)

    # Функція-обробник кнопки для демонстрації вікна довідки
    def showHelpWindow(self, helpText, helpGif):
        print("showHelpWindow")
        helpWindow = RebuildsComponents.ModalWindow(800, 200, 700, 600)
        helpWindow.setWindowTitle("Help window")
        helpWindow.setStyleSheet(f"""
                               QDialog {{
                                   background-color: {self.widgetsColor[1]}; /* Колір вікна */
                               }}
                           """)

        label_helpText = QLabel(helpWindow)
        label_helpText.setGeometry(20, 50, 200, 500)
        label_helpText.setText(helpText)

        font = QFont()
        font.setBold(True)
        font.setPointSize(14)
        label_helpText.setFont(font)
        label_helpText.setWordWrap(True)

        label_helpText.setStyleSheet(f"""
                        QLabel {{
                            background-color: {self.widgetsColor[0]}; /* Колір фону */
                            color: black; /* Колір тексту */
                            border-radius: 10px; /* Закруглення кутів */
                        }}
                    """)

        labelGif = QLabel(helpWindow)
        labelGif.setGeometry(250, 50, 400, 500)

        movie = QMovie(helpGif)
        labelGif.setMovie(movie)
        movie.start()

        labelGif.show()

        helpWindow.exec_()  # Запускаємо модальне вікно (блокує основне)

    # Функція, що заповнює фрейм level_checking картками
    def fill_frame_level_checking(self):
        # Контейнер для вмісту
        content_widget = QWidget()
        layout = QHBoxLayout(content_widget)  # Горизонтальне розташування
        layout.setContentsMargins(10, 10, 10, 10)  # Відступи між елементами
        layout.setSpacing(30)  # Проміжки між картками

        titles_cards = {
            0: ["Жести однією рукою", "Жести двума руками", "Користувацький рівень", "В розробці"],
            1: ["Gestures with one hand", "Gestures with two hand", "User level", "In development"]
        }
        text_cards = {
            0: ["💡 Мета: Ознайомлення з базовими жестами, такими як вказування, махання, показування знаків.",

                "💡 Мета: Вивчення жестів для взаємодії з великими об'єктами, передачі складних команд або вираження емоцій.",

                "\n💡 Мета: Дати можливість користувачам створювати унікальні жести чи міміку для персональних сценаріїв.",

                ""],
            1: ["💡 Meta: Familiarize yourself with basic gestures such as pointing, waving, and signing.",

                "💡 Meta: Learn gestures to interact with large objects, communicate complex commands, or express emotions.",

                "\n💡 Meta: Enable users to create unique gestures or facial expressions for personalized scenarios.",

                ""]
        }
        images_cards = ["FingerImages/1.jpg", "FingerImages/2.jpg", "FingerImages/3.jpg",
                        "FingerImages/InDevelopment.png"]

        # Додавання "карток" у контейнер
        for i in range(4):  # 4 карток
            card = self.create_card(titles_cards[self.widgetsLanguage][i], text_cards[self.widgetsLanguage][i],
                                    images_cards[i])

            # --------------------------------------------------------------------------------------------------------------Кнопка картки для переходу в режим тренування
            button_start = QPushButton(card)
            button_start.setGeometry(30, 393 + 100, 320, 55)
            button_start.setText(self.widgetsText["button_start"][self.widgetsLanguage])
            button_start.setStyleSheet(f"""
                                    QPushButton {{
                                        background-color: {self.widgetsColor[1]}; /* Колір кнопки */
                                        color: black; /* Колір тексту */
                                        border-radius: 10px; /* Закруглення кутів */
                                        font-size: 17px;
                                        font-weight: bold;
                                    }}
                                    QPushButton:hover {{
                                        background-color: #5dade2; /* Колір кнопки при наведенні */
                                    }}
                                    QPushButton:pressed {{
                                        background-color: #1f618d; /* Колір кнопки при натисканні */
                                    }}
                                """)
            # Підключення сигналу "clicked" до обробника
            if not card.objectName() == "Користувацький рівень" and not card.objectName() == "User level":
                button_start.clicked.connect(
                    partial(self.visible_select_level_click,card))
            else:
                button_start.clicked.connect(
                    partial(self.visible_select_levelForUserLevels_click, card))

            # --------------------------------------------------------------------------------------------------------------Кінець картки
            layout.addWidget(card)  # Додаємо картку у макет

        # Встановлення контейнера у QScrollArea
        content_widget.setLayout(layout)
        self.level_checking.setWidget(content_widget)
        self.level_checking.setWidgetResizable(True)  # Адаптація розміру контейнера до QScrollArea

    # Функція-обробник кнопки для відображення компонентів фрейму вибірки рівня
    def visible_select_level_click(self, card):
        for widget in self.select_Level.findChildren(QWidget):
            widget.deleteLater()
        if card.objectName() == "В розробці" or card.objectName() == "In development":
            # Створюємо повідомлення
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle(self.widgetsText["msg_box"][self.widgetsLanguage][0])
            msg_box.setText(self.widgetsText["msg_box"][self.widgetsLanguage][1])
            # Відображаємо повідомлення
            msg_box.exec_()
            return False

        self.select_Level.show()
        self.title_window.setStyleSheet(f"""
                    QLabel {{
                        background-color: {self.widgetsColor[1]}; /* Колір фону */
                        color: black; /* Колір тексту */
                        border-radius: 10px; /* Закруглення кутів */
                    }}
                """)
        self.button_help.setStyleSheet(f"""
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
        try:
            self.button_help.clicked.disconnect()
        except Exception:
            pass  # Якщо немає підключених обробників, ігноруємо помилку

        # Підключення сигналу "clicked" до обробника
        self.button_help.clicked.connect(
            partial(self.showHelpWindow, self.widgetsText["button_help_select_level"][self.widgetsLanguage],
                    "FingerImages/Записування з екрана 2025-04-16 112136.gif"))

        self.duplicate_card_to_frame(card)

        # ------------------------------------------------------------------------------------------------------------------Кнопка для повернення на головну сторінку

        button_return = QPushButton(self.select_Level)
        button_return.setGeometry(48, 23, 60, 60)
        # button_return.setText("<-")

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

        font = QFont()
        font.setBold(True)
        font.setPointSize(18)
        button_return.setFont(font)

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
            partial(self.hide_select_level_click))

        # ------------------------------------------------------------------------------------------------------------------Фрейм для відображення рівнів

        levels = QFrame(self.select_Level)
        levels.setGeometry(490, 100, 770, 750)
        levels.show()
        levels.setStyleSheet(f"""
                        QFrame {{
                            background-color: {self.widgetsColor[1]}; /* Фон картки */
                            border-radius: 10px; /* Закруглені кути */
                        }}
                    """)

        # ------------------------------------------------------------------------------------------------------------------Фрейм для відображення статусу рівня

        level_status = QFrame(levels)
        level_status.setGeometry(45, 480, 680, 230)
        level_status.setObjectName("level_status")
        level_status.setStyleSheet("""
                            QFrame {
                                background-color: none; /* Фон картки */
                                border-radius: 10px; /* Закруглені кути */
                                border: 5px solid blue;
                            }
                        """)
        level_status.hide()

        # ------------------------------------------------------------------------------------------------------------------Кнопки вибірки рівня

        self.show_levels_buttons(levels, 40, 1, level_status)
        self.show_levels_buttons(levels, 260, 4, level_status)

        # ------------------------------------------------------------------------------------------------------------------Відображення найкращого проходження рівня

        best_try_level = QLabel(level_status)
        best_try_level.setGeometry(50, 50, 250, 50)
        best_try_level.setText(self.widgetsText["best_try_level"][self.widgetsLanguage])
        best_try_level.setStyleSheet("""
                    QLabel {
                        background-color: none; /* Колір фону */
                        color: black; /* Колір тексту */
                        border: none;
                        font-size: 23px;
                    }
                """)

        best_try_level_num = QLabel(level_status)
        best_try_level_num.setGeometry(300, 50, 50, 50)
        best_try_level_num.setText("0 🖐️")
        best_try_level_num.setStyleSheet("""
                        QLabel {
                            background-color: none; /* Колір фону */
                            color: black; /* Колір тексту */
                            border: none;
                            font-size: 23px;
                            font-weight: bold;
                        }
                    """)

        # ------------------------------------------------------------------------------------------------------------------Відображення кількості проходжень рівня

        number_try_level = QLabel(level_status)
        number_try_level.setGeometry(50, 130, 250, 50)
        number_try_level.setText(self.widgetsText["number_try_level"][self.widgetsLanguage])
        number_try_level.setStyleSheet("""
                        QLabel {
                            background-color: none; /* Колір фону */
                            color: black; /* Колір тексту */
                            border: none;
                            font-size: 23px;
                        }
                    """)

        number_try_level_num = QLabel(level_status)
        number_try_level_num.setGeometry(300, 130, 50, 50)
        number_try_level_num.setText("0")
        number_try_level_num.setStyleSheet("""
                            QLabel {
                                background-color: none; /* Колір фону */
                                color: black; /* Колір тексту */
                                border: none;
                                font-size: 23px;
                                font-weight: bold;
                            }
                        """)

        # ------------------------------------------------------------------------------------------------------------------Фрейм для тренування

        level_cv_frame = QFrame(self.select_Level)
        level_cv_frame.setGeometry(0, 0, 1315, 917)
        level_cv_frame.hide()
        level_cv_frame.setStyleSheet(f"""
                        QFrame {{
                            background-color: {self.widgetsColor[0]}; /* Фон картки */
                            border-radius: 10px; /* Закруглені кути */
                        }}
                    """)

        # ------------------------------------------------------------------------------------------------------------------Кнопка для того, щоб розпочати тренування

        start_level_button = QPushButton(level_status)
        start_level_button.setGeometry(430, 80, 170, 80)
        start_level_button.setText(self.widgetsText["start_level_button"][self.widgetsLanguage])
        start_level_button.setObjectName("start_level_button")
        start_level_button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {self.widgetsColor[0]}; /* Фон кнопки */
                        border-radius: 10px; /* Закруглені кути */
                        border: 3px solid black;
                        border-color: {self.widgetsColor[0]};
                        font-size: 25px;
                        font-weight: bold;
                    }}
                    QPushButton:hover {{
                        border-color: #5dade2; /* Колір кнопки при наведенні */
                    }}
                    QPushButton:pressed {{
                        border-color: #1f618d; /* Колір кнопки при натисканні */
                    }}
                """)

        self.levelCounting.setDefaultParameters()
        start_level_button.clicked.connect(lambda: self.levelCounting.create_new_level_click(
            self.current_game_level, card.objectName(), level_cv_frame))

        # ------------------------------------------------------------------------------------------------------------------

    # Функція-обробник кнопки для приховання компонентів фрейму вибірки рівня
    def hide_select_level_click(self):
        print("Кнопку натиснуто!")
        self.select_Level.hide()
        self.title_window.setStyleSheet(f"""
                    QLabel {{
                        background-color: {self.widgetsColor[0]}; /* Колір фону */
                        color: black; /* Колір тексту */
                        border-radius: 10px; /* Закруглення кутів */
                    }}
                """)
        self.button_help.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {self.widgetsColor[0]}; /* Колір кнопки */
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
        try:
            self.button_help.clicked.disconnect()
        except Exception:
            pass  # Якщо немає підключених обробників, ігноруємо помилку

        # Підключення сигналу "clicked" до обробника
        self.button_help.clicked.connect(
            partial(self.showHelpWindow, self.widgetsText["button_help"][self.widgetsLanguage],
                    "FingerImages/Записування з екрана 2025-04-16 112136.gif"))

    # Функція для створення картки виду вправ
    def create_card(self, title_text, description_text, image_path, parent=None):
        card = QFrame(parent)
        card.setObjectName(title_text)
        card.setFixedSize(378, 750)  # Фіксований розмір картки
        card.setStyleSheet(f"""
                    QFrame {{
                        background-color: {self.widgetsColor[0]}; /* Фон картки */
                        border-radius: 10px; /* Закруглені кути */
                    }}
                """)

        # Наповнення картки
        # ------------------------------------------------------------------------------------------------------------------Назва картки
        title = QLabel(title_text, card)
        title.setGeometry(3, 30 + 100, 378, 50)
        title.setAlignment(Qt.AlignCenter)  # Центрування тексту
        title.setObjectName("title_label")  # Задання імені
        title.setStyleSheet("font-size: 23px; font-weight: bold;")

        # ------------------------------------------------------------------------------------------------------------------Опис картки
        text_card = QLabel(description_text, card)
        text_card.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        text_card.setWordWrap(True)
        text_card.setGeometry(30, 80 + 100, 320, 300)
        text_card.setObjectName("description_label")  # Задання імені
        text_card.setStyleSheet(f"font-size: 17px; font-weight: bold; background-color: {self.widgetsColor[1]};"
                                " /* Колір фону */ padding: 5px; /* Відступи всередині рамки */")

        # ------------------------------------------------------------------------------------------------------------------Фото картки
        image_label = QLabel(card)
        if not card.objectName() == "В розробці" or not card.objectName() == "In development":
            image_label.setGeometry(70, 90 + 100, 250, 170)
        else:
            image_label.setGeometry(70, 90 + 150, 250, 170)
        pixmap = QPixmap(image_path)
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)
        image_label.setObjectName("image_label")  # Задання імені

        return card

    # Функція для створення дублікату картки виду вправ
    def duplicate_card_to_frame(self, card):
        # Отримуємо текст і параметри оригінальної картки за назвою об'єкта
        title_label = card.findChild(QLabel, "title_label")
        description_label = card.findChild(QLabel, "description_label")
        image_label = card.findChild(QLabel, "image_label")

        # Зчитуємо дані
        title_text = title_label.text() if title_label else ""
        description_text = description_label.text() if description_label else ""
        pixmap = image_label.pixmap() if image_label else None

        # Створюємо дубльовану картку
        duplicated_card = self.create_card(title_text, description_text, pixmap, self.select_Level)

        # Встановлюємо позицію дубліката
        duplicated_card.setGeometry(45, 100, 378, 750)  # Задайте позицію вручну або автоматично
        duplicated_card.show()

    # Функція для відображення рівнів 1-6 у фреймі вибірки рівня (див. visible_select_level_click() )
    def show_levels_buttons(self, levels, stepY, num, level_status):
        # ------------------------------------------------------------------------------------------------------------------Кнопки вибірки рівня
        stepX = 0
        points = 3
        timeForLevel = 90
        for i in range(3):
            button_level = QPushButton(levels)
            button_level.setGeometry(45 + stepX, stepY, 200, 180)
            button_level.setObjectName("button_level_" + str(num))  # Задання імені
            button_level.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.widgetsColor[0]}; /* Фон кнопки */
                    border-radius: 10px; /* Закруглені кути */
                    border: 3px solid black;
                    border-color: {self.widgetsColor[0]};
                    font-size: 40px;
                    font-weight: bold;
                    padding-top: 20px;
                }}
                QPushButton:hover {{
                    border-color: #5dade2; /* Колір кнопки при наведенні */
                }}
                QPushButton:pressed {{
                    border-color: #1f618d; /* Колір кнопки при натисканні */
                }}
            """)

            if stepY == 40:
                button_level.setText(str(points) + "🖐️")
            else:
                button_level.setText(str(points) + "🖐️" + "\n" + str(timeForLevel) + "🕘")

            stepX += 240  # Збільшуємо крок по осі X
            points += 2
            timeForLevel -= 25
            button_level.show()
            button_level.setCheckable(True)
            button_level.setChecked(False)

            # Підключення сигналу "clicked" до обробника
            button_level.clicked.connect(partial(self.select_level_click, button_level, level_status))

            textForLevels = QLabel(button_level)
            textForLevels.setGeometry(68, 3, 200, 50)
            textForLevels.setText(self.widgetsText["textForLevels"][self.widgetsLanguage] + str(num))
            textForLevels.setStyleSheet("background-color: none; font-size: 15px; font-weight: bold;")
            textForLevels.show()
            num += 1

    # Функція-обробник кнопки для відображення інфо проходження рівня (див. show_levels_buttons() )
    def select_level_click(self, current_button_level, level_status):
        # Блокування всіх інших кнопок
        parent_frame = current_button_level.parent()  # Отримати батьківський фрейм
        for child in parent_frame.findChildren(QPushButton):
            if child != current_button_level and child.objectName() != "start_level_button":
                child.setEnabled(False)  # Заблокувати інші кнопки

        if current_button_level.isChecked():
            print("select_level_click(): " + current_button_level.objectName())
            current_button_level.setChecked(True)
            current_button_level.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {self.widgetsColor[0]}; /* Фон кнопки */
                            border-radius: 10px; /* Закруглені кути */
                            border: 3px solid black;
                            border-color: #6085ff;
                            font-size: 40px;
                            font-weight: bold;
                            padding-top: 20px;
                        }}
                        QPushButton:hover {{
                            border-color: lime; /* Колір кнопки при наведенні */
                        }}
                        QPushButton:pressed {{
                            border-color: #1f618d; /* Колір кнопки при натисканні */
                        }}
                    """)
            level_status.show()
            self.current_game_level = current_button_level.objectName()
        else:
            level_status.hide()
            current_button_level.setChecked(False)
            current_button_level.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {self.widgetsColor[0]}; /* Фон кнопки */
                            border-radius: 10px; /* Закруглені кути */
                            border: 3px solid black;
                            border-color: {self.widgetsColor[0]};
                            font-size: 40px;
                            font-weight: bold;
                            padding-top: 20px;
                        }}
                        QPushButton:hover {{
                            border-color: #5dade2; /* Колір кнопки при наведенні */
                        }}
                        QPushButton:pressed {{
                            border-color: #1f618d; /* Колір кнопки при натисканні */
                        }}
                    """)

            # Розблокування інших кнопок, якщо поточна кнопка відключається
            for child in parent_frame.findChildren(QPushButton):
                child.setEnabled(True)
            self.current_game_level = "Undefined"

    # Функція-обробник кнопки для відображення компонентів фрейму "Користувацький рівень"
    def visible_select_levelForUserLevels_click(self, card):
        for widget in self.select_Level.findChildren(QWidget):
            widget.deleteLater()
        self.select_Level.show()

        level_cv_frame = QFrame(self.select_Level)
        level_cv_frame.setGeometry(0, 0, 1315, 917)
        level_cv_frame.hide()
        level_cv_frame.setStyleSheet(f"""
                            QFrame {{
                                background-color: {self.widgetsColor[0]}; /* Фон картки */
                                border-radius: 10px; /* Закруглені кути */
                            }}
                        """)

        self.title_window.setStyleSheet(f"""
                        QLabel {{
                            background-color: {self.widgetsColor[1]}; /* Колір фону */
                            color: black; /* Колір тексту */
                            border-radius: 10px; /* Закруглення кутів */
                        }}
                    """)
        self.button_help.setStyleSheet(f"""
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

        try:
            self.button_help.clicked.disconnect()
        except Exception:
            pass  # Якщо немає підключених обробників, ігноруємо помилку

        # Підключення сигналу "clicked" до обробника
        self.button_help.clicked.connect(
            partial(self.showHelpWindow, self.widgetsText["button_help_ForUserLevels"][self.widgetsLanguage],
                    "FingerImages/Записування з екрана 2025-04-16 112136.gif"))

        self.duplicate_card_to_frame(card)

        # ------------------------------------------------------------------------------------------------------------------Кнопка для повернення на головну сторінку

        button_return = QPushButton(self.select_Level)
        button_return.setGeometry(48, 23, 60, 60)
        # button_return.setText("<-")

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

        font = QFont()
        font.setBold(True)
        font.setPointSize(18)
        button_return.setFont(font)

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
            partial(self.hide_select_level_click))

        # ------------------------------------------------------------------------------------------------------------------Фрейм для відображення фреймів

        scenario = QFrame(self.select_Level)
        scenario.setGeometry(490, 100, 770, 750)
        scenario.show()
        scenario.setStyleSheet(f"""
                            QFrame {{
                                background-color: {self.widgetsColor[1]}; /* Фон картки */
                                border-radius: 10px; /* Закруглені кути */
                            }}
                        """)

        # ------------------------------------------------------------------------------------------------------------------Фрейм розпочати користувацький рівень

        userLevel = UserLevelsModule.UserLevelsModule(self.widgetsLanguage, self.widgetsColor)
        startUserLevel_frame = RebuildsComponents.ClickableFrame(scenario)
        startUserLevel_frame.setGeometry(20, 20, 355, 710)
        startUserLevel_frame.show()
        startUserLevel_frame.setStyleSheet("""
                                QFrame {
                                    background-color: red; /* Фон картки */
                                    border-radius: 10px; /* Закруглені кути */
                                }
                            """)
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.4)
        startUserLevel_frame.setGraphicsEffect(opacity_effect)
        startUserLevel_frame.clicked.connect(lambda: userLevel.openUserLevelPanel(level_cv_frame))

        # ------------------------------------------------------------------------------------------------------------------Фрейм створення користувацього рівня

        createUserLevel_frame = RebuildsComponents.ClickableFrame(scenario)
        createUserLevel_frame.setGeometry(395, 20, 355, 710)
        createUserLevel_frame.show()
        createUserLevel_frame.setStyleSheet("""
                                QFrame {
                                    background-color: blue; /* Фон картки */
                                    border-radius: 10px; /* Закруглені кути */
                                }
                            """)
        createUserLevel_frame.setGraphicsEffect(opacity_effect)
        createUserLevel_frame.clicked.connect(lambda: userLevel.createUserLevel())

        level_cv_frame.raise_()

    # Функція для перевірки версії застосунку
    def check_for_updates(self):
        Version = "1.0.0"
        try:
            response = requests.get(f"https://api.github.com/repos/Whowrite/Dyplome_gesture/releases/latest")
            response.raise_for_status()
            latest_version = response.json()["tag_name"].lstrip("v")  # Припускаємо, що тег виглядає як "v1.0.0"

            if version.parse(latest_version) > version.parse(Version):
                print(f"Доступна нова версія {latest_version}! Поточна версія: {Version}")
                return latest_version
            else:
                print("Ви використовуєте останню версію.")
                return None
        except requests.RequestException as e:
            print(f"Помилка перевірки оновлень: {e}")
            return None

    # Функція для збереження відвідування користувача застосунку
    def addUserVisits(self):
        print("Доброго дня користувач")
        # Запит до бд


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.mainWindow(main)
    sys.exit(app.exec_())