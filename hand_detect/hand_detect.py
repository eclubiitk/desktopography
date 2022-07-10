import numpy as np
import mediapipe as mp
import cv2

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

def hand_found(color):
    results = hands.process(color)
    return results.multi_hand_landmarks

def find_hand(result_obj,depths,coords):
    for hand_landmarks in result_obj.multi_hand_landmarks:
        for id, lm in enumerate(hand_landmarks.landmark):
            if (id in (4,8,12,16,20)):                    #index finger
                pos_x = int(lm.x*480)
                pos_y = int(lm.y*640)
                # cv2.circle(depth_image,(int(lm.x*640),int(lm.y*480)),5,(0,0,255),5)                 #index finger
                # depths[id/4 - 1] = depth_image[pos_x][pos_y]
                coords[id/4 -1] = (pos_x,pos_y)
                # if not(ref_dep):
                #     ref_dep = img_grey[240][320]
        # FINGER_TO_SCR = [FINGER_DEP[x]-SCREEN_DEP for x in range(5)]