import sys, cv2, webbrowser, sqlite3
from sqlite3 import Error
from datetime import datetime
import mediapipe as mp
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QPushButton, QScrollArea, QFrame, QHBoxLayout, \
    QGraphicsOpacityEffect, QMessageBox, QProgressBar
from PyQt5.QtGui import QImage, QPixmap, QFont, QIcon, QTransform, QMovie
from PyQt5.QtCore import QTimer, Qt, QSize
from functools import partial
import LelelCounting, SettingsModule, RebuildsComponents, UserLevelsModule, Music
import requests
from packaging import version

class MainWindow():
    def __init__(self):
        self.current_game_level = "Undefined123"
        self.NumberOfCamera = 0
        self.widgetsColor = ["#9EFFA5", "#DAFFDF"]
        self.widgetsLanguage = 0
        self.widgetsText = {
            "title_window": ['Потренуємо ваші нейрони', 'ToTrainYourNeurons'],
            "About_program": ['Тренування нейропсихологічних вправ', 'Neuropsychological exercise training'],
            "About_programmmer": ['Розробник: Саприкін Антон Владиславович', 'Developer: Anton Saprykin'],
            "button_start": ['Спробувати', 'Try it'],
            "msg_box": [ ['Повідомлення', 'Вибачте, але рівень ще в стадії розробки😅'], ['Message', 'Sorry, but the level is still under development😅']],
            "msg_box2": [ ['Перевірка оновлень', 'Check for updates'], ['Чи бажаєте встановити оновлення?', 'Would you like to install an update?'],
                          ['Так', 'Yes'], ['Ні', 'No']],
            "msg_box3": [ ['Помилка', 'Error'], ['Камера не знайдена!!!\nПеревірте справність основної камери пристрою: ',
                         'Camera not found!!!\nCheck the main camera of the device for proper operation: ']],
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
        self.best_try_level_num = None
        self.number_try_level_num = None

        # Оголошення зв'язків з модулями застосунку
        self.connection = None
        self.levelCounting = LelelCounting.CreateLevel()
        self.MainWindowLink = None
        self.settingsModule = None
        self.Music = Music.Music()

    # Функція для ініціалізації зв'язків між модулями та показу фрейму "Зававантаження"
    def setMainWindowLink(self, MainWindowLink):
        self.MainWindowLink = MainWindowLink
        self.settingsModule = SettingsModule.SettingsModule(self.MainWindowLink, self.levelCounting, self.Music)
        self.settingsModule.uploadSettings()
        # --------------------------------------------------------------------------------------------------------------Фрейм "Зававантаження"
        loadingFrame = QFrame(self.window)
        loadingFrame.setGeometry(0, 0, 1315, 917)
        loadingFrame.show()
        loadingFrame.setStyleSheet(f"""
                            QFrame {{
                                background-color: {self.widgetsColor[0]}; /* Фон картки */
                                border-radius: 10px; /* Закруглені кути */
                            }}
                        """)

        title_program = QLabel(loadingFrame)
        title_program.setGeometry(310, 300, 700, 75)
        title_program.setText(self.widgetsText["title_window"][self.widgetsLanguage])

        font = QFont()
        font.setBold(True)
        font.setPointSize(27)
        title_program.setFont(font)

        title_program.setFrameShape(QLabel.StyledPanel)
        title_program.setFrameShadow(QLabel.Plain)
        title_program.setAlignment(Qt.AlignCenter)
        title_program.show()
        title_program.setStyleSheet(f"""
                        QLabel {{
                            background-color: {self.widgetsColor[1]}; /* Колір фону */
                            color: black; /* Колір тексту */
                            border-radius: 10px; /* Закруглення кутів */
                        }}
                    """)
        # ------------------------------------------------------------------------------
        About_program = QLabel(loadingFrame)
        About_program.setGeometry(390, 400, 530, 45)
        About_program.setText(self.widgetsText["About_program"][self.widgetsLanguage])

        font = QFont()
        font.setBold(True)
        font.setPointSize(14)
        About_program.setFont(font)

        About_program.setFrameShape(QLabel.StyledPanel)
        About_program.setFrameShadow(QLabel.Plain)
        About_program.setAlignment(Qt.AlignCenter)
        About_program.show()
        About_program.setStyleSheet(f"""
                                QLabel {{
                                    background-color: {self.widgetsColor[1]}; /* Колір фону */
                                    color: black; /* Колір тексту */
                                    border-radius: 10px; /* Закруглення кутів */
                                }}
                            """)
        # ------------------------------------------------------------------------------
        progress_bar = QProgressBar(loadingFrame)
        progress_bar.setGeometry(200, 570, 900, 55)
        progress_bar.setMinimum(0)
        progress_bar.setMaximum(100)
        progress_bar.setValue(0)
        # progress_bar.setFormat("%v/%m")  # Показує поточне значення / максимум (наприклад, 7/10)
        progress_bar.setAlignment(Qt.AlignCenter)  # Вирівнювання тексту по центру
        progress_bar.setStyleSheet("""
                        QProgressBar {
                            border: none;
                            border-radius: 15px;
                            background-color: #FFFFFF;  /* Колір фону */
                        }
                        QProgressBar::chunk {
                            background-color: #DFFF4F;  /* Колір заповнення */
                            border-radius: 15px;
                        }
                    """)
        progress_bar.show()

        # ------------------------------------------------------------------------------
        About_programmmer = QLabel(loadingFrame)
        About_programmmer.setGeometry(480, 860, 350, 40)
        About_programmmer.setText(self.widgetsText["About_programmmer"][self.widgetsLanguage])

        font = QFont()
        font.setBold(True)
        font.setPointSize(8)
        About_programmmer.setFont(font)

        About_programmmer.setFrameShape(QLabel.StyledPanel)
        About_programmmer.setFrameShadow(QLabel.Plain)
        About_programmmer.setAlignment(Qt.AlignCenter)
        About_programmmer.show()
        About_programmmer.setStyleSheet(f"""
                                        QLabel {{
                                            background-color: {self.widgetsColor[1]}; /* Колір фону */
                                            color: black; /* Колір тексту */
                                            border-radius: 10px; /* Закруглення кутів */
                                        }}
                                    """)

        # --------------------------------------------------------------------------------------------------------------
        # Анімація прогрес-бару
        def update_progress():
            current_value = progress_bar.value()
            if current_value < 100:
                if current_value == 0:
                    if self.is_camera_available() == False:
                        # Створюємо повідомлення
                        msg_box = QMessageBox()
                        msg_box.setIcon(QMessageBox.Critical)
                        msg_box.setWindowTitle(self.widgetsText["msg_box3"][0][self.widgetsLanguage])
                        msg_box.setText(self.widgetsText["msg_box3"][1][self.widgetsLanguage])
                        # Відображаємо повідомлення
                        msg_box.exec_()
                        QApplication.quit()
                elif current_value == 20:
                    Version, latest_version = self.check_for_updates()
                    if Version != None and latest_version != None:
                        self.show_messagebox_yesNo(Version, latest_version)
                elif current_value == 40:
                    self.levelCounting.LevelStatistics = self.levelCounting.load_level_statistics()
                elif current_value == 60:
                    self.connect_toBD('database\\statistics.db')
                    self.levelCounting.set_connect_ToBD(self.connection)
                    self.settingsModule.set_connect_ToBD(self.connection)
                    self.window.set_connect_ToBD(self.connection)
                    self.print_all_tables()
                elif current_value == 80:
                    self.addUserVisits()
                progress_bar.setValue(current_value + 20)
                QTimer.singleShot(1500, update_progress)
            else:
                loadingFrame.hide()

        # Запускаємо оновлення прогрес-бару через 1.5 секунди
        QTimer.singleShot(1500, update_progress)

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
    def mainWindow(self):
        # Головне вікно застосунку
        self.window = RebuildsComponents.MainWindow(self.Music, self.levelCounting)

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

        self.window.show()

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

        self.show_levels_buttons(levels, 40, 1, level_status, card.objectName())
        self.show_levels_buttons(levels, 260, 4, level_status, card.objectName())

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

        self.best_try_level_num = QLabel(level_status)
        self.best_try_level_num.setGeometry(300, 50, 50, 50)
        self.best_try_level_num.setText("0 🖐️")
        self.best_try_level_num.setStyleSheet("""
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

        self.number_try_level_num = QLabel(level_status)
        self.number_try_level_num.setGeometry(300, 130, 50, 50)
        self.number_try_level_num.setText("0")
        self.number_try_level_num.setStyleSheet("""
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
            self.current_game_level, card.objectName(), level_cv_frame, self.NumberOfCamera))

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
    def show_levels_buttons(self, levels, stepY, num, level_status, cardName):
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
            button_level.clicked.connect(partial(self.select_level_click, button_level, level_status, cardName))

            textForLevels = QLabel(button_level)
            textForLevels.setGeometry(68, 3, 200, 50)
            textForLevels.setText(self.widgetsText["textForLevels"][self.widgetsLanguage] + str(num))
            textForLevels.setStyleSheet("background-color: none; font-size: 15px; font-weight: bold;")
            textForLevels.show()
            num += 1

    # Функція-обробник кнопки для відображення інфо проходження рівня (див. show_levels_buttons() )
    def select_level_click(self, current_button_level, level_status, cardName):
        # Прибирання виділення всіх інших кнопок
        parent_frame = current_button_level.parent()  # Отримати батьківський фрейм
        for child in parent_frame.findChildren(QPushButton):
            if child != current_button_level and child.objectName() != "start_level_button":
                child.setStyleSheet(f"""
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
                child.setChecked(False)

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
            print(f"def select_level_click(): {cardName}")
            if cardName == "Жести однією рукою" or cardName == "Gestures with one hand":
                self.best_try_level_num.setText(
                    f"{self.levelCounting.LevelStatistics["Жести однією рукою"][self.current_game_level][0]} 🖐️")
                self.number_try_level_num.setText(
                    f"{self.levelCounting.LevelStatistics["Жести однією рукою"][self.current_game_level][1]}")
            elif cardName == "Жести двума руками" or cardName == "Gestures with two hand":
                self.best_try_level_num.setText(
                    f"{self.levelCounting.LevelStatistics["Жести двума руками"][self.current_game_level][0]} 🖐️")
                self.number_try_level_num.setText(
                    f"{self.levelCounting.LevelStatistics["Жести двума руками"][self.current_game_level][1]}")
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

        scenario = QLabel(self.select_Level)
        scenario.setGeometry(490, 100, 770, 750)
        pixmap2 = QPixmap("FingerImages/foreground-image.jpg")
        scenario.setPixmap(pixmap2)
        scenario.setScaledContents(True)
        scenario.show()
        # background-color: {self.widgetsColor[1]}; /* Фон картки */
        scenario.setStyleSheet(f"""
                            QFrame {{
                                
                                border-radius: 10px; /* Закруглені кути */
                            }}
                        """)

        # ------------------------------------------------------------------------------------------------------------------Фрейм розпочати користувацький рівень

        userLevel = UserLevelsModule.UserLevelsModule(self.widgetsLanguage, self.widgetsColor)
        userLevel.set_connect_ToBD(self.connection)
        startUserLevel_frame = RebuildsComponents.ClickableLabel("", 0.4, scenario)
        startUserLevel_frame.setGeometry(20, 20, 355, 710)

        pixmap2 = QPixmap("FingerImages/play-level.png")
        startUserLevel_frame.setPixmap(pixmap2)
        startUserLevel_frame.setScaledContents(True)
        startUserLevel_frame.show()
        startUserLevel_frame.setStyleSheet(f"""
                                QLabel {{
                                    background-color: {self.widgetsColor[0]}; /* Фон картки */
                                    border-radius: 10px; /* Закруглені кути */
                                }}
                            """)
        # opacity_effect = QGraphicsOpacityEffect()
        # opacity_effect.setOpacity(0.4)
        # startUserLevel_frame.setGraphicsEffect(opacity_effect)
        startUserLevel_frame.clicked.connect(lambda: userLevel.openUserLevelPanel(level_cv_frame, self.NumberOfCamera))

        # ------------------------------------------------------------------------------------------------------------------Фрейм створення користувацього рівня

        createUserLevel_frame = RebuildsComponents.ClickableLabel("",0.4, scenario)
        createUserLevel_frame.setGeometry(395, 20, 355, 710)

        pixmap3 = QPixmap("FingerImages/create-level.png")
        createUserLevel_frame.setPixmap(pixmap3)
        createUserLevel_frame.setScaledContents(True)
        createUserLevel_frame.show()
        createUserLevel_frame.setStyleSheet(f"""
                                QLabel {{
                                    background-color: {self.widgetsColor[1]}; /* Фон картки */
                                    border-radius: 10px; /* Закруглені кути */
                                }}
                            """)
        # opacity_effect2 = QGraphicsOpacityEffect()
        # opacity_effect2.setOpacity(0.4)
        # createUserLevel_frame.setGraphicsEffect(opacity_effect2)
        createUserLevel_frame.clicked.connect(lambda: userLevel.createUserLevel())

        level_cv_frame.raise_()

    # Функція для перевірки версії застосунку
    def check_for_updates(self):
        Version = "1.0.2"
        try:
            response = requests.get(f"https://api.github.com/repos/Whowrite/Dyplome_gesture/releases/latest")
            response.raise_for_status()
            latest_version = response.json()["tag_name"].lstrip("v")  # Припускаємо, що тег виглядає як "v1.0.0"

            if version.parse(latest_version) > version.parse(Version):
                print(f"Доступна нова версія {latest_version}! Поточна версія: {Version}")
                return Version, latest_version
            else:
                print("Ви використовуєте останню версію.")
                return None, None
        except requests.RequestException as e:
            print(f"Помилка перевірки оновлень: {e}")
            return None, None

    # Перевіряє, чи є доступна камера на пристрої.
    def is_camera_available(self):
        """
        Returns:
            bool: True, якщо камера доступна, False - якщо ні.
        """
        try:
            # Спроба відкрити камери з індексом 0 - 2
            for N in range(3):
                cap = cv2.VideoCapture(N)
                if cap is None or not cap.isOpened():
                    print("Камера не знайдена або недоступна")
                    continue
                    # return False
                print("Камера знайдена")
                cap.release()  # Звільняємо камеру
                self.NumberOfCamera = N
                return True
        except Exception as e:
            print(f"Помилка при перевірці камери: {e}")
            return False

    def show_messagebox_yesNo(self, Version, latest_version):
        update_url = "https://github.com/Whowrite/Dyplome_gesture"
        # Створюємо повідомлення
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)  # Іконка: Information, Warning, Critical, Question
        msg_box.setWindowTitle(self.widgetsText["msg_box2"][0][self.widgetsLanguage])
        if self.widgetsLanguage == 0:
            msg_box.setText(f"Доступна нова версія {latest_version}! Поточна версія: {Version}")
        elif self.widgetsLanguage == 1:
            msg_box.setText(f"A new version is available {latest_version}! Current version: {Version}")
        msg_box.setInformativeText(self.widgetsText["msg_box2"][1][self.widgetsLanguage])
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        btn_yes = msg_box.button(QMessageBox.Yes)
        btn_no = msg_box.button(QMessageBox.No)
        btn_yes.setText(self.widgetsText["msg_box2"][2][self.widgetsLanguage])
        btn_no.setText(self.widgetsText["msg_box2"][3][self.widgetsLanguage])
        # Відображаємо повідомлення та отримуємо результат
        msg_box.exec_()
        # Обробка дій користувача
        clicked_button = msg_box.clickedButton()
        if clicked_button == btn_yes:
            print("Натиснуто Так")
            try:
                webbrowser.open(update_url)
                print(f"Відкрито сторінку: {update_url}")
                QApplication.quit()
            except Exception as e:
                print(f"Помилка при відкритті браузера: {e}")
        elif clicked_button == btn_no:
            print("Натиснуто Ні")

    # Функція для встановлення зв'язку з бд
    def connect_toBD(self, db_file):
        """
        Встановлює з'єднання з базою даних SQLite, створює таблиці, якщо вони не існують,
        і додає початкові записи до таблиць GameModes, Gestures, Sessions, SessionGameModes
        і SessionGestures, перевіряючи, чи записи ще не існують.

        Args:
            db_file (str): Шлях до файлу бази даних SQLite.
        """
        print("Перевірка з'єднання з бд")
        try:
            # Підключення до бази даних
            self.connection = sqlite3.connect(db_file)
            print(f"Успішно підключено до бази даних: {db_file}")

            cursor = self.connection.cursor()

            # Створення таблиці Sessions
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Sessions (
                    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login_date DATE NOT NULL,
                    session_length INTEGER NOT NULL
                )
            ''')

            # Створення таблиці GameModes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS GameModes (
                    mode_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mode_name VARCHAR(255) NOT NULL
                )
            ''')

            # Оновлена таблиця SessionGameModes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS SessionGameModes (
                    mode_id INTEGER PRIMARY KEY,
                    session_id INTEGER NOT NULL,
                    usage_count INTEGER NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES Sessions(session_id) ON DELETE CASCADE,
                    FOREIGN KEY (mode_id) REFERENCES GameModes(mode_id) ON DELETE CASCADE
                )
            ''')

            # Створення таблиці Gestures
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Gestures (
                    gesture_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    gesture_name VARCHAR(255) NOT NULL
                )
            ''')

            # Створення таблиці SessionGestures
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS SessionGestures (
                    session_id INTEGER NOT NULL,
                    gesture_id INTEGER PRIMARY KEY,
                    correct_answers INTEGER NOT NULL,
                    total_answers INTEGER NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES Sessions(session_id) ON DELETE CASCADE,
                    FOREIGN KEY (gesture_id) REFERENCES Gestures(gesture_id) ON DELETE CASCADE
                )
            ''')

            # Додавання початкових записів до таблиці GameModes
            game_modes = ["Gestures with one hand", "Gestures with two hand", "User level"]
            for mode_name in game_modes:
                cursor.execute('''
                    INSERT INTO GameModes (mode_name)
                    SELECT ? WHERE NOT EXISTS (SELECT 1 FROM GameModes WHERE mode_name = ?)
                ''', (mode_name, mode_name))

            # Додавання початкових записів до таблиці Gestures
            gestures = [
                "gesture_oke", "gesture_peace", "gesture_wait", "gesture_butt",
                "gesture_jumbo", "gesture_fingers_crossed", "gesture_little_bit", "both_gesture_heart",
                "both_gesture_uwu", "both_gesture_camera", "both_gesture_tutupapa",
                "both_gesture_request", "both_gesture_doubleoke", "both_gesture_school"
            ]
            for gesture_name in gestures:
                cursor.execute('''
                    INSERT INTO Gestures (gesture_name)
                    SELECT ? WHERE NOT EXISTS (SELECT 1 FROM Gestures WHERE gesture_name = ?)
                ''', (gesture_name, gesture_name))

            # Створення першої сесії
            current_date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("SELECT session_id FROM Sessions WHERE login_date = ?", (current_date,))
            session = cursor.fetchone()
            if not session:
                cursor.execute("INSERT INTO Sessions (login_date, session_length) VALUES (?, ?)", (current_date, 0))
                cursor.execute("SELECT session_id FROM Sessions WHERE login_date = ?", (current_date,))
                session = cursor.fetchone()
            session_id = session[0]

            # Перевірка, чи таблиця SessionGameModes порожня
            cursor.execute("SELECT COUNT(*) FROM SessionGameModes")
            session_game_modes_count = cursor.fetchone()[0]
            if session_game_modes_count == 0:
                # Додавання початкових записів до таблиці SessionGameModes
                cursor.execute("SELECT mode_id FROM GameModes")
                mode_ids = cursor.fetchall()
                for mode_id in mode_ids:
                    cursor.execute('''
                        INSERT INTO SessionGameModes (session_id, mode_id, usage_count)
                        SELECT ?, ?, 0
                        WHERE NOT EXISTS (
                            SELECT 1 FROM SessionGameModes WHERE session_id = ? AND mode_id = ?
                        )
                    ''', (session_id, mode_id[0], session_id, mode_id[0]))

            # Перевірка, чи таблиця SessionGestures порожня
            cursor.execute("SELECT COUNT(*) FROM SessionGestures")
            session_gestures_count = cursor.fetchone()[0]
            if session_gestures_count == 0:
                # Додавання початкових записів до таблиці SessionGestures
                for gesture_id in range(1, 15):
                    cursor.execute('''
                        INSERT INTO SessionGestures (session_id, gesture_id, correct_answers, total_answers)
                        SELECT ?, ?, 0, 0
                        WHERE NOT EXISTS (
                            SELECT 1 FROM SessionGestures WHERE gesture_id = ?
                        )
                    ''', (session_id, gesture_id, gesture_id))

            # Збереження змін
            self.connection.commit()
            print("Таблиці успішно створено або вже існують. Початкові записи додано або вже існують.")

        except Error as e:
            print(f"Помилка при створенні бази даних: {e}")
            if self.connection:
                self.connection.close()
            self.connection = None

    # Функція для виводу всіх даних з таблиць бд
    def print_all_tables(self):
        try:
            # Створення курсора
            cursor = self.connection.cursor()

            # Отримання списку всіх таблиць у базі даних
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            if not tables:
                print("База даних не містить таблиць.")
                return

            # Перебір кожної таблиці
            for table in tables:
                table_name = table[0]
                print(f"\n=== Таблиця: {table_name} ===")

                # Отримання структури таблиці (назви стовпців)
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]
                print("Стовпці:", ", ".join(column_names))

                # Отримання всіх даних із таблиці
                cursor.execute(f"SELECT * FROM {table_name};")
                rows = cursor.fetchall()

                if not rows:
                    print("Дані відсутні.")
                else:
                    print("Дані:")
                    for row in rows:
                        # Форматування виводу для зрозумілості
                        formatted_row = [str(item) for item in row]
                        print(f"  {formatted_row}")

            # Не закриваємо з'єднання, оскільки воно передане через self.connection

        except Exception as e:
            print(f"Помилка при виведенні таблиць: {e}")

    # Функція для збереження відвідування користувача застосунку
    def addUserVisits(self):
        print("Доброго дня користувач")
        try:
            # Створення курсора
            cursor = self.connection.cursor()

            # Отримання поточної дати у форматі 'YYYY-MM-DD'
            current_date = datetime.now().strftime('%Y-%m-%d')

            # Якщо сесії немає, додаємо нову з session_length=0
            cursor.execute(
                "INSERT INTO Sessions (login_date, session_length) VALUES (?, ?)",
                (current_date, 0)
            )
            self.connection.commit()
            print(f"Нову сесію за {current_date} додано успішно.")

        except Exception as e:
            print(f"Помилка при збереженні відвідування: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.mainWindow()
    main.setMainWindowLink(main)
    sys.exit(app.exec_())