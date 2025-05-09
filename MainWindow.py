import sys
import mediapipe as mp
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QPushButton, QScrollArea, QFrame, QHBoxLayout, \
    QGraphicsOpacityEffect, QMessageBox
from PyQt5.QtGui import QImage, QPixmap, QFont, QIcon, QTransform
from PyQt5.QtCore import QTimer, Qt, QSize
from functools import partial
import LelelCounting, SettingsModule, RebuildsComponents, UserLevelsModule

class MainWindow():
    def __init__(self):
        self.current_game_level = "Undefined123"
        self.widgetsColor = "#DAFFDF"
        self.widgetsLanguage = 0
        self.widgetsText = {
            "title_window": ['Потренуємо ваші нейрони', 'ToTrainYourNeurons'],
            "": ['', ''],
        }

        # Компоненти, що залежні від налаштувань додатку
        self.title_window = None
        self.level_checking = None
        self.select_Level = None
        self.button_help = None

    def setLanguage(self, Language):
        self.widgetsLanguage = Language
        print(f"class MainWindow(): def setLanguage(self, Language): {Language}")
        self.update_ui()

    def update_ui(self):
        if self.title_window:
            self.title_window.setText(self.widgetsText["title_window"][self.widgetsLanguage])

        self.fill_frame_level_checking()

    def mainWindow(self):
        app = QApplication(sys.argv)
        window = QMainWindow()

        window.setWindowTitle("ToTrainYourNeurons")
        window.setGeometry(250, 100, 1315, 917)

        window.setStyleSheet("""
                    QMainWindow {
                        background-color: #DAFFDF; /* Колір вікна */
                    }
                """)

        # ------------------------------------------------------------------------------------------------------------------Фрейм Налаштувань

        settings_frame = QFrame(window)
        # settings_frame.setGeometry(48, 23, 390, 840)
        settings_frame.setGeometry(0, 0, 438, 863)
        settings_frame.hide()
        settings_frame.setStyleSheet("""
                        QFrame {
                            background-color: #9EFFA5; /* Фон картки #9EFFA5; */
                            border-radius: 10px; /* Закруглені кути */
                        }
                    """)

        # ------------------------------------------------------------------------------------------------------------------Фрейм Прозорий

        unvisible_frame = RebuildsComponents.ClickableFrame(window)
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

        button_settings = QPushButton(window)
        button_settings.setGeometry(48, 23, 60, 60)
        # Завантажуємо іконку
        icon = QIcon("FingerImages/settings.png")
        button_settings.setIcon(icon)
        button_settings.setIconSize(QSize(50, 50))  # Налаштовуємо розмір іконки (50x50 пікселів)

        font = QFont()
        font.setBold(True)
        font.setPointSize(14)
        button_settings.setFont(font)

        button_settings.setStyleSheet("""
                QPushButton {
                    background-color: #9EFFA5; /* Колір кнопки */
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

        settingsModule = SettingsModule.SettingsModule(main)

        # Підключення сигналу "clicked" до обробника
        button_settings.clicked.connect(lambda: settingsModule.show_settings(settings_frame, unvisible_frame, window))

        # ------------------------------------------------------------------------------------------------------------------Назва програми

        self.title_window = QLabel(window)
        self.title_window.setGeometry(468, 23, 380, 55)
        self.title_window.setText(self.widgetsText["title_window"][self.widgetsLanguage])

        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        self.title_window.setFont(font)

        self.title_window.setFrameShape(QLabel.StyledPanel)
        self.title_window.setFrameShadow(QLabel.Plain)
        self.title_window.setAlignment(Qt.AlignCenter)
        self.title_window.setStyleSheet("""
                QLabel {
                    background-color: #9EFFA5; /* Колір фону */
                    color: black; /* Колір тексту */
                    border-radius: 10px; /* Закруглення кутів */
                }
            """)

        # ------------------------------------------------------------------------------------------------------------------Кнопка Довідки

        self.button_help = QPushButton(window)
        self.button_help.setGeometry(1206, 18, 60, 60)
        self.button_help.setText("?")

        font = QFont()
        font.setBold(True)
        font.setPointSize(18)
        self.button_help.setFont(font)

        self.button_help.setStyleSheet("""
                    QPushButton {
                        background-color: #9EFFA5; /* Колір кнопки */
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

        # ------------------------------------------------------------------------------------------------------------------Фрейм вибірки рівня

        self.select_Level = QFrame(window)
        self.select_Level.setGeometry(0, 0, 1315, 917)
        self.select_Level.hide()
        self.select_Level.setStyleSheet("""
                    QFrame {
                        background-color: #9EFFA5; /* Фон картки */
                        border-radius: 10px; /* Закруглені кути */
                    }
                """)

        # ------------------------------------------------------------------------------------------------------------------Фрейм з картками для вибору режиму тренування

        self.level_checking = QScrollArea(window)
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
        settings_frame.raise_()

        # ------------------------------------------------------------------------------------------------------------------Закриття програми
        window.show()
        sys.exit(app.exec_())

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
            button_start.setText("Спробувати")
            button_start.setStyleSheet("""
                                    QPushButton {
                                        background-color: #DAFFDF; /* Колір кнопки */
                                        color: black; /* Колір тексту */
                                        border-radius: 10px; /* Закруглення кутів */
                                        font-size: 17px;
                                        font-weight: bold;
                                    }
                                    QPushButton:hover {
                                        background-color: #5dade2; /* Колір кнопки при наведенні */
                                    }
                                    QPushButton:pressed {
                                        background-color: #1f618d; /* Колір кнопки при натисканні */
                                    }
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
        if card.objectName() == "В розробці":
            # Створюємо повідомлення
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("Повідомлення")
            msg_box.setText("Вибачте, але рівень ще в стадії розробки😅")
            # Відображаємо повідомлення
            msg_box.exec_()
            return False

        self.select_Level.show()
        self.title_window.setStyleSheet("""
                    QLabel {
                        background-color: #DAFFDF; /* Колір фону */
                        color: black; /* Колір тексту */
                        border-radius: 10px; /* Закруглення кутів */
                    }
                """)
        self.button_help.setStyleSheet("""
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
            partial(self.hide_select_level_click))

        # ------------------------------------------------------------------------------------------------------------------Фрейм для відображення рівнів

        levels = QFrame(self.select_Level)
        levels.setGeometry(490, 100, 770, 750)
        levels.show()
        levels.setStyleSheet("""
                        QFrame {
                            background-color: #DAFFDF; /* Фон картки */
                            border-radius: 10px; /* Закруглені кути */
                        }
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
        best_try_level.setText("Найкращий результат: ")
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
        number_try_level.setText("Кількість спроб: ")
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
        level_cv_frame.setStyleSheet("""
                        QFrame {
                            background-color: #9EFFA5; /* Фон картки */
                            border-radius: 10px; /* Закруглені кути */
                        }
                    """)

        # ------------------------------------------------------------------------------------------------------------------Кнопка для того, щоб розпочати тренування

        start_level_button = QPushButton(level_status)
        start_level_button.setGeometry(430, 80, 170, 80)
        start_level_button.setText("Почати")
        start_level_button.setObjectName("start_level_button")
        start_level_button.setStyleSheet("""
                    QPushButton {
                        background-color: #9EFFA5; /* Фон кнопки */
                        border-radius: 10px; /* Закруглені кути */
                        border: 3px solid black;
                        border-color: #9EFFA5;
                        font-size: 25px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        border-color: #5dade2; /* Колір кнопки при наведенні */
                    }
                    QPushButton:pressed {
                        border-color: #1f618d; /* Колір кнопки при натисканні */
                    }
                """)

        levelCounting = LelelCounting.CreateLevel()

        start_level_button.clicked.connect(lambda: levelCounting.create_new_level_click(
            self.current_game_level, card.objectName(), level_cv_frame))

        # ------------------------------------------------------------------------------------------------------------------

    # Функція-обробник кнопки для приховання компонентів фрейму вибірки рівня
    def hide_select_level_click(self):
        print("Кнопку натиснуто!")
        self.select_Level.hide()
        self.title_window.setStyleSheet("""
                    QLabel {
                        background-color: #9EFFA5; /* Колір фону */
                        color: black; /* Колір тексту */
                        border-radius: 10px; /* Закруглення кутів */
                    }
                """)
        self.button_help.setStyleSheet("""
                        QPushButton {
                            background-color: #9EFFA5; /* Колір кнопки */
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

    # Функція для створення картки виду вправ
    def create_card(self, title_text, description_text, image_path, parent=None):
        card = QFrame(parent)
        card.setObjectName(title_text)
        card.setFixedSize(378, 750)  # Фіксований розмір картки
        card.setStyleSheet("""
                    QFrame {
                        background-color: #9EFFA5; /* Фон картки */
                        border-radius: 10px; /* Закруглені кути */
                    }
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
        text_card.setStyleSheet("font-size: 17px; font-weight: bold; background-color: #DAFFDF;"
                                " /* Колір фону */ padding: 5px; /* Відступи всередині рамки */")

        # ------------------------------------------------------------------------------------------------------------------Фото картки
        image_label = QLabel(card)
        if not card.objectName() == "В розробці":
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
            button_level.setStyleSheet("""
                QPushButton {
                    background-color: #9EFFA5; /* Фон кнопки */
                    border-radius: 10px; /* Закруглені кути */
                    border: 3px solid black;
                    border-color: #9EFFA5;
                    font-size: 40px;
                    font-weight: bold;
                    padding-top: 20px;
                }
                QPushButton:hover {
                    border-color: #5dade2; /* Колір кнопки при наведенні */
                }
                QPushButton:pressed {
                    border-color: #1f618d; /* Колір кнопки при натисканні */
                }
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
            textForLevels.setText("Рівень " + str(num))
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
            current_button_level.setStyleSheet("""
                        QPushButton {
                            background-color: #9EFFA5; /* Фон кнопки */
                            border-radius: 10px; /* Закруглені кути */
                            border: 3px solid black;
                            border-color: #6085ff;
                            font-size: 40px;
                            font-weight: bold;
                            padding-top: 20px;
                        }
                        QPushButton:hover {
                            border-color: lime; /* Колір кнопки при наведенні */
                        }
                        QPushButton:pressed {
                            border-color: #1f618d; /* Колір кнопки при натисканні */
                        }
                    """)
            level_status.show()
            self.current_game_level = current_button_level.objectName()
        else:
            level_status.hide()
            current_button_level.setChecked(False)
            current_button_level.setStyleSheet("""
                        QPushButton {
                            background-color: #9EFFA5; /* Фон кнопки */
                            border-radius: 10px; /* Закруглені кути */
                            border: 3px solid black;
                            border-color: #9EFFA5;
                            font-size: 40px;
                            font-weight: bold;
                            padding-top: 20px;
                        }
                        QPushButton:hover {
                            border-color: #5dade2; /* Колір кнопки при наведенні */
                        }
                        QPushButton:pressed {
                            border-color: #1f618d; /* Колір кнопки при натисканні */
                        }
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
        level_cv_frame.setStyleSheet("""
                            QFrame {
                                background-color: #9EFFA5; /* Фон картки */
                                border-radius: 10px; /* Закруглені кути */
                            }
                        """)

        self.title_window.setStyleSheet("""
                        QLabel {
                            background-color: #DAFFDF; /* Колір фону */
                            color: black; /* Колір тексту */
                            border-radius: 10px; /* Закруглення кутів */
                        }
                    """)
        self.button_help.setStyleSheet("""
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
            partial(self.hide_select_level_click))

        # ------------------------------------------------------------------------------------------------------------------Фрейм для відображення кнопок

        scenario = QFrame(self.select_Level)
        scenario.setGeometry(490, 100, 770, 750)
        scenario.show()
        scenario.setStyleSheet("""
                            QFrame {
                                background-color: #DAFFDF; /* Фон картки */
                                border-radius: 10px; /* Закруглені кути */
                            }
                        """)

        # ------------------------------------------------------------------------------------------------------------------Фрейм розпочати користувацький рівень

        userLevel = UserLevelsModule.UserLevelsModule()
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

if __name__ == "__main__":
    main = MainWindow()
    main.mainWindow()