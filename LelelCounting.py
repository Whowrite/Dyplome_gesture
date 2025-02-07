import time
import cv2
import HandTModule as htm
import CollectionLevels as Cl
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QFrame, QHBoxLayout, \
    QStyle, QMessageBox
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt

class CreateLevel:
    def __init__(self):
        self.current_level = 0
        self.numberTasks = 0
        self.current_game_level = ""

    # Функція-обробник кнопки для створення рівня
    def create_new_level_click(self, current_game_level, card_name, level_cv_frame):
        print("Good luck: " + current_game_level)
        self.current_game_level = current_game_level
        self.numberTasks = self.getNumTasks(current_game_level)
        print("Good luck: " + card_name)
        level_cv_frame.show()

        # ------------------------------------------------------------------------------------------------------------------Мітки для відображення рук
        left_hand_label = QLabel(level_cv_frame)
        left_hand_label.setGeometry(25, 290, 200, 300)
        pixmap = QPixmap("FingerImages/left_hand.png")
        left_hand_label.setPixmap(pixmap)
        left_hand_label.setScaledContents(True)
        left_hand_label.show()

        right_hand_label = QLabel(level_cv_frame)
        right_hand_label.setGeometry(1085, 290, 200, 300)
        pixmap = QPixmap("FingerImages/right_hand.png")
        right_hand_label.setPixmap(pixmap)
        right_hand_label.setScaledContents(True)
        right_hand_label.show()

        # ------------------------------------------------------------------------------------------------------------------Фрейм для відображення кількості завдань

        frameForLevelCounters = QFrame(level_cv_frame)
        frameForLevelCounters.setGeometry(250, 780, 820, 70)
        frameForLevelCounters.setStyleSheet("""
                            QFrame {
                                background-color: none; /* Колір фону */
                            }
                        """)
        frameForLevelCounters.show()

        # ------------------------------------------------------------------------------------------------------------------Контейнер для відображення кількості завдань

        paddingLeft = self.getPadding(current_game_level)
        paddingCenter = 0
        for i in range(self.numberTasks):
            level_Counter = QLabel(frameForLevelCounters)
            level_Counter.setGeometry(paddingLeft + paddingCenter, 15, 40, 40)
            level_Counter.setObjectName("level_Counter_" + str(i))
            level_Counter.setStyleSheet("""
                        QLabel {
                            background-color: #DAFFDF; /* Колір фону */
                            color: black; /* Колір тексту */
                            border-radius: 5px; /* Закруглення кутів */
                            border: 2px solid blue;
                        }
                    """)
            level_Counter.show()
            paddingCenter += 43
            if i < self.numberTasks - 1:
                arrow_connector = QLabel(frameForLevelCounters)
                arrow_connector.setGeometry(paddingLeft + paddingCenter, 13, 30, 40)
                arrow_connector.setText("→")
                arrow_connector.setStyleSheet("""
                                    QLabel {
                                        background-color: none; /* Колір фону */
                                        color: black; /* Колір тексту */
                                        border: none;
                                        font-size: 23px;
                                    }
                                """)
                arrow_connector.setAlignment(Qt.AlignHCenter | Qt.AlignCenter)  # Центрування тексту
                arrow_connector.show()
                paddingCenter += 33

        # ------------------------------------------------------------------------------------------------------------------Фрейм для відображення камери

        # Додамо QLabel для відображення відео
        camera_label = QLabel(level_cv_frame)
        camera_label.setGeometry(250, 120, 820, 650)
        camera_label.setStyleSheet("background-color: #9EFFA5;")
        camera_label.setAlignment(Qt.AlignCenter)
        camera_label.show()

        # Ініціалізація камери та QTimer
        cap = cv2.VideoCapture(0)  # Використовуємо першу камеру (0)

        if not cap.isOpened():
            print("Error: Camera not found!")
            return

        timer = QTimer()

        detector = htm.handDetector()

        def update_frame():
            ret, img = cap.read()
            if ret:
                frame = detector.findHands(img, Draw=False)
                lmList = detector.findPosition(frame, Draw=False)

                levelGestures = [
                    [Cl.gesture_oke_right, Cl.gesture_oke_left, cv2.imread(f'FingerImages/gesture_oke.jpg')],
                    [Cl.gesture_peace_right, Cl.gesture_peace_left, cv2.imread(f'FingerImages/gesture_peace.jpg')],
                    [Cl.gesture_wait_right, Cl.gesture_wait_left, cv2.imread(f'FingerImages/gesture_wait.jpg')]]
                detector.setGesture(levelGestures[self.current_level][1], levelGestures[self.current_level][0])

                gesture_img = levelGestures[self.current_level][2]

                if gesture_img is not None:
                    h, w, c = gesture_img.shape  # Отримуємо розміри
                    frame[0:h, 0:w] = gesture_img  # Вставляємо зображення

                if len(lmList) != 0:
                    # Список точок, які потрібно знайти (IDs)
                    targetPoints = [4, 8, 12, 16, 20]
                    # Знаходимо потрібні точки
                    tempArray = detector.extractPoints(lmList, targetPoints)
                    print(tempArray)

                    # Порівнюємо з жестом
                    if detector.compareGestures(tempArray):
                        founded_label = frameForLevelCounters.findChild(QLabel,
                                                                        "level_Counter_" + str(self.current_level))
                        founded_label.setStyleSheet("""
                                                                QLabel {
                                                                    background-color: #DAFFDF; /* Колір фону */
                                                                    color: black; /* Колір тексту */
                                                                    border-radius: 5px; /* Закруглення кутів */
                                                                    border: 2px solid green;
                                                                    font-size: 25px;
                                                                    font-weight: bold;
                                                                }
                                                            """)
                        founded_label.setText("✓")
                        self.current_level += 1
                        if self.current_level == self.numberTasks:
                            self.show_message_box(0)
                            # Завершення рівня
                            stop_camera()
                            self.closingCVframe(level_cv_frame, frameForLevelCounters)

                # Конвертуємо кадр OpenCV в формат QImage
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

                # Створюємо QPixmap і масштабуємо до розміру QLabel
                pixmap = QPixmap.fromImage(q_img)
                scaled_pixmap = pixmap.scaled(
                    camera_label.size(),  # Розмір QLabel
                    Qt.KeepAspectRatio,  # Зберігаємо пропорції
                    Qt.SmoothTransformation  # Використовуємо плавну трансформацію
                )

                # Відображаємо масштабоване відео
                camera_label.setPixmap(scaled_pixmap)
            else:
                print("Error: Cannot read frame!")

        # Підключаємо таймер до функції оновлення кадру
        timer.timeout.connect(update_frame)
        timer.start(30)  # Оновлюємо кадри кожні 30 мс (~33 fps)

        # Закриття камери при виході
        def stop_camera():
            timer.stop()
            cap.release()
            camera_label.clear()
            print("Camera stopped")

        # ------------------------------------------------------------------------------------------------------------------Кнопка для повернення на сторінку вибору рівня

        button_return = QPushButton(level_cv_frame)
        button_return.setGeometry(48, 23, 60, 60)
        button_return.setText("X")
        button_return.show()

        font = QFont()
        font.setBold(True)
        font.setPointSize(18)
        button_return.setFont(font)

        button_return.setStyleSheet("""
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
        button_return.clicked.connect(lambda: (stop_camera(), self.closingCVframe(level_cv_frame, frameForLevelCounters)))

        # ------------------------------------------------------------------------------------------------------------------

    # Функція для визначення кількоcті завдань від вибраного рівня
    def getNumTasks(self, current_game_level):
        if current_game_level == "button_level_1" or current_game_level == "button_level_4":
            return 3
        elif current_game_level == "button_level_2" or current_game_level == "button_level_5":
            return 5
        else:
            return 7

    # Функція для визначення відступу між елементами контейнеру для відображення кількості завдань
    def getPadding(self, current_game_level):
        if current_game_level == "button_level_1" or current_game_level == "button_level_4":
            return 320
        elif current_game_level == "button_level_2" or current_game_level == "button_level_5":
            return 240
        else:
            return 160

    # Функція-обробник кнопки для дострокового завершення рівня
    def closingCVframe(self, level_cv_frame, frameForLevelCounters):
        print("Close level_cv_frame")
        level_cv_frame.hide()
        self.current_level = 0
        # Отримуємо всіх дочірніх віджетів фрейму
        for child in frameForLevelCounters.findChildren(QWidget):
            # Видаляємо кожного дочірнього віджета
            child.deleteLater()

    # Функція для відображення повідомлення про завершення рівня
    def show_message_box(self, problems):
        # Створюємо повідомлення
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)  # Іконка: Information, Warning, Critical, Question
        msg_box.setWindowTitle("Повідомлення")
        if problems == 0:
            msg_box.setText("Рівень пройдено!")
            msg_box.setInformativeText("Бажаєте продовжити?")
            msg_box.setDefaultButton(QMessageBox.Ok)
        else:
            msg_box.setText(f"Ви зробили {problems} помилок під час проходження рівня!")
            msg_box.setInformativeText("Бажаєте пройти рівень заново?")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        # Відображаємо повідомлення та отримуємо результат
        result = msg_box.exec_()

        # Обробка дій користувача
        if result == QMessageBox.Ok:
            print("Натиснуто Ok")
        elif result == QMessageBox.Yes:
            print("Натиснуто Yes")
        elif result == QMessageBox.No:
            print("Натиснуто No")