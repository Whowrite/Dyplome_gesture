import tkinter as tk
from tkinter import messagebox
import pygame
import threading

# Ініціалізація pygame для роботи з музикою
pygame.mixer.init()

def play_music():
    """Функція для програвання музики у фоні"""
    pygame.mixer.music.load("music1.mp3")  # Вкажіть шлях до вашого файлу
    pygame.mixer.music.play(-1)  # -1 означає повторювати трек нескінченно

def stop_music():
    """Зупинити музику"""
    pygame.mixer.music.stop()

def on_close():
    """Закриття програми з очищенням ресурсів"""
    stop_music()
    root.destroy()

# Створення головного вікна Tkinter
root = tk.Tk()
root.title("Додаток з музикою")
root.geometry("400x300")

# Додавання кнопок
play_button = tk.Button(root, text="Запустити музику", command=lambda: threading.Thread(target=play_music).start())
play_button.pack(pady=10)

stop_button = tk.Button(root, text="Зупинити музику", command=stop_music)
stop_button.pack(pady=10)

exit_button = tk.Button(root, text="Вийти", command=on_close)
exit_button.pack(pady=10)

# Обробка закриття вікна
root.protocol("WM_DELETE_WINDOW", on_close)

# Запуск програми
root.mainloop()
