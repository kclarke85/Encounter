import streamlit as st
import cv2
import sounddevice as sd
import numpy as np
import subprocess
import threading
import time
import os

# --- Configuration ---
VIDEO_OUTPUT_DIR = "recordings"
if not os.path.exists(VIDEO_OUTPUT_DIR):
    os.makedirs(VIDEO_OUTPUT_DIR)

RECORDING_RESOLUTION = (640, 480) # Adjust for Pi Zero 2 W performance
RECORDING_FPS = 15                 # Adjust for Pi Zero 2 W performance
AUDIO_SAMPLERATE = 44100
AUDIO_CHANNELS = 2
RECORDING_DURATION_SECONDS = 30 # Duration for each recorded segment

# --- Global Variables for Recording Control ---
is_recording = False
recording_process = None
recording_filename = None
stop_event = threading.Event()

# --- Functions for Recording ---

def start_ffmpeg_recording():
    global recording_process, recording_filename, stop_event, is_recording

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    recording_filename = os.path.join(VIDEO_OUTPUT_DIR, f"recording_{timestamp}.mp4")

    # FFmpeg command for recording video and audio from USB camera and microphone
    # Adjust input devices as necessary.
    # On Pi, video often is /dev/video0, audio often hw:CARD=XXX,DEV=0 or similar.
    # You might need to use `arecord -L` to find your audio device name.
    ffmpeg_cmd = [
        "ffmpeg",
        "-f", "v4l2",             # Input format for video (Video4Linux2)
        "-i", "/dev/video0",      # Your USB camera device
        "-f", "alsa",             # Input format for audio (ALSA)
        "-i", "hw:CARD=USB,DEV=0", # Your USB microphone device (adjust as needed, e.g., 'hw:1,0')
        "-c:v", "h264_omx",       # Hardware accelerated H.264 encoding on Pi (if available and configured)
                                 # Otherwise, use "libx264" (CPU intensive)
        "-preset", "ultrafast",   # Speed preset for libx264 (if not using h264_omx)
        "-r", str(RECORDING_FPS),
        "-s", f"{RECORDING_RESOLUTION[0]}x{RECORDING_RESOLUTION[1]}",
        "-c:a", "aac",            # Audio codec
        "-b:a", "128k",           # Audio bitrate
        "-map", "0:v",            # Map video stream from input 0
        "-map", "1:a",            # Map audio stream from input 1
        "-t", str(RECORDING_DURATION_SECONDS), # Max duration for this segment
        "-y",                     # Overwrite output file without asking
        recording_filename
    ]

    st.info(f"Starting recording to: {recording_filename}")
    try:
        recording_process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        is_recording = True
        # Monitor the process in a separate thread to detect completion
        def monitor_recording():
            global is_recording, recording_process
            recording_process.wait() # Wait for ffmpeg to finish
            is_recording = False
            st.warning("Recording segment finished.") # This won't update the UI directly, but helpful for logs
        threading.Thread(target=monitor_recording, daemon=True).start()
    except Exception as e:
        st.error(f"Error starting recording: {e}")
        is_recording = False

def stop_ffmpeg_recording():
    global recording_process, is_recording
    if recording_process and recording_process.poll() is None: # If process is still running
        st.info("Stopping recording...")
        recording_process.terminate() # Send SIGTERM
        recording_process.wait(timeout=5) # Wait for it to terminate
        if recording_process.poll() is None:
            st.warning("Recording process did not terminate gracefully, killing it.")
            recording_process.kill() # Send SIGKILL if it doesn't terminate
        is_recording = False
        st.success("Recording stopped.")
    else:
        st.info("No active recording to stop.")

# --- Streamlit UI ---
st.set_page_config(page_title="Pi Camera Recorder", layout="centered")
st.title("Raspberry Pi Camera & Audio Recorder")

# --- Live Video (Snapshot based or very low FPS) ---
st.header("Live Camera Feed (Snapshot)")
video_placeholder = st.empty()

