import os
import time
import datetime
import webbrowser
import requests
import pythoncom
from win32com.client import Dispatch
import speech_recognition as sr
import google.generativeai as genai
import feedparser

# -----------------------
# Modular services
# -----------------------
from gmail_service import get_gmail_service, check_new_emails
from calendar_service import get_calendar_service, get_today_events

# -----------------------
# Configure Gemini API
# -----------------------
genai.configure(api_key="AIzaSyDamLtxG6mKcvTNyWwKwA4MBdWzb9LJzFA")

# -----------------------
# Speech Recognition
# -----------------------
recognizer = sr.Recognizer()
last_hourly_checkin = None
last_halfhour_checkin = None
last_45min_check = None

# -----------------------
# Text-to-Speech
# -----------------------
def speak(text: str):
    pythoncom.CoInitialize()
    engine = Dispatch("SAPI.SpVoice")
    for i in range(engine.GetVoices().Count):
        voice = engine.GetVoices().Item(i)
        if "Zira" in voice.GetDescription() or "Samantha" in voice.GetDescription():
            engine.Voice = voice
            break
    print(f"Agent: {text}")
    engine.Speak(text)

# -----------------------
# Speech Listening
# -----------------------
def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("🎤 Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            command = recognizer.recognize_google(audio).lower()
            print(f"🗣️ You said: {command}")
            return command
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return ""
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return ""

# -----------------------
# Gemini Integration
# -----------------------
def ask_gemini(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"You are Agent, a helpful female AI assistant. {prompt}")
        return response.text.strip()
    except Exception as e:
        return f"Gemini error: {e}"

# -----------------------
# Spanish Lesson Generator
# -----------------------
def spanish_lesson_prompt():
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            "You are a Spanish tutor. Create a 5-minute intermediate Spanish lesson "
            "for Kevin. Include vocabulary, short explanations, and at least 2 practice questions. "
            "Keep it practical, clear, and fun."
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Spanish lesson generation failed: {e}"

# -----------------------
# Spanish Lesson Check
# -----------------------
def check_45min_spanish_lesson():
    global last_45min_check
    now = datetime.datetime.now()
    if now.minute == 45 and (last_45min_check is None or last_45min_check.hour != now.hour):
        last_45min_check = now
        speak("Kevin, do you have time for a Spanish lesson?")
        command = listen()
        if "yes" in command or "sure" in command or "ok" in command:
            lesson = spanish_lesson_prompt()
            speak("Here’s your Spanish mini-lesson.")
            print("\n📘 === Spanish Mini-Lesson ===\n")
            print(lesson)
            # Speak first part only so it doesn’t cut off mid-text
            speak(lesson[:800])
        else:
            speak("No worries, we can do it later.")

# -----------------------
# Weather Lookup
# -----------------------
def get_weather(city="Cumming, Georgia"):
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=34.2073&longitude=-84.1402&current_weather=true"
        response = requests.get(url).json()
        temp_c = response["current_weather"]["temperature"]
        wind_kmh = response["current_weather"]["windspeed"]
        temp_f = round((temp_c * 9 / 5) + 32, 1)
        wind_mph = round(wind_kmh * 0.621371, 1)
        return f"The current temperature in {city} is {temp_f}°F with wind speed {wind_mph} mph."
    except Exception as e:
        return f"Weather lookup failed: {e}"

# -----------------------
# Get Google News Headlines
# -----------------------
def get_google_news():
    try:
        feed_url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(feed_url)

        if not feed.entries:
            return "No news headlines available at the moment."

        headlines = []
        for entry in feed.entries[:3]:
            title = entry.title
            if " - " in title:
                title = title.split(" - ")[0]
            headlines.append(title)

        if len(headlines) == 1:
            return f"Here's your top news headline: {headlines[0]}"
        else:
            return f"Here are your top {len(headlines)} news headlines: " + ". ".join(headlines)

    except Exception as e:
        return f"News lookup failed: {e}"

# -----------------------
# Half-Hour News Report
# -----------------------
def halfhour_news_report():
    news_info = get_google_news()
    speak(f"Hi Kevin, here's your half-hour news update. {news_info}")

# -----------------------
# Check for Half-Hour News
# -----------------------
def check_halfhour_news():
    global last_halfhour_checkin
    now = datetime.datetime.now()
    if now.minute == 30 and (last_halfhour_checkin is None or last_halfhour_checkin.hour != now.hour):
        last_halfhour_checkin = now
        halfhour_news_report()

# -----------------------
# Gmail Lookup
# -----------------------
def get_first_new_email():
    try:
        gmail = get_gmail_service()
        results = gmail.users().messages().list(userId="me", labelIds=["INBOX"], maxResults=1).execute()
        messages = results.get("messages", [])
        if not messages:
            return "No new emails."

        msg = messages[0]
        msg_data = gmail.users().messages().get(userId="me", id=msg["id"]).execute()
        headers = msg_data["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No subject")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown sender")

        if "<" in sender:
            sender = sender.split("<")[0].strip().strip('"')

        return f"Your most recent email is from {sender}, subject: {subject}"
    except Exception as e:
        return f"Email check failed: {e}"

# -----------------------
# Calendar Lookup
# -----------------------
def get_calendar_summary():
    try:
        from dateutil import parser
        calendar = get_calendar_service()
        now = datetime.datetime.utcnow().isoformat() + "Z"
        end = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + "Z"
        events_result = calendar.events().list(
            calendarId="primary", timeMin=now, timeMax=end,
            singleEvents=True, orderBy="startTime"
        ).execute()
        events = events_result.get("items", [])

        if not events:
            return "You have no events scheduled today."

        event_summaries = []
        for event in events[:3]:
            start = event["start"].get("dateTime", event["start"].get("date"))
            try:
                start_time = parser.parse(start).strftime("%I:%M %p")
            except Exception:
                start_time = "all day"
            event_summaries.append(f"{event['summary']} at {start_time}")

        if len(events) == 1:
            return f"You have one event today: {event_summaries[0]}"
        elif len(events) <= 3:
            return f"You have {len(events)} events today: " + ", ".join(event_summaries)
        else:
            return f"You have {len(events)} events today. The first three are: " + ", ".join(event_summaries)

    except Exception as e:
        return f"Calendar lookup failed: {e}"

# -----------------------
# Enhanced Hourly Report
# -----------------------
def hourly_report():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    weather_info = get_weather("Cumming, Georgia")
    email_info = get_first_new_email()
    calendar_info = get_calendar_summary()

    speak(f"Hi Kevin, it's a great day! The time is {current_time}. {weather_info} {email_info} {calendar_info}")

def check_hourly_checkin():
    global last_hourly_checkin
    now = datetime.datetime.now()
    if now.minute == 0 and (last_hourly_checkin is None or last_hourly_checkin.hour != now.hour):
        last_hourly_checkin = now
        hourly_report()

# -----------------------
# Built-in Commands
# -----------------------
def run_commands(command):
    if "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
        return True

    elif "weather" in command:
        speak(get_weather("Cumming, Georgia"))
        return True

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube.")
        return True

    elif "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google.")
        return True

    elif "open notepad" in command:
        os.system("notepad.exe")
        speak("Opening Notepad.")
        return True

    elif "play" in command or "music" in command:
        query = command.replace("play", "").replace("music", "").strip()
        if query:
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            webbrowser.open(url)
            speak(f"Playing {query} on YouTube.")
        else:
            webbrowser.open("https://music.youtube.com")
            speak("Opening YouTube Music.")
        return True

    elif "check email" in command or "gmail" in command:
        try:
            gmail = get_gmail_service()
            check_new_emails(gmail, speak)
        except Exception as e:
            speak(f"Gmail check failed: {e}")
        return True

    elif "calendar" in command or "schedule" in command:
        try:
            calendar = get_calendar_service()
            get_today_events(calendar, speak)
        except Exception as e:
            speak(f"Calendar lookup failed: {e}")
        return True

    elif "news" in command:
        speak(get_google_news())
        return True

    elif "quit" in command or "exit" in command or "stop" in command:
        speak("Goodbye.")
        exit()

    return False

# -----------------------
# Main Loop
# -----------------------
def run_Agent():
    speak("Agent is online. Say 'Agent' to wake me up.")
    wake_words = ["Agent", "la la"]

    while True:
        check_hourly_checkin()
        check_halfhour_news()
        check_45min_spanish_lesson()
        command = listen()
        if not command:
            continue
        if not any(wake in command for wake in wake_words):
            continue
        for wake in wake_words:
            command = command.replace(wake, "").strip()
        if command == "":
            speak("Yes? What can I do for you?")
            continue
        if not run_commands(command):
            reply = ask_gemini(command)
            speak(reply)

# -----------------------
# Entry Point
# -----------------------
if __name__ == "__main__":
    run_Agent()
