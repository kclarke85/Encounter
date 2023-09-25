# # # # # from fuzzywuzzy import fuzz
# # # # # import speech_recognition as sr
# # # # # from transmit import *
# # # # # from drop import *
# # # # #
# # # # # def detect_negative_words(text):
# # # # #     negative_keywords = [
# # # # #         "no", "stop", "get out", "help", "You're wrong", "I don't have to",
# # # # #         "This is ridiculous", "I know my rights", "You can't do this"
# # # # #     ]
# # # # #
# # # # #     for word in negative_keywords:
# # # # #         similarity_ratio = fuzz.partial_ratio(word.lower(), text.lower())
# # # # #         if similarity_ratio > 50:
# # # # #
# # # # #             play_mp3()
# # # # #             record_audio_video () , upload_to_dropbox()
# # # # #
# # # # #     return False
# # # # #
# # # # # def detect_positive_words(text):
# # # # #     positive_keywords = [
# # # # #         "Please", "thank you", "Excuse me", "I apologize",
# # # # #         "may I", "good morning", "good night", "good evening"
# # # # #     ]
# # # # #
# # # # #     for word in positive_keywords:
# # # # #         similarity_ratio = fuzz.partial_ratio(word.lower(), text.lower())
# # # # #         if similarity_ratio > 50:
# # # # #
# # # # #
# # # # #             return True
# # # # #     return False
# # # # #
# # # # # r = sr.Recognizer()
# # # # #
# # # # # with sr.Microphone() as source:
# # # # #     print("Listening...")
# # # # #     audio = r.listen(source)
# # # # #
# # # # # try:
# # # # #     text = r.recognize_google(audio)
# # # # #     print("Transcription:", text)
# # # # #
# # # # #     # Save all transcribed text to 'audio_all.txt'
# # # # #     with open("audio_all.txt", "a") as file:
# # # # #         file.write(text + "\n")
# # # # #     print("Audio transcribed and saved to 'audio_all.txt'.")
# # # # #
# # # # #     if detect_negative_words(text):
# # # # #         with open("negative_keywords.txt", "a") as file:
# # # # #             file.write(text + "\n")
# # # # #         print("Negative keywords detected and saved to 'negative_keywords.txt'.")
# # # # #
# # # # #     if detect_positive_words(text):
# # # # #         with open("positive_keywords.txt", "a") as file:
# # # # #             file.write(text + "\n")
# # # # #         print("Positive keywords detected and saved to 'positive_keywords.txt'.")
# # # # #
# # # # # except sr.UnknownValueError:
# # # # #     print("Audio could not be understood.")
# # # # # except sr.RequestError as e:
# # # # #     print(f"Could not request results from Google Speech Recognition service; {e}")
# # # #
# # # # from fuzzywuzzy import fuzz
# # # # import speech_recognition as sr
# # # # from transmit import *
# # # # from drop import *
# # # # import time
# # # # import Send_SMS_Alert
# # # # def detect_negative_words(text):
# # # #     negative_keywords = [
# # # #         "no", "stop", "get out", "help", "You're wrong", "I don't have to",
# # # #         "This is ridiculous", "I know my rights", "You can't do this"
# # # #     ]
# # # #
# # # #     for word in negative_keywords:
# # # #         similarity_ratio = fuzz.partial_ratio(word.lower(), text.lower())
# # # #         if similarity_ratio > 50:
# # # #             time.sleep(3.3)
# # # #             # Stop recording, play MP3, and record audio/video
# # # #             play_mp3("transmit.mp3")
# # # #             record_audio_video("video_out.mp4", duration=10)
# # # #             upload_to_dropbox("video_out.mp4", "/Your/Folder/Dropbox","sl.Bj3CdkCUiviufiSmUWsiZ47TIdMAIUaU6sj-_t_v9zbW4k8v4oY0DjWaTfSmcXT-pzpJwZUFNRXMPGCsGrK0fyQJIUN813Y8q4hzmVOa7u0ysHAIINh3mNVhgDTQlLBiySHP71LO_NqBbnoAIU1jRyE")
# # # #             Send_SMS_Alert.send_sms("+16785201149")
# # # #
# # # #             # Save negative keyword detected to 'negative_keywords.txt'
# # # #             with open("negative_keywords.txt", "a") as file:
# # # #                 file.write(text + "\n")
# # # #             print("Negative keywords detected and saved to 'negative_keywords.txt'.")
# # # #             return True
# # # #
# # # #     return False
# # # #
# # # #
# # # # def detect_positive_words(text):
# # # #     positive_keywords = [
# # # #         "Please", "thank you", "Excuse me", "I apologize",
# # # #         "may I", "good morning", "good night", "good evening"
# # # #     ]
# # # #
# # # #     for word in positive_keywords:
# # # #         similarity_ratio = fuzz.partial_ratio(word.lower(), text.lower())
# # # #         if similarity_ratio > 50:
# # # #             return True
# # # #     return False
# # # #
# # # #
# # # # r = sr.Recognizer()
# # # #
# # # # with sr.Microphone() as source:
# # # #     print("Listening...")
# # # #     audio = r.listen(source)
# # # #
# # # # try:
# # # #     text = r.recognize_google(audio)
# # # #     print("Transcription:", text)
# # # #
# # # #     # Save all transcribed text to 'audio_all.txt'
# # # #     with open("audio_all.txt", "a") as file:
# # # #         file.write(text + "\n")
# # # #     print("Audio transcribed and saved to 'audio_all.txt'.")
# # # #
# # # #     # Detect negative words and perform the necessary actions
# # # #     if detect_negative_words(text):
# # # #         exit()  # Exit the program once negative keywords are detected and processed
# # # #
# # # #     # Detect positive words
# # # #     if detect_positive_words(text):
# # # #         with open("positive_keywords.txt", "a") as file:
# # # #             file.write(text + "\n")
# # # #         print("Positive keywords detected and saved to 'positive_keywords.txt'.")
# # # #
# # # # except sr.UnknownValueError:
# # # #     print("Audio could not be understood.")
# # # # except sr.RequestError as e:
# # # #     print(f"Could not request results from Google Speech Recognition service; {e}")
# # # #
# # # from fuzzywuzzy import fuzz
# # # import speech_recognition as sr
# # # from transmit import *
# # # from drop import *
# # # import time
# # # import Send_SMS_Alert
# # #
# # # def detect_negative_words(text):
# # #     negative_keywords = [
# # #         "no", "stop", "get out", "help", "You're wrong", "I don't have to",
# # #         "This is ridiculous", "I know my rights", "You can't do this"
# # #     ]
# # #
# # #     for word in negative_keywords:
# # #         similarity_ratio = fuzz.partial_ratio(word.lower(), text.lower())
# # #         if similarity_ratio > 50:
# # #             time.sleep(3.3)
# # #             # Stop recording, play MP3, and record audio/video
# # #             play_mp3("transmit.mp3")
# # #             record_audio_video("video_out.mp4", duration=10)
# # #             upload_to_dropbox("video_out.mp4", "/Your/Folder/Dropbox","sl.Bj3CdkCUiviufiSmUWsiZ47TIdMAIUaU6sj-_t_v9zbW4k8v4oY0DjWaTfSmcXT-pzpJwZUFNRXMPGCsGrK0fyQJIUN813Y8q4hzmVOa7u0ysHAIINh3mNVhgDTQlLBiySHP71LO_NqBbnoAIU1jRyE")
# # #             Send_SMS_Alert.send_sms("+16785201149")
# # #
# # #             # Save negative keyword detected to 'negative_keywords.txt'
# # #             with open("negative_keywords.txt", "a") as file:
# # #                 file.write(text + "\n")
# # #             print("Negative keywords detected and saved to 'negative_keywords.txt'.")
# # #             return True
# # #
# # #     return False
# # #
# # # def detect_positive_words(text):
# # #     positive_keywords = [
# # #         "Please", "thank you", "Excuse me", "I apologize",
# # #         "may I", "good morning", "good night", "good evening"
# # #     ]
# # #
# # #     for word in positive_keywords:
# # #         similarity_ratio = fuzz.partial_ratio(word.lower(), text.lower())
# # #         if similarity_ratio > 50:
# # #             return True
# # #     return False
# # #
# # # r = sr.Recognizer()
# # #
# # # with sr.Microphone() as source:
# # #     print("Listening...")
# # #     audio = r.listen(source)
# # #
# # # try:
# # #     text = r.recognize_google(audio)
# # #     print("Transcription:", text)
# # #
# # #     # Save all transcribed text to 'audio_all.txt'
# # #     with open("audio_all.txt", "a") as file:
# # #         file.write(text + "\n")
# # #     print("Audio transcribed and saved to 'audio_all.txt'.")
# # #
# # #     # Detect negative words and perform the necessary actions
# # #     if detect_negative_words(text):
# # #         exit()  # Exit the program once negative keywords are detected and processed
# # #
# # #     # Detect positive words
# # #     if detect_positive_words(text):
# # #         with open("positive_keywords.txt", "a") as file:
# # #             file.write(text + "\n")
# # #         print("Positive keywords detected and saved to 'positive_keywords.txt'.")
# # #
# # # except sr.UnknownValueError:
# # #     print("Audio could not be understood.")
# # # except sr.RequestError as e:
# # #     print(f"Could not request results from Google Speech Recognition service; {e}")
# # from fuzzywuzzy import fuzz
# # import speech_recognition as sr
# #
# # #from drop import *
# # #import time
# # import transmit
# # import camvid_out
# # def detect_negative_words(text):
# #     negative_keywords = ["This is ridiculous", "I know my rights", "You can't do this"]
# #
# #     for word in negative_keywords:
# #         similarity_ratio = fuzz.partial_ratio(word.lower(), text.lower())
# #         if similarity_ratio > 50:
# #             transmit.play_mp3("transmit.mp3")
# #             camvid_out.camvid("output.mp4")
# #             #time.sleep(3.3)
# #             # Stop recording, play MP3, and record audio/video
# #
# #
# #             #record_audio_video("video_out.mp4", duration=10)
# #             #upload_to_dropbox("video_out.mp4", "/Your/Folder/Dropbox","sl.BkC5wb1vmY-J54BEmmKRYtmLPObMoiyr0eZcfH8z8Aa_lKdhTb_XZE0sNy_9BVAdsYtmc8RUnPsG2jUYLxvuIT6aDk52NJdkqdVTBaiTXSMHiF1IZR5I0fyxPqOY0MyDOk83OttYrFgL-X6rEjgJZMU")
# #             # After all actions (including the upload), send the SMS
# #
# #             # Save negative keyword detected to 'negative_keywords.txt'
# #             with open("negative_keywords.txt", "a") as file:
# #                 file.write(text + "\n")
# #             print("Negative keywords detected and saved to 'negative_keywords.txt'.")
# #             return True
# #
# #     return False
# #
# #
# # def detect_positive_words(text):
# #     positive_keywords = [
# #         "Please", "thank you", "Excuse me", "I apologize",
# #         "may I", "good morning", "good night", "good evening"
# #     ]
# #
# #     for word in positive_keywords:
# #         similarity_ratio = fuzz.partial_ratio(word.lower(), text.lower())
# #         if similarity_ratio > 50:
# #             return True
# #     return False
# #
# # r = sr.Recognizer()
# #
# # with sr.Microphone() as source:
# #     print("Listening...")
# #     audio = r.listen(source)
# #
# # try:
# #     text = r.recognize_google(audio)
# #     print("Transcription:", text)
# #
# #     # Save all transcribed text to 'audio_all.txt'
# #     with open("audio_all.txt", "a") as file:
# #         file.write(text + "\n")
# #     print("Audio transcribed and saved to 'audio_all.txt'.")
# #
# #     # Detect negative words and perform the necessary actions
# #     if detect_negative_words(text):
# #         exit()  # Exit the program once negative keywords are detected and processed
# #
# #     # Detect positive words
# #     if detect_positive_words(text):
# #         with open("positive_keywords.txt", "a") as file:
# #             file.write(text + "\n")
# #         print("Positive keywords detected and saved to 'positive_keywords.txt'.")
# #
# # except sr.UnknownValueError:
# #     print("Audio could not be understood.")
# # except sr.RequestError as e:
# #     print(f"Could not request results from Google Speech Recognition service; {e}")
from fuzzywuzzy import fuzz, process
import speech_recognition as sr
import camvid_out
import transmit


