import sys
import mediapipe as mp
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QPushButton, QScrollArea, QFrame, QHBoxLayout, \
    QGraphicsOpacityEffect
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import QTimer, Qt
from functools import partial
import LelelCounting, SettingsModule, RebuildsComponents

current_game_level = "Undefined123"

def mainWindow():
    app = QApplication(sys.argv)
    window = QMainWindow()

    window.setWindowTitle("Window")
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
    button_settings.setGeometry(48, 23, 215, 55)
    button_settings.setText("⚙️Settings")

    font = QFont()
    font.setBold(True)
    font.setPointSize(18)
    button_settings.setFont(font)

    button_settings.setStyleSheet("""
            QPushButton {
                background-color: #9EFFA5; /* Колір кнопки */
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

    settingsModule = SettingsModule.SettingsModule()

    # Підключення сигналу "clicked" до обробника
    button_settings.clicked.connect(lambda: settingsModule.show_settings(settings_frame, unvisible_frame))

    # ------------------------------------------------------------------------------------------------------------------Назва програми

    title_window = QLabel(window)
    title_window.setGeometry(568, 23, 330, 55)
    title_window.setText("ToTrainYourNeurons")

    font = QFont()
    font.setBold(True)
    font.setPointSize(18)
    title_window.setFont(font)

    title_window.setFrameShape(QLabel.StyledPanel)
    title_window.setFrameShadow(QLabel.Plain)
    title_window.setAlignment(Qt.AlignCenter)
    title_window.setStyleSheet("""
            QLabel {
                background-color: #9EFFA5; /* Колір фону */
                color: black; /* Колір тексту */
                border-radius: 10px; /* Закруглення кутів */
            }
        """)

    # ------------------------------------------------------------------------------------------------------------------Кнопка Довідки

    button_help = QPushButton(window)
    button_help.setGeometry(1206, 18, 60, 60)
    button_help.setText("?")

    font = QFont()
    font.setBold(True)
    font.setPointSize(18)
    button_help.setFont(font)

    button_help.setStyleSheet("""
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

    # ------------------------------------------------------------------------------------------------------------------Фрейм вибірки рівня

    select_Level = QFrame(window)
    select_Level.setGeometry(0, 0, 1315, 917)
    select_Level.hide()
    select_Level.setStyleSheet("""
                QFrame {
                    background-color: #9EFFA5; /* Фон картки */
                    border-radius: 10px; /* Закруглені кути */
                }
            """)

    # ------------------------------------------------------------------------------------------------------------------Фрейм з картками для вибору режиму тренування

    level_checking = QScrollArea(window)
    level_checking.setGeometry(48, 90, 1216, 800)

    level_checking.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # Горизонтальна прокрутка
    level_checking.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Відключення вертикальної прокрутки

    # Контейнер для вмісту
    content_widget = QWidget()
    layout = QHBoxLayout(content_widget)  # Горизонтальне розташування
    layout.setContentsMargins(10, 10, 10, 10)  # Відступи між елементами
    layout.setSpacing(30)  # Проміжки між картками

    titles_cards = ["Жести однією рукою", "Жести двума руками", "Міміка обличчя", "Користувацький рівень"]
    text_cards = ["💡 Мета: Ознайомлення з базовими жестами, такими як вказування, махання, показування знаків.",

                  "💡 Мета: Вивчення жестів для взаємодії з великими об'єктами, передачі складних команд або вираження емоцій.",

                  "💡 Мета: Навчання розпізнаванню ключових емоцій, таких як радість, здивування, гнів і сум.\n",

                  "💡 Мета: Дати можливість користувачам створювати унікальні жести чи міміку для персональних сценаріїв."]
    images_cards = ["FingerImages/1.jpg", "FingerImages/2.jpg", "FingerImages/3.jpg", "FingerImages/4.jpg"]

    # Додавання "карток" у контейнер
    for i in range(4):  # 4 карток
        card = create_card(titles_cards[i], text_cards[i], images_cards[i])

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
        button_start.clicked.connect(partial(visible_select_level_click, select_Level, title_window, button_help, card))

        # --------------------------------------------------------------------------------------------------------------Кінець картки
        layout.addWidget(card)  # Додаємо картку у макет

    # Встановлення контейнера у QScrollArea
    content_widget.setLayout(layout)
    level_checking.setWidget(content_widget)
    level_checking.setWidgetResizable(True)  # Адаптація розміру контейнера до QScrollArea

    level_checking.setStyleSheet("""
    QScrollArea {
        border: none; /* Забрати рамку, якщо потрібне чисте тло */
        background-color: #DAFFDF; /* Колір фону */
    }
    """)

    # ------------------------------------------------------------------------------------------------------------------Кінець Фрейм з картками для вибору режиму тренування

    # Підняття елементів на інші поверхи
    select_Level.raise_()
    title_window.raise_()
    button_help.raise_()
    unvisible_frame.raise_()
    settings_frame.raise_()

    # ------------------------------------------------------------------------------------------------------------------Закриття програми
    window.show()
    sys.exit(app.exec_())

#Функція-обробник кнопки для відображення компонентів фрейму вибірки рівня
def visible_select_level_click(select_Level, title_window, button_help, card):
    select_Level.show()
    title_window.setStyleSheet("""
                QLabel {
                    background-color: #DAFFDF; /* Колір фону */
                    color: black; /* Колір тексту */
                    border-radius: 10px; /* Закруглення кутів */
                }
            """)
    button_help.setStyleSheet("""
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

    duplicate_card_to_frame(card, select_Level)

    # ------------------------------------------------------------------------------------------------------------------Кнопка для повернення на головну сторінку

    button_return = QPushButton(select_Level)
    button_return.setGeometry(48, 23, 60, 60)
    button_return.setText("<-")
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
    button_return.clicked.connect(
        partial(hide_select_level_click, select_Level, title_window, button_help))

    # ------------------------------------------------------------------------------------------------------------------Фрейм для відображення рівнів

    levels = QFrame(select_Level)
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

    show_levels_buttons(levels, 40, 1, level_status)
    show_levels_buttons(levels, 260, 4, level_status)

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

    best_try_level_num= QLabel(level_status)
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

    level_cv_frame = QFrame(select_Level)
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
        current_game_level, card.objectName(), level_cv_frame))

    # ------------------------------------------------------------------------------------------------------------------

# Функція-обробник кнопки для приховання компонентів фрейму вибірки рівня
def hide_select_level_click(select_Level, title_window, button_help):
    print("Кнопку натиснуто!")
    select_Level.hide()
    title_window.setStyleSheet("""
                QLabel {
                    background-color: #9EFFA5; /* Колір фону */
                    color: black; /* Колір тексту */
                    border-radius: 10px; /* Закруглення кутів */
                }
            """)
    button_help.setStyleSheet("""
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

#Функція для створення картки виду вправ
def create_card(title_text, description_text, image_path, parent=None):
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
    image_label.setGeometry(70, 90 + 100, 250, 170)
    pixmap = QPixmap(image_path)
    image_label.setPixmap(pixmap)
    image_label.setScaledContents(True)
    image_label.setObjectName("image_label")  # Задання імені

    return card

#Функція для створення дублікату картки виду вправ
def duplicate_card_to_frame(card, target_frame):
    # Отримуємо текст і параметри оригінальної картки за назвою об'єкта
    title_label = card.findChild(QLabel, "title_label")
    description_label = card.findChild(QLabel, "description_label")
    image_label = card.findChild(QLabel, "image_label")

    # Зчитуємо дані
    title_text = title_label.text() if title_label else ""
    description_text = description_label.text() if description_label else ""
    pixmap = image_label.pixmap() if image_label else None

    # Створюємо дубльовану картку
    duplicated_card = create_card(title_text, description_text, pixmap, target_frame)

    # Встановлюємо позицію дубліката
    duplicated_card.setGeometry(45, 100, 378, 750)  # Задайте позицію вручну або автоматично
    duplicated_card.show()

#Функція для відображення рівнів 1-6 у фреймі вибірки рівня (див. visible_select_level_click() )
def show_levels_buttons(levels, stepY, num, level_status):
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
        button_level.clicked.connect(partial(select_level_click, button_level, level_status))

        textForLevels = QLabel(button_level)
        textForLevels.setGeometry(68, 3, 200, 50)
        textForLevels.setText("Рівень " + str(num))
        textForLevels.setStyleSheet("background-color: none; font-size: 15px; font-weight: bold;")
        textForLevels.show()
        num += 1

#Функція-обробник кнопки для відображення інфо проходження рівня (див. show_levels_buttons() )
def select_level_click(current_button_level, level_status):
    global current_game_level  # Оголосіть змінну глобально
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
        current_game_level = current_button_level.objectName()
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
        current_game_level = "Undefined"

if __name__ == "__main__":
    mainWindow()