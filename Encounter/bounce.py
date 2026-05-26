# streamlit_app.py
import streamlit as st

st.title("Email Validation Dashboard")

uploaded_file = st.file_uploader("Upload your email CSV", type="csv")
if uploaded_file:
    email_list = load_email_csv(uploaded_file)
    st.write(f"Loaded {len(email_list)} emails")

    if st.button("Run Validation"):
        results_df = validate_email_list(email_list)
        st.dataframe(results_df)
