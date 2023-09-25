import cv2
import dropbox
import speech_recognition as sr

# Define word lists
POSITIVE_WORDS = ["good", "happy", "love", "great"]
NEGATIVE_WORDS = ["bad", "sad", "hate", "terrible"]

# For Dropbox
ACCESS_TOKEN = "sl.BjxXuHBZcWJjPHAD9uqzSliR-TVAAXj-gdCIaIEgpZvSDCpNcMe-GakHdW5zPpTnycfV8H_DeWRwazPd8iDVOJr3A5z4M7V9s4TcSz2ofNc4mYSdfSBUvyHYYGvkAMzntMG9vmEZb8zFImg8PRvFSuY"
dbx = dropbox.Dropbox(ACCESS_TOKEN)

# Recognizer for speech
recognizer = sr.Recognizer()

# Check for positive words
def has_positive(text):
    return any(word in text for word in POSITIVE_WORDS)


# Check for negative words
def has_negative(text):
    return any(word in text for word in NEGATIVE_WORDS)


# Record video and audio, and upload to Dropbox
def record_and_upload():
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

    with sr.Microphone() as source:
        while True:
            audio_data = recognizer.listen(source)
            try:
                # Using CMU Sphinx for speech recognition
                text = recognizer.recognize_sphinx(audio_data)

                if has_positive(text) and has_negative(text):
                    ret, frame = cap.read()
                    if not ret:
                        break
                    out.write(frame)

                    # Placeholder for checking the end of a conversation
                    if conversation_end():
                        break
            except sr.UnknownValueError:
                print("CMU Sphinx could not understand audio")
            except sr.RequestError:
                print("API unavailable")

    cap.release()
    out.release()

    with open("output.avi", "rb") as f:
        dbx.files_upload(f.read(), "/output.avi")


# Placeholder for determining the end of the conversation
def conversation_end():
    return False  # Placeholder


# Main function
if __name__ == "__main__":
    record_and_upload()
