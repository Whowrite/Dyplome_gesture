import time
import cv2
import mediapipe as mp
import numpy as np

# Захват видео с камеры
cap = cv2.VideoCapture(0)

# Инициализация Mediapipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=2,
                      min_tracking_confidence=0.5, min_detection_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while cap.isOpened():
    success, img = cap.read()
    if not success:
        print("Не удалось получить изображение с камеры.")
        break

    # Конвертация BGR в RGB (Mediapipe ожидает RGB)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Обработка изображения
    result = hands.process(imgRGB)

    # Проверка, найдены ли руки
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id, cx, cy)
                if id==4:
                    cv2.circle(img, (cx, cy), 25, (255,0,255), cv2.FILLED)
            # Рисуем линии и точки
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)),(10,70), cv2.FONT_HERSHEY_PLAIN,3, (255,0,255), 3)

    # Показ изображения
    cv2.imshow("Image", img)

    # Выход при нажатии "q"
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()