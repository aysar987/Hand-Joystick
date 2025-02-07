import cv2
import mediapipe as mp
import pyautogui

# Initialize Mediapipe Hands module
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the image and convert to RGB
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame for hand detection
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract landmark points
            thumb_tip = hand_landmarks.landmark[4]  # Thumb tip
            index_tip = hand_landmarks.landmark[8]  # Index finger tip
            middle_tip = hand_landmarks.landmark[12]  # Middle finger tip

            # Gesture detection
            if index_tip.y < middle_tip.y:  # Jump (if index is above middle)
                pyautogui.press("up")
            elif index_tip.x < thumb_tip.x:  # Move Left
                pyautogui.press("left")
            elif index_tip.x > thumb_tip.x:  # Move Right
                pyautogui.press("right")
            elif index_tip.y > middle_tip.y:  # Roll (if index is below middle)
                pyautogui.press("down")

    cv2.imshow("Hand Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

#python /Users/aysarakbar/Desktop/PROJECT/Try/Motion.py
#conda activate mp-env