import cv2
from cvzone.HandTrackingModule import HandDetector
from directkeys import PressKey, ReleaseKey
from directkeys import space_pressed
import time

# Initializing hand detector with confidence threshold and maximum hands to detect
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Defining the key to be pressed
space_key_pressed = space_pressed

time.sleep(2.0)

# Initializing a set to keep track of currently pressed keys
current_key_pressed = set()

# Starting to capture video from the default camera
video = cv2.VideoCapture(0)
# 0 because we are going to use default camera

while True:
    # Reading a frame from the video feed
    ret, frame = video.read()

    keyPressed = False
    key_count = 0
    key_pressed = 0

    # Detecting hands in the frame
    hands, img = detector.findHands(frame)

    # Drawing rectangles on the image for UI
    cv2.rectangle(img, (0, 480), (300, 425), (144, 85, 247), -2)  # Pink rectangle
    cv2.rectangle(img, (640, 480), (400, 425), (203, 255, 16), -2)  # Cyan rectangle

    if hands:
        lmList = hands[0]
        fingerUp = detector.fingersUp(lmList)

        # If all fingers are down, jump
        if fingerUp == [0, 0, 0, 0, 0]:
            cv2.putText(frame, 'Finger Count: 0', (20, 460), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1,
                        cv2.LINE_AA)
            cv2.putText(frame, 'Jumping', (440, 460), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

            # If space key is not pressed, pressing it
            if space_key_pressed not in current_key_pressed:
                PressKey(space_key_pressed)
                current_key_pressed.add(space_key_pressed)
                keyPressed = True
                key_count += 1

        # If any finger is up, stop jumping
        else:
            if space_key_pressed in current_key_pressed:
                ReleaseKey(space_key_pressed)
                current_key_pressed.remove(space_key_pressed)

        # Displaying finger count and action status based on fingers up
        if fingerUp == [0, 1, 0, 0, 0]:
            cv2.putText(frame, 'Finger Count: 1', (20, 460), cv2.FONT_HERSHEY_DUPLEX, 1, (17, 23, 41), 1,
                        cv2.LINE_AA)
            cv2.putText(frame, 'Not Jumping', (420, 460), cv2.FONT_HERSHEY_DUPLEX, 1, (17, 23, 41), 1,
                        cv2.LINE_AA)

        if fingerUp == [0, 1, 1, 0, 0]:
            cv2.putText(frame, 'Finger Count: 2', (20, 460), cv2.FONT_HERSHEY_DUPLEX, 1, (17, 23, 41), 1,
                        cv2.LINE_AA)
            cv2.putText(frame, 'Not Jumping', (420, 460), cv2.FONT_HERSHEY_DUPLEX, 1, (17, 23, 41), 1,
                        cv2.LINE_AA)

        if fingerUp == [0, 1, 1, 1, 0]:
            cv2.putText(frame, 'Finger Count: 3', (20, 460), cv2.FONT_HERSHEY_DUPLEX, 1, (17, 23, 41), 1,
                        cv2.LINE_AA)
            cv2.putText(frame, 'Not Jumping', (420, 460), cv2.FONT_HERSHEY_DUPLEX, 1, (17, 23, 41), 1,
                        cv2.LINE_AA)

        if fingerUp == [0, 1, 1, 1, 1]:
            cv2.putText(frame, 'Finger Count: 4', (20, 460), cv2.FONT_HERSHEY_DUPLEX, 1, (17, 23, 41), 1,
                        cv2.LINE_AA)
            cv2.putText(frame, 'Not Jumping', (420, 460), cv2.FONT_HERSHEY_DUPLEX, 1, (17, 23, 41), 1,
                        cv2.LINE_AA)

        if fingerUp == [1, 1, 1, 1, 1]:
            cv2.putText(frame, 'Finger Count: 5', (20, 460), cv2.FONT_HERSHEY_DUPLEX, 1, (17, 23, 41), 1,
                        cv2.LINE_AA)
            cv2.putText(frame, 'Not Jumping', (420, 460), cv2.FONT_HERSHEY_DUPLEX, 1, (17, 23, 41), 1,
                        cv2.LINE_AA)

    # Displaying the processed frame
    cv2.imshow("Hand Gesture Dino Game", frame)

    # Waiting for user input to break the loop
    k = cv2.waitKey(1)

    if k == ord('q'):
        break

# Releasing the video capture object and close all OpenCV windows
video.release()
cv2.destroyAllWindows()
