from PyQt5.QtWidgets import QFrame, QDialog, QLabel, QMainWindow, QGraphicsOpacityEffect
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from datetime import datetime
import sqlite3

class ClickableFrame(QFrame):
    clicked = pyqtSignal()  # створюємо власний сигнал

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()  # емітуємо сигнал при кліку

class ClickableLabel(QLabel):
    clicked = pyqtSignal()  # створюємо власний сигнал

    def __init__(self, text, opacityON = 1.0, parent=None):
        super().__init__(text, parent)
        self.opacityON = opacityON
        self.setMouseTracking(True)  # Увімкнення відстеження миші
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(self.opacityON)  # Початкова прозорість
        self.setGraphicsEffect(self.opacity_effect)

    def enterEvent(self, event):
        """Змінюємо прозорість при наведенні."""
        self.opacity_effect.setOpacity(1.0)  # Повна непрозорість

    def leaveEvent(self, event):
        """Повертаємо початкову прозорість."""
        self.opacity_effect.setOpacity(self.opacityON)  # Початкова прозорість

    def mousePressEvent(self, event):
        """Емітуємо сигнал при кліку."""
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

class ModalWindow(QDialog):
    def __init__(self, x, y, lenght, height, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Модальне вікно")
        self.setGeometry(x, y, lenght, height)
        self.setStyleSheet("""
            QDialog {
                background-color: #F0F0F0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)


class MainWindow(QMainWindow):
    def __init__(self, Music, levelCounting):
        super().__init__()
        self.connection = None
        self.levelCounting = levelCounting
        self.music = Music
        self.widgetsColor = ["#9EFFA5", "#DAFFDF"]
        self.widgetsLanguage = 0

        self.session_time = 0
        self.session_timer = QTimer()
        self.session_timer.timeout.connect(self.update_session_time)
        self.session_timer.start(1000)

        self.setWindowTitle("ToTrainYourNeurons")
        self.setGeometry(250, 100, 1315, 917)

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.widgetsColor[1]}; /* Колір вікна */
            }}
        """)

    # Встановлення підключення до бд
    def set_connect_ToBD(self, con):
        self.connection = con
        print("Підлючення встановлено: MainWindow:")

    def closeEvent(self, event):
        """
        Перевизначаємо подію закриття вікна, щоб зберегти налаштування перед виходом.
        """
        # self.music.stop_music()
        self.saveSettings()
        self.saveSessionTime()
        self.music.stop_music()
        self.levelCounting.save_level_statistics()
        self.connection.close()
        event.accept()  # Дозволяємо вікну закритися

    def saveSettings(self):
        print("Збереження налаштувань...")
        filename = "settings.txt"
        languages = {
            0: "ukrainian",
            1: "english"
        }

        try:
            current_language = languages[self.widgetsLanguage]
            current_colors = self.widgetsColor

            settings_content = f"Language: {current_language}\n"
            settings_content += f"Color: \"{current_colors[0]}\", \"{current_colors[1]}\""

            with open(filename, 'w', encoding='utf-8') as file:
                file.write(settings_content)

        except Exception as e:
            print(f"Помилка при збереженні налаштувань: {e}")

    def set_color(self, colors):
        self.widgetsColor = colors
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.widgetsColor[1]};
            }}
        """)

    def set_language(self, language):
        self.widgetsLanguage = language

    def update_session_time(self):
        self.session_time += 1

    def saveSessionTime(self):
        """
        Зберігає тривалість сесії, додаючи її до останнього запису сесії за поточною датою.
        Шукає останню сесію за максимальним session_id для поточної дати і додає
        self.session_time до session_length без перевірки, чи нове значення більше.
        """
        try:
            # Зупинка таймера
            self.session_timer.stop()

            # Форматування часу у зручний вигляд (години:хвилини:секунди)
            hours = self.session_time // 3600
            minutes = (self.session_time % 3600) // 60
            seconds = self.session_time % 60
            session_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            print(f"Ваша сесія тривала: {session_str}")

            # Перевірка з'єднання
            if self.connection is None:
                print("Помилка: з'єднання з базою даних не встановлено.")
                return

            # Створення курсора
            cursor = self.connection.cursor()

            # Отримання поточної дати у форматі 'YYYY-MM-DD'
            current_date = datetime.now().strftime('%Y-%m-%d')

            # Пошук останньої сесії за поточною датою (максимальний session_id)
            cursor.execute(
                "SELECT session_id, session_length FROM Sessions WHERE login_date = ? ORDER BY session_id DESC LIMIT 1",
                (current_date,)
            )
            session = cursor.fetchone()

            if not session:
                print(f"Сесія за {current_date} не знайдена.")
                return

            session_id, current_session_length = session

            # Додавання нової тривалості до поточної
            new_session_length = current_session_length + self.session_time

            # Оновлення тривалості сесії
            cursor.execute(
                "UPDATE Sessions SET session_length = ? WHERE session_id = ?",
                (new_session_length, session_id)
            )
            self.connection.commit()
            print(f"Тривалість сесії за {current_date} оновлено до {new_session_length} секунд.")

        except Exception as e:
            print(f"Помилка при збереженні тривалості сесії: {e}")