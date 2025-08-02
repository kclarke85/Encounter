# import streamlit as st
# import cv2
# import numpy as np
# import time
# import os
# from datetime import datetime
# import requests
# import tempfile
#
# # Set page config for a fun, colorful interface
# st.set_page_config(
#     page_title="🐦 Bird Spotter Pro",
#     page_icon="🐦",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )
#
# # Custom CSS for teen-friendly styling
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 3rem;
#         color: #FF6B6B;
#         text-align: center;
#         margin-bottom: 2rem;
#         text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
#     }
#     .fun-metric {
#         background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
#         padding: 1rem;
#         border-radius: 10px;
#         color: white;
#         text-align: center;
#         margin: 0.5rem 0;
#     }
#     .detection-status {
#         font-size: 1.5rem;
#         padding: 1rem;
#         border-radius: 10px;
#         text-align: center;
#         margin: 1rem 0;
#     }
#     .bird-detected {
#         background: linear-gradient(45deg, #95E1D3, #F38BA8);
#         color: white;
#         animation: pulse 1s infinite;
#     }
#     .no-bird {
#         background: #F0F0F0;
#         color: #666;
#     }
#     .auto-capture {
#         background: linear-gradient(45deg, #FFD93D, #FF6B6B);
#         color: white;
#         animation: flash 0.5s infinite;
#     }
#     .debug-info {
#         background: #E8F4FD;
#         padding: 1rem;
#         border-radius: 5px;
#         font-family: monospace;
#         font-size: 0.8rem;
#     }
#     @keyframes pulse {
#         0% { transform: scale(1); }
#         50% { transform: scale(1.05); }
#         100% { transform: scale(1); }
#     }
#     @keyframes flash {
#         0% { opacity: 1; }
#         50% { opacity: 0.7; }
#         100% { opacity: 1; }
#     }
#     .stButton > button {
#         background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
#         color: white;
#         border: none;
#         border-radius: 20px;
#         padding: 0.5rem 2rem;
#         font-size: 1.1rem;
#         font-weight: bold;
#         transition: all 0.3s;
#     }
#     .stButton > button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 4px 8px rgba(0,0,0,0.2);
#     }
# </style>
# """, unsafe_allow_html=True)
#
#
# class BirdDetector:
#     def __init__(self):
#         self.net = None
#         self.classes = []
#         self.bird_class_ids = []  # Support multiple bird-related classes
#         self.od_confidence_threshold = 0.3  # Start with higher threshold
#         self.detection_cooldown = 3.0
#         self.min_detection_frames = 2  # Reduced for better responsiveness
#         self.detection_frame_count = 0
#         self.last_capture_time = 0
#         self.last_bird_detection_count_time = 0
#         self.model_loaded = False
#         self.last_detections = []  # Store recent detections for debugging
#         self.load_object_detector()
#
#     def download_model_files(self):
#         """Download YOLO model files if they don't exist"""
#         model_dir = "models"
#         if not os.path.exists(model_dir):
#             os.makedirs(model_dir)
#
#         # Using YOLOv4-tiny for better performance and easier setup
#         model_files = {
#             "yolov4-tiny.weights": "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights",
#             "yolov4-tiny.cfg": "https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg",
#             "coco.names": "https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names"
#         }
#
#         for filename, url in model_files.items():
#             filepath = os.path.join(model_dir, filename)
#             if not os.path.exists(filepath):
#                 try:
#                     st.info(f"📥 Downloading {filename}...")
#                     response = requests.get(url, stream=True)
#                     response.raise_for_status()
#
#                     with open(filepath, 'wb') as f:
#                         for chunk in response.iter_content(chunk_size=8192):
#                             f.write(chunk)
#                     st.success(f"✅ Downloaded {filename}")
#                 except Exception as e:
#                     st.error(f"❌ Failed to download {filename}: {e}")
#                     return False
#         return True
#
#     def load_object_detector(self):
#         model_dir = "models"
#
#         # Try to download model files if they don't exist
#         if not self.download_model_files():
#             st.error("Failed to download model files. Using fallback detection method.")
#             return
#
#         model_weights = os.path.join(model_dir, "yolov4-tiny.weights")
#         model_config = os.path.join(model_dir, "yolov4-tiny.cfg")
#         class_names_file = os.path.join(model_dir, "coco.names")
#
#         st.info("🔍 Loading AI model for bird detection...")
#
#         try:
#             # Load YOLO model
#             self.net = cv2.dnn.readNet(model_weights, model_config)
#             self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
#             self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
#
#             # Load class names
#             with open(class_names_file, 'rt') as f:
#                 self.classes = f.read().rstrip('\n').split('\n')
#
#             # Find bird-related classes (COCO has class 14 for 'bird')
#             bird_related_terms = ['bird']
#             self.bird_class_ids = []
#
#             for i, class_name in enumerate(self.classes):
#                 if any(term in class_name.lower() for term in bird_related_terms):
#                     self.bird_class_ids.append(i)
#
#             if self.bird_class_ids:
#                 st.success(
#                     f"✅ AI model loaded! Bird detection ready (classes: {[self.classes[i] for i in self.bird_class_ids]})")
#                 self.model_loaded = True
#             else:
#                 st.warning("⚠️ Model loaded but no bird classes found")
#
#         except Exception as e:
#             st.error(f"❌ Failed to load AI model: {e}")
#             st.info("💡 Falling back to motion-based detection")
#             self.model_loaded = False
#
#     def detect_birds_simple_motion(self, frame, prev_frame):
#         """Fallback motion-based detection when AI model fails"""
#         if prev_frame is None:
#             return False, frame, False, 0.0
#
#         # Convert to grayscale
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
#
#         # Calculate frame difference
#         diff = cv2.absdiff(gray, prev_gray)
#         _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
#
#         # Find contours
#         contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
#         motion_detected = False
#         processed_frame = frame.copy()
#
#         for contour in contours:
#             area = cv2.contourArea(contour)
#             # Look for medium-sized moving objects (potential birds)
#             if 500 < area < 10000:
#                 x, y, w, h = cv2.boundingRect(contour)
#                 # Check aspect ratio (birds are usually not too thin or too wide)
#                 aspect_ratio = w / h
#                 if 0.3 < aspect_ratio < 3.0:
#                     motion_detected = True
#                     cv2.rectangle(processed_frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
#                     cv2.putText(processed_frame, "Possible Bird Motion", (x, y - 10),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
#
#         return motion_detected, processed_frame, motion_detected, 0.8 if motion_detected else 0.0
#
#     def should_auto_capture(self):
#         current_time = time.time()
#         if current_time - self.last_capture_time > self.detection_cooldown:
#             self.last_capture_time = current_time
#             return True
#         return False
#
#     def should_increment_bird_count(self):
#         current_time = time.time()
#         if current_time - self.last_bird_detection_count_time > self.detection_cooldown:
#             self.last_bird_detection_count_time = current_time
#             return True
#         return False
#
#     def detect_birds(self, frame, prev_frame=None):
#         processed_frame = frame.copy()
#         bird_found_in_frame = False
#         highest_confidence = 0
#         detection_info = []
#
#         if not self.model_loaded:
#             # Use motion-based fallback
#             return self.detect_birds_simple_motion(frame, prev_frame)
#
#         try:
#             # Create blob from frame
#             blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
#             self.net.setInput(blob)
#
#             # Get detections
#             layer_outputs = self.net.forward(self.net.getUnconnectedOutLayersNames())
#
#             boxes = []
#             confidences = []
#             class_ids = []
#
#             h, w = frame.shape[:2]
#
#             # Process each output layer
#             for output in layer_outputs:
#                 for detection in output:
#                     scores = detection[5:]
#                     class_id = np.argmax(scores)
#                     confidence = scores[class_id]
#
#                     # Check if it's a bird class with sufficient confidence
#                     if class_id in self.bird_class_ids and confidence > self.od_confidence_threshold:
#                         center_x = int(detection[0] * w)
#                         center_y = int(detection[1] * h)
#                         width = int(detection[2] * w)
#                         height = int(detection[3] * h)
#
#                         x = int(center_x - width / 2)
#                         y = int(center_y - height / 2)
#
#                         boxes.append([x, y, width, height])
#                         confidences.append(float(confidence))
#                         class_ids.append(class_id)
#
#             # Apply non-maximum suppression
#             indices = cv2.dnn.NMSBoxes(boxes, confidences, self.od_confidence_threshold, 0.4)
#
#             if len(indices) > 0:
#                 bird_found_in_frame = True
#                 for i in indices.flatten():
#                     x, y, w, h = boxes[i]
#                     confidence = confidences[i]
#                     class_id = class_ids[i]
#                     highest_confidence = max(highest_confidence, confidence)
#
#                     # Draw bounding box
#                     cv2.rectangle(processed_frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
#                     label = f"{self.classes[class_id]}: {int(confidence * 100)}%"
#                     cv2.putText(processed_frame, label, (x, y - 10),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
#
#                     detection_info.append({
#                         'class': self.classes[class_id],
#                         'confidence': confidence,
#                         'box': [x, y, w, h]
#                     })
#
#             # Store detection info for debugging
#             self.last_detections = detection_info
#
#         except Exception as e:
#             st.error(f"Detection error: {e}")
#             return False, frame, False, 0.0
#
#         # Update detection frame count
#         if bird_found_in_frame:
#             self.detection_frame_count += 1
#         else:
#             self.detection_frame_count = 0
#
#         confirmed_detection = self.detection_frame_count >= self.min_detection_frames
#
#         return confirmed_detection, processed_frame, bird_found_in_frame, highest_confidence
#
#
# class CameraManager:
#     def __init__(self):
#         self.cap = None
#         self.is_recording = False
#         self.video_writer = None
#         self.available_cameras = []
#         self.current_camera_info = ""
#         self.video_record_fps = 30
#         self.prev_frame = None  # Store previous frame for motion detection
#
#     def scan_available_cameras(self):
#         self.available_cameras = []
#         st.info("🔍 Scanning for cameras...")
#
#         for index in range(4):  # Reduced scan range for faster startup
#             try:
#                 cap = cv2.VideoCapture(index)
#                 if cap.isOpened():
#                     ret, frame = cap.read()
#                     if ret and frame is not None:
#                         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#                         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#                         fps = int(cap.get(cv2.CAP_PROP_FPS))
#
#                         camera_info = {
#                             'index': index,
#                             'resolution': f"{width}x{height}",
#                             'fps': fps,
#                             'name': f"Camera {index}" if index == 0 else f"USB Camera {index}"
#                         }
#                         self.available_cameras.append(camera_info)
#                         st.success(f"✅ Found {camera_info['name']} - {width}x{height}")
#                 cap.release()
#             except:
#                 pass
#
#         if not self.available_cameras:
#             st.error("❌ No cameras found!")
#         return self.available_cameras
#
#     def initialize_camera(self, camera_index=0):
#         if self.cap:
#             self.cap.release()
#             time.sleep(1)
#
#         try:
#             self.cap = cv2.VideoCapture(camera_index)
#             if self.cap.isOpened():
#                 # Set optimal resolution
#                 self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#                 self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#                 self.cap.set(cv2.CAP_PROP_FPS, 30)
#
#                 # Test the camera
#                 ret, frame = self.cap.read()
#                 if ret and frame is not None:
#                     actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#                     actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#                     self.current_camera_info = f"Camera {camera_index} - {actual_width}x{actual_height}"
#                     st.success(f"✅ Connected: {self.current_camera_info}")
#                     return True
#
#             st.error(f"❌ Failed to connect to Camera {camera_index}")
#             return False
#
#         except Exception as e:
#             st.error(f"❌ Camera error: {e}")
#             return False
#
#     def get_frame(self):
#         if self.cap and self.cap.isOpened():
#             ret, frame = self.cap.read()
#             if ret and frame is not None:
#                 # Store previous frame for motion detection
#                 if self.prev_frame is None:
#                     self.prev_frame = frame.copy()
#                 else:
#                     self.prev_frame = frame.copy()
#                 return frame
#         return None
#
#     def take_photo(self, frame, filename):
#         try:
#             timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             cv2.putText(frame, f"Bird Spotted: {timestamp}", (10, 30),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
#             cv2.imwrite(filename, frame)
#             return True
#         except Exception as e:
#             st.error(f"Failed to save photo: {e}")
#             return False
#
#     def start_recording(self, filename):
#         try:
#             if self.cap and self.cap.isOpened():
#                 width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#                 height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#             else:
#                 width, height = 640, 480
#
#             fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#             self.video_writer = cv2.VideoWriter(filename, fourcc, self.video_record_fps, (width, height))
#             self.is_recording = True
#             return True
#         except Exception as e:
#             st.error(f"Failed to start recording: {e}")
#             return False
#
#     def record_frame(self, frame):
#         if self.is_recording and self.video_writer and frame is not None:
#             self.video_writer.write(frame)
#
#     def stop_recording(self):
#         if self.video_writer:
#             self.video_writer.release()
#             self.video_writer = None
#         self.is_recording = False
#
#     def release(self):
#         if self.cap:
#             self.cap.release()
#         self.stop_recording()
#
#
# # Initialize session state
# if 'camera_manager' not in st.session_state:
#     st.session_state.camera_manager = CameraManager()
#     st.session_state.bird_detector = BirdDetector()
#     st.session_state.photos_taken = 0
#     st.session_state.videos_recorded = 0
#     st.session_state.birds_detected = 0
#     st.session_state.auto_capture_enabled = True
#     st.session_state.auto_record_enabled = False
#     st.session_state.last_photo_path = None
#     st.session_state.cameras_scanned = False
#     st.session_state.recording_start_time = None
#     st.session_state.show_debug = False
#
# # Auto-scan cameras on first load
# if not st.session_state.cameras_scanned:
#     with st.spinner("🔍 Setting up bird detection..."):
#         st.session_state.camera_manager.scan_available_cameras()
#         st.session_state.cameras_scanned = True
#
# # Main app header
# st.markdown('<h1 class="main-header">🐦 Enhanced Bird Spotter Pro 🐦</h1>', unsafe_allow_html=True)
#
# # Sidebar with stats and controls
# st.sidebar.markdown("### 📊 Your Bird Spotting Stats")
# col1, col2 = st.sidebar.columns(2)
# with col1:
#     st.metric("🔍 Birds Detected", st.session_state.birds_detected)
#     st.metric("📸 Photos Taken", st.session_state.photos_taken)
# with col2:
#     st.metric("🎥 Videos Recorded", st.session_state.videos_recorded)
#     model_status = "✅ AI" if st.session_state.bird_detector.model_loaded else "⚠️ Motion"
#     st.metric("Detection Mode", model_status)
#
# # Camera controls
# st.sidebar.markdown("### 🎮 Camera Controls")
#
# # Camera selection and connection
# available_cameras = st.session_state.camera_manager.available_cameras
# if available_cameras:
#     camera_names = [f"{cam['name']} ({cam['resolution']})" for cam in available_cameras]
#     selected_idx = st.sidebar.selectbox("Select Camera", range(len(camera_names)),
#                                         format_func=lambda x: camera_names[x])
#     camera_index = available_cameras[selected_idx]['index']
# else:
#     camera_index = st.sidebar.number_input("Camera Index", 0, 10, 0)
#
# if st.sidebar.button("🔧 Connect Camera"):
#     st.session_state.camera_manager.initialize_camera(camera_index)
#
# if st.sidebar.button("🔍 Rescan Cameras"):
#     st.session_state.camera_manager.scan_available_cameras()
#
# # Detection settings
# st.sidebar.markdown("### ⚙️ Detection Settings")
# confidence_threshold = st.sidebar.slider("Detection Sensitivity", 0.1, 0.9, 0.3, 0.05,
#                                          help="Lower = more sensitive (more false positives)")
# st.session_state.bird_detector.od_confidence_threshold = confidence_threshold
#
# min_frames = st.sidebar.slider("Confirmation Frames", 1, 5, 2,
#                                help="Frames needed to confirm bird detection")
# st.session_state.bird_detector.min_detection_frames = min_frames
#
# # Auto-capture settings
# st.sidebar.markdown("### 🤖 Auto-Capture")
# st.session_state.auto_capture_enabled = st.sidebar.checkbox("📸 Auto-Photo", value=True)
# st.session_state.auto_record_enabled = st.sidebar.checkbox("🎥 Auto-Record", value=False)
#
# capture_delay = st.sidebar.slider("Capture Cooldown (seconds)", 1, 10, 3)
# st.session_state.bird_detector.detection_cooldown = float(capture_delay)
#
# # Debug options
# st.sidebar.markdown("### 🔧 Debug")
# st.session_state.show_debug = st.sidebar.checkbox("Show Debug Info")
#
# # File management
# for folder in ["bird_photos", "bird_videos", "models"]:
#     if not os.path.exists(folder):
#         os.makedirs(folder)
#
# # Main content
# col1, col2 = st.columns([3, 1])
#
# with col1:
#     st.markdown("### 📹 Live Camera Feed")
#     video_placeholder = st.empty()
#     status_placeholder = st.empty()
#
#     if st.session_state.show_debug:
#         debug_placeholder = st.empty()
#
# with col2:
#     st.markdown("### 🎯 Controls")
#
#     manual_photo = st.button("📸 Take Photo", type="primary")
#     start_recording = st.button("🎥 Start Recording")
#
#     if st.button("🔄 Reset Stats"):
#         st.session_state.photos_taken = 0
#         st.session_state.videos_recorded = 0
#         st.session_state.birds_detected = 0
#         st.rerun()
#
#     # Show current status
#     auto_status = "✅ ON" if st.session_state.auto_capture_enabled else "❌ OFF"
#     st.write(f"**Auto-Photo:** {auto_status}")
#
#     record_status = "✅ ON" if st.session_state.auto_record_enabled else "❌ OFF"
#     st.write(f"**Auto-Record:** {record_status}")
#
#     # Show last photo
#     if st.session_state.last_photo_path and os.path.exists(st.session_state.last_photo_path):
#         st.markdown("### 📸 Latest Capture")
#         st.image(st.session_state.last_photo_path, use_column_width=True)
#
# # Camera status check
# if not (st.session_state.camera_manager.cap and st.session_state.camera_manager.cap.isOpened()):
#     st.warning("📹 Camera not connected. Use sidebar controls to connect a camera.")
#     st.info("💡 Make sure your camera isn't being used by another application!")
#     st.stop()
#
# # Main detection loop
# detection_active = True
# frame_count = 0
#
# while detection_active and st.session_state.camera_manager.cap.isOpened():
#     frame = st.session_state.camera_manager.get_frame()
#     if frame is None:
#         st.error("Failed to get camera frame")
#         break
#
#     frame_count += 1
#
#     # Manual photo capture
#     if manual_photo:
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         photo_path = os.path.join("bird_photos", f"manual_{timestamp}.jpg")
#         if st.session_state.camera_manager.take_photo(frame, photo_path):
#             st.session_state.photos_taken += 1
#             st.session_state.last_photo_path = photo_path
#             st.success("📸 Photo saved!")
#
#     # Bird detection
#     confirmed_bird, processed_frame, any_bird, confidence = st.session_state.bird_detector.detect_birds(
#         frame, st.session_state.camera_manager.prev_frame)
#
#     # Update display
#     if confirmed_bird:
#         status_placeholder.markdown(
#             '<div class="detection-status bird-detected"><h3>🐦 BIRD DETECTED! 🐦</h3></div>',
#             unsafe_allow_html=True)
#
#         # Count detection
#         if st.session_state.bird_detector.should_increment_bird_count():
#             st.session_state.birds_detected += 1
#
#         # Auto-capture
#         if st.session_state.auto_capture_enabled and st.session_state.bird_detector.should_auto_capture():
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             photo_path = os.path.join("bird_photos", f"auto_{timestamp}.jpg")
#             if st.session_state.camera_manager.take_photo(frame, photo_path):
#                 st.session_state.photos_taken += 1
#                 st.session_state.last_photo_path = photo_path
#                 st.success("📸 Auto-captured bird!")
#
#     elif any_bird:
#         status_placeholder.markdown(
#             '<div class="detection-status no-bird"><h3>🐦 Possible Bird (confirming...)</h3></div>',
#             unsafe_allow_html=True)
#     else:
#         status_placeholder.markdown(
#             '<div class="detection-status no-bird"><h3>👀 Watching for Birds...</h3></div>',
#             unsafe_allow_html=True)
#
#     # Show debug info
#     if st.session_state.show_debug:
#         debug_info = f"""
#         **Frame:** {frame_count}
#         **Detection Count:** {st.session_state.bird_detector.detection_frame_count}
#         **Confidence:** {confidence:.2f}
#         **Model Loaded:** {st.session_state.bird_detector.model_loaded}
#         **Recent Detections:** {len(st.session_state.bird_detector.last_detections)}
#         """
#         debug_placeholder.markdown(f'<div class="debug-info">{debug_info}</div>', unsafe_allow_html=True)
#
#     # Display frame
#     display_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
#     video_placeholder.image(display_frame, channels="RGB", use_column_width=True)
#
#     # Small delay to prevent overwhelming the display
#     time.sleep(0.1)
#
#     # Break after some time to prevent infinite loop in Streamlit
#     if frame_count > 1000:  # Reset after 1000 frames
#         st.rerun()
#
# # Cleanup
# if st.sidebar.button("🛑 Stop Camera"):
#     st.session_state.camera_manager.release()
#     st.success("Camera stopped. Refresh page to restart.")
#     st.stop()


