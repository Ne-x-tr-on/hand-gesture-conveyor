import cv2
import mediapipe as mp
import serial
import time

# Serial setup
arduino_port = "COM4"  # Change if needed
baud_rate = 9600
arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)           # Wait for Arduino reset
arduino.flushInput()

# MediaPipe hand setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

def classify_gesture(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    return "FIST" if thumb_tip.y < index_tip.y else "OPEN_HAND"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    gesture = None
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            gesture = classify_gesture(hand_landmarks)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Convert gesture to Arduino command
            if gesture == "OPEN_HAND":
                command = "ON"
            else:
                command = "OFF"

            arduino.write((command + "\n").encode())
            print("Sent:", command)  # Debugging

    if gesture:
        cv2.putText(frame, f"Gesture: {gesture}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
