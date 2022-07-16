import mediapipe as mp
import cv2

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

def recognise(img,dep):
    result = hands.process(img)
    finger_xy = []
    finger_dep = []
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmarks.landmark):
                if (id in (4,8,12,16,20)):
                    pos_x = int(lm.x*480)
                    pos_y = int(lm.y*640)
                    finger_dep[int(id/4 - 1)] = dep[pos_x][pos_y]
                    # TODO cv2.circle(dep,(int(lm.x*640),int(lm.y*480)),5,(0,0,255),5)             
                    finger_xy[int(id/4 -1)] = (pos_x,pos_y)
        return finger_xy,finger_dep
    else:
        return None,None
        

def draw(img,dep,finger_xy):
    for finger in finger_xy:
        cv2.circle(dep,(int(finger[0]*640),int(finger[1]*480)),5,(0,0,255),5)
        cv2.circle(img,(int(finger[0]*640),int(finger[1]*480)),5,(0,0,255),5)
    return img,dep


def detect(finger_xy,finger_dep,screen,thresh=100):
    finger_dep = [screen-i for i in finger_dep]
    clicks = []
    for num,dep in enumerate(finger_dep):
        if dep<thresh:
            clicks.append(finger_xy[num])
    return clicks
    

