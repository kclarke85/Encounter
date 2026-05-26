# streamlit_selenium_recorder.py
import streamlit as st
import threading
import time
import uuid
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# --- Session State ---
if 'recording' not in st.session_state:
    st.session_state.recording = False
if 'test_steps' not in st.session_state:
    st.session_state.test_steps = []
if 'test_case_output' not in st.session_state:
    st.session_state.test_case_output = None
if 'test_case_id' not in st.session_state:
    st.session_state.test_case_id = ""

# --- IEEE Test Case Generator ---
def generate_ieee_test_case(steps):
    test_case_id = f"TC-{uuid.uuid4().hex[:8].upper()}"
    st.session_state.test_case_id = test_case_id

    procedure_table = "| Step | Action | Expected Result |\n| :--- | :--- | :--- |\n"
    for i, step in enumerate(steps, 1):
        procedure_table += f"| {i} | {step} | (Auto-generated) |\n"

    markdown_output = f"""
# QA Test Case Specification

**Test Case ID**: `{test_case_id}`
**Date Created**: `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`

### 8. Test Procedure (Recorded Actions)

{procedure_table}
"""
    return markdown_output

# --- Selenium Recorder Thread ---
def run_selenium(url):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # Inject JS listeners
    driver.execute_script("""
        window.recordedEvents = [];
        document.addEventListener('click', function(e) {
            let text = e.target.innerText || e.target.value || e.target.name || e.target.id;
            window.recordedEvents.push("Then user clicks '" + text + "'");
        }, true);
        document.addEventListener('input', function(e) {
            if(e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                let name = e.target.name || e.target.id || e.target.placeholder || 'field';
                window.recordedEvents.push("When user enters '" + e.target.value + "' in '" + name + "'");
            }
        }, true);
    """)

    st.session_state.test_steps.append(f"Given user is on '{driver.title}' page")

    while st.session_state.recording:
        events = driver.execute_script("let ev=window.recordedEvents; window.recordedEvents=[]; return ev;")
        if events:
            st.session_state.test_steps.extend(events)
        time.sleep(0.5)

    driver.quit()

# --- Streamlit UI ---
st.title("📝 QA Test Case Writer + Cucumber Recorder")

if not st.session_state.recording:
    url = st.text_input("Enter URL to test", "https://example.com")
    if st.button("Start Recording"):
        st.session_state.test_steps = []
        st.session_state.recording = True
        threading.Thread(target=run_selenium, args=(url,), daemon=True).start()

else:
    if st.button("Stop Recording"):
        st.session_state.recording = False
        st.session_state.test_case_output = generate_ieee_test_case(st.session_state.test_steps)

if st.session_state.test_steps:
    st.subheader("Recorded Steps (Cucumber Format)")
    for i, step in enumerate(st.session_state.test_steps, 1):
        st.write(f"{i}. {step}")

if st.session_state.test_case_output:
    st.subheader("Generated IEEE Test Case")
    st.markdown(st.session_state.test_case_output)
    st.download_button(
        "Download Test Case as Markdown",
        st.session_state.test_case_output,
        file_name=f"{st.session_state.test_case_id}.md",
        mime="text/markdown"
    )
