import time
import os
import cv2
import mediapipe as mp
import numpy as np
import CollectionLevels as cl

class handDetector():
    def __init__(self, right_gest = cl.gesture_oke_right, left_gest = cl.gesture_oke_left, mode=False, hands=2, detectionCon=0.75, trackCon=0.5):
        self.mode = mode
        self.hands = hands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        folderPath = "FingerImages"
        myList = os.listdir(folderPath)
        self.overlayList = []
        for imPath in myList:
            image = cv2.imread(f'{folderPath}/{imPath}')
            self.overlayList.append(image)

        # Инициализация Mediapipe Hands
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.hands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

        self.gesture_right = right_gest
        self.gesture_left = left_gest

    def findHands(self, img, Draw=True):
        # Конвертация BGR в RGB (Mediapipe ожидает RGB)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Обработка изображения
        self.result = self.hands.process(imgRGB)
        # Проверка, найдены ли руки
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if Draw:  # Рисуем линии и точки
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, Draw=True):
        lmList = []
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if Draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        return lmList

    def findPositionsBothHands(self, img, Draw=True):
        hands_positions = []  # Список для зберігання точок обох рук

        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                lmList = []
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])

                    if Draw:
                        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

                hands_positions.append(lmList)  # Додаємо координати поточної руки

        return hands_positions  # Повертає список списків, де кожен список — це точки однієї руки

    #-------------------------------------------------------------------------------------------------------------------Вирахоовує кількість піднятих пальців
    def fingerUpCount(self, lmList):
        tipIds = [4, 8, 12, 16, 20]
        if len(lmList) != 0:
            fingers = []

            # Великий палець правої руки
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # 4 пальці правої руки
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            # print(fingers)
            totalFingers = fingers.count(1)
            return totalFingers
        else: return 0

    #-------------------------------------------------------------------------------------------------------------------Порівнює кількість піднятих пальців з числом
    def fingerUpCount_withId(self, frame, id):
        lmList = self.findPosition(frame, draw=False)
        h, w, c = self.overlayList[id - 1].shape
        frame[0:h, 0:w] = self.overlayList[id - 1]
        totalFingersUp = self.fingerUpCount(lmList)
        if totalFingersUp == id:
            return True
        else: return False

    #-------------------------------------------------------------------------------------------------------------------Знаходить потрібні точки за їхніми ID з lmList
    def extractPoints(self, lmList, pointIds):
        """
        Знаходить потрібні точки за їхніми ID з lmList.

        :param lmList: Список всіх точок руки.
        :param pointIds: Список ID точок, які потрібно знайти.
        :return: Тимчасовий масив з потрібними точками.
        """
        tempArray = []
        for pointId in pointIds:
            for lm in lmList:
                if lm[0] == pointId:  # Якщо ID співпадає
                    tempArray.append(lm)
                    break
        return tempArray

    def extractPointsBothHands(self, lmList, pointIds):
        """
        Знаходить потрібні точки за їхніми ID з lmList.

        :param lmList: Список всіх точок руки.
        :param pointIds: Список ID точок, які потрібно знайти.
        :return: Тимчасовий масив з потрібними точками.
        """
        tempArray = []
        for pointId in pointIds:
            for lm in lmList[0]:
                if lm[0] == pointId:  # Якщо ID співпадає
                    tempArray.append(lm)
                    break
            for lm in lmList[1]:
                if lm[0] == pointId:  # Якщо ID співпадає
                    tempArray.append(lm)
                    break
        return tempArray

    def setGesture(self, leftGesture, rightGesture):
        self.gesture_right = rightGesture
        self.gesture_left = leftGesture

    def moveXY(self, x, y):
        for i in range(len(self.gesture_right)):
            self.gesture_right[i][1] -= x
            self.gesture_right[i][2] -= y

    def moveXY_left(self, x, y):
        for i in range(len(self.gesture_left)):
            self.gesture_left[i][1] -= x
            self.gesture_left[i][2] -= y

    def compareGestures(self, tempArray):
        """
        Порівнює масив self.gesture_right із тимчасовим масивом точок tempArray.

        :param tempArray: Масив точок для порівняння.
        """

        x = self.gesture_right[0][1] - tempArray[0][1]
        y = self.gesture_right[0][2] - tempArray[0][2]

        self.moveXY(x, y)

        x = self.gesture_left[0][1] - tempArray[0][1]
        y = self.gesture_left[0][2] - tempArray[0][2]

        self.moveXY_left(x, y)

        if len(tempArray) == len(self.gesture_right):
            matches = True
            for i in range(len(self.gesture_right)):
                if tempArray[i][0] == self.gesture_right[i][0] and \
                        abs(tempArray[i][1] - self.gesture_right[i][1]) < 50 and \
                        abs(tempArray[i][2] - self.gesture_right[i][2]) < 50:  # Додаємо допустиму похибку
                    continue
                elif tempArray[i][0] == self.gesture_left[i][0] and \
                        abs(tempArray[i][1] - self.gesture_left[i][1]) < 50 and \
                        abs(tempArray[i][2] - self.gesture_left[i][2]) < 50:  # Додаємо допустиму похибку
                    continue
                else:
                    matches = False
                    break
            if matches:
                print("Жест повністю співпадає!")
                return True
            else:
                print("Жест не співпадає.")
                return False
        else:
            print("Розмір масивів не співпадає.")
            return False

def main():
    pTime = 0
    cTime = 0

    # Захват видео с камеры
    cap = cv2.VideoCapture(0)
    detector = handDetector(cl.both_gesture_school_right, cl.both_gesture_school_left)

    # Список точок, які потрібно знайти (IDs)
    targetPoints = [4, 8, 12, 16, 20]

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            print("Не удалось получить изображение с камеры.")
            break

        # Отримання зображення в RGB
        img = detector.findHands(img, Draw=False)

        lmLists = detector.findPositionsBothHands(img, Draw=False)

        if len(lmLists) == 2:
            # rightHand = lmLists[0]  # Перша рука (залежить від того, яку руку модель розпізнала першою)
            # leftHand = lmLists[1]  # Друга рука
            # print("Права рука:", rightHand)
            # print("Ліва рука:", leftHand)

            # Знаходимо потрібні точки
            tempArray = detector.extractPointsBothHands(lmLists, targetPoints)
            print(tempArray)
            # Порівнюємо з gesture_oke
            detector.compareGestures(tempArray)

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

if __name__ == "__main__":
    main()