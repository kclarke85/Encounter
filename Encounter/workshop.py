import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="QA Powerhouse Tracker", layout="wide")

# --- DATA STRUCTURE BASED ON WORKFLOW ---
ROADMAP = {
    "Phase 1: Shift-Left Foundation": [
        "Three Amigos Requirement Shaping",
        "Jira-to-Agent Feedback Loop Configured",
        "Shift-Left Security (SAST/DAST) Integration"
    ],
    "Phase 2: MAS Orchestration": [
        "Deploy MAS Engine (Planner, Coder, Critic, Reporter)",
        "Autonomous Decision Making Setup",
        "Achieve 30-40% Manual Labor Reduction"
    ],
    "Phase 3: Playwright CI/CD": [
        "Automation Pyramid (Unit, API, UI) Implementation",
        "Visual Traces for Root Cause Analysis",
        "Self-Healing Execution (AI Locators)",
        "Smart Orchestration & Sharding in CI"
    ],
    "Phase 4: Balanced Quality": [
        "80% Automated Regression & Smoke Coverage",
        "High-Value Exploratory Testing & UX Auditing",
        "Unified AI-driven Dashboards"
    ]
}

# --- APP LOGIC ---
st.title("🚀 One-Man QA Powerhouse Tracker")
st.markdown("Transforming from Solo Tester to **Autonomous Quality Engineer**.")

# Initialize session state for tracking
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["Date", "Phase", "Milestone", "Status"])

# --- SIDEBAR: LOGGING ---
with st.sidebar:
    st.header("📌 Log Milestone")
    phase = st.selectbox("Current Phase", list(ROADMAP.keys()))
    milestone = st.selectbox("Milestone Achieved", ROADMAP[phase])
    date_achieved = st.date_input("Date", datetime.now())

    if st.button("Mark as Complete"):
        new_data = pd.DataFrame([[date_achieved, phase, milestone, "Completed"]],
                                columns=["Date", "Phase", "Milestone", "Status"])
        st.session_state.history = pd.concat([st.session_state.history, new_data]).drop_duplicates(subset=["Milestone"])
        st.success(f"Logged: {milestone}")

# --- DASHBOARD ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🛠️ Roadmap Progress")
    for p_name, tasks in ROADMAP.items():
        with st.expander(p_name, expanded=True):
            for t in tasks:
                is_done = t in st.session_state.history["Milestone"].values
                st.checkbox(t, value=is_done, key=t, disabled=True)

with col2:
    st.subheader("💰 Powerhouse ROI Meter")
    completed_count = len(st.session_state.history)
    total_tasks = sum(len(tasks) for tasks in ROADMAP.values())
    progress_pct = completed_count / total_tasks

    # ROI Calculation based on the $240k over 2 years from the image
    estimated_savings = progress_pct * 240000
    st.metric("Estimated Savings (2yr)", f"${estimated_savings:,.2f}",
              delta=f"{progress_pct:.0%} Roadmap Completion")

    st.info("""
    **Model Gains:**
    - Maintenance: High ➔ Low (AI Self-Healing)
    - Feedback: Reactive ➔ Proactive
    - Scalability: Linear ➔ Exponential
    """)

# --- WEEKLY/MONTHLY VIEW ---
st.divider()
st.subheader("📅 Activity Logs")
if not st.session_state.history.empty:
    df = st.session_state.history.copy()
    df['Date'] = pd.to_datetime(df['Date'])

    view_type = st.radio("View by:", ["All Time", "This Month", "This Week"], horizontal=True)

    now = datetime.now()
    if view_type == "This Month":
        df = df[df['Date'].dt.month == now.month]
    elif view_type == "This Week":
        start_week = now - timedelta(days=now.weekday())
        df = df[df['Date'] >= pd.Timestamp(start_week.date())]

    st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)
else:
    st.write("No milestones logged yet. Start from the sidebar!")