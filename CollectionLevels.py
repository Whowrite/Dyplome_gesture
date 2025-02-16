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

def getlevelarray(card_name, current_game_level):
    if card_name == "Жести однією рукою":
        if current_game_level == "button_level_1" or current_game_level == "button_level_4":
            return [
                    [gesture_oke_right, gesture_oke_left, cv2.imread(f'FingerImages/gesture_oke.jpg')],
                    [gesture_peace_right, gesture_peace_left, cv2.imread(f'FingerImages/gesture_peace.jpg')],
                    [gesture_wait_right, gesture_wait_left, cv2.imread(f'FingerImages/gesture_wait.jpg')]
            ]
        elif current_game_level == "button_level_2" or current_game_level == "button_level_5":
            return [
                    [gesture_peace_right, gesture_peace_left, cv2.imread(f'FingerImages/gesture_peace.jpg')],
                    [gesture_little_bit_right, gesture_little_bit_left, cv2.imread(f'FingerImages/gesture_little_bit.jpg')],
                    [gesture_jumbo_right, gesture_jumbo_left, cv2.imread(f'FingerImages/gesture_jumbo.jpg')],
                    [gesture_butt_right, gesture_butt_left, cv2.imread(f'FingerImages/gesture_butt.jpg')],
                    [gesture_wait_right, gesture_wait_left, cv2.imread(f'FingerImages/gesture_wait.jpg')]
            ]
        else:
            return [
                    [gesture_butt_right, gesture_butt_left, cv2.imread(f'FingerImages/gesture_butt.jpg')],
                    [gesture_oke_right, gesture_oke_left, cv2.imread(f'FingerImages/gesture_oke.jpg')],
                    [gesture_wait_right, gesture_wait_left, cv2.imread(f'FingerImages/gesture_wait.jpg')],
                    [gesture_jumbo_right, gesture_jumbo_left, cv2.imread(f'FingerImages/gesture_jumbo.jpg')],
                    [gesture_little_bit_right, gesture_little_bit_left, cv2.imread(f'FingerImages/gesture_little_bit.jpg')],
                    [gesture_fingers_crossed_right, gesture_fingers_crossed_left, cv2.imread(f'FingerImages/gesture_fingers_crossed.jpg')],
                    [gesture_peace_right, gesture_peace_left, cv2.imread(f'FingerImages/gesture_peace.jpg')]
            ]
    elif card_name == "Жести двума руками":
        if current_game_level == "button_level_1" or current_game_level == "button_level_4":
            return [
                    [both_gesture_heart_right, both_gesture_heart_left, cv2.imread(f'FingerImages/both_gesture_heart.jpg')],
                    [both_gesture_uwu_right, both_gesture_uwu_left, cv2.imread(f'FingerImages/both_gesture_uwu.jpg')],
                    [both_gesture_camera_right, both_gesture_camera_left, cv2.imread(f'FingerImages/both_gesture_camera.jpg')]
            ]
        elif current_game_level == "button_level_2" or current_game_level == "button_level_5":
            return
        else:
            return
    elif card_name == "Міміка обличчя":
        if current_game_level == "button_level_1" or current_game_level == "button_level_4":
            return
        elif current_game_level == "button_level_2" or current_game_level == "button_level_5":
            return
        else:
            return