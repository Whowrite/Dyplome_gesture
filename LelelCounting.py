import json, os, cv2
import HandTModule as htm
import CollectionLevels as Cl
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QFrame, QHBoxLayout, \
    QStyle, QMessageBox
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt

class CreateLevel:
    def __init__(self, numberTasks = 0, Time = 0, UserGestures = [], widgetsLanguage = 0):
        self.current_level = 0
        self.numberTasks = numberTasks
        self.current_game_level = ""
        if UserGestures != []:
            self.levelGestures = Cl.getUserLevelArray(numberTasks, UserGestures)
        else:
            self.levelGestures = []
        self.errorAnswers = 0
        self.time_remaining = Time
        self.countdown_timer = QTimer()
        self.infoAboutGestures = {}
        self.countpoints = 0
        self.cards_names = {
            "Gestures with one hand": "Жести однією рукою",
            "Gestures with two hand": "Жести двума руками",
            "User level": "Користувацький рівень"
        }
        self.card_name = ""
        self.widgetsColor = ["#9EFFA5", "#DAFFDF"]
        self.widgetsLanguage = widgetsLanguage
        self.widgetsText = {
            "button_skip": ['Пропустити', 'Skip'],
            "msg_box": [['Повідомлення', 'Рівень пройдено!', "Бажаєте продовжити?", "Добре", "Ви зробили ", " помилок під час проходження рівня!",
                         "Бажаєте пройти рівень заново?", "Так", "Ні"],
                        ['Message', 'The level is completed!', "Would you like to continue?", "Good", "You have done ", " errors during the level passage!",
                         "Do you want to go through the level again?", "Yes", "No"]],
        }
        self.LevelStatistics = {
            "Жести однією рукою": {
                "button_level_1": [0, 0],
                "button_level_2": [0, 0],
                "button_level_3": [0, 0],
                "button_level_4": [0, 0],
                "button_level_5": [0, 0],
                "button_level_6": [0, 0]
            },
            "Жести двума руками": {
                "button_level_1": [0, 0],
                "button_level_2": [0, 0],
                "button_level_3": [0, 0],
                "button_level_4": [0, 0],
                "button_level_5": [0, 0],
                "button_level_6": [0, 0]
            }
        }

    # Функція для зміни мови додатку
    def setLanguage(self, Language):
        self.widgetsLanguage = Language
        # print(f"class CreateLevel(): def setLanguage(self, Language): {Language}")

    # Функція для зміни мови додатку
    def setColor(self, color):
        self.widgetsColor = color
        # print(f"class CreateLevel(): def setColor(self, color): {color}")

    # Функція для зміни мови додатку
    def setDefaultParameters(self):
        self.current_level = 0
        self.errorAnswers = 0
        self.countpoints = 0
        self.time_remaining = 0
        self.countdown_timer = QTimer()
        self.infoAboutGestures = {}
        # print(f"setDefaultParameters:")

    # Функція-обробник кнопки для створення рівня
    def create_new_level_click(self, current_game_level, card_name, level_cv_frame):
        if card_name in self.cards_names:
            self.card_name = self.cards_names[card_name]
        else:
            self.card_name = card_name
        print("Good luck: " + current_game_level)
        self.current_game_level = current_game_level
        if not self.card_name == "Користувацький рівень":
            self.numberTasks = self.getNumTasks()
            print("Good luck: " + self.card_name)
            self.levelGestures = Cl.getlevelarray(self.card_name, self.current_game_level)
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

        paddingLeft = self.getPadding()
        paddingCenter = 0
        for i in range(self.numberTasks):
            level_Counter = QLabel(frameForLevelCounters)
            level_Counter.setGeometry(paddingLeft + paddingCenter, 15, 40, 40)
            level_Counter.setObjectName("level_Counter_" + str(i))
            level_Counter.setStyleSheet(f"""
                        QLabel {{
                            background-color: {self.widgetsColor[1]}; /* Колір фону */
                            color: black; /* Колір тексту */
                            border-radius: 5px; /* Закруглення кутів */
                            border: 2px solid blue;
                        }}
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
        camera_label.setStyleSheet(f"background-color: {self.widgetsColor[0]};")
        camera_label.setAlignment(Qt.AlignCenter)
        camera_label.show()

        # Ініціалізація камери та QTimer
        cap = cv2.VideoCapture(0)  # Використовуємо першу камеру (0)

        if not cap.isOpened():
            print("Error: Camera not found!")
            return

        timer = QTimer()

        # Таймер на 90-40 секунд для автоматичного закриття рівня
        if self.current_game_level == "button_level_4" or (self.current_game_level == "Користувацький рівень" and self.time_remaining == 90):
            QTimer.singleShot(93000,
                                    lambda: self.force_end_level(timer, cap, camera_label, level_cv_frame, frameForLevelCounters))
        elif self.current_game_level == "button_level_5" or (self.current_game_level == "Користувацький рівень" and self.time_remaining == 65):
            QTimer.singleShot(68000,
                              lambda: self.force_end_level(timer, cap, camera_label, level_cv_frame, frameForLevelCounters))
        elif self.current_game_level == "button_level_6" or (self.current_game_level == "Користувацький рівень" and self.time_remaining == 40):
            QTimer.singleShot(43000,
                              lambda: self.force_end_level(timer, cap, camera_label, level_cv_frame, frameForLevelCounters))

        detector = htm.handDetector()

        def update_frame():
            ret, img = cap.read()
            if ret:
                frame = detector.findHands(img, Draw=False)
                lmList = []
                if self.current_level != self.numberTasks:
                    if self.levelGestures[self.current_level][3] in Cl.oneHandGestures_list:
                        lmList = detector.findPosition(frame, Draw=False)
                        self.countpoints = 21
                    elif self.levelGestures[self.current_level][3] in Cl.twoHandGestures_list:
                        lmList = detector.findPositionsBothHands(frame, Draw=False)
                        self.countpoints = 2
                    detector.setGesture(self.levelGestures[self.current_level][1],
                                        self.levelGestures[self.current_level][0])
                    gesture_img = self.levelGestures[self.current_level][2]
                    if gesture_img is not None:
                        h, w, c = gesture_img.shape  # Отримуємо розміри
                        frame[0:h, 0:w] = gesture_img  # Вставляємо зображення

                    if len(lmList) == self.countpoints:
                        # Список точок, які потрібно знайти (IDs)
                        targetPoints = [4, 8, 12, 16, 20]
                        # Знаходимо потрібні точки
                        tempArray = []
                        if self.levelGestures[self.current_level][3] in Cl.oneHandGestures_list:
                            tempArray = detector.extractPoints(lmList, targetPoints)
                        elif self.levelGestures[self.current_level][3] in Cl.twoHandGestures_list:
                            tempArray = detector.extractPointsBothHands(lmList, targetPoints)

                        # print(tempArray)

                        # Порівнюємо з жестом
                        if detector.compareGestures(tempArray):
                            founded_label = frameForLevelCounters.findChild(QLabel,
                                                                            "level_Counter_" + str(self.current_level))
                            founded_label.setStyleSheet(f"""
                                                                    QLabel {{
                                                                        background-color: {self.widgetsColor[1]}; /* Колір фону */
                                                                        color: black; /* Колір тексту */
                                                                        border-radius: 5px; /* Закруглення кутів */
                                                                        border: 2px solid green;
                                                                        font-size: 25px;
                                                                        font-weight: bold;
                                                                    }}
                                                                """)
                            founded_label.setText("✓")
                            self.addAnswerCorrectGesture(1)
                            self.current_level += 1
                            if self.current_level == self.numberTasks:
                                self.countdown_timer.stop()  # Зупиняємо таймер
                                def end_level():
                                    if self.show_message_box():
                                        # Завершення рівня після показу повідомлення
                                        self.addStatisticsGesture()
                                        self.stop_camera(timer, cap, camera_label)
                                        self.closingCVframe(level_cv_frame, frameForLevelCounters)
                                    else:
                                        self.current_level = 0
                                        self.errorAnswers = 0
                                        self.infoAboutGestures = {}
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
        timer_label.setGeometry(250, 26, 200, 50)
        timer_label.setAlignment(Qt.AlignCenter)
        timer_label.setFont(QFont("Arial", 18, QFont.Bold))
        timer_label.setStyleSheet(f"""
            QLabel {{
                background-color: {self.widgetsColor[1]}; 
                color: black;
                border-radius: 10px;
                border: 2px solid blue;
            }}
        """)

        # Встановлюємо початковий час залежно від рівня
        if (self.current_game_level == "button_level_4" or self.current_game_level == "button_level_5" or
                self.current_game_level == "button_level_6") or (self.current_game_level == "Користувацький рівень" and self.time_remaining != 0):
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
        button_return.clicked.connect(lambda: (self.stop_camera(timer, cap, camera_label), self.closingCVframe(level_cv_frame, frameForLevelCounters)))

        # ------------------------------------------------------------------------------------------------------------------Кнопка пропуску жеста

        button_skip = QPushButton(level_cv_frame)
        button_skip.setGeometry(570, 850, 200, 60)
        button_skip.setText(self.widgetsText["button_skip"][self.widgetsLanguage])
        button_skip.show()

        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        button_skip.setFont(font)

        button_skip.setStyleSheet(f"""
                                        QPushButton {{
                                            background-color: {self.widgetsColor[1]}; /* Колір кнопки */
                                            color: black; /* Колір тексту */
                                            border-radius: 10px; /* Закруглення кутів */
                                        }}
                                        QPushButton:hover {{
                                            background-color: #5dade2; /* Колір кнопки при наведенні */
                                        }}
                                        QPushButton:pressed {{
                                            background-color: #1f618d; /* Колір кнопки при натисканні */
                                        }}
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
            timer_label.setStyleSheet(f"""
                        QLabel {{
                            background-color: {self.widgetsColor[1]}; 
                            color: red;
                            border-radius: 10px;
                            border: 2px solid blue;
                        }}
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
            founded_label.setStyleSheet(f"""
                            QLabel {{
                                    background-color: {self.widgetsColor[1]}; /* Колір фону */
                                    color: black; /* Колір тексту */
                                    border-radius: 5px; /* Закруглення кутів */
                                    border: 2px solid blue;
                            }}
                            """)
            founded_label.setText("")

    # Закриття камери при виході
    def stop_camera(self, timer, cap, camera_label):
        timer.stop()
        cap.release()
        camera_label.clear()
        print("Camera stopped")

    # Функція для визначення кількоcті завдань від вибраного рівня
    def getNumTasks(self):
        if self.current_game_level == "button_level_1" or self.current_game_level == "button_level_4":
            return 3
        elif self.current_game_level == "button_level_2" or self.current_game_level == "button_level_5":
            return 5
        else:
            return 7

    # Функція для визначення відступу між елементами контейнеру для відображення кількості завдань
    def getPadding(self):
        if self.numberTasks == 3:
            return 320
        elif self.numberTasks == 5:
            return 240
        elif self.numberTasks == 7:
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
        founded_label.setStyleSheet(f"""
                                        QLabel {{
                                            background-color: {self.widgetsColor[1]}; /* Колір фону */
                                            color: black; /* Колір тексту */
                                            border-radius: 5px; /* Закруглення кутів */
                                            border: 2px solid red;
                                            font-size: 25px;
                                            font-weight: bold;
                                        }}
                                    """)
        founded_label.setText("X")
        self.addAnswerCorrectGesture(0)
        self.current_level += 1
        self.errorAnswers += 1
        if self.current_level == self.numberTasks:
            self.countdown_timer.stop()  # Зупиняємо таймер
            def end_level():
                if self.show_message_box():
                    # Завершення рівня після показу повідомлення
                    self.addStatisticsGesture()
                    self.stop_camera(timer, cap, camera_label)
                    self.closingCVframe(level_cv_frame, frameForLevelCounters)
                else:
                    self.current_level = 0
                    self.errorAnswers = 0
                    self.infoAboutGestures = {}
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
        elif self.current_game_level == "Користувацький рівень":
            self.time_remaining += timeadd

    # Функція для відображення повідомлення про завершення рівня
    def show_message_box(self):
        # Створюємо повідомлення
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)  # Іконка: Information, Warning, Critical, Question
        msg_box.setWindowTitle(self.widgetsText["msg_box"][self.widgetsLanguage][0])

        if self.errorAnswers == 0:
            msg_box.setText(self.widgetsText["msg_box"][self.widgetsLanguage][1])
            msg_box.setInformativeText(self.widgetsText["msg_box"][self.widgetsLanguage][2])
            btn_ok = msg_box.addButton(self.widgetsText["msg_box"][self.widgetsLanguage][3], QMessageBox.AcceptRole)
        else:
            temp_str = self.widgetsText["msg_box"][self.widgetsLanguage][4] + str(self.errorAnswers) + self.widgetsText["msg_box"][self.widgetsLanguage][5]
            msg_box.setText(temp_str)
            msg_box.setInformativeText(self.widgetsText["msg_box"][self.widgetsLanguage][6])
            btn_yes = msg_box.addButton(self.widgetsText["msg_box"][self.widgetsLanguage][7], QMessageBox.YesRole)
            btn_no = msg_box.addButton(self.widgetsText["msg_box"][self.widgetsLanguage][8], QMessageBox.NoRole)

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

    # Зберігає словник LevelStatistics у файл у форматі JSON.
    def save_level_statistics(self, filename="level_statistics.json"):
        """
        Args:
            statistics (dict): Словник зі статистикою рівнів
            filename (str): Ім'я файлу для збереження (за замовчуванням level_statistics.json)
        """
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(self.LevelStatistics, file, ensure_ascii=False, indent=4)
            print(f"Дані успішно збережено у файл {filename}")
        except Exception as e:
            print(f"Помилка при збереженні даних: {e}")

    # Зчитує словник LevelStatistics з файлу JSON.
    def load_level_statistics(self, filename="level_statistics.json"):
        """
        Args:
            filename (str): Ім'я файлу для зчитування (за замовчуванням level_statistics.json)
        Returns:
            dict: Словник зі статистикою рівнів або None у разі помилки
        """
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                print(f"Файл {filename} не знайдено")
                return None
        except Exception as e:
            print(f"Помилка при зчитуванні даних: {e}")
            return None

    # Функція для збереження статистики про використані жести
    def addAnswerCorrectGesture(self, answerResult):
        """
        Формат: { "назва жесту": [правильна відповідь, кількість використань] }
        """
        gesture_name = self.levelGestures[self.current_level][3]  # Отримуємо назву жесту
        if gesture_name in self.infoAboutGestures:
            # Якщо жест уже є, оновлюємо статистику
            self.infoAboutGestures[gesture_name][0] += answerResult  # Оновлюємо правильні відповіді
            self.infoAboutGestures[gesture_name][1] += 1  # Збільшуємо кількість використань
        else:
            # Якщо жест новий, додаємо новий запис
            self.infoAboutGestures[gesture_name] = [answerResult, 1]

    # Функція для оновлення статистики про використані жести в бд та level_statistics.json
    def addStatisticsGesture(self):
        resultOfLevel = self.numberTasks - self.errorAnswers
        if self.LevelStatistics[self.card_name][self.current_game_level][0] < resultOfLevel:
            self.LevelStatistics[self.card_name][self.current_game_level][0] = resultOfLevel
        self.LevelStatistics[self.card_name][self.current_game_level][1] += 1
        print(f"Назва режиму гри: {self.card_name}")
        print(f"Статистика пройденого рівня: \n{self.infoAboutGestures}")