import streamlit as st
import cv2
import os
import pandas as pd
from datetime import datetime
from ultralytics import YOLO
import numpy as np

SAVE_DIR = "birdbabies"
os.makedirs(SAVE_DIR, exist_ok=True)

st.title("🐦 Bird Detector with Live Video (YOLOv8l for best accuracy)")

if "log" not in st.session_state:
    st.session_state.log = pd.DataFrame(columns=["Timestamp", "Filename"])

@st.cache_resource
def load_model():
    model = YOLO("yolov8l.pt")  # Use large model for better detection
    return model

model = load_model()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

video_placeholder = st.empty()
table_placeholder = st.empty()

stop_button = st.button("Stop Camera")

def detect_and_save_birds(frame):
    # Convert BGR to RGB for model
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = model(frame_rgb)[0]
    detections_to_save = []

    for r in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = r
        x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
        class_id = int(class_id)
        score = float(score)

        label = model.names[class_id] if model.names else str(class_id)
        color = (0, 255, 0) if class_id == 15 else (255, 0, 0)

        # Draw boxes for all detections with confidence > 0.1
        if score > 0.1:
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"{label} {score:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Save only birds with confidence > 0.25 (tweak if needed)
        if class_id == 15 and score > 0.25:
            bird_img = frame[y1:y2, x1:x2]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"bird_{timestamp}.jpg"
            filepath = os.path.join(SAVE_DIR, filename)
            cv2.imwrite(filepath, bird_img)
            detections_to_save.append((timestamp, filename))

            # Debug print to console
            print(f"Bird detected: {filename} with confidence {score:.2f}")

    return frame, detections_to_save

while cap.isOpened() and not stop_button:
    ret, frame = cap.read()
    if not ret:
        st.error("Failed to capture video")
        break

    frame, birds_detected = detect_and_save_birds(frame)

    if birds_detected:
        for ts, fname in birds_detected:
            new_row = pd.DataFrame({"Timestamp": [ts], "Filename": [fname]})
            st.session_state.log = pd.concat([st.session_state.log, new_row], ignore_index=True)

    frame_rgb_display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    video_placeholder.image(frame_rgb_display, channels="RGB")
    table_placeholder.dataframe(st.session_state.log)

cap.release()
st.write("Camera stopped")
