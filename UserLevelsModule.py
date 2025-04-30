from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QPushButton, QFrame, QVBoxLayout, \
    QStyle, QMessageBox, QRadioButton, QButtonGroup, QDialog, QScrollArea
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from functools import partial
import RebuildsComponents

class UserLevelsModule:
    def __init__(self):
        self.variable = "??????"

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

        frame_order_gesture = QFrame(modal)
        frame_order_gesture.setGeometry(360, 100, 920, 300)
        frame_order_gesture.setStyleSheet("""
                                QFrame {
                                    background-color: #9EFFA5; /* Фон картки */
                                    border-radius: 10px; /* Закруглені кути */
                                }
                            """)
        N = 0
        # Додавання "карток" у контейнер
        for i in range(5):  # 5 карток
            image_card = RebuildsComponents.ClickableLabel(frame_order_gesture)
            image_card.setGeometry(30 + N, 70, 150, 150)
            image_card.setStyleSheet("""
                                    QLabel {
                                        background-color: #DAFFDF; /* Фон картки */
                                        border-radius: 10px; /* Закруглені кути */
                                    }
                                """)
            image_card.setObjectName(f"order_label_{i}")  # Задання імені
            # Підключаємо сигнал кліку до обробника
            image_card.clicked.connect(partial(self.order_gesture_click, image_card))
            N += 25 + 150

        # ------------------------------------------------------------------------------------------------------------------

        modal.exec_()  # Запускаємо модальне вікно (блокує основне)

    # Функція-обробник мітки для вибору жесту
    def on_gesture_click(self, image_path):
        # Зберігаємо шлях до обраного жесту
        print(f"Обраний жест: {image_path}")

    # Функція-обробник мітки для видалення жесту з фрейму "порядок жестів"
    def order_gesture_click(self, image_card):
        image_card.setStyleSheet("""
                                QLabel {
                                    background-color: #DAFFDF; /* Фон картки */
                                    border-radius: 10px; /* Закруглені кути */
                                   }
                                """)
        print(f"Клік на: {image_card.objectName()}")


    def startUserLevel(self):
        print("UserLevelsModule: def startUserLevel()")