
# <b>Desktopography</b>
This is official repository of Desktopography, a summer project under Electronics Club.

## Overview
In this project, we have tried to implement touch-detection on projections created using a projector on any flat surface. The idea is to use depth feed of `Intel RealSense D435i`, a stereo vision based depth sensing camera, to detect the closeness of finger to the surface on which the projection is created.

We have utilized `MediaPipe`, a light-weight ML based model to detect positions of various landmarks of hand in the RGB image, and exploiting the change in depth of pixel where the index finger is located, we conclude if a touch has been made.

Further using a mapping generated on the basis of size and origin of detected projection in the RGB feed, we guide the computer to click at a specific spot.

To know in detail, consult the documentary of the project.

## Installation
To install the packeges for intelrealsense use this [link](https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md)

Further install python wrapper for `pyrealsense2` using the commands given [here](https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python#installation)

After successfully following the above 2 steps, run the following command to install other necessary libraries used in the project-

`pip install -r requirements.txt`  

You're all set now to go to run the [main.py](./hands_detection/screens.py)

Follow the open-source [pyrealsense2](https://dev.intelrealsense.com/docs/python2) documentation for other functions implemented using RealSense cameras.