def detect_negative_words(text):
    negative_keywords = [
      "No", "Step out of the car", "This is ridiculous", "I know my rights", "You can't do this"
    ]

    for word in negative_keywords:
        similarity_ratio = fuzz.partial_ratio(word.lower(), text.lower())
        if similarity_ratio > 70:
            with open("negative_keywords.txt", "a") as file:
                file.write(text + "\n")
            print("Negative keywords detected and saved to 'negative_keywords.txt'.")

            # Run program 1
            transmit.play_mp3('transmit.mp3')
            camvid_out.rec_vid()


            return True
    return False

def detect_positive_words(text):
    positive_keywords = [
        "Please", "thank you", "Excuse me", "I apologize",
        "may I", "good morning", "good night", "good evening"
    ]

    for word in positive_keywords:
        similarity_ratio = fuzz.partial_ratio(word.lower(), text.lower())
        if similarity_ratio > 5:
            return True
    return False

r = sr.Recognizer()

# Use a microphone as the audio source
with sr.Microphone() as source:
    print("Listening...")
    audio = r.listen(source)

try:
    # Transcribe the audio
    text = r.recognize_google(audio)
    print("Transcription:", text)

    # Log the transcribed text
    with open("audio_all.txt", "a") as file:
        file.write(text + "\n")
    print("Audio transcribed and saved to 'audio_all.txt'.")

    # Detect and handle negative words
    if detect_negative_words(text):
        exit()

    # Detect and log positive words
    if detect_positive_words(text):
        with open("positive_keywords.txt", "a") as file:
            file.write(text + "\n")
        print("Positive keywords detected and saved to 'positive_keywords.txt'.")

except sr.UnknownValueError:
    print("Audio could not be understood.")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")
