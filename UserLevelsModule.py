from PyQt5.QtWidgets import QGraphicsOpacityEffect, QLabel, QWidget, QPushButton, QFrame, QVBoxLayout, \
    QStyle, QMessageBox, QRadioButton, QButtonGroup, QDialog, QScrollArea, QComboBox
from PyQt5.QtGui import QImage, QPixmap, QMovie, QIcon, QTransform, QFont
from PyQt5.QtCore import QTimer, Qt, QSize
from functools import partial
import os
import time
import RebuildsComponents, LelelCounting

class UserLevelsModule:
    def __init__(self, widgetsLanguage, widgetsColor):
        self.numberGestures = 3
        self.Time = 0
        self.gestures = ["", "", ""]
        self.selectPositionGesture = ""
        self.frame_order_gesture = QFrame()
        self.HelpInformationType = False
        self.helpValue = 0
        self.widgetsColor = widgetsColor
        self.widgetsLanguage = widgetsLanguage
        self.widgetsText = {
            "title_FrameUserLevel": ['Виберіть рівень зі списку:', 'Select a level from the list:'],
            "title_gesture": ['Жести', 'Gestures'],
            "title_orderGesture": ['Порядок жестів', 'Order gestures'],
            "title_FrameNumber": ['Кількість жестів', 'Count of gestures'],
            "title_FrameTime": ['Ліміт за часом, сек.', 'Limit of time, sec.'],
            "cleaning_button": ['Початкова форма', 'The begining form'],
            "save_level_button": ['Зберегти рівень', 'Save level'],
            "helpButtonNextText": ['Далі', 'Next']
        }
        self.images_cards = ["FingerImages/gesture_wait.png", "FingerImages/gesture_peace.png",
                             "FingerImages/gesture_oke.png",
                             "FingerImages/gesture_little_bit.png", "FingerImages/gesture_jumbo.png",
                             "FingerImages/gesture_fingers_crossed.png",
                             "FingerImages/gesture_butt.png", "FingerImages/both_gesture_uwu.png",
                             "FingerImages/both_gesture_tutupapa.png",
                             "FingerImages/both_gesture_school.png", "FingerImages/both_gesture_request.png",
                             "FingerImages/both_gesture_heart.png",
                             "FingerImages/both_gesture_doubleoke.png", "FingerImages/both_gesture_camera.png"]
        self.connection = None
        self.frame_select_gesture = None
        self.arrow = None
        self.helpText = None
        self.helpButtonNextText = None
        self.frame_UserStatisticsHelp = None

    # Функція для встановлення типу довідки
    def setHelpInformationType(self, type):
        self.HelpInformationType = type

    # Функція для повернення типу довідки
    def getHelpInformationType(self):
        return self.HelpInformationType

    # Встановлення підключення до бд
    def set_connect_ToBD(self, con):
        self.connection = con
        print("Підлючення встановлено: LelelCounting")

    # Функція-обробник для створення користувацького рівня
    def createUserLevel(self):
        print("UserLevelsModule: def createUserLevel()")
        self.selectPositionGesture = ""
        # Створюємо та показуємо модальне вікно
        modal = RebuildsComponents.ModalWindow(250, 100, 1315, 917)
        modal.setWindowTitle("Creation User Level")
        modal.setStyleSheet(f"""
                       QDialog {{
                           background-color: {self.widgetsColor[1]}; /* Колір вікна */
                       }}
                   """)

        # ------------------------------------------------------------------------------------------------------------------Заголовок меню вибору жестів

        title_gesture = QLabel(modal)
        title_gesture.setGeometry(30, 30, 300, 55)
        title_gesture.setText(self.widgetsText["title_gesture"][self.widgetsLanguage])

        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        title_gesture.setFont(font)

        title_gesture.setFrameShape(QLabel.StyledPanel)
        title_gesture.setFrameShadow(QLabel.Plain)
        title_gesture.setAlignment(Qt.AlignCenter)
        title_gesture.setStyleSheet(f"""
                    QLabel {{
                        background-color: {self.widgetsColor[0]}; /* Колір фону */
                        color: black; /* Колір тексту */
                        border-radius: 10px; /* Закруглення кутів */
                    }}
                """)

        # ------------------------------------------------------------------------------------------------------------------Кнопка для повернення на головну сторінку

        button_return = QPushButton(modal)
        button_return.setGeometry(370, 23, 60, 60)

        # Завантажуємо зображення в QPixmap
        pixmap2 = QPixmap("FingerImages/right-arrow.png")  # Вкажіть шлях до вашого зображення

        # Обертаємо зображення
        transform = QTransform().rotate(180)
        rotated_pixmap = pixmap2.transformed(transform)

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
        button_return.clicked.connect(modal.close)

        # ------------------------------------------------------------------------------------------------------------------Кнопка довідки

        button_help = QPushButton(modal)
        button_help.setGeometry(1206, 18, 60, 60)
        button_help.setText("?")

        font2 = QFont()
        font2.setBold(True)
        font2.setPointSize(18)
        button_help.setFont(font2)

        button_help.setStyleSheet(f"""
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
        button_help.clicked.connect(self.NextHelpInfo)

        # ------------------------------------------------------------------------------------------------------------------Меню вибору жестів

        self.frame_select_gesture = QScrollArea(modal)
        self.frame_select_gesture.setGeometry(30, 100, 300, 780)
        self.frame_select_gesture.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Відключення Горизонтальна прокрутка
        self.frame_select_gesture.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # Вертикальна прокруткa
        self.frame_select_gesture.setStyleSheet(f"""
                        QFrame {{
                            background-color: {self.widgetsColor[0]}; /* Фон картки */
                            border-radius: 10px; /* Закруглені кути */
                        }}
                    """)

        # Контейнер для вмісту
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)  # Горизонтальне розташування
        layout.setContentsMargins(10, 10, 10, 10)  # Відступи між елементами
        layout.setSpacing(30)  # Проміжки між картками

        # Додавання "карток" у контейнер
        for i in range(self.images_cards.__len__()):  # 14 карток
            image_card = RebuildsComponents.ClickableLabel("", 0.9)
            image_card.setFixedSize(200, 200)
            pixmap = QPixmap(self.images_cards[i])
            image_card.setPixmap(pixmap)
            image_card.setScaledContents(True)
            image_card.setObjectName(f"image_label_{i}")  # Задання імені
            # Підключаємо сигнал кліку до обробника
            image_card.clicked.connect(partial(self.on_gesture_click, i, image_card))
            layout.addWidget(image_card)  # Додаємо картку у макет

        # Встановлення контейнера у QScrollArea
        content_widget.setLayout(layout)
        self.frame_select_gesture.setWidget(content_widget)
        self.frame_select_gesture.setWidgetResizable(True)  # Адаптація розміру контейнера до QScrollArea

        # ------------------------------------------------------------------------------------------------------------------Заголовок меню для відображення порядку жестів

        title_orderGesture = QLabel(modal)
        title_orderGesture.setGeometry(660, 30, 300, 55)
        title_orderGesture.setText(self.widgetsText["title_orderGesture"][self.widgetsLanguage])

        title_orderGesture.setFont(font)

        title_orderGesture.setFrameShape(QLabel.StyledPanel)
        title_orderGesture.setFrameShadow(QLabel.Plain)
        title_orderGesture.setAlignment(Qt.AlignCenter)
        title_orderGesture.setStyleSheet(f"""
                            QLabel {{
                                background-color: {self.widgetsColor[0]}; /* Колір фону */
                                color: black; /* Колір тексту */
                                border-radius: 10px; /* Закруглення кутів */
                            }}
                        """)

        # ------------------------------------------------------------------------------------------------------------------Фрейм порядку жестів

        self.frame_order_gesture = QFrame(modal)
        self.frame_order_gesture.setGeometry(360, 100, 920, 300)
        self.frame_order_gesture.setStyleSheet(f"""
                                QFrame {{
                                    background-color: {self.widgetsColor[0]}; /* Фон картки */
                                    border-radius: 10px; /* Закруглені кути */
                                }}
                            """)
        # Додавання "карток" у контейнер
        tmpCard = self.add_CardsOfGestures(3)
        self.order_gesture_click(tmpCard)
        # ------------------------------------------------------------------------------------------------------------------Фрейм для визначення кількості жестів

        frame_number_gestures = QFrame(modal)
        frame_number_gestures.setGeometry(400, 440, 350, 200)
        frame_number_gestures.setStyleSheet(f"""
                                        QFrame {{
                                            background-color: {self.widgetsColor[0]}; /* Фон картки */
                                            border-radius: 10px; /* Закруглені кути */
                                        }}
                                    """)

        title_FrameNumber = QLabel(frame_number_gestures)
        title_FrameNumber.setGeometry(20, 10, 300, 55)
        title_FrameNumber.setText(self.widgetsText["title_FrameNumber"][self.widgetsLanguage])

        title_FrameNumber.setFont(font)

        title_FrameNumber.setFrameShape(QLabel.StyledPanel)
        title_FrameNumber.setFrameShadow(QLabel.Plain)
        title_FrameNumber.setAlignment(Qt.AlignCenter)
        title_FrameNumber.setStyleSheet(f"""
                                    QLabel {{
                                        background-color: {self.widgetsColor[0]}; /* Колір фону */
                                        color: black; /* Колір тексту */
                                        border-radius: 10px; /* Закруглення кутів */
                                    }}
                                """)

        # Додавання випадаючого списку
        combo_gestures = QComboBox(frame_number_gestures)
        combo_gestures.setGeometry(100, 90, 140, 40)
        combo_gestures.addItems(["3", "5", "7"])
        combo_gestures.setStyleSheet(f"""
            QComboBox {{
                background-color: {self.widgetsColor[1]};
                border: 1px solid #4CAF50;
                border-radius: 5px;
                padding: 5px;
                font-size: 20px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: url(FingerImages/down_arrow.png); /* Вкажіть шлях до іконки, якщо потрібно */
                width: 25px;
                height: 25px;
                margin-right: 10px; /* Зміщення стрілки лівіше */
                subcontrol-origin: padding;
                subcontrol-position: center right; /* Позиціонування стрілки */
            }}
            QComboBox QAbstractItemView {{
                background-color: {self.widgetsColor[1]}; /* Фон випадаючого меню */
                selection-background-color: #1d70f5; /* Фон виділеного елемента */
                selection-color: white; /* Колір тексту виділеного елемента */
                border: 1px solid #003087; /* Межа випадаючого меню */
            }}
        """)

        combo_gestures.currentIndexChanged.connect(lambda: self.number_gestures_changed(combo_gestures.currentText()))

        # ------------------------------------------------------------------------------------------------------------------Фрейм для визначення ліміту часу

        frame_time_gestures = QFrame(modal)
        frame_time_gestures.setGeometry(880, 440, 350, 200)
        frame_time_gestures.setStyleSheet(f"""
                                                QFrame {{
                                                    background-color: {self.widgetsColor[0]}; /* Фон картки */
                                                    border-radius: 10px; /* Закруглені кути */
                                                }}
                                            """)

        title_FrameTime = QLabel(frame_time_gestures)
        title_FrameTime.setGeometry(20, 10, 300, 55)
        title_FrameTime.setText(self.widgetsText["title_FrameTime"][self.widgetsLanguage])

        title_FrameTime.setFont(font)

        title_FrameTime.setFrameShape(QLabel.StyledPanel)
        title_FrameTime.setFrameShadow(QLabel.Plain)
        title_FrameTime.setAlignment(Qt.AlignCenter)
        title_FrameTime.setStyleSheet(f"""
                                            QLabel {{
                                                background-color: {self.widgetsColor[0]}; /* Колір фону */
                                                color: black; /* Колір тексту */
                                                border-radius: 10px; /* Закруглення кутів */
                                            }}
                                        """)

        # Додавання випадаючого списку
        combo_time = QComboBox(frame_time_gestures)
        combo_time.setGeometry(100, 90, 140, 40)
        combo_time.addItems(["0", "40", "65", "90"])
        combo_time.setStyleSheet(f"""
                    QComboBox {{
                        background-color: {self.widgetsColor[1]};
                        border: 1px solid #4CAF50;
                        border-radius: 5px;
                        padding: 5px;
                        font-size: 20px;
                    }}
                    QComboBox::drop-down {{
                        border: none;
                    }}
                    QComboBox::down-arrow {{
                        image: url(FingerImages/down_arrow.png); /* Вкажіть шлях до іконки, якщо потрібно */
                        width: 25px;
                        height: 25px;
                        margin-right: 10px; /* Зміщення стрілки лівіше */
                        subcontrol-origin: padding;
                        subcontrol-position: center right; /* Позиціонування стрілки */
                    }}
                    QComboBox QAbstractItemView {{
                        background-color: {self.widgetsColor[1]}; /* Фон випадаючого меню */
                        selection-background-color: #1d70f5; /* Фон виділеного елемента */
                        selection-color: white; /* Колір тексту виділеного елемента */
                        border: 1px solid #003087; /* Межа випадаючого меню */
                    }}
                """)

        combo_time.currentIndexChanged.connect(lambda: self.limit_time_changed(combo_time.currentText()))

        # ------------------------------------------------------------------------------------------------------------------Фрейм для кнопок взаємодії з формою

        frame_control_buttons = QFrame(modal)
        frame_control_buttons.setGeometry(400, 680, 830, 200)
        frame_control_buttons.setStyleSheet(f"""
                                                        QFrame {{
                                                            background-color: {self.widgetsColor[0]}; /* Фон картки */
                                                            border-radius: 10px; /* Закруглені кути */
                                                        }}
                                                    """)

        cleaning_button = QPushButton(frame_control_buttons)
        cleaning_button.setGeometry(80, 60, 280, 80)
        cleaning_button.setText(self.widgetsText["cleaning_button"][self.widgetsLanguage])
        cleaning_button.setObjectName("cleaning_button")
        cleaning_button.setStyleSheet(f"""
                                QPushButton {{
                                    background-color: {self.widgetsColor[1]}; /* Фон кнопки */
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
        cleaning_button.clicked.connect(partial(self.clear_frame_click, modal))

        save_level_button = QPushButton(frame_control_buttons)
        save_level_button.setGeometry(460, 60, 280, 80)
        save_level_button.setText(self.widgetsText["save_level_button"][self.widgetsLanguage])
        save_level_button.setObjectName("save_level_button")
        save_level_button.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {self.widgetsColor[1]}; /* Фон кнопки */
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
        save_level_button.clicked.connect(partial(self.save_UserLevel_click, modal))

        # ------------------------------------------------------------------------------------------------------------------Компоненти для відображення довідки

        self.frame_UserStatisticsHelp = QFrame(modal)
        self.frame_UserStatisticsHelp.setGeometry(0, 0, 1315, 917)
        self.frame_UserStatisticsHelp.hide()
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.5)  # Прозорість
        self.frame_UserStatisticsHelp.setGraphicsEffect(opacity_effect)
        self.frame_UserStatisticsHelp.setStyleSheet(f"""
                                                    QFrame {{
                                                        background-color: #eac792; /* Фон картки */
                                                        border-radius: 10px; /* Закруглені кути */
                                                    }}
                                                """)

        # Стрілка
        self.arrow = QLabel(modal)
        self.arrow.setGeometry(400, 130, 100, 100)
        self.arrow.setScaledContents(True)
        self.arrow.setStyleSheet(f"""
                                            QLabel {{
                                                background-color: none; /* Колір фону */
                                            }}
                                        """)
        self.arrow.hide()

        # Інформація
        self.helpText = QLabel(modal)
        self.helpText.setWordWrap(True)
        self.helpText.setFrameShape(QLabel.StyledPanel)
        self.helpText.setFrameShadow(QLabel.Plain)
        self.helpText.setAlignment(Qt.AlignCenter)
        self.helpText.setStyleSheet(f"""
                                                    QLabel {{
                                                        background-color: none; /* Колір фону */
                                                        color: blue;
                                                        border: none;
                                                    }}
                                                """)
        self.helpText.hide()

        # Кнопка для переходу на наступну інформацію
        self.helpButtonNextText = QPushButton(modal)
        self.helpButtonNextText.setText(self.widgetsText["helpButtonNextText"][self.widgetsLanguage])
        self.helpButtonNextText.setStyleSheet(f"""
                                                        QPushButton {{
                                                            background-color: blue; /* Колір кнопки */
                                                            color: white; /* Колір тексту */
                                                            border-radius: 10px; /* Закруглення кутів */
                                                        }}
                                                        QPushButton:hover {{
                                                            background-color: #5dade2; /* Колір кнопки при наведенні */
                                                        }}
                                                        QPushButton:pressed {{
                                                            background-color: #1f618d; /* Колір кнопки при натисканні */
                                                        }}
                                                    """)
        self.helpButtonNextText.clicked.connect(self.NextHelpInfo)
        self.helpButtonNextText.hide()

        modal.exec_()  # Запускаємо модальне вікно (блокує основне)

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

    # Функція для наповнення фрейму "порядок жестів"
    def add_CardsOfGestures(self, number):
        for widget in self.frame_order_gesture.findChildren(QWidget):
            widget.deleteLater()
        N = 0
        tmpCard = None
        for i in range(number):  # N карток
            image_card = RebuildsComponents.ClickableLabel("", 0.7, self.frame_order_gesture)
            if number == 3:
                image_card.setGeometry(80 + N, 50, 200, 200)
                N += 70 + 200
            elif number == 5:
                image_card.setGeometry(30 + N, 70, 150, 150)
                N += 25 + 150
            elif number == 7:
                image_card.setGeometry(30 + N, 100, 100, 100)
                N += 25 + 100
            else:
                print("Error in function: def add_CardsOfGestures(self, frame_order_gesture, number)")
                return
            image_card.setStyleSheet(f"""
                                    QLabel {{
                                        background-color: {self.widgetsColor[1]}; /* Фон картки */
                                        border-radius: 10px; /* Закруглені кути */
                                    }}
                                """)
            image_card.setObjectName(f"order_label_{i}")  # Задання імені
            # Підключаємо сигнал кліку до обробника
            image_card.clicked.connect(partial(self.order_gesture_click, image_card))
            image_card.show()
            if i == 0:
                tmpCard = image_card
        return tmpCard

    # Функція-обробник зміни кількості жестів рівня
    def number_gestures_changed(self, selected_value):
        if self.selectPositionGesture != "":
            for label in self.frame_order_gesture.findChildren(QLabel):
                if label.objectName() == self.selectPositionGesture:
                    label.setStyleSheet(f"""
                                        QLabel {{
                                             background-color: {self.widgetsColor[1]}; /* Фон картки */
                                             border-radius: 10px; /* Закруглені кути */
                                            }}
                                        """)
                    self.selectPositionGesture = ""
                    break

        self.selectPositionGesture = ""
        self.numberGestures = int(selected_value)
        if self.numberGestures == 3:
            self.gestures = ["", "", ""]
        elif self.numberGestures == 5:
            self.gestures = ["", "", "", "", ""]
        elif self.numberGestures == 7:
            self.gestures = ["", "", "", "", "", "", ""]
        print(f"Вибрано кількість жестів: {self.numberGestures}")
        tmpCard = self.add_CardsOfGestures(self.numberGestures)
        self.order_gesture_click(tmpCard)
        for labelGesture in self.frame_select_gesture.findChildren(QLabel):
            labelGesture.show()

    # Функція-обробник зміни часу рівня
    def limit_time_changed(self, selected_value):
        self.Time = selected_value
        print(f"Встановлено ліміт часу: {self.Time}")

    # Функція-обробник для очищення форми
    def clear_frame_click(self, modal):
        print(f"Очищення форми:")
        modal.close()
        self.__init__(self.widgetsLanguage, self.widgetsColor)
        self.createUserLevel()

    # Функція-обробник для збереження користувацького рівня
    def save_UserLevel_click(self, modal):
        for gest in self.gestures:
            if gest == "":
                print("Присутнє не заповнене поле порядку жестів")
                # Створюємо повідомлення
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)  # Іконка: Information, Warning, Critical, Question
                msg_box.setWindowTitle("Повідомлення")
                msg_box.setText("Присутнє не заповнене поле порядку жестів!!!")
                msg_box.exec_()
                return

        print(f"Збереження рівня: {self.gestures}")
        print(f"Збереження рівня: {self.Time}")
        print(f"Збереження рівня: {self.numberGestures}")

        # Вказуємо директорію для збереження
        save_directory = "UserLevels/"

        # Створюємо директорію, якщо вона не існує
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # Створюємо унікальну назву файлу з поточним часом
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{save_directory}user_level_{timestamp}.txt"

        # Дані для запису
        data = [
            f"Gestures: {self.gestures}",
            f"Time: {self.Time}",
            f"Number of Gestures: {self.numberGestures}"
        ]

        # Запис у файл
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                for line in data:
                    file.write(line + '\n')
            print(f"Дані збережено у файл: {filename}")
        except Exception as e:
            print(f"Помилка при збереженні файлу: {e}")

        modal.close()
        self.__init__(self.widgetsLanguage, self.widgetsColor)

    # Функція-обробник мітки для вибору жесту
    def on_gesture_click(self, image_ID, image_card):
        # Зберігаємо шлях до обраного жесту
        print(f"Обраний жест: {self.images_cards[image_ID]}")
        prevGesture = ""
        if self.selectPositionGesture != "":
            for label in self.frame_order_gesture.findChildren(QLabel):
                if label.objectName() == self.selectPositionGesture:
                    pixmap = QPixmap(self.images_cards[image_ID])
                    label.setPixmap(pixmap)
                    label.setScaledContents(True)
                    N = int(label.objectName()[12])
                    # print(f"N = int(label.objectName()[12]) = {N}")
                    prevGesture = self.gestures[N]
                    self.gestures[N] = self.images_cards[image_ID]
                    image_card.hide()
                    break
            for i in range(self.gestures.__len__()):
                if self.gestures[i] == "":
                    for nextCard in self.frame_order_gesture.findChildren(QLabel):
                        if nextCard.objectName() == f"order_label_{i}":
                            self.order_gesture_click(nextCard)
                            break
                    break
        if prevGesture != "":
            ID = 0
            for i in range(self.images_cards.__len__()):
                if self.images_cards[i] == prevGesture:
                    ID = i
                    break
            for labelGesture in self.frame_select_gesture.findChildren(QLabel):
                if labelGesture.objectName() == f"image_label_{ID}":
                    labelGesture.show()
                    print("labelGesture.show()")
                    break

    # Функція-обробник мітки для редагування жесту з фрейму "порядок жестів"
    def order_gesture_click(self, image_card):
        print(f"image_card: {image_card.objectName()}")
        if image_card.objectName() == self.selectPositionGesture:
            image_card.setStyleSheet(f"""
                                QLabel {{
                                    background-color: {self.widgetsColor[1]}; /* Фон картки */
                                    border-radius: 10px; /* Закруглені кути */
                                   }}
                                """)
            self.selectPositionGesture = ""
        else:
            if self.selectPositionGesture != "":
                for label in self.frame_order_gesture.findChildren(QLabel):
                    if label.objectName() == self.selectPositionGesture:
                        label.setStyleSheet(f"""
                                        QLabel {{
                                             background-color: {self.widgetsColor[1]}; /* Фон картки */
                                             border-radius: 10px; /* Закруглені кути */
                                            }}
                                        """)
                        break
            image_card.setStyleSheet(f"""
                                QLabel {{
                                     background-color: {self.widgetsColor[1]}; /* Фон картки */
                                     border-radius: 10px; /* Закруглені кути */
                                     border: 5px solid red;
                                    }}
                                """)
            self.selectPositionGesture = image_card.objectName()
        print(f"Клік на: {self.selectPositionGesture}")

    def closeUserLevel(self, level_cv_frame):
        print("Close level_cv_frame")
        level_cv_frame.hide()
        self.setHelpInformationType(False)
        for widget in level_cv_frame.findChildren(QWidget):
            widget.deleteLater()

    # Функція зчитування даних з файлу
    def readDataFile(self, filename):
        gestures = []
        time = 0
        numberGestures = 0

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith("Gestures:"):
                        # Витягуємо список жестів із рядка, видаляючи квадратні дужки та розділяючи за комами
                        gestures_str = line.replace("Gestures: ", "").strip("[]")
                        gestures = [gesture.strip().strip("'") for gesture in gestures_str.split(", ")]
                    elif line.startswith("Time:"):
                        time = int(line.replace("Time: ", "").strip())
                    elif line.startswith("Number of Gestures:"):
                        numberGestures = int(line.replace("Number of Gestures: ", "").strip())
        except Exception as e:
            print(f"Помилка при зчитуванні файлу: {e}")

        return numberGestures, time, gestures

    # Функція-обробник вибору користувацького рівня з директорії UserLevels/...
    def openUserLevelPanel(self, level_cv_frame, NumberOfCamera):
        for widget in level_cv_frame.findChildren(QWidget):
            widget.deleteLater()
        level_cv_frame.show()
        # ------------------------------------------------------------------------------------------------------------------Фрейм для визначення рівня користувача

        frame_checkUserLevel = QFrame(level_cv_frame)
        frame_checkUserLevel.show()
        frame_checkUserLevel.setGeometry(400, 240, 500, 500)
        frame_checkUserLevel.setStyleSheet(f"""
                                                QFrame {{
                                                    background-color: {self.widgetsColor[1]}; /* Фон картки */
                                                    border-radius: 10px; /* Закруглені кути */
                                                }}
                                            """)

        title_FrameUserLevel = QLabel(frame_checkUserLevel)
        title_FrameUserLevel.show()
        title_FrameUserLevel.setGeometry(60, 170, 380, 55)
        title_FrameUserLevel.setText(self.widgetsText["title_FrameUserLevel"][self.widgetsLanguage])

        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        title_FrameUserLevel.setFont(font)

        title_FrameUserLevel.setFrameShape(QLabel.StyledPanel)
        title_FrameUserLevel.setFrameShadow(QLabel.Plain)
        title_FrameUserLevel.setAlignment(Qt.AlignCenter)
        title_FrameUserLevel.setStyleSheet(f"""
                                            QLabel {{
                                                background-color: {self.widgetsColor[1]}; /* Колір фону */
                                                color: black; /* Колір тексту */
                                                border-radius: 10px; /* Закруглення кутів */
                                            }}
                                        """)

        folderPath = "UserLevels/"
        myList = os.listdir(folderPath)
        print(f"def openUserLevelPanel:\n {myList}")
        # Створення відображення між зручними назвами та реальними іменами файлів
        display_names = [f"Рівень {i + 1}" for i in range(len(myList))]
        file_mapping = dict(zip(display_names, myList))  # Відображення: "Рівень X" -> ім'я файлу

        # Додавання випадаючого списку
        combo_UserLevel = QComboBox(frame_checkUserLevel)
        combo_UserLevel.show()
        combo_UserLevel.setGeometry(60, 250, 380, 40)
        combo_UserLevel.addItems(display_names)
        combo_UserLevel.setCurrentIndex(-1)  # Знімаємо вибір, щоб не було автоматично вибраного елемента
        combo_UserLevel.setStyleSheet(f"""
                            QComboBox {{
                                background-color: {self.widgetsColor[0]};
                                border: 1px solid {self.widgetsColor[1]};
                                border-radius: 5px;
                                padding: 5px;
                                font-size: 20px;
                            }}
                            QComboBox::drop-down {{
                                border: none;
                            }}
                            QComboBox::down-arrow {{
                                image: url(FingerImages/down_arrow.png); /* Вкажіть шлях до іконки, якщо потрібно */
                                width: 25px;
                                height: 25px;
                                margin-right: 10px; /* Зміщення стрілки лівіше */
                                subcontrol-origin: padding;
                                subcontrol-position: center right; /* Позиціонування стрілки */
                            }}
                            QComboBox QAbstractItemView {{
                                background-color: {self.widgetsColor[1]}; /* Фон випадаючого меню */
                                selection-background-color: #1d70f5; /* Фон виділеного елемента */
                                selection-color: white; /* Колір тексту виділеного елемента */
                                border: 1px solid {self.widgetsColor[1]}; /* Межа випадаючого меню */
                            }}
                        """)

        # Підключення сигналу з використанням реального імені файлу
        def on_combobox_changed():
            selected_display_name = combo_UserLevel.currentText()
            if selected_display_name:
                selected_file = file_mapping.get(selected_display_name, "")
                if selected_file:
                    self.startUserLevel(level_cv_frame, folderPath + selected_file, NumberOfCamera)

        combo_UserLevel.currentIndexChanged.connect(on_combobox_changed)

        # -------------------------------------------------------------------------------------------------------------Кнопка для повернення на сторінку Користувацький рівень
        button_return = QPushButton(level_cv_frame)
        button_return.setGeometry(48, 23, 60, 60)
        button_return.setText("X")
        button_return.show()

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
        button_return.clicked.connect(lambda: self.closeUserLevel(level_cv_frame))

    # Функція-обробник кнопки для демонстрації довідки
    def NextHelpInfo(self):
        ListText = {
            "helpText_1": ["Це вікно для створення користувацького рівня!",
                           "This is the window for creating a custom level!"],
            "helpText_2": ["Для того, щоб розпочати потрібно вибрати кількість жестів",
                           "To get started, you need to select the number of gestures"],
            "helpText_3": ["Встановити, якщо необхідно, ліміт за часом для рівня. Або залишити 0, якщо ліміт часу не потрібен",
                           "Set a time limit for the level, if necessary. Or leave it at 0 if no time limit is required"],
            "helpText_4": ["Це порядок жестів, вибравши необхідний елемент порядку, він набуде червоного виділення контуру",
                           "This is the order of gestures, by selecting the necessary element of the order, it will get a red outline selection"],
            "helpText_5": ["Тепер виберемо жест, зі списку жестів, клікнувши по ньому",
                "Now select a gesture from the list of gestures by clicking on it"],
            "helpText_6": ["Проведіть ці маніпуляції стільки разів, скільки встановлено кількість жестів",
                "Perform these manipulations as many times as you set the number of gestures"],
            "helpText_7": ["Та збережіть рівень за допомогою кнопки",
                "And save the level using the button"],
            "helpText_8": ["Для того, щоб очистити все вікно від вибраних жестів натисніть на кнопку",
                "To clear the entire window of selected gestures, click the button"]
        }
        if self.helpValue == 0:
            self.frame_UserStatisticsHelp.show()
            font1 = QFont()
            font1.setBold(True)
            font1.setPointSize(14)
            self.helpText.setGeometry(500, 300, 300, 200)
            self.helpText.setText(ListText["helpText_1"][self.widgetsLanguage])
            self.helpText.setFont(font1)
            self.helpText.show()
            font2 = QFont()
            font2.setBold(True)
            font2.setPointSize(12)
            self.helpButtonNextText.setGeometry(590, 450, 100, 50)
            self.helpButtonNextText.setFont(font2)
            self.helpButtonNextText.show()
        elif self.helpValue == 20:
            self.arrow.setGeometry(600, 470, 100, 100)
            pixmap = QPixmap("FingerImages/BlueArrow.png")
            # Обертаємо зображення
            transform = QTransform().rotate(200)
            rotated_pixmap = pixmap.transformed(transform)
            self.arrow.setPixmap(rotated_pixmap)
            self.arrow.show()
            self.helpText.setGeometry(670, 450, 300, 200)
            self.helpText.setText(ListText["helpText_2"][self.widgetsLanguage])
            self.helpButtonNextText.setGeometry(760, 600, 100, 50)
        elif self.helpValue == 40:
            self.arrow.setGeometry(910, 530, 100, 100)
            pixmap = QPixmap("FingerImages/BlueArrow.png")
            self.arrow.setPixmap(pixmap)
            self.helpText.setGeometry(630, 450, 300, 200)
            self.helpText.setText(ListText["helpText_3"][self.widgetsLanguage])
            self.helpButtonNextText.setGeometry(720, 650, 100, 50)
        elif self.helpValue == 60:
            self.arrow.setGeometry(600, 170, 100, 100)
            pixmap = QPixmap("FingerImages/BlueArrow.png")
            # Обертаємо зображення
            transform = QTransform().rotate(200)
            rotated_pixmap = pixmap.transformed(transform)
            self.arrow.setPixmap(rotated_pixmap)
            self.helpText.setGeometry(670, 130, 350, 200)
            self.helpText.setText(ListText["helpText_4"][self.widgetsLanguage])
            self.helpButtonNextText.setGeometry(790, 320, 100, 50)
        elif self.helpValue == 80:
            self.arrow.setGeometry(150, 170, 100, 100)
            self.helpText.setGeometry(240, 120, 350, 200)
            self.helpText.setText(ListText["helpText_5"][self.widgetsLanguage])
            self.helpButtonNextText.setGeometry(360, 280, 100, 50)
        elif self.helpValue == 100:
            self.arrow.hide()
            self.helpText.setGeometry(520, 320, 350, 200)
            self.helpText.setText(ListText["helpText_6"][self.widgetsLanguage])
            self.helpButtonNextText.setGeometry(640, 480, 100, 50)
            self.helpButtonNextText.show()
        elif self.helpValue == 120:
            pixmap = QPixmap("FingerImages/BlueArrow.png")
            self.arrow.setPixmap(pixmap)
            self.arrow.show()
            self.arrow.setGeometry(830, 750, 100, 100)
            self.helpText.setGeometry(670, 600, 300, 200)
            self.helpText.setText(ListText["helpText_7"][self.widgetsLanguage])
            self.helpButtonNextText.setGeometry(760, 750, 100, 50)
        elif self.helpValue == 140:
            self.arrow.setGeometry(600, 700, 100, 100)
            pixmap = QPixmap("FingerImages/BlueArrow.png")
            # Обертаємо зображення
            transform = QTransform().rotate(200)
            rotated_pixmap = pixmap.transformed(transform)
            self.arrow.setPixmap(rotated_pixmap)
            self.helpText.setGeometry(680, 600, 350, 200)
            self.helpText.setText(ListText["helpText_8"][self.widgetsLanguage])
            self.helpButtonNextText.setGeometry(780, 760, 100, 50)
        else:
            self.frame_UserStatisticsHelp.hide()
            self.arrow.hide()
            self.helpButtonNextText.hide()
            self.helpText.hide()
            self.helpValue = -20
        self.helpValue += 20

    # Функція-обробник зчитування даних з вибраного файлу та запуску рівня
    def startUserLevel(self, level_cv_frame, filename, NumberOfCamera):
        print("UserLevelsModule: def startUserLevel()")
        print(f'filename: {filename}')

        numberGestures, time, UserGestures = self.readDataFile(filename)

        print(f'self.readDataFile(filename):\n {numberGestures, time, UserGestures}')

        levelCounting = LelelCounting.CreateLevel(numberGestures, time, UserGestures)
        levelCounting.setLanguage(self.widgetsLanguage)
        levelCounting.setColor(self.widgetsColor)
        levelCounting.set_connect_ToBD(self.connection)

        levelCounting.create_new_level_click("Користувацький рівень", "User level", level_cv_frame, NumberOfCamera)
