import pyaudio
import picamera
import socket

# Socket configuration
HOST = ''  # Empty string indicates localhost
PORT = 8000

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open a microphone stream
microphone_stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

# Initialize PiCamera
camera = picamera.PiCamera()

# Set camera resolution (optional)
camera.resolution = (640, 480)

# Start camera preview (optional)
camera.start_preview()

# Create a socket and bind to the specified host and port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print("Waiting for a client connection...")

    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print("Client connected:", client_address)

    # Main loop to continuously stream audio and video
    try:
        while True:
            # Read audio data from the microphone
            audio_data = microphone_stream.read(1024)

            # Capture a frame from the camera
            camera.capture('image.jpg')

            # Send audio and video data to the client
            client_socket.sendall(audio_data)
            with open('image.jpg', 'rb') as image_file:
                image_data = image_file.read()
                client_socket.sendall(image_data)

    except KeyboardInterrupt:
        # Stop the microphone stream and close PyAudio
        microphone_stream.stop_stream()
        microphone_stream.close()
        audio.terminate()

        # Stop the camera preview
        camera.stop_preview()
