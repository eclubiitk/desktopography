import pyautogui
import cv2


def bg_adjust(pos,screenEdges):
    '''Take the actual coordinates of the click and convert it to coordinates with respect to screen edges
    Input: pos - position of click, a tuple of integers (x,y)
    Output: new_pos - adjusted position of click, a tuple of integers (X,Y)'''
    # TODO

def clickat(coord):
    a,b = pyautogui.size()
    u=coord[0]*a
    v = coord[1]*b
    pyautogui.click(u,v)


def detect(img):
    '''Finds the edges of screen and returns coordinates
    Input: img - a frame of the color_image
    Output: screenEdges - list of two integer tuples for centre, left, right, top, bottom coordinates'''
    # TODO- DONE
    
    ratio = img.shape[0]/300
    orig = img.copy()
    # image = cv2.resize(color_image, (320,240), interpolation=cv2.INTER_LINEAR)
    greyed_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    greyed_image = cv2.bilateralFilter(greyed_image, 11, 17, 17)
    # ret2,otsu_img = cv2.threshold(greyed_image,127,255,cv2.THRESH_TRUNC+cv2.THRESH_OTSU)
    # otsu_img, otsu_cnts, hierarchy = cv2.findContours(otsu_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    edged_image = cv2.Canny(greyed_image,30,200)
    cnts = cv2.findContours(edged_image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#         for i in range(len(otsu_cnts)):
#             color_contours = (0, 255, 0) # green - color for contours
#             color = (255, 0, 0) # blue - color for convex hull
# # draw ith contour
#             cv2.drawContours(otsu_img, otsu_cnts, i, color_contours, 1, 8, hierarchy)

# # draw ith convex hull object

#             cv2.drawContours(otsu_img, hull, i, color, 1, 8)
    cnts = sorted(cnts[0], key = cv2.contourArea, reverse = True)[:10]
    screenCnt = None

    for c in cnts:
        peri = cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,0.015*peri, True)

        if len(approx)==4:
            screenCnt = approx
            break
    

    if screenCnt is not None:
        cv2.drawContours(img,[screenCnt],-1,(0,255,0),3)
        # cv2.drawContours(depth_colormap,[screenCnt],-1,(0,255,0),3)
        extLeft = tuple(screenCnt[screenCnt[:, :, 0].argmin()][0])[0]
        extRight = tuple(screenCnt[screenCnt[:, :, 0].argmax()][0])[0]
        extTop = tuple(screenCnt[screenCnt[:, :, 1].argmin()][0])[0]
        extBot = tuple(screenCnt[screenCnt[:, :, 1].argmax()][0])[0]
        # print(extRight)
        cx = int((0.5*(extLeft + extRight))*480/1000)
        cy = int((0.5*(extTop+extBot))*640/1000)
        left= (extLeft*480/1000,cy)
        right= (extRight*480/1000,cy)
        top= (cx,extTop*640/1000)
        bot= (cx,extBot*640/1000)
        center=(cx,cy)
        screenEdges = [center,left,right,top,bot]
        return screenEdges
