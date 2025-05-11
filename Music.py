import pygame
import os

class Music:
    def __init__(self):
        # Ініціалізація pygame для роботи з музикою
        pygame.mixer.init()

        # Шлях до єдиного треку
        self.track = "Musics/music1.mp3"
        self.is_playing = False  # Статус відтворення
        self.volume = 0.3  # Початкова гучність (0.0 до 1.0)

        # Встановлюємо початкову гучність
        pygame.mixer.music.set_volume(self.volume)

    def play_music(self):
        """Починає відтворення треку"""
        try:
            if not self.is_playing:
                # print(f"Спроба відтворення треку: {self.track}")
                # Перевіряємо, чи файл існує
                if not os.path.exists(self.track):
                    print(f"Файл {self.track} не знайдено")
                    return
                self.is_playing = True
                # Очищаємо стан pygame.mixer
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                # Завантажуємо та відтворюємо трек
                pygame.mixer.music.load(self.track)
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play()
                # print(f"Трек {self.track} відтворюється")
        except Exception as e:
            print(f"Помилка відтворення треку {self.track}: {e}")
            self.is_playing = False

    def stop_music(self):
        """Зупиняє музику"""
        # print("Зупинка музики")
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        self.is_playing = False