# # import streamlit as st
# # import pyttsx3
# #
# #
# # def text_to_speech(text):
# #     engine = pyttsx3.init()
# #     engine.setProperty('rate', 150)
# #     voices = engine.getProperty('voices')
# #     engine.setProperty('voice', voices[1].id)  # Female voice, you can change the index to select a different voice.
# #     engine.say(text)
# #     engine.runAndWait()
# #
# #
# # def main():
# #     # Set the text color to blue
# #     st.markdown('<style>h1 {color: blue;}</style>', unsafe_allow_html=True)
# #
# #     # Newspaper-style header
# #     st.title("HIPPA Support APP")
# #     st.markdown("---")
# #     st.write(
# #         "Welcome to the HIPPA Support App. This app provides information and resources to help you understand and comply with HIPPA regulations. Lets get started")
# #
# #     # Add more content or functionality to the app below
# #
# #     # Start female voice and say "123" when the page loads
# #     if 'is_done' not in st.session_state:
# #         st.session_state.is_done = True
# #
# #         def speak_text():
# #             text = "Welcome, please use your wired or Bluetooth headphone. The content of this page will be read aloud for you. Any data sensitive information will be masked. Providing  an additional robust layer of data security.Lets get started"
# #             text_to_speech(text)
# #             st.session_state.is_done = False
# #
# #         speak_text()
# #
# #
# # if __name__ == "__main__":
# #     main()
# # #Above and below is working code
# import streamlit as st
# import pyttsx3
#
#
# def text_to_speech(text):
#     engine = pyttsx3.init()
#     engine.setProperty('rate', 150)
#     voices = engine.getProperty('voices')
#     engine.setProperty('voice', voices[1].id)  # Female voice
#     engine.say(text)
#     engine.runAndWait()
#
#
# def main():
#     # Set the text color to blue
#     st.markdown('<style>h1 {color: blue;}</style>', unsafe_allow_html=True)
#
#     # Newspaper-style header
#     st.title("HIPPA Support APP")
#     st.markdown("---")
#     st.write(
#         "Welcome to the HIPPA Support App. This app provides information and resources to help you understand and comply with HIPPA regulations. Let's get started")
#
#     # Start female voice and say "123" when the page loads
#     if 'is_done' not in st.session_state:
#         st.session_state.is_done = True
#
#         def speak_text():
#             text = "Welcome, please use your wired or Bluetooth headphone. The content of this page will be read aloud for you. Any data-sensitive information will be masked, providing an additional robust layer of data security. Let's get started"
#             text_to_speech(text)
#             st.session_state.is_done = False
#
#         speak_text()
#
#     # Input URL
#     url = st.text_input("Enter or search for the URL of the web page you want to visit:", value='', type='default')
#
#     if url:  # if URL is entered
#         if st.button('Go'):  # When 'Go' button is clicked
#             # Open the URL in a new tab
#             st.markdown(f'<a href="{url}" target="_blank">Click here to visit the website</a>', unsafe_allow_html=True)
#
# if __name__ == "__main__":
#     main()
# import streamlit as st
# import pyttsx3
#
# def text_to_speech(text):
#     try:
#         engine = pyttsx3.init()
#         engine.setProperty('rate', 150)
#         voices = engine.getProperty('voices')
#         engine.setProperty('voice', voices[1].id)  # Female voice
#         engine.say(text)
#         engine.runAndWait()
#     except Exception as e:
#         st.write("Error: Text-to-speech functionality is not supported in Streamlit.")
#         st.write(f"Exception: {str(e)}")
#
# def main():
#     # Set the text color to blue
#     st.markdown('<style>h1 {color: blue;}</style>', unsafe_allow_html=True)
#
#     # Newspaper-style header
#     st.title("HIPPA Support APP")
#     st.markdown("---")
#     st.write(
#         "Welcome to the HIPPA Support App. This app provides information and resources to help you understand and comply with HIPPA regulations. Let's get started")
#
#     # Start female voice and say "123" when the page loads
#     if 'is_done' not in st.session_state:
#         st.session_state.is_done = True
#
#         def speak_text():
#             text = "Welcome, please use your wired or Bluetooth headphone. The content of this page will be read aloud for you. Any data-sensitive information will be masked, providing an additional robust layer of data security. Let's get started"
#             text_to_speech(text)
#             st.session_state.is_done = False
#
#         speak_text()
#
#     # Input URL
#     url = st.text_input("Enter or search for the URL of the web page you want to visit:", value='', type='default')
#
#     if url:  # if URL is entered
#         if st.button('Go'):  # When 'Go' button is clicked
#             # Open the URL in a new tab
#             st.markdown(f'<a href="{url}" target="_blank">Click here to visit the website</a>', unsafe_allow_html=True)
#
# if __name__ == "__main__":
#     main()
import json
import subprocess
from tqdm import tqdm

def run_lighthouse(url):
    result = subprocess.run([
        "lighthouse",
        url,
        "--output=json",
        "--chrome-flags=--headless",
        "--quiet",
        "--only-categories=accessibility"
    ], capture_output=True)

    return json.loads(result.stdout)

def analyze_report(report):
    return report['categories']['accessibility']['score']

def main():
    urls = ["https://www.example1.com", "https://www.example2.com", "https://www.example3.com"]  # Replace with your own urls
    with open("index.txt", "w") as index_file:
        for url in tqdm(urls, desc="Scanning URLs for accessibility", unit="URL"):
            report = run_lighthouse(url)
            score = analyze_report(report)
            index_file.write(f"{url}: {score}\n")

if __name__ == "__main__":
    main()
