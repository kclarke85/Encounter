import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse

# --- UI Configuration ---
st.set_page_config(page_title="QA Scenario & Case Gen", layout="wide")


# --- 1. AI SCENARIO LOGIC ---
def get_ai_context(url):
    if not url:
        return "Waiting for URL...", "Please enter a target URL to begin the AI analysis and test case generation."

    domain = urlparse(url).netloc.lower()
    path = urlparse(url).path.lower()

    if any(k in domain or k in path for k in ['shop', 'store', 'cart', 'checkout', 'product']):
        scenario = "🛒 Scenario: E-Commerce Transactional Flow"
        objective = "Verify product selection, cart persistence, and the integrity of the checkout funnel."
    elif any(k in domain or k in path for k in ['login', 'signin', 'auth', 'account', 'profile']):
        scenario = "🔐 Scenario: User Authentication & Identity"
        objective = "Test credential validation, session management, and secure access to protected resources."
    elif any(k in domain or k in path for k in ['blog', 'article', 'news', 'post']):
        scenario = "📄 Scenario: Content Delivery & Readability"
        objective = "Audit SEO metadata, media rendering, and internal linking structure."
    elif any(k in domain or k in path for k in ['api', 'dev', 'docs', 'console']):
        scenario = "🔌 Scenario: Technical Documentation & API"
        objective = "Ensure technical accuracy, endpoint clarity, and developer experience (DX) consistency."
    else:
        scenario = f"🌐 Scenario: General Web Audit ({domain.split('.')[0].capitalize()})"
        objective = "Analyze DOM structure for functional accessibility and UI component responsiveness."

    return scenario, objective


# --- 2. HEADER SECTION ---
url_input = st.text_input("Enter URL to Scan:", placeholder="https://example.com")
scenario_title, scenario_objective = get_ai_context(url_input)

st.markdown(f"# {scenario_title}")
st.info(f"**Primary Testing Objective:** {scenario_objective}")
st.divider()


# --- 3. TEST CASE GENERATOR LOGIC ---
def generate_test_cases(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (QA Automation Bot)'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        page_name = soup.title.string.strip() if soup.title else "Unknown Page"
        test_cases = []

        # Find Interactive Elements: Inputs
        inputs = soup.find_all(['input', 'textarea', 'select'])
        for i, tag in enumerate(inputs):
            if tag.get('type') == 'hidden': continue
            name = tag.get('name') or tag.get('id') or tag.get('placeholder') or f"Field_{i}"
            scanned_html = str(tag)[:100] + ("..." if len(str(tag)) > 100 else "")

            test_cases.append({
                "Vcase ID": f"TC_IN_{i + 1:02d}",
                "Page": page_name,
                "Step Description": f"Input valid data into the '{name}' field.",
                "Expected Result": "Input is accepted; no validation error appears.",
                "Category": "Functional",
                "Scanned Element": scanned_html
            })

        # Find Interactive Elements: Actions
        actions = soup.find_all(['button', 'a'], limit=20)
        for i, act in enumerate(actions):
            text = act.get_text(strip=True) or act.get('value') or "Action/Link"
            if not text or len(text) > 50: continue
            scanned_html = str(act)[:100] + ("..." if len(str(act)) > 100 else "")

            test_cases.append({
                "Vcase ID": f"TC_ACT_{i + 1:02d}",
                "Page": page_name,
                "Step Description": f"Interact with the '{text}' element.",
                "Expected Result": "The application performs correctly.",
                "Category": "UI/UX",
                "Scanned Element": scanned_html
            })

        return page_name, test_cases
    except Exception as e:
        return None, str(e)


# --- 4. EXECUTION & RESULTS ---
if st.button("Generate Test Cases"):
    if url_input:
        with st.spinner('AI is analyzing the page structure...'):
            page_name, cases = generate_test_cases(url_input)
            if page_name:
                df = pd.DataFrame(cases)
                # Ensure correct column order
                cols = ["Vcase ID", "Page", "Step Description", "Expected Result", "Category", "Scanned Element"]
                st.session_state['test_df'] = df[cols]
                st.session_state['page_name'] = page_name
            else:
                st.error(f"Scan failed: {cases}")
    else:
        st.warning("Please provide a URL first.")

# Display results and additional actions if data exists
if 'test_df' in st.session_state:
    st.success(f"Successfully Analyzed: {st.session_state['page_name']}")
    st.dataframe(st.session_state['test_df'], use_container_width=True)

    # Export Button
    csv = st.session_state['test_df'].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Test Cases (CSV)",
        data=csv,
        file_name=f"test_cases_{st.session_state['page_name'].replace(' ', '_')}.csv",
        mime="text/csv"
    )

    st.divider()

    # --- 5. NEW ACTION BUTTONS ---
    st.subheader("Next Steps & Data Integration")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🛠️ Load Test Data", use_container_width=True):
            st.toast("Loading QA Environment datasets...")
            # Placeholder for future logic

    with col2:
        if st.button("🚀 Load Production Data", use_container_width=True):
            st.toast("Accessing anonymized production logs...")
            # Placeholder for future logic

    with col3:
        if st.button("🤖 Generate Playwright Script", use_container_width=True):
            st.toast("Generating .spec.ts automation file...")
            # Placeholder for future logic