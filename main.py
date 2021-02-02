import time
from threading import Thread
from pynput.mouse import Listener
import pyautogui
import pytesseract
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# todo: take a big screenshot to remove any areas with black

# Color variables for "unseen object text"
lower_red = np.array([0,0,110])
upper_red = np.array([15,15,255])
pyautogui.FAILSAFE = False
global x, y, xx, yy, current_x, current_y
x = 0
y = 0
xx = 0
yy = 0
current_x = 0
current_y = 0


def get_shots():
    global current_x, current_y
    while (current_y < yy):
        pyautogui.moveTo(current_x, current_y, _pause=False)
        shots.append([current_x, current_y, pyautogui.screenshot(region=(current_x + 220, current_y + 30, 45, 50))])
        current_x+=x_increment
        if (current_x >= xx):
            current_x = x
            current_y+=y_increment

def process_shots():
    global shots
    global found
    while (len(shots) > 0 or t1.is_alive()):
        if (len(shots)== 0):
            time.sleep(.1)
            continue
        x, y, shot = shots.pop()
        image = cv2.cvtColor(np.array(shot), cv2.COLOR_RGB2BGR)
        mask = cv2.inRange(image, lower_red, upper_red)
        res = cv2.bitwise_and(image, image, mask=mask)
        text = pytesseract.image_to_string(res)
        if ("obj" in text):
            cv2.imwrite("./"+str(x+y)+".png",res)
            # build an array of found unseen objects
            found.append([x,y])

def display_found():
    # Cancel watch tower
    pyautogui.press('b')
    for x,y in found:
        pyautogui.keyDown('shift')
        pyautogui.click(x = x, y = y, button='right')
        pyautogui.keyUp('shift')
        print("found at location "+ str(x) + " " + str(y))
        time.sleep(.01)
    if len(found) == 0:
        pyautogui.press('insert')
        print('none found')

def on_click(x_clicked, y_clicked, button, pressed):
    if(button.name == "x1" and pressed):
        # reset variables
        global x, xx, y, yy, current_x, current_y
        if (x == 0):
            x = x_clicked
            current_x = x_clicked
            y = y_clicked
            current_y = y_clicked
            return
        else:
            xx = x_clicked
            yy = y_clicked
        global x_increment
        x_increment = 60
        global y_increment
        y_increment = 60
        global shots
        shots = []
        global found
        found = []

        global t1
        t1 = Thread(target = get_shots)
        t2 = Thread(target = process_shots)
        t3 = Thread(target = process_shots)
        t4 = Thread(target = process_shots)
        t5 = Thread(target = process_shots)
        t6 = Thread(target = process_shots)
        t7 = Thread(target = process_shots)
        t8 = Thread(target = process_shots)
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()
        t8.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        t8.join()
        display_found()
        # Reset
        x = 0
        y = 0
        xx = 0
        yy = 0

    # break out of loop
    if(button.name == "x2" and pressed):
        return False
    # print(button.text)
    # if button.text == "Button.x2":
    #     print ("run script")
    # if button.text == "Button.x1":
    #     return False

with Listener(on_click=on_click) as listener:
    listener.join()