import numpy as np
import cv2

gesture_oke_right = np.array([[4, 260, 332], [8, 255, 316], [12, 241, 218], [16, 195, 199], [20, 144, 204]])
gesture_oke_left = np.array([[4, 286, 351], [8, 283, 330], [12, 274, 244], [16, 311, 196], [20, 378, 176]])

gesture_butt_right = np.array([[4, 262, 216], [8, 278, 306], [12, 251, 335], [16, 215, 345], [20, 179, 345]])
gesture_butt_left = np.array([[4, 393, 221], [8, 388, 296], [12, 421, 319], [16, 452, 345], [20, 488, 353]])

gesture_jumbo_right = np.array([[4, 416, 374], [8, 293, 383], [12, 260, 390], [16, 233, 376], [20, 243, 177]])
gesture_jumbo_left = np.array([[4, 223, 337], [8, 337, 358], [12, 362, 368], [16, 379, 359], [20, 423, 195]])

gesture_fingers_crossed_right = np.array([[4, 239, 326], [8, 252, 216], [12, 273, 209], [16, 216, 398], [20, 199, 417]])
gesture_fingers_crossed_left = np.array([[4, 247, 307], [8, 209, 198], [12, 194, 181], [16, 274, 394], [20, 306, 406]])

gesture_little_bit_right = np.array([[4, 337, 325], [8, 340, 254], [12, 221, 334], [16, 193, 335], [20, 175, 327]])
gesture_little_bit_left = np.array([[4, 239, 348], [8, 227, 273], [12, 376, 345], [16, 394, 346], [20, 411, 345]])

gesture_wait_right = np.array([[4, 291, 329], [8, 264, 198], [12, 226, 207], [16, 178, 216], [20, 120, 257]])
gesture_wait_left = np.array([[4, 210, 306], [8, 231, 209], [12, 254, 185], [16, 282, 197], [20, 309, 230]])

gesture_peace_right = np.array([[4, 184, 314], [8, 268, 180], [12, 221, 153], [16, 190, 384], [20, 165, 402]])
gesture_peace_left = np.array([[4, 360, 313], [8, 285, 201], [12, 344, 178], [16, 351, 375], [20, 371, 390]])

both_gesture_heart_left = np.array([[4, 313, 351], [4, 295, 359], [8, 314, 262], [8, 318, 270], [12, 315, 265], [12, 316, 264], [16, 317, 268], [16, 310, 267], [20, 323, 263], [20, 300, 278]])
both_gesture_heart_right = np.array([[4, 295, 359], [4, 313, 351], [8, 318, 270], [8, 314, 262], [12, 316, 264], [12, 315, 265], [16, 310, 267], [16, 317, 268], [20, 300, 278], [20, 323, 263]])

both_gesture_request_left = np.array([[4, 450, 279], [4, 143, 257], [8, 347, 180], [8, 198, 174], [12, 322, 174], [12, 227, 163], [16, 303, 182], [16, 247, 172], [20, 286, 203], [20, 264, 206]])
both_gesture_request_right = np.array([[4, 143, 257], [4, 450, 279], [8, 198, 174], [8, 347, 180], [12, 227, 163], [12, 322, 174], [16, 247, 172], [16, 303, 182], [20, 264, 206], [20, 286, 203]])

both_gesture_uwu_left = np.array([[4, 183, 277], [4, 421, 235], [8, 282, 367], [8, 300, 362], [12, 170, 375], [12, 414, 353], [16, 160, 402], [16, 423, 376], [20, 153, 424], [20, 431, 397]])
both_gesture_uwu_right = np.array([[4, 421, 235], [4, 183, 277], [8, 300, 362], [8, 282, 367], [12, 414, 353], [12, 170, 375], [16, 423, 376], [16, 160, 402], [20, 431, 397], [20, 153, 424]])

both_gesture_camera_right = np.array([[4, 282, 258], [4, 417, 215], [8, 418, 170], [8, 256, 300], [12, 249, 137], [12, 381, 326], [16, 240, 121], [16, 384, 354], [20, 256, 100], [20, 392, 380]])
both_gesture_camera_left = np.array([[4, 417, 215], [4, 282, 258], [8, 256, 300], [8, 418, 170], [12, 381, 326], [12, 249, 137], [16, 384, 354], [16, 240, 121], [20, 392, 380], [20, 256, 100]])

