import streamlit as st
import pandas as pd
import json

# --- 1. CONFIGURATION AND UTILITY FUNCTIONS ---

# Use Streamlit's session state to track quiz scores
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False


def submit_quiz(answers, correct_answers):
    """Calculates quiz score and updates session state."""
    st.session_state.score = 0
    for key, correct_answer in correct_answers.items():
        if answers.get(key) == correct_answer:
            st.session_state.score += 1
    st.session_state.quiz_submitted = True


# --- 2. COURSE STRUCTURE & LAYOUT ---

st.set_page_config(
    page_title="QA Python Automation Course",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("📚 3-Day QA Automation Course")
selected_day = st.sidebar.selectbox(
    "Select Course Day",
    ["Day 1: Python Fundamentals (Beginner)", "Day 2: Automation Toolkit (Intermediate)",
     "Day 3: Scalability & CI/CD (Advanced)"]
)

st.title(f"🚀 {selected_day}")
st.markdown("---")

# --- 3. DAY 1 MODULE CONTENT ---

if selected_day == "Day 1: Python Fundamentals (Beginner)":

    # Navigation for Day 1 Modules
    lesson, structures, quiz = st.tabs([
        "1. Core Python & Logic",
        "2. Data Structures & I/O",
        "3. Quiz: Beginner Fundamentals"
    ])

    # --- 3.1 LESSON 1: CORE PYTHON & LOGIC ---
    with lesson:
        st.header("1. Core Python & Logic")
        st.subheader("💡 Variables and Data Types")
        st.markdown("""
        Variables store data. As a QA Engineer, you'll use them for things like storing credentials or expected test results.
        """)
        st.code("""
# String (text)
username = "qa_tester" 
# Integer (whole number)
expected_status_code = 200
# Boolean (True/False)
is_test_passed = True
        """)

        st.subheader("💡 Conditional Flow (`if/elif/else`)")
        st.markdown("This is how your scripts make **decisions** based on test results.")
        st.code("""
actual_status = 404
if actual_status == 200:
    st.success("Test Passed: Status is 200 OK.")
elif actual_status == 404:
    st.warning("Test Failed: Page Not Found.")
else:
    st.error("Test Failed: Unknown Error.")
        """)

        st.subheader("💡 Functions for Reusability")
        st.markdown(
            "Functions are essential for making your code **DRY** (Don't Repeat Yourself) by packaging reusable steps.")
        st.code("""
def check_login(user, password):
    # In a real test, this would interact with a browser
    if user == "admin" and password == "secure":
        return True
    return False

# Use the function
login_result = check_login("admin", "secure")
st.write(f"Login Result: {login_result}")
        """)

    # --- 3.2 LESSON 2: DATA STRUCTURES & I/O ---
    with structures:
        st.header("2. Data Structures & I/O")
        st.subheader("🗂️ Lists and Dictionaries")
        st.markdown("""
        * **Lists:** Ordered collections (e.g., a sequence of URLs to hit). Accessed by index (starting at 0).
        * **Dictionaries:** Key-value pairs (e.g., a config file). Accessed by key name.
        """)
        st.code("""
# Dictionary: Key-value pair for a user profile
user_data = {"username": "qa_user", "email": "test@example.com", "role": "admin"}
st.write("Accessing email:", user_data["email"])

# List: Ordered sequence of test inputs
test_inputs = ["A", "B", "C", "D"]
st.write("Accessing first input:", test_inputs[0])
        """)

        st.subheader("📄 File Handling (JSON Example)")
        st.markdown("As a QA, you'll constantly read **JSON** (API responses, config) and **CSV** (test data).")

        json_data = {
            "api_endpoint": "/v1/users",
            "expected_count": 5
        }

        # Display the JSON structure
        st.json(json_data)

        st.markdown("Here's how you load it in Python:")
        st.code("""
# Simulate loading JSON from a file
import json
data = json.dumps({"api_endpoint": "/v1/users", "expected_count": 5})

# Convert JSON string to Python dictionary
python_dict = json.loads(data) 

# Access the data
endpoint = python_dict['api_endpoint']
st.write(f"Endpoint loaded: {endpoint}")
        """)

    # --- 3.3 QUIZ: BEGINNER FUNDAMENTALS ---
    with quiz:
        st.header("3. Quiz: Beginner Fundamentals")
        st.markdown("Test your knowledge on Day 1 concepts!")

        # Define correct answers for the quiz
        quiz_key = {
            "q1": "def login():",
            "q2": "dictionary",
            "q3": 2,  # Index 2 is 'C'
            "q4": "400"
        }

        with st.form("day_1_quiz"):
            # Quiz Questions
            st.subheader("Question 1: Functions")
            q1 = st.radio("Which keyword is used to define a function in Python?",
                          ["function login()", "def login():", "func login()"], key='q1')

            st.subheader("Question 2: Data Structures")
            q2 = st.radio("Which Python data structure is best suited for storing user credentials as key-value pairs?",
                          ["list", "tuple", "dictionary"], key='q2')

            st.subheader("Question 3: List Indexing")
            st.markdown("Given the list `data = ['A', 'B', 'C', 'D']`, which index accesses the value 'C'?")
            q3 = st.radio("", [0, 1, 2, 3], key='q3')

            st.subheader("Question 4: Conditional Logic")
            st.markdown("What will the following code output if `status_code = 400`?")
            st.code("""
if status_code < 400:
    print("200s")
elif status_code == 400:
    print("400")
else:
    print("500s")
            """)
            q4 = st.text_input("Your expected output:", key='q4_text')

            submit_button = st.form_submit_button("Submit Quiz and See Results")

        if submit_button or st.session_state.quiz_submitted:

            # Re-map the text input answer for consistency
            user_answers = {
                "q1": q1,
                "q2": q2,
                "q3": q3,
                "q4": q4.strip()  # Remove any extra spaces
            }

            submit_quiz(user_answers, quiz_key)

            st.subheader("Quiz Results")
            max_score = len(quiz_key)
            if st.session_state.score == max_score:
                st.balloons()
                st.success(
                    f"Perfect Score! You got {st.session_state.score}/{max_score} correct. You are ready for Day 2.")
            elif st.session_state.score > max_score / 2:
                st.info(f"Great Job! You scored {st.session_state.score}/{max_score}. Review the missed questions.")
            else:
                st.warning(
                    f"You scored {st.session_state.score}/{max_score}. It is recommended to review Day 1 before proceeding.")

            # Display feedback
            if st.checkbox("Show Detailed Feedback"):
                for q, correct in quiz_key.items():
                    user_answer = user_answers.get(q, 'N/A')
                    is_correct = user_answer == correct
                    icon = "✅" if is_correct else "❌"

                    st.markdown(f"**{icon} {q.upper()}** - Your Answer: `{user_answer}` | Correct Answer: `{correct}`")

# --- 4. DAY 2 AND DAY 3 PLACEHOLDERS ---

# --- DAY 2 Placeholder ---
elif selected_day == "Day 2: Automation Toolkit (Intermediate)":
    st.header("🛠️ Intermediate: Automation Toolkit (WIP)")
    st.markdown("""
    This day focuses on integrating Python with automation tools.

    **Modules to be built:**
    * **Pytest:** Fixtures, Assertions.
    * **Selenium Core:** Locators (XPath, CSS), Basic Interactions.
    * **OOP & POM:** Implementing the Page Object Model structure.
    * **API Testing:** Using the `requests` library.

    *Challenge:* Install `pytest` and `selenium` and start writing your first browser launch fixture!
    """)

# --- DAY 3 Placeholder ---
elif selected_day == "Day 3: Scalability & CI/CD (Advanced)":
    st.header("🚀 Advanced: Scalability & CI/CD (WIP)")
    st.markdown("""
    This day focuses on optimizing and deploying your test suite.

    **Modules to be built:**
    * **Advanced Pytest:** Parameterization, Markers.
    * **Reporting:** Allure Reporter Integration.
    * **Optimization:** Parallel Execution (`pytest-xdist`), Headless Mode.
    * **CI/CD:** Basic GitHub Actions workflow integration.

    *Challenge:* Try creating a `.github/workflows/main.yml` file to run a basic `pytest` command.
    """)