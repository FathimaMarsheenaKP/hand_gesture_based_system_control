#!/usr/bin/python3

from turtle import goto
import cv2
from cvzone.HandTrackingModule import HandDetector as htm
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller
try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

def run_keyboard_input():
    # Creating a video capture object to return video from the first webcam on the computer
    cap = cv2.VideoCapture(0)
    # Setting the properties of the frame
    cap.set(3, 1440)
    cap.set(4, 860)

    detector = htm(detectionCon=0.8)

    # 2D list
    keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", ":"],
            ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
            ["ok", " ", " ", " ", " ", " ", " ", " ", " ", "<-"]]
    finalText = ""
    keyboard = Controller()  # To simulate pressing individual keys

    # Function for drawing the buttons
    def drawAll(img, buttonList):
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            cv2.rectangle(img, (button.pos), (x + w, y + h), (88, 16, 13), cv2.FILLED)  # Blue filled boxes
            cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)  # Text
            cv2.rectangle(img, (button.pos), (x + w, y + h), (0, 0, 0), 2)  # Black border
        return img

    # Class to create the buttons
    class Button():
        def __init__(self, pos, text, size=[85, 85]):
            self.pos = pos
            self.size = size
            self.text = text

    buttonList = []
    # Create a grid of buttons based on the keys 2D list
    # Each button is assigned a position based on its row and column indices
    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonList.append(Button([100 * j + 50, 100 * i], key))

    lmList = []
    searchText = ""

    while True:
        success, img = cap.read()  # Read a frame
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img)  # Returns the processed image with landmarks and hand connections on it
        if hands:
            for hand in hands:
                lmList = hand["lmList"]  # List of landmark coordinates

        # Display the image with detected hands, landmarks, and the buttons
        img = drawAll(img, buttonList)
        if lmList:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                    cv2.rectangle(img, (x - 10, y - 10), (x + w + 10, y + h + 10), (255, 255, 153), cv2.FILLED)  # Cyan filled box
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)  # Black text
                    l, _, _ = detector.findDistance(lmList[8][0:2], lmList[12][0:2], img)  # Find distance between tips of index and middle finger

                    if l < 30:
                        if len(button.text) == 1:
                            keyboard.press(button.text)
                            finalText += button.text
                            sleep(0.3)
                        elif button.text == "ok":
                            searchText = finalText
                            sleep(0.3)
                            cv2.destroyAllWindows()  # Close the window
                            sleep(0.9)
                            print("Window closed.")
                            # Execute a search using the specified query and iterate over the results
                            print(searchText)
                            query = searchText
                            for j in search(query):
                                print(j)
                            break
                        elif button.text == "<-":
                            finalText = finalText[:-1]
                            sleep(0.15)

        cv2.rectangle(img, (50, 450), (1150, 550), (88, 16, 13), cv2.FILLED)  # Blue filled box as search bar
        cv2.putText(img, finalText, (60, 530), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)  # White text
        cv2.rectangle(img, (50, 450), (1150, 550), (0, 0, 0), 2)  # Black border

        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord('q'):  # Exit if 'q' is pressed
            break

    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    run_keyboard_input()
