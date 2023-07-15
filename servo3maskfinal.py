import pyfirmata
import time
import asyncio
import random
import cv2
import numpy as np
from math import sqrt
import pickle

from function1 import scaled_output

port = 'COM3'

current1 = 160 #stable=160, limit=130
current2 = 155 #stable=155,  limit=125
ang1 = 160
ang2 = 155

# Limits of servo
servo1_min = 130
servo1_stable = 160
servo1_max = 180

servo2_min = 125
servo2_stable = 155
servo2_max = 175

#don't forget to change the serial port to suit
board = pyfirmata.Arduino(port)
 
# start an iterator thread so
# serial buffer doesn't overflow
iter8 = pyfirmata.util.Iterator(board)
iter8.start()
 
# set up pin D9 as Servo Output
pin9 = board.get_pin('d:9:s')
pin10 = board.get_pin('d:10:s')

pin9.write(current1)
pin10.write(current2)



# Function to run servoes
# Returns the final position of the servo
def send_angle(pin, current, target):
    final=current
    if target < current:
        final = current - 1
        pin.write(final)
    elif target > current:
        final = current + 1
        pin.write(final)
    return(final)


async def move_servo():
    global current1, current2
    global ang1, ang2
    global pin9_inputs
    while True:
        current1 = send_angle(pin9, current1, ang1)
        current2 = send_angle(pin10, current2, ang2)

        await asyncio.sleep(0.007)


async def cv_everything():
    global ang1, ang2
    vid = cv2.VideoCapture(1)

    while(True):
        # Capture the video frame
        # by frame
        ret, cimg = vid.read()
        cimg = cv2.GaussianBlur(cimg,(5,5),0)
        # cimg = cv2.medianBlur(cimg,5)
        # img = cv2.cvtColor(cimg,cv2.COLOR_BGR2GRAY)

        hsv = cv2.cvtColor(cimg, cv2.COLOR_BGR2HSV)

        l_b = np.array([9, 23, 219])
        u_b = np.array([59, 255, 255])
        mask = cv2.inRange(hsv, l_b, u_b)

        cv2.imshow("Mask", mask)
        cv2.waitKey(1)

        circles = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1.2,40,
                                    param1=200,param2=15,minRadius=20,maxRadius=50)

        # 1 is the ratio - directly proportional to the senstivity
        # 20 is the min_dist
        # param_1 is the canny threshold
        # param_2 is the threshold for center - smaller the threshold is, the more circles will be detected 

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

            # height, width = cimg.shape

            #denominator = max(height - center_height, center_height, width - center_width, center_width)

            # Center of the plate - hardcoded
            center_height = 328
            center_width = 236

            x_extent=240 # hardcoded
            y_extent=240

            del_h = i[0] - center_height
            del_w = i[1] - center_width

            print(del_h, del_w)
            # ang1 = control_function(del_h/denominator)
            # ang2 = control_function(del_w/denominator)
            ang1 = scaled_output(2,del_w/y_extent)
            ang2 = scaled_output(1,del_h/x_extent)


            # print(del_h,del_w)
        
        cv2.imshow("Image", cimg)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            vid.release()
            cv2.destroyAllWindows()
            break

        await asyncio.sleep(0.01)


async def main():
    task1 = asyncio.create_task(
        move_servo()
    )
    task2 = asyncio.create_task(
        cv_everything()
    )

    pin9.write(current1)
    pin10.write(current2)

    await task1
    await task2

asyncio.run(main())
