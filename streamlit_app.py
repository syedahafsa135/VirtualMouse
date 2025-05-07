import streamlit as st
import cv2
import mediapipe as mp
import pyautogui
import random
import util
import time
import os
from pynput.mouse import Button, Controller
from PIL import Image
import numpy as np
from cloudinary_utils import upload_screenshot_to_cloudinary

mouse = Controller()
screen_width, screen_height = pyautogui.size()

# Mediapipe hand setup
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

# Timing for gesture debounce
last_left_click_time = 0
last_right_click_time = 0
last_double_click_time = 0
last_screenshot_time = 0
gesture_delay = 1  # seconds

SCREENSHOT_DIR = "."

def count_fingers(hand_landmarks):
    tips_ids = [
        mpHands.HandLandmark.INDEX_FINGER_TIP,
        mpHands.HandLandmark.MIDDLE_FINGER_TIP,
        mpHands.HandLandmark.RING_FINGER_TIP,
        mpHands.HandLandmark.PINKY_TIP,
    ]
    pip_ids = [
        mpHands.HandLandmark.INDEX_FINGER_PIP,
        mpHands.HandLandmark.MIDDLE_FINGER_PIP,
        mpHands.HandLandmark.RING_FINGER_PIP,
        mpHands.HandLandmark.PINKY_PIP,
    ]

    count = 0
    for tip_id, pip_id in zip(tips_ids, pip_ids):
        tip_y = hand_landmarks.landmark[tip_id].y
        pip_y = hand_landmarks.landmark[pip_id].y
        if tip_y < pip_y:
            count += 1
    return count

def detect_gesture(frame, hand_landmarks):
    global last_left_click_time, last_right_click_time, last_double_click_time, last_screenshot_time

    current_time = time.time()
    gesture = None

    landmark_list = [(lm.x, lm.y) for lm in hand_landmarks.landmark]
    index_finger_tip = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]

    thumb_index_dist = util.get_distance([landmark_list[4], landmark_list[5]])
    index_angle = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8])

    if thumb_index_dist < 50 and index_angle > 90:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y * screen_height / 2)
        pyautogui.moveTo(x, y)

    finger_count = count_fingers(hand_landmarks)

    if finger_count == 3:
        pyautogui.scroll(20)
        cv2.putText(frame, "Scroll Up", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    elif finger_count == 4:
        pyautogui.scroll(-20)
        cv2.putText(frame, "Scroll Down", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    left_angle = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8])
    right_angle = util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12])

    if left_angle < 50 and thumb_index_dist > 50:
        gesture = "Left Click"
    elif right_angle < 50 and thumb_index_dist > 50:
        gesture = "Right Click"
    elif left_angle < 50 and right_angle < 50 and thumb_index_dist > 50:
        gesture = "Double Click"
    elif left_angle < 50 and right_angle < 50 and thumb_index_dist < 50:
        gesture = "Screenshot"

    if gesture == "Left Click" and current_time - last_left_click_time > gesture_delay:
        mouse.press(Button.left)
        mouse.release(Button.left)
        cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        last_left_click_time = current_time

    elif gesture == "Right Click" and current_time - last_right_click_time > gesture_delay:
        mouse.press(Button.right)
        mouse.release(Button.right)
        cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        last_right_click_time = current_time

    elif gesture == "Double Click" and current_time - last_double_click_time > gesture_delay:
        pyautogui.doubleClick()
        cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        last_double_click_time = current_time

    elif gesture == "Screenshot" and current_time - last_screenshot_time > 2:
        im1 = pyautogui.screenshot()
        label = random.randint(1, 1000)
        filename = f'my_screenshot_{label}.png'
        path = os.path.join(SCREENSHOT_DIR, filename)
        im1.save(path)

        url = upload_screenshot_to_cloudinary(path)
        if url:
            print(f"✅ Uploaded to Cloudinary: {url}")
            st.sidebar.image(url, caption="Uploaded to Cloudinary", use_container_width=True)
        else:
            print("❌ Failed to upload to Cloudinary")

        cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        last_screenshot_time = current_time

    return frame

def virtual_keyboard():
    st.sidebar.subheader("Virtual Keyboard")
    if 'typed_text' not in st.session_state:
        st.session_state.typed_text = ""

    # Use a container to hold the keys to avoid multiple reruns
    with st.sidebar.container():
        keys = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '⌫'],
            ['Space', 'Enter']
        ]

        for row in keys:
            cols = st.columns(len(row))
            for i, key in enumerate(row):
                if cols[i].button(key):
                    if key == 'Space':
                        pyautogui.press('space')
                        st.session_state.typed_text += ' '
                    elif key == 'Enter':
                        pyautogui.press('enter')
                        st.session_state.typed_text += '\n'
                    elif key == '⌫':
                        pyautogui.press('backspace')
                        st.session_state.typed_text = st.session_state.typed_text[:-1]
                    else:
                        pyautogui.press(key.lower())
                        st.session_state.typed_text += key.lower()

                    # Break after processing one key press to avoid multiple presses in one run
                    break

    # Update the text area with new text after key press
    st.sidebar.text_area("Typed Text", value=st.session_state.typed_text, height=150, key="typed_text_display", disabled=True)


def main():
    st.title("Virtual Mouse Detector with Streamlit")
    st.sidebar.title("Controls")

    run_camera = st.sidebar.checkbox("Activate Camera", key="activate_camera_main")

    st.sidebar.subheader("Screenshots")

    if st.sidebar.button("🔄 Refresh Screenshots"):
        st.rerun()

    screenshot_files = [
        f for f in os.listdir(SCREENSHOT_DIR)
        if f.startswith("my_screenshot_") and f.endswith(".png")
    ]

    frame_placeholder = st.empty()
    status_text = st.empty()

    virtual_keyboard()

    if run_camera:
        if 'cap' not in st.session_state:
            st.session_state.cap = cv2.VideoCapture(0)

        cap = st.session_state.cap

        if not cap.isOpened():
            st.error("Failed to open camera. Please check if it's connected or in use.")
        else:
            while run_camera:
                ret, frame = cap.read()

                if not ret or frame is None or frame.shape[0] == 0 or frame.shape[1] == 0:
                    status_text.error("Failed to capture frame.")
                    break

                frame = cv2.flip(frame, 1)
                processed = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

                if processed.multi_hand_landmarks:
                    hand_landmarks = processed.multi_hand_landmarks[0]
                    mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
                    frame = detect_gesture(frame, hand_landmarks)

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_placeholder.image(frame_rgb, channels="RGB")
                time.sleep(0.03)  # To avoid overloading CPU

    else:
        if 'cap' in st.session_state:
            st.session_state.cap.release()
            del st.session_state["cap"]
        

    if screenshot_files:
        for file in screenshot_files:
            col1, col2 = st.sidebar.columns([3, 1])
            col1.image(os.path.join(SCREENSHOT_DIR, file), use_container_width=True)
            if col2.button("🗑️ Delete", key=file):
                os.remove(os.path.join(SCREENSHOT_DIR, file))
                st.rerun()
    else:
        st.sidebar.write("No screenshots found")

if __name__ == "__main__":
    main()
