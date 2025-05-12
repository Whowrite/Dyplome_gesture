from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
import os
import sys


class Music:
    def __init__(self):
        # Ініціалізація QApplication (потрібно для QMediaPlayer)
        self.app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()

        # Ініціалізація QMediaPlayer
        self.player = QMediaPlayer()

        # Список із трьох треків
        self.tracks = [
            "Musics/music1.mp3",
            "Musics/music2.mp3",
            "Musics/music3.mp3"
        ]
        self.current_track_index = 0  # Індекс поточного треку
        self.is_playing = False  # Статус відтворення
        self.volume = 0.3  # Початкова гучність (0.0 до 1.0)

        # Встановлюємо початкову гучність (QMediaPlayer використовує діапазон 0-100)
        self.player.setVolume(int(self.volume * 100))

        # Підключаємо сигнал завершення треку
        self.player.mediaStatusChanged.connect(self.handle_media_status)

    def play_music(self):
        """Починає відтворення поточного треку"""
        try:
            if not self.is_playing:
                # Отримуємо поточний трек
                current_track = self.tracks[self.current_track_index]
                # Перевіряємо, чи файл існує
                if not os.path.exists(current_track):
                    print(f"Файл {current_track} не знайдено")
                    return
                self.is_playing = True
                # Зупиняємо попереднє відтворення, якщо є
                self.player.stop()
                # Завантажуємо трек
                self.player.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.abspath(current_track))))
                # Встановлюємо гучність
                self.player.setVolume(int(self.volume * 100))
                # Починаємо відтворення
                self.player.play()
                # print(f"Трек {current_track} відтворюється")
        except Exception as e:
            print(f"Помилка відтворення треку {current_track}: {e}")
            self.is_playing = False

    def stop_music(self):
        """Зупиняє музику"""
        # print("Зупинка музики")
        self.player.stop()
        self.is_playing = False

    def handle_media_status(self, status):
        """Обробляє зміну статусу медіа (наприклад, завершення треку)"""
        if status == QMediaPlayer.EndOfMedia:
            # Трек завершено, переходимо до наступного
            self.next_track()

    def next_track(self):
        """Переходить до наступного треку"""
        # Збільшуємо індекс треку (з циклічним поверненням до 0)
        self.current_track_index = (self.current_track_index + 1) % len(self.tracks)
        self.is_playing = False  # Скидаємо статус, щоб дозволити відтворення
        self.play_music()  # Відтворюємо наступний трек