## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2017 Intel Corporation. All Rights Reserved.

#####################################################
##              Align Depth to Color               ##
#####################################################

# First import the library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
import mediapipe as mp
import math

# Import OpenCV for easy image rendering
import cv2
import scaler

# Global Vars
FINGER_DEP = [0,0,0,0,0]
FINGER_XY = [(0,0),(0,0),(0,0),(0,0),(0,0)]
FINGER_TO_SCR = [0,0,0,0,0]
SCREEN_DEP = 7800

# Create a pipeline
pipeline = rs.pipeline()

# Create a config and configure the pipeline to stream
#  different resolutions of color and depth streams
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("Color sensor not found")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: " , depth_scale)

# We will be removing the background of objects more than
#  clipping_distance_in_meters meters away
clipping_distance_in_meters = 8 #1 meter
clipping_distance = clipping_distance_in_meters / depth_scale

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Streaming loop
try:
    while True:
        # Get frameset of color and depth
        frames = pipeline.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image

        # Align the depth frame to color frame
        aligned_frames = align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        # print(depth_image.shape)
        color_image = np.asanyarray(color_frame.get_data())
        # print(color_image.shape)

        
        #my editing
        results = hands.process(color_image)
        # print(type(results))
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for id, lm in enumerate(hand_landmarks.landmark):
                    if (id in (4,8,12,16,20)):                    #index finger
                        pos_x = int(lm.x*480)
                        pos_y = int(lm.y*640)
                        FINGER_DEP[int(id/4 - 1)] = depth_image[pos_x][pos_y]
                        cv2.circle(depth_image,(int(lm.x*640),int(lm.y*480)),5,(0,0,255),5)                 #index finger
                        # if depth_image[pos_x][pos_y]:
                            # FINGER_DEP[int(id/4 - 1)] = 5000000
                        FINGER_XY[int(id/4 -1)] = (pos_x,pos_y)
                        # if not(ref_dep):
                        #     ref_dep = img_grey[240][320]
                FINGER_TO_SCR = [abs(FINGER_DEP[x]-SCREEN_DEP) for x in range(5)]
                print(FINGER_TO_SCR)
                mp_draw.draw_landmarks(color_image,hand_landmarks,mp_hands.HAND_CONNECTIONS)
                # mp_draw.draw_landmarks(depth_image,hand_landmarks,mp_hands.HAND_CONNECTIONS)
            for i,val in enumerate(FINGER_TO_SCR):
                if val<50:
                    print(f"CLICK AT {(FINGER_XY[i][0]/480,FINGER_XY[i][1]/640)}")
                    # scaler.coordinate(FINGER_XY[i][0]/480,FINGER_XY[i][1]/640)
            # print(FINGER_XY)
            # dif = abs(FINGER_DEP[1]-SCREEN_DEP)
            # print(f'Index Finger Depth: {FINGER_DEP[1]}, Screen Depth: {SCREEN_DEP}, Difference: {dif}')
        else:
            ratio = color_image.shape[0]/300
            orig = color_image.copy()
            # image = cv2.resize(color_image, (320,240), interpolation=cv2.INTER_LINEAR)
            greyed_image = cv2.cvtColor(color_image,cv2.COLOR_BGR2GRAY)
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
            
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

            if screenCnt is not None:
                cv2.drawContours(color_image,[screenCnt],-1,(0,255,0),3)
                cv2.drawContours(depth_colormap,[screenCnt],-1,(0,255,0),3)
                extLeft = tuple(screenCnt[screenCnt[:, :, 0].argmin()][0])[0]
                extRight = tuple(screenCnt[screenCnt[:, :, 0].argmax()][0])[0]
                extTop = tuple(screenCnt[screenCnt[:, :, 1].argmin()][0])[0]
                extBot = tuple(screenCnt[screenCnt[:, :, 1].argmax()][0])[0]
                # print(extRight)
                cx = int((0.5*(extLeft + extRight))*480/1000)
                cy = int((0.5*(extTop+extBot))*640/1000)
                dep = depth_image[cx][cy]
                if (dep!=0):
                    SCREEN_DEP = dep
                print(SCREEN_DEP)

        # Remove background - Set pixels further than clipping_distance to grey
        # grey_color = 153
        # depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
        # bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)

        # Render images:
        #   depth align to color on left
        #   depth on right
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        images = np.hstack((color_image, depth_colormap))

        cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
        cv2.imshow('Edges',edged_image)
        cv2.imshow('Align Example', images)
        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
finally:
    pipeline.stop()