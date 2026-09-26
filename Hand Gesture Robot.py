# Hand Gesture Robot using Python

# Install required libraries:

# pip install opencv-python mediapipe

import cv2
import mediapipe as mp

# Initialize MediaPipe Hands

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
max_num_hands=1,
min_detection_confidence=0.7,
min_tracking_confidence=0.7
)

# Start webcam

camera = cv2.VideoCapture(0)

def robot_command(gesture):
if gesture == "OPEN":
print("Robot: MOVE FORWARD")

```
elif gesture == "FIST":
    print("Robot: STOP")

elif gesture == "LEFT":
    print("Robot: TURN LEFT")

elif gesture == "RIGHT":
    print("Robot: TURN RIGHT")

else:
    print("Robot: UNKNOWN GESTURE")
```

while True:

```
success, frame = camera.read()

if not success:
    print("Camera not available.")
    break

# Flip camera image
frame = cv2.flip(frame, 1)

# Convert BGR to RGB
rgb_frame = cv2.cvtColor(
    frame,
    cv2.COLOR_BGR2RGB
)

results = hands.process(rgb_frame)

gesture = "UNKNOWN"

if results.multi_hand_landmarks:

    for hand_landmarks in results.multi_hand_landmarks:

        # Draw hand landmarks
        mp_draw.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )

        # Get landmark positions
        landmarks = hand_landmarks.landmark

        # Finger positions
        thumb = landmarks[4].x
        index = landmarks[8].y
        middle = landmarks[12].y
        ring = landmarks[16].y
        little = landmarks[20].y

        index_tip = landmarks[8].y
        index_base = landmarks[6].y

        # Open hand
        if (
            index < landmarks[6].y
            and middle < landmarks[10].y
            and ring < landmarks[14].y
            and little < landmarks[18].y
        ):
            gesture = "OPEN"

        # Fist
        elif (
            index > landmarks[6].y
            and middle > landmarks[10].y
            and ring > landmarks[14].y
            and little > landmarks[18].y
        ):
            gesture = "FIST"

        # Index finger pointing
        elif (
            index < index_base
            and middle > landmarks[10].y
            and ring > landmarks[14].y
            and little > landmarks[18].y
        ):
            # Use hand position for left/right
            if landmarks[8].x < 0.4:
                gesture = "LEFT"

            elif landmarks[8].x > 0.6:
                gesture = "RIGHT"

            else:
                gesture = "OPEN"

        robot_command(gesture)

# Display gesture
cv2.putText(
    frame,
    f"Gesture: {gesture}",
    (20, 50),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 255, 0),
    2
)

cv2.imshow(
    "Hand Gesture Robot",
    frame
)

# Press Q to quit
if cv2.waitKey(1) & 0xFF == ord("q"):
    break
```

camera.release()
cv2.destroyAllWindows()
