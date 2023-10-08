import cv2              # OpenCV for capturing video and image processing
import subprocess       # Subprocess for running terminal commands
import mediapipe as mp  # MediaPipe for hand tracking

cap = cv2.VideoCapture(0)  # Open the default camera (camera index 0)
mp_hands = mp.solutions.hands  # Initialize the MediaPipe hands module
hands = mp_hands.Hands(
    static_image_mode=False,  # Continuous hand tracking (not static image)
    max_num_hands=1,           # Track only one hand
    min_detection_confidence=0.5,  # Minimum confidence to detect a hand
    min_tracking_confidence=0.5   # Minimum confidence to track hand landmarks
)
mp_drawing = mp.solutions.drawing_utils  # Utility functions for drawing landmarks

while True:
    ret, frame = cap.read()  # Read a frame from the webcam
    if not ret:
        break  # Exit the loop if there's no frame

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the frame to RGB format

    results = hands.process(image_rgb)  # Process the frame to detect hand landmarks

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        index_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
        thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

        if index_finger_y < thumb_y:
            hand_gesture = 'pointing up'
        elif index_finger_y > thumb_y:
            hand_gesture = 'pointing down'
        else:
            hand_gesture = 'other'

        if hand_gesture == 'pointing up':
            # Increase volume using osascript
            subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 5)"])
        elif hand_gesture == 'pointing down':
            # Decrease volume using osascript
            subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 5)"])

    cv2.imshow('Hand Gesture', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
