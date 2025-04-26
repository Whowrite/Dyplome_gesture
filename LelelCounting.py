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
        self.levelGestures = []
        self.errorAnswers = 0
        self.time_remaining = 0
        self.countdown_timer = QTimer()
        self.countpoints = 0

    # Функція-обробник кнопки для створення рівня
    def create_new_level_click(self, current_game_level, card_name, level_cv_frame):
        print("Good luck: " + current_game_level)
        self.current_game_level = current_game_level
        self.numberTasks = self.getNumTasks(current_game_level)
        print("Good luck: " + card_name)
        self.levelGestures = Cl.getlevelarray(card_name, current_game_level)
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

        # Таймер на 90-40 секунд для автоматичного закриття рівня
        if self.current_game_level == "button_level_4":
            QTimer.singleShot(93000,
                                    lambda: self.force_end_level(timer, cap, camera_label, level_cv_frame, frameForLevelCounters))
        elif self.current_game_level == "button_level_5":
            QTimer.singleShot(68000,
                              lambda: self.force_end_level(timer, cap, camera_label, level_cv_frame, frameForLevelCounters))
        elif self.current_game_level == "button_level_6":
            QTimer.singleShot(43000,
                              lambda: self.force_end_level(timer, cap, camera_label, level_cv_frame, frameForLevelCounters))

        detector = htm.handDetector()

        def update_frame():
            ret, img = cap.read()
            if ret:
                frame = detector.findHands(img, Draw=False)
                lmList = []
                if card_name == "Жести однією рукою":
                    lmList = detector.findPosition(frame, Draw=False)
                    self.countpoints = 21
                elif card_name == "Жести двума руками":
                    lmList = detector.findPositionsBothHands(frame, Draw=False)
                    self.countpoints = 2

                if self.current_level != self.numberTasks:
                    detector.setGesture(self.levelGestures[self.current_level][1], self.levelGestures[self.current_level][0])
                    gesture_img = self.levelGestures[self.current_level][2]
                    if gesture_img is not None:
                        h, w, c = gesture_img.shape  # Отримуємо розміри
                        frame[0:h, 0:w] = gesture_img  # Вставляємо зображення

                    if len(lmList) == self.countpoints:
                        # Список точок, які потрібно знайти (IDs)
                        targetPoints = [4, 8, 12, 16, 20]
                        # Знаходимо потрібні точки
                        tempArray = []
                        if card_name == "Жести однією рукою":
                            tempArray = detector.extractPoints(lmList, targetPoints)
                        elif card_name == "Жести двума руками":
                            tempArray = detector.extractPointsBothHands(lmList, targetPoints)

                        # print(tempArray)

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
                                self.countdown_timer.stop()  # Зупиняємо таймер
                                def end_level():
                                    if self.show_message_box():
                                        # Завершення рівня після показу повідомлення
                                        self.stop_camera(timer, cap, camera_label)
                                        self.closingCVframe(level_cv_frame, frameForLevelCounters)
                                    else:
                                        self.current_level = 0
                                        self.errorAnswers = 0
                                        self.uncheckButtons(frameForLevelCounters)
                                        self.setTime_remaining(1)
                                        self.countdown_timer.start()

                                QTimer.singleShot(1000, end_level) # Затримка 3 секунди (3000 мс)


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

        # --------------------------------------------------------------------------------------------------------------Мітка для відображення таймеру

        # Додаємо QLabel для відображення таймера
        timer_label = QLabel(level_cv_frame)
        timer_label.setGeometry(300, 26, 210, 50)
        timer_label.setAlignment(Qt.AlignCenter)
        timer_label.setFont(QFont("Arial", 18, QFont.Bold))
        timer_label.setStyleSheet("""
            QLabel {
                background-color: #DAFFDF; 
                color: black;
                border-radius: 10px;
                border: 2px solid blue;
            }
        """)

        # Встановлюємо початковий час залежно від рівня
        if self.current_game_level == "button_level_4" or self.current_game_level == "button_level_5" or self.current_game_level == "button_level_6":
            timer_label.show()
            self.setTime_remaining()

        # Оновлення відображення часу
        timer_label.setText(f"Час: {self.time_remaining} сек")

        # Таймер для оновлення часу щосекунди
        self.countdown_timer.timeout.connect(lambda: self.update_timer(timer_label))
        self.countdown_timer.start(1000)  # Оновлення кожну секунду

        # --------------------------------------------------------------------------------------------------------------Кнопка для повернення на сторінку вибору рівня

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
        button_return.clicked.connect(lambda: (self.stop_camera(timer, cap, camera_label), self.closingCVframe(level_cv_frame, frameForLevelCounters)))

        # ------------------------------------------------------------------------------------------------------------------Кнопка пропуску жеста

        button_skip = QPushButton(level_cv_frame)
        button_skip.setGeometry(570, 850, 200, 60)
        button_skip.setText("Пропустити")
        button_skip.show()

        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        button_skip.setFont(font)

        button_skip.setStyleSheet("""
                                        QPushButton {
                                            background-color: #DAFFDF; /* Колір кнопки */
                                            color: black; /* Колір тексту */
                                            border-radius: 10px; /* Закруглення кутів */
                                        }
                                        QPushButton:hover {
                                            background-color: #5dade2; /* Колір кнопки при наведенні */
                                        }
                                        QPushButton:pressed {
                                            background-color: #1f618d; /* Колір кнопки при натисканні */
                                        }
                                    """)
        button_skip.clicked.connect(
            lambda: (self.skipGesture(level_cv_frame, frameForLevelCounters, timer, cap, camera_label)))

        # ------------------------------------------------------------------------------------------------------------------

    # Примусове завершення рівня після N секунд
    def force_end_level(self, timer, cap, camera_label, level_cv_frame, frameForLevelCounters):
        """Примусове завершення рівня після N секунд"""
        print("Час вийшов! Рівень закрито.")
        self.countdown_timer.stop()  # Зупиняємо таймер
        self.stop_camera(timer, cap, camera_label)
        self.closingCVframe(level_cv_frame, frameForLevelCounters)

    # Метод для оновлення таймеру
    def update_timer(self, timer_label):
        """Оновлює таймерний відлік на екрані"""
        if self.time_remaining <= 10:
            timer_label.setFont(QFont("Arial", 20, QFont.Bold))
            timer_label.setStyleSheet("""
                        QLabel {
                            background-color: #DAFFDF; 
                            color: red;
                            border-radius: 10px;
                            border: 2px solid blue;
                        }
                    """)
        if self.time_remaining > 0:
            self.time_remaining -= 1
            timer_label.setText(f"Час: {self.time_remaining} сек")
        else:
            self.countdown_timer.stop()  # Зупиняємо таймер після завершення часу
            timer_label.setText("Час вийшов!")

    # Повернення стану кнопок контейнера для відображення кількості завдань
    def uncheckButtons(self, frameForLevelCounters):
        for i in range(self.numberTasks):
            founded_label = frameForLevelCounters.findChild(QLabel,
                                                            "level_Counter_" + str(i))
            founded_label.setStyleSheet("""
                            QLabel {
                                    background-color: #DAFFDF; /* Колір фону */
                                    color: black; /* Колір тексту */
                                    border-radius: 5px; /* Закруглення кутів */
                                    border: 2px solid blue;
                            }
                            """)
            founded_label.setText("")

    # Закриття камери при виході
    def stop_camera(self, timer, cap, camera_label):
        timer.stop()
        cap.release()
        camera_label.clear()
        print("Camera stopped")

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
        self.errorAnswers = 0
        # Отримуємо всіх дочірніх віджетів фрейму
        for child in frameForLevelCounters.findChildren(QWidget):
            # Видаляємо кожного дочірнього віджета
            child.deleteLater()

    # Функція-обробник кнопки для пропуску жеста
    def skipGesture(self, level_cv_frame, frameForLevelCounters, timer, cap, camera_label):
        founded_label = frameForLevelCounters.findChild(QLabel,
                                                        "level_Counter_" + str(self.current_level))
        founded_label.setStyleSheet("""
                                                                        QLabel {
                                                                            background-color: #DAFFDF; /* Колір фону */
                                                                            color: black; /* Колір тексту */
                                                                            border-radius: 5px; /* Закруглення кутів */
                                                                            border: 2px solid red;
                                                                            font-size: 25px;
                                                                            font-weight: bold;
                                                                        }
                                                                    """)
        founded_label.setText("X")
        self.current_level += 1
        self.errorAnswers += 1
        if self.current_level == self.numberTasks:
            self.countdown_timer.stop()  # Зупиняємо таймер
            def end_level():
                if self.show_message_box():
                    # Завершення рівня після показу повідомлення
                    self.stop_camera(timer, cap, camera_label)
                    self.closingCVframe(level_cv_frame, frameForLevelCounters)
                else:
                    self.current_level = 0
                    self.errorAnswers = 0
                    self.uncheckButtons(frameForLevelCounters)
                    self.setTime_remaining(1)
                    self.countdown_timer.start()

            QTimer.singleShot(1000, end_level)  # Затримка 3 секунди (3000 мс)

    def setTime_remaining(self, timeadd = 0):
        # Встановлюємо початковий час залежно від рівня
        if self.current_game_level == "button_level_4":
            self.time_remaining = 90 + timeadd
        elif self.current_game_level == "button_level_5":
            self.time_remaining = 65 + timeadd
        elif self.current_game_level == "button_level_6":
            self.time_remaining = 40 + timeadd

    # Функція для відображення повідомлення про завершення рівня
    def show_message_box(self):
        # Створюємо повідомлення
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)  # Іконка: Information, Warning, Critical, Question
        msg_box.setWindowTitle("Повідомлення")

        if self.errorAnswers == 0:
            msg_box.setText("Рівень пройдено!")
            msg_box.setInformativeText("Бажаєте продовжити?")
            btn_ok = msg_box.addButton("Добре", QMessageBox.AcceptRole)
        else:
            msg_box.setText(f"Ви зробили {self.errorAnswers} помилок під час проходження рівня!")
            msg_box.setInformativeText("Бажаєте пройти рівень заново?")
            btn_yes = msg_box.addButton("Так", QMessageBox.YesRole)
            btn_no = msg_box.addButton("Ні", QMessageBox.NoRole)

        # Відображаємо повідомлення та отримуємо результат
        msg_box.exec_()

        # Обробка дій користувача
        clicked_button = msg_box.clickedButton()

        if self.errorAnswers == 0:
            if clicked_button == btn_ok:
                print("Натиснуто Добре")
                return True
        else:
            if clicked_button == btn_yes:
                print("Натиснуто Так")
                return False
            elif clicked_button == btn_no:
                print("Натиснуто Ні")
                return True