import streamlit as st
import cv2
import numpy as np
import time
import os
from datetime import datetime
import requests
import tempfile

# Set page config for a fun, colorful interface
st.set_page_config(
    page_title="🐦 Bird Spotter Pro",
    page_icon="🐦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for teen-friendly styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .fun-metric {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .detection-status {
        font-size: 1.5rem;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    .bird-detected {
        background: linear-gradient(45deg, #95E1D3, #F38BA8);
        color: white;
        animation: pulse 1s infinite;
    }
    .no-bird {
        background: #F0F0F0;
        color: #666;
    }
    .auto-capture {
        background: linear-gradient(45deg, #FFD93D, #FF6B6B);
        color: white;
        animation: flash 0.5s infinite;
    }
    .debug-info {
        background: #E8F4FD;
        padding: 1rem;
        border-radius: 5px;
        font-family: monospace;
        font-size: 0.8rem;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    @keyframes flash {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    .stButton > button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)


class BirdDetector:
    def __init__(self):
        self.net = None
        self.classes = []
        self.bird_class_ids = []  # Support multiple bird-related classes
        self.od_confidence_threshold = 0.3  # Start with higher threshold
        self.detection_cooldown = 3.0
        self.min_detection_frames = 2  # Reduced for better responsiveness
        self.detection_frame_count = 0
        self.last_capture_time = 0
        self.last_bird_detection_count_time = 0
        self.model_loaded = False
        self.last_detections = []  # Store recent detections for debugging
        self.load_object_detector()

    def download_model_files(self):
        """Download YOLO model files if they don't exist"""
        model_dir = "models"
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        # Using YOLOv4-tiny for better performance and easier setup
        model_files = {
            "yolov4-tiny.weights": "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights",
            "yolov4-tiny.cfg": "https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg",
            "coco.names": "https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names"
        }

        for filename, url in model_files.items():
            filepath = os.path.join(model_dir, filename)
            if not os.path.exists(filepath):
                try:
                    st.info(f"📥 Downloading {filename}...")
                    response = requests.get(url, stream=True)
                    response.raise_for_status()

                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    st.success(f"✅ Downloaded {filename}")
                except Exception as e:
                    st.error(f"❌ Failed to download {filename}: {e}")
                    return False
        return True

    def load_object_detector(self):
        model_dir = "models"

        # Try to download model files if they don't exist
        if not self.download_model_files():
            st.error("Failed to download model files. Using fallback detection method.")
            return

        model_weights = os.path.join(model_dir, "yolov4-tiny.weights")
        model_config = os.path.join(model_dir, "yolov4-tiny.cfg")
        class_names_file = os.path.join(model_dir, "coco.names")

        st.info("🔍 Loading AI model for bird detection...")

        try:
            # Load YOLO model
            self.net = cv2.dnn.readNet(model_weights, model_config)
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

            # Load class names
            with open(class_names_file, 'rt') as f:
                self.classes = f.read().rstrip('\n').split('\n')

            # Find bird-related classes (COCO has class 14 for 'bird')
            bird_related_terms = ['bird']
            self.bird_class_ids = []

            for i, class_name in enumerate(self.classes):
                if any(term in class_name.lower() for term in bird_related_terms):
                    self.bird_class_ids.append(i)

            if self.bird_class_ids:
                st.success(
                    f"✅ AI model loaded! Bird detection ready (classes: {[self.classes[i] for i in self.bird_class_ids]})")
                self.model_loaded = True
            else:
                st.warning("⚠️ Model loaded but no bird classes found")

        except Exception as e:
            st.error(f"❌ Failed to load AI model: {e}")
            st.info("💡 Falling back to motion-based detection")
            self.model_loaded = False

    def detect_birds_simple_motion(self, frame, prev_frame):
        """Fallback motion-based detection when AI model fails"""
        if prev_frame is None:
            return False, frame, False, 0.0

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

        # Calculate frame difference
        diff = cv2.absdiff(gray, prev_gray)
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        processed_frame = frame.copy()

        for contour in contours:
            area = cv2.contourArea(contour)
            # Look for medium-sized moving objects (potential birds)
            if 500 < area < 10000:
                x, y, w, h = cv2.boundingRect(contour)
                # Check aspect ratio (birds are usually not too thin or too wide)
                aspect_ratio = w / h
                if 0.3 < aspect_ratio < 3.0:
                    motion_detected = True
                    cv2.rectangle(processed_frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                    cv2.putText(processed_frame, "Possible Bird Motion", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        return motion_detected, processed_frame, motion_detected, 0.8 if motion_detected else 0.0

    def should_auto_capture(self):
        current_time = time.time()
        if current_time - self.last_capture_time > self.detection_cooldown:
            self.last_capture_time = current_time
            return True
        return False

    def should_increment_bird_count(self):
        current_time = time.time()
        if current_time - self.last_bird_detection_count_time > self.detection_cooldown:
            self.last_bird_detection_count_time = current_time
            return True
        return False

    def detect_birds(self, frame, prev_frame=None):
        processed_frame = frame.copy()
        bird_found_in_frame = False
        highest_confidence = 0
        detection_info = []

        if not self.model_loaded:
            # Use motion-based fallback
            return self.detect_birds_simple_motion(frame, prev_frame)

        try:
            # Create blob from frame
            blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
            self.net.setInput(blob)

            # Get detections
            layer_outputs = self.net.forward(self.net.getUnconnectedOutLayersNames())

            boxes = []
            confidences = []
            class_ids = []

            h, w = frame.shape[:2]

            # Process each output layer
            for output in layer_outputs:
                for detection in output:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]

                    # Check if it's a bird class with sufficient confidence
                    if class_id in self.bird_class_ids and confidence > self.od_confidence_threshold:
                        center_x = int(detection[0] * w)
                        center_y = int(detection[1] * h)
                        width = int(detection[2] * w)
                        height = int(detection[3] * h)

                        x = int(center_x - width / 2)
                        y = int(center_y - height / 2)

                        boxes.append([x, y, width, height])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            # Apply non-maximum suppression
            indices = cv2.dnn.NMSBoxes(boxes, confidences, self.od_confidence_threshold, 0.4)

            if len(indices) > 0:
                bird_found_in_frame = True
                for i in indices.flatten():
                    x, y, w, h = boxes[i]
                    confidence = confidences[i]
                    class_id = class_ids[i]
                    highest_confidence = max(highest_confidence, confidence)

                    # Draw bounding box
                    cv2.rectangle(processed_frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    label = f"{self.classes[class_id]}: {int(confidence * 100)}%"
                    cv2.putText(processed_frame, label, (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                    detection_info.append({
                        'class': self.classes[class_id],
                        'confidence': confidence,
                        'box': [x, y, w, h]
                    })

            # Store detection info for debugging
            self.last_detections = detection_info

        except Exception as e:
            st.error(f"Detection error: {e}")
            return False, frame, False, 0.0

        # Update detection frame count
        if bird_found_in_frame:
            self.detection_frame_count += 1
        else:
            self.detection_frame_count = 0

        confirmed_detection = self.detection_frame_count >= self.min_detection_frames

        return confirmed_detection, processed_frame, bird_found_in_frame, highest_confidence


class CameraManager:
    def __init__(self):
        self.cap = None
        self.is_recording = False
        self.video_writer = None
        self.available_cameras = []
        self.current_camera_info = ""
        self.video_record_fps = 30
        self.prev_frame = None  # Store previous frame for motion detection

    def scan_available_cameras(self):
        self.available_cameras = []
        st.info("🔍 Scanning for cameras...")

        for index in range(4):  # Reduced scan range for faster startup
            try:
                cap = cv2.VideoCapture(index)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        fps = int(cap.get(cv2.CAP_PROP_FPS))

                        camera_info = {
                            'index': index,
                            'resolution': f"{width}x{height}",
                            'fps': fps,
                            'name': f"Camera {index}" if index == 0 else f"USB Camera {index}"
                        }
                        self.available_cameras.append(camera_info)
                        st.success(f"✅ Found {camera_info['name']} - {width}x{height}")
                cap.release()
            except:
                pass

        if not self.available_cameras:
            st.error("❌ No cameras found!")
        return self.available_cameras

    def initialize_camera(self, camera_index=0):
        if self.cap:
            self.cap.release()
            time.sleep(1)

        try:
            self.cap = cv2.VideoCapture(camera_index)
            if self.cap.isOpened():
                # Set optimal resolution
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.cap.set(cv2.CAP_PROP_FPS, 30)

                # Test the camera
                ret, frame = self.cap.read()
                if ret and frame is not None:
                    actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    self.current_camera_info = f"Camera {camera_index} - {actual_width}x{actual_height}"
                    st.success(f"✅ Connected: {self.current_camera_info}")
                    return True

            st.error(f"❌ Failed to connect to Camera {camera_index}")
            return False

        except Exception as e:
            st.error(f"❌ Camera error: {e}")
            return False

    def get_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret and frame is not None:
                # Store previous frame for motion detection
                if self.prev_frame is None:
                    self.prev_frame = frame.copy()
                else:
                    self.prev_frame = frame.copy()
                return frame
        return None

    def take_photo(self, frame, filename):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(frame, f"Bird Spotted: {timestamp}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.imwrite(filename, frame)
            return True
        except Exception as e:
            st.error(f"Failed to save photo: {e}")
            return False

    def start_recording(self, filename):
        try:
            if self.cap and self.cap.isOpened():
                width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            else:
                width, height = 640, 480

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_writer = cv2.VideoWriter(filename, fourcc, self.video_record_fps, (width, height))
            self.is_recording = True
            return True
        except Exception as e:
            st.error(f"Failed to start recording: {e}")
            return False

    def record_frame(self, frame):
        if self.is_recording and self.video_writer and frame is not None:
            self.video_writer.write(frame)

    def stop_recording(self):
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
        self.is_recording = False

    def release(self):
        if self.cap:
            self.cap.release()
        self.stop_recording()


# Initialize session state
if 'camera_manager' not in st.session_state:
    st.session_state.camera_manager = CameraManager()
    st.session_state.bird_detector = BirdDetector()
    st.session_state.photos_taken = 0
    st.session_state.videos_recorded = 0
    st.session_state.birds_detected = 0
    st.session_state.auto_capture_enabled = True
    st.session_state.auto_record_enabled = False
    st.session_state.last_photo_path = None
    st.session_state.cameras_scanned = False
    st.session_state.recording_start_time = None
    st.session_state.show_debug = False

# Auto-scan cameras on first load
if not st.session_state.cameras_scanned:
    with st.spinner("🔍 Setting up bird detection..."):
        st.session_state.camera_manager.scan_available_cameras()
        st.session_state.cameras_scanned = True

# Main app header
st.markdown('<h1 class="main-header">🐦 Enhanced Bird Spotter Pro 🐦</h1>', unsafe_allow_html=True)

# Sidebar with stats and controls
st.sidebar.markdown("### 📊 Your Bird Spotting Stats")
col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("🔍 Birds Detected", st.session_state.birds_detected)
    st.metric("📸 Photos Taken", st.session_state.photos_taken)
with col2:
    st.metric("🎥 Videos Recorded", st.session_state.videos_recorded)
    model_status = "✅ AI" if st.session_state.bird_detector.model_loaded else "⚠️ Motion"
    st.metric("Detection Mode", model_status)

# Camera controls
st.sidebar.markdown("### 🎮 Camera Controls")

# Camera selection and connection
available_cameras = st.session_state.camera_manager.available_cameras
if available_cameras:
    camera_names = [f"{cam['name']} ({cam['resolution']})" for cam in available_cameras]
    selected_idx = st.sidebar.selectbox("Select Camera", range(len(camera_names)),
                                        format_func=lambda x: camera_names[x])
    camera_index = available_cameras[selected_idx]['index']
else:
    camera_index = st.sidebar.number_input("Camera Index", 0, 10, 0)

if st.sidebar.button("🔧 Connect Camera"):
    st.session_state.camera_manager.initialize_camera(camera_index)

if st.sidebar.button("🔍 Rescan Cameras"):
    st.session_state.camera_manager.scan_available_cameras()

# Detection settings
st.sidebar.markdown("### ⚙️ Detection Settings")
confidence_threshold = st.sidebar.slider("Detection Sensitivity", 0.1, 0.9, 0.3, 0.05,
                                         help="Lower = more sensitive (more false positives)")
st.session_state.bird_detector.od_confidence_threshold = confidence_threshold

min_frames = st.sidebar.slider("Confirmation Frames", 1, 5, 2,
                               help="Frames needed to confirm bird detection")
st.session_state.bird_detector.min_detection_frames = min_frames

# Auto-capture settings
st.sidebar.markdown("### 🤖 Auto-Capture")
st.session_state.auto_capture_enabled = st.sidebar.checkbox("📸 Auto-Photo", value=True)
st.session_state.auto_record_enabled = st.sidebar.checkbox("🎥 Auto-Record", value=False)

capture_delay = st.sidebar.slider("Capture Cooldown (seconds)", 1, 10, 3)
st.session_state.bird_detector.detection_cooldown = float(capture_delay)

# Debug options
st.sidebar.markdown("### 🔧 Debug")
st.session_state.show_debug = st.sidebar.checkbox("Show Debug Info")

# File management
for folder in ["bird_photos", "bird_videos", "models"]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Main content
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### 📹 Live Camera Feed")
    video_placeholder = st.empty()
    status_placeholder = st.empty()

    if st.session_state.show_debug:
        debug_placeholder = st.empty()

with col2:
    st.markdown("### 🎯 Controls")

    manual_photo = st.button("📸 Take Photo", type="primary")
    start_recording = st.button("🎥 Start Recording")

    if st.button("🔄 Reset Stats"):
        st.session_state.photos_taken = 0
        st.session_state.videos_recorded = 0
        st.session_state.birds_detected = 0
        st.rerun()

    # Show current status
    auto_status = "✅ ON" if st.session_state.auto_capture_enabled else "❌ OFF"
    st.write(f"**Auto-Photo:** {auto_status}")

    record_status = "✅ ON" if st.session_state.auto_record_enabled else "❌ OFF"
    st.write(f"**Auto-Record:** {record_status}")

    # Show last photo
    if st.session_state.last_photo_path and os.path.exists(st.session_state.last_photo_path):
        st.markdown("### 📸 Latest Capture")
        st.image(st.session_state.last_photo_path, use_column_width=True)

# Camera status check
if not (st.session_state.camera_manager.cap and st.session_state.camera_manager.cap.isOpened()):
    st.warning("📹 Camera not connected. Use sidebar controls to connect a camera.")
    st.info("💡 Make sure your camera isn't being used by another application!")
    st.stop()

# Main detection loop
detection_active = True
frame_count = 0

while detection_active and st.session_state.camera_manager.cap.isOpened():
    frame = st.session_state.camera_manager.get_frame()
    if frame is None:
        st.error("Failed to get camera frame")
        break

    frame_count += 1

    # Manual photo capture
    if manual_photo:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        photo_path = os.path.join("bird_photos", f"manual_{timestamp}.jpg")
        if st.session_state.camera_manager.take_photo(frame, photo_path):
            st.session_state.photos_taken += 1
            st.session_state.last_photo_path = photo_path
            st.success("📸 Photo saved!")

    # Bird detection
    confirmed_bird, processed_frame, any_bird, confidence = st.session_state.bird_detector.detect_birds(
        frame, st.session_state.camera_manager.prev_frame)

    # Update display
    if confirmed_bird:
        status_placeholder.markdown(
            '<div class="detection-status bird-detected"><h3>🐦 BIRD DETECTED! 🐦</h3></div>',
            unsafe_allow_html=True)

        # Count detection
        if st.session_state.bird_detector.should_increment_bird_count():
            st.session_state.birds_detected += 1

        # Auto-capture
        if st.session_state.auto_capture_enabled and st.session_state.bird_detector.should_auto_capture():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            photo_path = os.path.join("bird_photos", f"auto_{timestamp}.jpg")
            if st.session_state.camera_manager.take_photo(frame, photo_path):
                st.session_state.photos_taken += 1
                st.session_state.last_photo_path = photo_path
                st.success("📸 Auto-captured bird!")

    elif any_bird:
        status_placeholder.markdown(
            '<div class="detection-status no-bird"><h3>🐦 Possible Bird (confirming...)</h3></div>',
            unsafe_allow_html=True)
    else:
        status_placeholder.markdown(
            '<div class="detection-status no-bird"><h3>👀 Watching for Birds...</h3></div>',
            unsafe_allow_html=True)

    # Show debug info
    if st.session_state.show_debug:
        debug_info = f"""
        **Frame:** {frame_count}
        **Detection Count:** {st.session_state.bird_detector.detection_frame_count}
        **Confidence:** {confidence:.2f}
        **Model Loaded:** {st.session_state.bird_detector.model_loaded}
        **Recent Detections:** {len(st.session_state.bird_detector.last_detections)}
        """
        debug_placeholder.markdown(f'<div class="debug-info">{debug_info}</div>', unsafe_allow_html=True)

    # Display frame
    display_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
    video_placeholder.image(display_frame, channels="RGB", use_column_width=True)

    # Small delay to prevent overwhelming the display
    time.sleep(0.1)

    # Break after some time to prevent infinite loop in Streamlit
    if frame_count > 1000:  # Reset after 1000 frames
        st.rerun()

# Cleanup
if st.sidebar.button("🛑 Stop Camera"):
    st.session_state.camera_manager.release()
    st.success("Camera stopped. Refresh page to restart.")
    st.stop()