both_gesture_tutupapa_left = np.array([[4, 152, 264], [4, 322, 167], [8, 34, 320], [8, 188, 109], [12, 19, 357], [12, 141, 124], [16, 26, 387], [16, 118, 163], [20, 51, 420], [20, 116, 211]])
both_gesture_tutupapa_right = np.array([[4, 322, 167], [4, 152, 264], [8, 188, 109], [8, 34, 320], [12, 141, 124], [12, 19, 357], [16, 118, 163], [16, 26, 387], [20, 116, 211], [20, 51, 420]])

both_gesture_doubleoke_left = np.array([[4, 246, 263], [4, 277, 255], [8, 267, 242], [8, 244, 280], [12, 326, 171], [12, 166, 316], [16, 318, 102], [16, 146, 381], [20, 261, 50], [20, 160, 428]])
both_gesture_doubleoke_right = np.array([[4, 277, 255], [4, 246, 263], [8, 244, 280], [8, 267, 242], [12, 166, 316], [12, 326, 171], [16, 146, 381], [16, 318, 102], [20, 160, 428], [20, 261, 50]])

both_gesture_school_left = np.array([[4, 290, 338], [4, 336, 331], [8, 289, 205], [8, 351, 205], [12, 195, 317], [12, 445, 313], [16, 169, 322], [16, 473, 316], [20, 152, 321], [20, 488, 313]])
both_gesture_school_right = np.array([[4, 336, 331], [4, 290, 338], [8, 351, 205], [8, 289, 205], [12, 445, 313], [12, 195, 317], [16, 473, 316], [16, 169, 322], [20, 488, 313], [20, 152, 321]])

# Словник для зіставлення назв файлів із жестами
gesture_map = {
    'gesture_oke.png': [gesture_oke_right, gesture_oke_left],
    'gesture_peace.png': [gesture_peace_right, gesture_peace_left],
    'gesture_wait.png': [gesture_wait_right, gesture_wait_left],
    'gesture_butt.png': [gesture_butt_right, gesture_butt_left],
    'gesture_jumbo.png': [gesture_jumbo_right, gesture_jumbo_left],
    'gesture_fingers_crossed.png': [gesture_fingers_crossed_right, gesture_fingers_crossed_left],
    'gesture_little_bit.png': [gesture_little_bit_right, gesture_little_bit_left],
    'both_gesture_heart.png': [both_gesture_heart_right, both_gesture_heart_left],
    'both_gesture_uwu.png': [both_gesture_uwu_right, both_gesture_uwu_left],
    'both_gesture_camera.png': [both_gesture_camera_right, both_gesture_camera_left],
    'both_gesture_tutupapa.png': [both_gesture_tutupapa_right, both_gesture_tutupapa_left],
    'both_gesture_request.png': [both_gesture_request_right, both_gesture_request_left],
    'both_gesture_doubleoke.png': [both_gesture_doubleoke_right, both_gesture_doubleoke_left],
    'both_gesture_school.png': [both_gesture_school_right, both_gesture_school_left]
}

oneHandGestures_list = {
    'FingerImages/gesture_oke.png',
    'FingerImages/gesture_peace.png',
    'FingerImages/gesture_wait.png',
    'FingerImages/gesture_butt.png',
    'FingerImages/gesture_jumbo.png',
    'FingerImages/gesture_fingers_crossed.png',
    'FingerImages/gesture_little_bit.png'
}

twoHandGestures_list = {
    'FingerImages/both_gesture_heart.png',
    'FingerImages/both_gesture_uwu.png',
    'FingerImages/both_gesture_camera.png',
    'FingerImages/both_gesture_tutupapa.png',
    'FingerImages/both_gesture_request.png',
    'FingerImages/both_gesture_doubleoke.png',
    'FingerImages/both_gesture_school.png'
}

