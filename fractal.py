import streamlit as st
import pyttsx3
import requests
from bs4 import BeautifulSoup


def text_to_speech(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # Female voice, you can change the index to select a different voice.
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"Text-to-speech error: {str(e)}")


def main():
    # Set the text color to blue
    st.markdown('<style>h1, .btn {color: blue;}</style>', unsafe_allow_html=True)

    # Newspaper-style header
    st.title("HIPPA Support APP")
    st.markdown("---")
    st.write(
        "Welcome to the HIPPA Support App. This app provides information and resources to help you understand and comply with HIPPA regulations.")

    # Text box for entering the healthcare URL
    url = st.text_input("Enter the healthcare URL:")

    # "Tell Me" button to trigger text-to-speech
    if st.button("Tell Me"):
        if url:
            try:
                # Fetch the page content
                response = requests.get(url)
                response.raise_for_status()  # Check for HTTP errors
                soup = BeautifulSoup(response.content, 'html.parser')
                text_content = soup.get_text()

                # Read the content aloud
                text_to_speech(text_content)
            except requests.exceptions.RequestException as e:
                st.error(f"Error: Unable to fetch the page content. {str(e)}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a healthcare URL.")


if __name__ == "__main__":
    main()
