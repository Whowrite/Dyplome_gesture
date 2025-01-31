import time
import cv2
import mediapipe as mp
import HandTModule as htm

pTime = 0
cTime = 0

# Захват видео с камеры
cap = cv2.VideoCapture(0)
detector = htm.handDetector()

while cap.isOpened():
    success, img = cap.read()
    if not success:
        print("Не удалось получить изображение с камеры.")
        break

    # Отримання зображення в RGB
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        print(lmList[4])

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    # Показ изображения
    cv2.imshow("Image", img)

    # Выход при нажатии "q"
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