def getlevelarray(card_name, current_game_level):
    if card_name == "Жести однією рукою":
        if current_game_level == "button_level_1" or current_game_level == "button_level_4":
            return [
                    [gesture_oke_right, gesture_oke_left, 'FingerImages/gesture_oke.png'],
                    [gesture_peace_right, gesture_peace_left, 'FingerImages/gesture_peace.png'],
                    [gesture_wait_right, gesture_wait_left, 'FingerImages/gesture_wait.png']
            ]
        elif current_game_level == "button_level_2" or current_game_level == "button_level_5":
            return [
                    [gesture_peace_right, gesture_peace_left, 'FingerImages/gesture_peace.png'],
                    [gesture_little_bit_right, gesture_little_bit_left, 'FingerImages/gesture_little_bit.png'],
                    [gesture_jumbo_right, gesture_jumbo_left, 'FingerImages/gesture_jumbo.png'],
                    [gesture_butt_right, gesture_butt_left, 'FingerImages/gesture_butt.png'],
                    [gesture_wait_right, gesture_wait_left, 'FingerImages/gesture_wait.png']
            ]
        else:
            return [
                    [gesture_butt_right, gesture_butt_left, 'FingerImages/gesture_butt.png'],
                    [gesture_oke_right, gesture_oke_left, 'FingerImages/gesture_oke.png'],
                    [gesture_wait_right, gesture_wait_left, 'FingerImages/gesture_wait.png'],
                    [gesture_jumbo_right, gesture_jumbo_left, 'FingerImages/gesture_jumbo.png'],
                    [gesture_little_bit_right, gesture_little_bit_left, 'FingerImages/gesture_little_bit.png'],
                    [gesture_fingers_crossed_right, gesture_fingers_crossed_left, 'FingerImages/gesture_fingers_crossed.png'],
                    [gesture_peace_right, gesture_peace_left, 'FingerImages/gesture_peace.png']
            ]
    elif card_name == "Жести двума руками":
        if current_game_level == "button_level_1" or current_game_level == "button_level_4":
            return [
                    [both_gesture_heart_right, both_gesture_heart_left, 'FingerImages/both_gesture_heart.png'],
                    [both_gesture_uwu_right, both_gesture_uwu_left, 'FingerImages/both_gesture_uwu.png'],
                    [both_gesture_camera_right, both_gesture_camera_left, 'FingerImages/both_gesture_camera.png']
            ]
        elif current_game_level == "button_level_2" or current_game_level == "button_level_5":
            return [
                    [both_gesture_tutupapa_right, both_gesture_tutupapa_left, 'FingerImages/both_gesture_tutupapa.png'],
                    [both_gesture_request_right, both_gesture_request_left, 'FingerImages/both_gesture_request.png'],
                    [both_gesture_heart_right, both_gesture_heart_left, 'FingerImages/both_gesture_heart.png'],
                    [both_gesture_doubleoke_right, both_gesture_doubleoke_left, 'FingerImages/both_gesture_doubleoke.png'],
                    [both_gesture_uwu_right, both_gesture_uwu_left, 'FingerImages/both_gesture_uwu.png']
            ]
        else:
            return [
                    [both_gesture_school_right, both_gesture_school_left, 'FingerImages/both_gesture_school.png'],
                    [both_gesture_tutupapa_right, both_gesture_tutupapa_left, 'FingerImages/both_gesture_tutupapa.png'],
                    [both_gesture_camera_right, both_gesture_camera_left, 'FingerImages/both_gesture_camera.png'],
                    [both_gesture_uwu_right, both_gesture_uwu_left, 'FingerImages/both_gesture_uwu.png'],
                    [both_gesture_doubleoke_right, both_gesture_doubleoke_left, 'FingerImages/both_gesture_doubleoke.png'],
                    [both_gesture_heart_right, both_gesture_heart_left, 'FingerImages/both_gesture_heart.png'],
                    [both_gesture_request_right, both_gesture_request_left, 'FingerImages/both_gesture_request.png']
            ]

def getUserLevelArray(numberTasks, UserGestures):
    UserLevelMassive = []
    for i in range(numberTasks):
        # Отримуємо шлях до файлу жесту
        gesture_path = UserGestures[i]
        # Витягуємо ім'я файлу з шляху
        gesture_filename = gesture_path.split('/')[-1]
        # Отримуємо відповідні масиви жестів зі словника
        if gesture_filename in gesture_map:
            right_gesture, left_gesture = gesture_map[gesture_filename]
            # Додаємо масив [right_gesture, left_gesture, зображення] до результату
            UserLevelMassive.append([right_gesture, left_gesture, gesture_path])
        else:
            # Якщо жест не знайдено, можна додати порожній список або підняти помилку
            UserLevelMassive.append([])

    return UserLevelMassive