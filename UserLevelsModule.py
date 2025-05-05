from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QPushButton, QFrame, QVBoxLayout, \
    QStyle, QMessageBox, QRadioButton, QButtonGroup, QDialog, QScrollArea, QComboBox
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from functools import partial
import os
import time
import RebuildsComponents, LelelCounting

class UserLevelsModule:
    def __init__(self):
        self.numberGestures = 3
        self.Time = 0
        self.gestures = ["", "", ""]
        self.selectPositionGesture = ""
        self.frame_order_gesture = QFrame()

    # Вікно для створення користувацького рівня
    def createUserLevel(self):
        print("UserLevelsModule: def createUserLevel()")
        # Створюємо та показуємо модальне вікно
        modal = RebuildsComponents.ModalWindow(250, 100, 1315, 917)
        modal.setWindowTitle("Creation User Level")
        modal.setStyleSheet("""
                       QDialog {
                           background-color: #DAFFDF; /* Колір вікна */
                       }
                   """)

        # ------------------------------------------------------------------------------------------------------------------Заголовок меню вибору жестів

        title_gesture = QLabel(modal)
        title_gesture.setGeometry(30, 30, 300, 55)
        title_gesture.setText("Жести")

        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        title_gesture.setFont(font)

        title_gesture.setFrameShape(QLabel.StyledPanel)
        title_gesture.setFrameShadow(QLabel.Plain)
        title_gesture.setAlignment(Qt.AlignCenter)
        title_gesture.setStyleSheet("""
                    QLabel {
                        background-color: #9EFFA5; /* Колір фону */
                        color: black; /* Колір тексту */
                        border-radius: 10px; /* Закруглення кутів */
                    }
                """)

        # ------------------------------------------------------------------------------------------------------------------Меню вибору жестів

        frame_select_gesture = QScrollArea(modal)
        frame_select_gesture.setGeometry(30, 100, 300, 780)
        frame_select_gesture.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Відключення Горизонтальна прокрутка
        frame_select_gesture.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # Вертикальна прокруткa
        frame_select_gesture.setStyleSheet("""
                        QFrame {
                            background-color: #9EFFA5; /* Фон картки */
                            border-radius: 10px; /* Закруглені кути */
                        }
                    """)

        # Контейнер для вмісту
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)  # Горизонтальне розташування
        layout.setContentsMargins(10, 10, 10, 10)  # Відступи між елементами
        layout.setSpacing(30)  # Проміжки між картками

        images_cards = ["FingerImages/gesture_wait.jpg", "FingerImages/gesture_peace.jpg", "FingerImages/gesture_oke.jpg",
                        "FingerImages/gesture_little_bit.jpg", "FingerImages/gesture_jumbo.jpg", "FingerImages/gesture_fingers_crossed.jpg",
                        "FingerImages/gesture_butt.jpg", "FingerImages/both_gesture_uwu.jpg", "FingerImages/both_gesture_tutupapa.jpg",
                        "FingerImages/both_gesture_school.jpg", "FingerImages/both_gesture_request.jpg", "FingerImages/both_gesture_heart.jpg",
                        "FingerImages/both_gesture_doubleoke.jpg", "FingerImages/both_gesture_camera.jpg"]

        # Додавання "карток" у контейнер
        for i in range(14):  # 14 карток
            image_card = RebuildsComponents.ClickableLabel()
            image_card.setFixedSize(200, 200)
            pixmap = QPixmap(images_cards[i])
            image_card.setPixmap(pixmap)
            image_card.setScaledContents(True)
            image_card.setObjectName(f"image_label_{i}")  # Задання імені
            # Підключаємо сигнал кліку до обробника
            image_card.clicked.connect(partial(self.on_gesture_click, images_cards[i]))
            layout.addWidget(image_card)  # Додаємо картку у макет

        # Встановлення контейнера у QScrollArea
        content_widget.setLayout(layout)
        frame_select_gesture.setWidget(content_widget)
        frame_select_gesture.setWidgetResizable(True)  # Адаптація розміру контейнера до QScrollArea

        # ------------------------------------------------------------------------------------------------------------------Заголовок меню для відображення порядку жестів

        title_orderGesture = QLabel(modal)
        title_orderGesture.setGeometry(660, 30, 300, 55)
        title_orderGesture.setText("Порядок жестів")

        title_orderGesture.setFont(font)

        title_orderGesture.setFrameShape(QLabel.StyledPanel)
        title_orderGesture.setFrameShadow(QLabel.Plain)
        title_orderGesture.setAlignment(Qt.AlignCenter)
        title_orderGesture.setStyleSheet("""
                            QLabel {
                                background-color: #9EFFA5; /* Колір фону */
                                color: black; /* Колір тексту */
                                border-radius: 10px; /* Закруглення кутів */
                            }
                        """)

        # ------------------------------------------------------------------------------------------------------------------Фрейм порядку жестів

        self.frame_order_gesture = QFrame(modal)
        self.frame_order_gesture.setGeometry(360, 100, 920, 300)
        self.frame_order_gesture.setStyleSheet("""
                                QFrame {
                                    background-color: #9EFFA5; /* Фон картки */
                                    border-radius: 10px; /* Закруглені кути */
                                }
                            """)
        # Додавання "карток" у контейнер
        self.add_CardsOfGestures(3)

        # ------------------------------------------------------------------------------------------------------------------Фрейм для визначення кількості жестів

        frame_number_gestures = QFrame(modal)
        frame_number_gestures.setGeometry(400, 440, 350, 200)
        frame_number_gestures.setStyleSheet("""
                                        QFrame {
                                            background-color: #9EFFA5; /* Фон картки */
                                            border-radius: 10px; /* Закруглені кути */
                                        }
                                    """)

        title_FrameNumber = QLabel(frame_number_gestures)
        title_FrameNumber.setGeometry(20, 10, 300, 55)
        title_FrameNumber.setText("Кількість жестів")

        title_FrameNumber.setFont(font)

        title_FrameNumber.setFrameShape(QLabel.StyledPanel)
        title_FrameNumber.setFrameShadow(QLabel.Plain)
        title_FrameNumber.setAlignment(Qt.AlignCenter)
        title_FrameNumber.setStyleSheet("""
                                    QLabel {
                                        background-color: #9EFFA5; /* Колір фону */
                                        color: black; /* Колір тексту */
                                        border-radius: 10px; /* Закруглення кутів */
                                    }
                                """)

        # Додавання випадаючого списку
        combo_gestures = QComboBox(frame_number_gestures)
        combo_gestures.setGeometry(100, 90, 140, 40)
        combo_gestures.addItems(["3", "5", "7"])
        combo_gestures.setStyleSheet("""
            QComboBox {
                background-color: #DAFFDF;
                border: 1px solid #4CAF50;
                border-radius: 5px;
                padding: 5px;
                font-size: 20px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(FingerImages/down_arrow.png); /* Вкажіть шлях до іконки, якщо потрібно */
                width: 25px;
                height: 25px;
                margin-right: 10px; /* Зміщення стрілки лівіше */
                subcontrol-origin: padding;
                subcontrol-position: center right; /* Позиціонування стрілки */
            }
            QComboBox QAbstractItemView {
                background-color: #DAFFDF; /* Фон випадаючого меню */
                selection-background-color: #1d70f5; /* Фон виділеного елемента */
                selection-color: white; /* Колір тексту виділеного елемента */
                border: 1px solid #003087; /* Межа випадаючого меню */
            }
        """)

        combo_gestures.currentIndexChanged.connect(lambda: self.number_gestures_changed(combo_gestures.currentText()))

        # ------------------------------------------------------------------------------------------------------------------Фрейм для визначення ліміту часу

        frame_time_gestures = QFrame(modal)
        frame_time_gestures.setGeometry(880, 440, 350, 200)
        frame_time_gestures.setStyleSheet("""
                                                QFrame {
                                                    background-color: #9EFFA5; /* Фон картки */
                                                    border-radius: 10px; /* Закруглені кути */
                                                }
                                            """)

        title_FrameTime = QLabel(frame_time_gestures)
        title_FrameTime.setGeometry(20, 10, 300, 55)
        title_FrameTime.setText("Ліміт за часом, сек.")

        title_FrameTime.setFont(font)

        title_FrameTime.setFrameShape(QLabel.StyledPanel)
        title_FrameTime.setFrameShadow(QLabel.Plain)
        title_FrameTime.setAlignment(Qt.AlignCenter)
        title_FrameTime.setStyleSheet("""
                                            QLabel {
                                                background-color: #9EFFA5; /* Колір фону */
                                                color: black; /* Колір тексту */
                                                border-radius: 10px; /* Закруглення кутів */
                                            }
                                        """)

        # Додавання випадаючого списку
        combo_time = QComboBox(frame_time_gestures)
        combo_time.setGeometry(100, 90, 140, 40)
        combo_time.addItems(["0", "40", "65", "90"])
        combo_time.setStyleSheet("""
                    QComboBox {
                        background-color: #DAFFDF;
                        border: 1px solid #4CAF50;
                        border-radius: 5px;
                        padding: 5px;
                        font-size: 20px;
                    }
                    QComboBox::drop-down {
                        border: none;
                    }
                    QComboBox::down-arrow {
                        image: url(FingerImages/down_arrow.png); /* Вкажіть шлях до іконки, якщо потрібно */
                        width: 25px;
                        height: 25px;
                        margin-right: 10px; /* Зміщення стрілки лівіше */
                        subcontrol-origin: padding;
                        subcontrol-position: center right; /* Позиціонування стрілки */
                    }
                    QComboBox QAbstractItemView {
                        background-color: #DAFFDF; /* Фон випадаючого меню */
                        selection-background-color: #1d70f5; /* Фон виділеного елемента */
                        selection-color: white; /* Колір тексту виділеного елемента */
                        border: 1px solid #003087; /* Межа випадаючого меню */
                    }
                """)

        combo_time.currentIndexChanged.connect(lambda: self.limit_time_changed(combo_time.currentText()))

        # ------------------------------------------------------------------------------------------------------------------Фрейм для кнопок взаємодії з формою

        frame_control_buttons = QFrame(modal)
        frame_control_buttons.setGeometry(400, 680, 830, 200)
        frame_control_buttons.setStyleSheet("""
                                                        QFrame {
                                                            background-color: #9EFFA5; /* Фон картки */
                                                            border-radius: 10px; /* Закруглені кути */
                                                        }
                                                    """)

        cleaning_frame = QPushButton(frame_control_buttons)
        cleaning_frame.setGeometry(80, 60, 280, 80)
        cleaning_frame.setText("Початкова форма")
        cleaning_frame.setObjectName("cleaning_frame")
        cleaning_frame.setStyleSheet("""
                                QPushButton {
                                    background-color: #DAFFDF; /* Фон кнопки */
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
        cleaning_frame.clicked.connect(partial(self.clear_frame_click, modal))

        save_level_button = QPushButton(frame_control_buttons)
        save_level_button.setGeometry(460, 60, 280, 80)
        save_level_button.setText("Зберегти рівень")
        save_level_button.setObjectName("save_level_button")
        save_level_button.setStyleSheet("""
                        QPushButton {
                            background-color: #DAFFDF; /* Фон кнопки */
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
        save_level_button.clicked.connect(partial(self.save_UserLevel_click, modal))

        modal.exec_()  # Запускаємо модальне вікно (блокує основне)

    # Функція для наповнення фрейму "порядок жестів"
    def add_CardsOfGestures(self, number):
        for widget in self.frame_order_gesture.findChildren(QWidget):
            widget.deleteLater()
        N = 0
        for i in range(number):  # N карток
            image_card = RebuildsComponents.ClickableLabel(self.frame_order_gesture)
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
            image_card.setStyleSheet("""
                                    QLabel {
                                        background-color: #DAFFDF; /* Фон картки */
                                        border-radius: 10px; /* Закруглені кути */
                                    }
                                """)
            image_card.setObjectName(f"order_label_{i}")  # Задання імені
            # Підключаємо сигнал кліку до обробника
            image_card.clicked.connect(partial(self.order_gesture_click, image_card))
            image_card.show()

    # Функція-обробник зміни кількості жестів рівня
    def number_gestures_changed(self, selected_value):
        if self.selectPositionGesture != "":
            for label in self.frame_order_gesture.findChildren(QLabel):
                if label.objectName() == self.selectPositionGesture:
                    label.setStyleSheet("""
                                        QLabel {
                                             background-color: #DAFFDF; /* Фон картки */
                                             border-radius: 10px; /* Закруглені кути */
                                            }
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
        self.add_CardsOfGestures(self.numberGestures)

    # Функція-обробник зміни часу рівня
    def limit_time_changed(self, selected_value):
        self.Time = selected_value
        print(f"Встановлено ліміт часу: {self.Time}")

    # Функція-обробник для очищення форми
    def clear_frame_click(self, modal):
        print(f"Очищення форми:")
        modal.close()
        self.__init__()
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
        self.__init__()

    # Функція-обробник мітки для вибору жесту
    def on_gesture_click(self, image_path):
        # Зберігаємо шлях до обраного жесту
        print(f"Обраний жест: {image_path}")
        if self.selectPositionGesture != "":
            for label in self.frame_order_gesture.findChildren(QLabel):
                if label.objectName() == self.selectPositionGesture:
                    pixmap = QPixmap(image_path)
                    label.setPixmap(pixmap)
                    label.setScaledContents(True)
                    N = int(label.objectName()[12])
                    print(f"N = int(label.objectName()[12]) = {N}")
                    self.gestures[N] = image_path
                    break

    # Функція-обробник мітки для редагування жесту з фрейму "порядок жестів"
    def order_gesture_click(self, image_card):
        if image_card.objectName() == self.selectPositionGesture:
            image_card.setStyleSheet("""
                                QLabel {
                                    background-color: #DAFFDF; /* Фон картки */
                                    border-radius: 10px; /* Закруглені кути */
                                   }
                                """)
            self.selectPositionGesture = ""
        else:
            if self.selectPositionGesture != "":
                for label in self.frame_order_gesture.findChildren(QLabel):
                    if label.objectName() == self.selectPositionGesture:
                        label.setStyleSheet("""
                                        QLabel {
                                             background-color: #DAFFDF; /* Фон картки */
                                             border-radius: 10px; /* Закруглені кути */
                                            }
                                        """)
                        break
            image_card.setStyleSheet("""
                                QLabel {
                                     background-color: #DAFFDF; /* Фон картки */
                                     border-radius: 10px; /* Закруглені кути */
                                     border: 5px solid red;
                                    }
                                """)
            self.selectPositionGesture = image_card.objectName()
        print(f"Клік на: {self.selectPositionGesture}")

    # Функція зчитування даних з файлу
    def readDataFile(self):
        gestures = []
        time = 0
        numberGestures = 0

        # Додати обробник файлу

        return numberGestures, time, gestures

    # Вікно для запуску користувацького рівня
    def startUserLevel(self, level_cv_frame):
        print("UserLevelsModule: def startUserLevel()")
        level_cv_frame.show()

        # Додати список з усіма файлами директорії користувацьких рівнів (для того, щоб вибрати рівень)

        UserGestures = [
            'FingerImages/both_gesture_uwu.jpg',
            'FingerImages/both_gesture_school.jpg',
            'FingerImages/gesture_peace.jpg'
        ]
        levelCounting = LelelCounting.CreateLevel(3, 0, UserGestures)

        levelCounting.create_new_level_click("Користувацький рівень", "Користувацький рівень", level_cv_frame)
