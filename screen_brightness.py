import cv2 as cv
import numpy as np
import screen_brightness_control as sbc
from cvzone.HandTrackingModule import HandDetector

def run_brightness_control():
    cap = cv.VideoCapture(0) # Creating a video capture object to return video from the first webcam on the computer
    hd = HandDetector() # Creating an instance of the HandDetector class
    val = 0
    
    while True:
        _, img = cap.read() # Read a frame
        hands, img = hd.findHands(img) # Find hands in the image
        
        if hands:
            lm = hands[0]['lmList'] # Access the landmark coordinates for the first detected hand
            
            length, info, img = hd.findDistance(lm[8][0:2], lm[4][0:2], img) # Calculate the distance between thumb and index finger
            
            blevel = np.interp(length, [25, 145], [0, 100]) # Interpolate to get brightness level percentage
            val = np.interp(length, [25, 145], [400, 150]) # Interpolate to get level value
            blevel = int(blevel)
            
            sbc.set_brightness(blevel) # Set the screen brightness
            
            cv.rectangle(img, (20, 150), (85, 400), (139, 139, 0), 4) # Draw the border of brightness bar
            cv.rectangle(img, (20, int(val)), (85, 400), (255, 255, 153), -1) # Draw the brightness level
            cv.putText(img, str(blevel)+'%', (20, 430), cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 153), 3) # Display the brightness percentage
        
        cv.imshow('frame', img)
        if cv.waitKey(1) == ord('q'): # Exit if 'q' is pressed
            break

    cap.release()
    cv.destroyAllWindows()