# This is a basic way to get a snapshot. For continuous, see note below.
# A more robust live feed would involve capturing frames in a separate thread
# and updating the placeholder. This will be resource-intensive.
try:
    cap = cv2.VideoCapture(0) # 0 for default camera
    if not cap.isOpened():
        st.error("Could not open video device. Check camera connection and permissions.")
    else:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            video_placeholder.image(frame, channels="RGB", width=RECORDING_RESOLUTION[0], caption="Current Snapshot")
        else:
            st.warning("Could not read frame from camera.")
    cap.release()
except Exception as e:
    st.error(f"Error accessing camera for snapshot: {e}")

st.markdown("""
<small>
    *Note: Live video embedding on a Pi Zero 2 W is very resource-intensive. 
    This is a snapshot, or will be a very low-FPS live stream. 
    For better performance, consider recording directly to file.*
</small>
""", unsafe_allow_html=True)


# --- Recording Controls ---
st.header("Record Video and Audio")

col1, col2 = st.columns(2)

if not is_recording:
    if col1.button("Start Recording"):
        start_ffmpeg_recording()
        st.experimental_rerun() # Rerun to update button state
else:
    if col2.button("Stop Recording"):
        stop_ffmpeg_recording()
        st.experimental_rerun() # Rerun to update button state

if is_recording:
    st.warning(f"Recording in progress... (segment will last {RECORDING_DURATION_SECONDS} seconds)")
    st.progress(0.0) # Placeholder, actual progress is hard to show without parsing ffmpeg output

# --- Recorded Files ---
st.header("Recorded Files")
recorded_files = [f for f in os.listdir(VIDEO_OUTPUT_DIR) if f.endswith(".mp4")]
if recorded_files:
    for f_name in sorted(recorded_files):
        file_path = os.path.join(VIDEO_OUTPUT_DIR, f_name)
        st.write(f"- {f_name}")
        with open(file_path, "rb") as file:
            st.download_button(
                label=f"Download {f_name}",
                data=file.read(),
                file_name=f_name,
                mime="video/mp4"
            )
        st.audio(file_path, format="video/mp4", start_time=0) # Can play video as audio if no video player
else:
    st.info("No recordings yet.")

# --- Persistent Live Stream (More Advanced & Resource Intensive) ---
# For a truly 'live' stream, you'd need a separate thread to continuously capture
# frames and send them to the Streamlit image placeholder. This would involve:
# 1. A producer thread that reads from cv2.VideoCapture and puts frames into a queue.
# 2. The main Streamlit thread periodically checking the queue and updating st.image.
# This will consume significant CPU and RAM on a Zero 2 W.
# Example (conceptual, not fully implemented for brevity and resource reasons):
#
# video_capture_thread_running = False
# video_frame_queue = queue.Queue(maxsize=1) # Use a small queue to drop old frames
#
# def capture_frames_live():
#     global video_capture_thread_running
#     cap_live = cv2.VideoCapture(0)
#     cap_live.set(cv2.CAP_PROP_FRAME_WIDTH, RECORDING_RESOLUTION[0])
#     cap_live.set(cv2.CAP_PROP_FRAME_HEIGHT, RECORDING_RESOLUTION[1])
#     cap_live.set(cv2.CAP_PROP_FPS, 5) # Very low FPS for live stream
#     while video_capture_thread_running:
#         ret, frame = cap_live.read()
#         if ret:
#             if not video_frame_queue.full():
#                 video_frame_queue.put(frame)
#         time.sleep(0.1) # Simulate low FPS
#     cap_live.release()
#
# if st.button("Start Live Stream (Experimental)"):
#     video_capture_thread_running = True
#     threading.Thread(target=capture_frames_live, daemon=True).start()
#
# if video_capture_thread_running:
#     if not video_frame_queue.empty():
#         live_frame = video_frame_queue.get()
#         live_frame = cv2.cvtColor(live_frame, cv2.COLOR_BGR2RGB)
#         video_placeholder.image(live_frame, channels="RGB", width=RECORDING_RESOLUTION[0])
#     # You'd need a loop or st.experimental_rerun() for continuous update
#     st.button("Stop Live Stream", on_click=lambda: setattr(__builtins__, 'video_capture_thread_running', False))