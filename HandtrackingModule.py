import cv2
import mediapipe as mp
import time

#  Class for tracking
#  Put self before every object to allow access to the methods and the attributes of that object.
#  Each object possess its own attributes and methods.
class handDetector():
    def __init__(self, mode=False, maxHands=2, modelComplexity=1,  detectionCon=0.5, trackCon=0.5 ):#parameters and initializations
        self.mode=mode
        self.maxHands=maxHands
        self.modelComplexity=modelComplexity
        self.detectionCon=detectionCon
        self.trackCon=trackCon

        self.mpHands = mp.solutions.hands #creates an instance variable that holds a reference to the mp.solutions.hands module
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplexity, self.detectionCon,self.trackCon) #instance variable that holds a reference to a Hands object
        self.mpDraw = mp.solutions.drawing_utils #imports the drawing utility functions provided by the MediaPipe library

# Track the hands in our input image
# Converts the image to RGB and processes the RGB image (mediapipe uses rgb format but default in opencv is bgr)
# Draws the hand landmarks on the image
# Finally draws the hand connections.
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:#working with one hand at a time
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    
#Finding the x and y coordinates of each of the 21 hand points. 
#Creating a list to store the values of these coordinates.
#Circle the hand-point that we want to use.
    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        #if hand detected
        if self.results.multi_hand_landmarks: 
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape #returns the dimensions...height, width, no of channels(3)
                cx, cy = int(lm.x*w), int(lm.y*h)#convert the normalized landmark position to pixel coordinates(decimal values in terms of h and w)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (51, 0, 25), cv2.FILLED)
        return lmList
    
#Dummy code to identify and track hands.
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)#Creating a video capture object to return video from first webcam on computer
    detector = handDetector()
    while True:
        success, img = cap.read()#Read a frame 
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (51, 0, 25), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

#main() executed only if the script is being run as the main program, and not if it is being imported as a module into another program.
if __name__ == "__main__":
    main()