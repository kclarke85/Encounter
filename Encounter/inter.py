import streamlit as st
import random

st.set_page_config(page_title="SQL Flashcard Tutor", page_icon="🧠")

st.title("🧠 SQL Flashcard Tutor")
st.write("Practice SQL from beginner to advanced using flashcards. Reveal answers, switch levels, and drill yourself before your interview.")

# ---------------------------------------------------------
# FLASHCARD DATA (ALL LEVELS COMBINED)
# ---------------------------------------------------------
FLASHCARDS = {
    "Beginner": [
        {
            "question": "Select all columns from a table named employees.",
            "answer": "SELECT * FROM employees;"
        },
        {
            "question": "Select name and salary from employees.",
            "answer": "SELECT name, salary FROM employees;"
        },
        {
            "question": "Return all rows where department = 'Sales'.",
            "answer": "SELECT * FROM employees WHERE department = 'Sales';"
        },
        {
            "question": "Return unique department values.",
            "answer": "SELECT DISTINCT department FROM employees;"
        },
        {
            "question": "Sort employees by salary descending.",
            "answer": "SELECT * FROM employees ORDER BY salary DESC;"
        },
    ],

    "Intermediate": [
        {
            "question": "Count employees in each department.",
            "answer": "SELECT department, COUNT(*) FROM employees GROUP BY department;"
        },
        {
            "question": "Average salary per department (only departments with >5 employees).",
            "answer": "SELECT department, AVG(salary) FROM employees GROUP BY department HAVING COUNT(*) > 5;"
        },
        {
            "question": "Employees with salary between 50k and 80k.",
            "answer": "SELECT * FROM employees WHERE salary BETWEEN 50000 AND 80000;"
        },
        {
            "question": "Employees whose name starts with 'A'.",
            "answer": "SELECT * FROM employees WHERE name LIKE 'A%';"
        },
        {
            "question": "Top 3 highest paid employees.",
            "answer": "SELECT * FROM employees ORDER BY salary DESC LIMIT 3;"
        },
    ],

    "Joins": [
        {
            "question": "Inner join employees with departments on department_id.",
            "answer": "SELECT e.*, d.name AS department_name FROM employees e INNER JOIN departments d ON e.department_id = d.id;"
        },
        {
            "question": "Left join employees with departments (keep all employees).",
            "answer": "SELECT e.*, d.name FROM employees e LEFT JOIN departments d ON e.department_id = d.id;"
        },
        {
            "question": "Right join example (keep all departments).",
            "answer": "SELECT e.*, d.name FROM employees e RIGHT JOIN departments d ON e.department_id = d.id;"
        },
        {
            "question": "Full outer join example.",
            "answer": "SELECT e.*, d.name FROM employees e FULL OUTER JOIN departments d ON e.department_id = d.id;"
        },
        {
            "question": "Self‑join: find employees who share the same manager.",
            "answer": "SELECT e1.name, e2.name FROM employees e1 JOIN employees e2 ON e1.manager_id = e2.manager_id;"
        },
    ],

    "Window Functions": [
        {
            "question": "Add row numbers ordered by salary descending.",
            "answer": "SELECT name, salary, ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn FROM employees;"
        },
        {
            "question": "Running total of salary ordered by hire date.",
            "answer": "SELECT name, salary, SUM(salary) OVER (ORDER BY hire_date) AS running_total FROM employees;"
        },
        {
            "question": "Show each employee with department average salary.",
            "answer": "SELECT name, salary, AVG(salary) OVER (PARTITION BY department_id) AS dept_avg FROM employees;"
        },
        {
            "question": "Rank employees by salary within each department.",
            "answer": "SELECT name, salary, RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dept_rank FROM employees;"
        },
        {
            "question": "Difference between employee salary and department average.",
            "answer": "SELECT name, salary, salary - AVG(salary) OVER (PARTITION BY department_id) AS diff FROM employees;"
        },
    ],

    "Optimization": [
        {
            "question": "Find rows where an index will be used (simple equality).",
            "answer": "SELECT * FROM employees WHERE employee_id = 123;"
        },
        {
            "question": "Avoid SELECT * for performance — rewrite this query.",
            "answer": "SELECT name, salary FROM employees WHERE department_id = 10;"
        },
        {
            "question": "Rewrite a slow subquery using a join.",
            "answer": "SELECT e.* FROM employees e JOIN departments d ON e.department_id = d.id WHERE d.name = 'Sales';"
        },
        {
            "question": "Use EXISTS instead of IN for better performance.",
            "answer": "SELECT * FROM employees e WHERE EXISTS (SELECT 1 FROM departments d WHERE d.id = e.department_id);"
        },
        {
            "question": "Why does '%abc' break index usage?",
            "answer": "Because leading wildcards prevent index use; 'abc%' can use an index."
        },
    ],

    "Advanced": [
        {
            "question": "Employees whose salary is above the overall average.",
            "answer": "SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);"
        },
        {
            "question": "Second highest distinct salary.",
            "answer": "SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);"
        },
        {
            "question": "Find duplicates based on email.",
            "answer": "SELECT email, COUNT(*) FROM employees GROUP BY email HAVING COUNT(*) > 1;"
        },
        {
            "question": "CTE: employees with salary above department average.",
            "answer": "WITH dept_avg AS (SELECT department_id, AVG(salary) AS avg_sal FROM employees GROUP BY department_id) SELECT e.* FROM employees e JOIN dept_avg d ON e.department_id = d.department_id WHERE e.salary > d.avg_sal;"
        },
        {
            "question": "Recursive CTE: get all subordinates of a manager.",
            "answer": "WITH RECURSIVE subordinates AS (SELECT id, manager_id FROM employees WHERE manager_id = 10 UNION ALL SELECT e.id, e.manager_id FROM employees e JOIN subordinates s ON e.manager_id = s.id) SELECT * FROM subordinates;"
        },
    ],
}

# ---------------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------------
if "current_level" not in st.session_state:
    st.session_state.current_level = "Beginner"
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

def load_new_card(randomize=True):
    cards = FLASHCARDS[st.session_state.current_level]
    if randomize:
        st.session_state.current_index = random.randint(0, len(cards) - 1)
    else:
        st.session_state.current_index = (st.session_state.current_index + 1) % len(cards)
    st.session_state.show_answer = False

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.header("Settings")
level = st.sidebar.selectbox(
    "Difficulty level",
    list(FLASHCARDS.keys()),
    index=list(FLASHCARDS.keys()).index(st.session_state.current_level),
)

if level != st.session_state.current_level:
    st.session_state.current_level = level
    load_new_card(randomize=True)

random_mode = st.sidebar.checkbox("Random card each time", value=True)

# ---------------------------------------------------------
# MAIN UI
# ---------------------------------------------------------
cards = FLASHCARDS[st.session_state.current_level]
card = cards[st.session_state.current_index]

st.subheader(f"Level: {st.session_state.current_level}")
st.markdown("### ❓ Question")
st.code(card["question"], language="sql")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Show / Hide Answer"):
        st.session_state.show_answer = not st.session_state.show_answer

with col2:
    if st.button("Next Card"):
        load_new_card(randomize=random_mode)

with col3:
    if st.button("Restart Level"):
        st.session_state.current_index = 0
        st.session_state.show_answer = False

if st.session_state.show_answer:
    st.markdown("### ✅ Answer")
    st.code(card["answer"], language="sql")

st.markdown("---")
st.write("Add more cards anytime by editing the FLASHCARDS dictionary.")
