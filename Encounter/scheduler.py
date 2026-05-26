import streamlit as st
import pandas as pd
import time
import io

# --- Session State Initialization ---
def initialize_session_state():
    if 'email_df' not in st.session_state:
        st.session_state.email_df = pd.DataFrame(columns=['Email'])
    if 'company_df' not in st.session_state:
        st.session_state.company_df = pd.DataFrame(columns=['Company'])
    if 'scheduler_running' not in st.session_state:
        st.session_state.scheduler_running = False
    if 'last_sent_index' not in st.session_state:
        st.session_state.last_sent_index = 0
    if 'last_run_time' not in st.session_state:
        st.session_state.last_run_time = None
    if 'num_emails_to_send' not in st.session_state:
        st.session_state.num_emails_to_send = 1
    if 'interval_minutes' not in st.session_state:
        # Initialize interval_minutes as a float to match min_value and step
        st.session_state.interval_minutes = 1.0
    if 'status_message_placeholder' not in st.session_state:
        st.session_state.status_message_placeholder = None

initialize_session_state()

# --- Page Configuration ---
st.set_page_config(
    page_title="Email Scheduler",
    page_icon="📧",
    layout="centered"
)

# --- Header Section ---
st.image("https://media.istockphoto.com/id/2188188739/photo/planning-and-scheduling-meeting-calendars-activities-time-management-notifications-and.webp?a=1&b=1&s=612x612&w=0&k=20&c=d9TDGqaISASio8pftFdQLw7VF0pJ9hgwTsnOsWMPDy8=",
         caption="Efficient Email Scheduling",
         use_container_width=True)

st.title("📧 Automated Email Sender Scheduler")
st.markdown("""
This application allows you to schedule the sending of emails in batches.
Upload your email list, configure the sending parameters, and hit start!
""")

# --- Data Input Section ---
st.header("1. Upload or Paste Your Data")

tab1, tab2 = st.tabs(["Upload CSV Files", "Paste Text Data"])

with tab1:
    st.subheader("Upload CSV Files")
    email_file = st.file_uploader("Upload Email Addresses CSV (e.g., 'email@example.com')", type=["csv"], key="email_csv_upload")
    company_file = st.file_uploader("Upload Company Names CSV (e.g., 'Company A')", type=["csv"], key="company_csv_upload")

    if st.button("Load Uploaded CSVs", key="load_csv_button"):
        if email_file is not None:
            try:
                df_temp_email = pd.read_csv(email_file, header=None, names=['Email'])
                # Remove duplicates for emails
                st.session_state.email_df = df_temp_email.drop_duplicates(subset=['Email']).reset_index(drop=True)
                st.success(f"Email CSV loaded successfully! Removed {len(df_temp_email) - len(st.session_state.email_df)} duplicate(s).")
            except Exception as e:
                st.error(f"Error loading email CSV: {e}")
        else:
            st.warning("Please upload an Email CSV file.")

        if company_file is not None:
            try:
                df_temp_company = pd.read_csv(company_file, header=None, names=['Company'])
                # Remove duplicates for companies
                st.session_state.company_df = df_temp_company.drop_duplicates(subset=['Company']).reset_index(drop=True)
                st.success(f"Company CSV loaded successfully! Removed {len(df_temp_company) - len(st.session_state.company_df)} duplicate(s).")
            except Exception as e:
                st.error(f"Error loading company CSV: {e}")
        else:
            st.info("No Company CSV uploaded. This is optional.")

with tab2:
    st.subheader("Paste Text Data (One entry per line)")
    email_text = st.text_area("Paste Email Addresses (one per line)", height=150, key="email_text_area")
    company_text = st.text_area("Paste Company Names (one per line)", height=150, key="company_text_area")

    if st.button("Load Pasted Data", key="load_text_button"):
        if email_text:
            emails = [line.strip() for line in email_text.split('\n') if line.strip()]
            df_temp_email = pd.DataFrame(emails, columns=['Email'])
            # Remove duplicates for emails
            st.session_state.email_df = df_temp_email.drop_duplicates(subset=['Email']).reset_index(drop=True)
            st.success(f"Email data pasted successfully! Removed {len(df_temp_email) - len(st.session_state.email_df)} duplicate(s).")
        else:
            st.warning("Please paste email addresses.")

        if company_text:
            companies = [line.strip() for line in company_text.split('\n') if line.strip()]
            df_temp_company = pd.DataFrame(companies, columns=['Company'])
            # Remove duplicates for companies
            st.session_state.company_df = df_temp_company.drop_duplicates(subset=['Company']).reset_index(drop=True)
            st.success(f"Company data pasted successfully! Removed {len(df_temp_company) - len(st.session_state.company_df)} duplicate(s).")
        else:
            st.info("No company data pasted. This is optional.")

# --- Display Loaded Data ---
st.header("2. Loaded Data Preview")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Email Addresses")
    if not st.session_state.email_df.empty:
        st.dataframe(st.session_state.email_df, use_container_width=True)
        # Display record count
        st.write(f"Total unique emails loaded: **{len(st.session_state.email_df)}**")
    else:
        st.info("No email addresses loaded yet.")

with col2:
    st.subheader("Company Names (Optional)")
    if not st.session_state.company_df.empty:
        st.dataframe(st.session_state.company_df, use_container_width=True)
        # Display record count
        st.write(f"Total unique companies loaded: **{len(st.session_state.company_df)}**")
    else:
        st.info("No company names loaded yet.")

# --- Scheduler Configuration ---
st.header("3. Scheduler Settings")
st.session_state.num_emails_to_send = st.number_input(
    "Number of emails to send per batch (x)",
    min_value=1,
    value=st.session_state.num_emails_to_send,
    step=1,
    help="Number of emails to send in each interval."
)
st.session_state.interval_minutes = st.number_input(
    "Interval in minutes (y)",
    min_value=0.1, # Allow for faster testing
    value=st.session_state.interval_minutes,
    step=0.1,
    help="Time interval between sending batches (in minutes)."
)

# --- Email Content Definition ---
email_subject = "NYC LL 144: Your Annual AEDT Audit simplified."
email_body_html = """
<p>Hi there — NYC Local Law 144 is enforced: companies risk $500–$1,500 daily fines for non-compliance.
We’ll get you compliant in 48 hours.</p>

<p><strong>Reply now to lock in your audit and avoid fines — it’s that simple.</strong></p>

<p>Please see the attached PDF for more details.</p>

<p>
K. Clarke<br>
<a href="https://app.encounter-engineering.com/" target="_blank" style="color: #007bff; text-decoration: none;">Encounter Engineering</a><br>
470-404-5798
</p>

<img src="https://hook.us2.make.com/lne3c93vv0dajq9hkkym9j8dkver1ggs?UID={{EmailUUID}}" width="1" height="1" style="display:none;">
"""

# --- Simulate PDF Attachment Download ---
st.header("5. Simulated Attachment")
st.markdown("In a real email, a PDF would be attached. For demonstration, you can download a dummy PDF here:")
dummy_pdf_content = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj 3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Contents 4 0 R/Parent 2 0 R>>endobj 4 0 obj<</Length 100>>stream\nBT /F1 24 Tf 100 700 Td (This is a dummy PDF for demonstration.) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000055 00000 n\n0000000109 00000 n\n0000000200 00000 n\ntrailer<</Size 5/Root 1 0 R>>startxref\n300\n%%EOF"
st.download_button(
    label="Download Dummy PDF",
    data=dummy_pdf_content,
    file_name="NYC_LL_144_Details.pdf",
    mime="application/pdf",
    help="This is a dummy PDF file to simulate the attachment mentioned in the email."
)

# --- Control Buttons ---
st.header("4. Control Scheduler") # Reordered header to be visually consistent with previous version

# Placeholder for dynamic status messages
st.session_state.status_message_placeholder = st.empty()

col_buttons = st.columns(2)

with col_buttons[0]:
    if st.button("▶️ Start Sending", disabled=st.session_state.scheduler_running or st.session_state.email_df.empty, use_container_width=True):
        if st.session_state.email_df.empty:
            st.session_state.status_message_placeholder.error("Please load email addresses before starting the scheduler.")
        else:
            st.session_state.scheduler_running = True
            if st.session_state.last_run_time is None:
                st.session_state.last_run_time = time.time()
            st.session_state.status_message_placeholder.info("Scheduler started...")
            st.rerun() # Trigger rerun to start the loop

with col_buttons[1]:
    if st.button("⏸️ Stop Sending", disabled=not st.session_state.scheduler_running, use_container_width=True):
        st.session_state.scheduler_running = False
        st.session_state.status_message_placeholder.info("Scheduler paused.")

# --- Scheduler Logic (Runs on every rerun if active) ---
if st.session_state.scheduler_running:
    current_time = time.time()
    time_elapsed = current_time - (st.session_state.last_run_time or current_time) # Handle initial None
    required_interval_seconds = st.session_state.interval_minutes * 60

    if time_elapsed >= required_interval_seconds:
        # Time to send emails
        st.session_state.status_message_placeholder.info("Sending emails...")
        emails_df = st.session_state.email_df

        if not emails_df.empty:
            start_index = st.session_state.last_sent_index
            # Calculate end index, ensuring it doesn't exceed the DataFrame length
            end_index = min(start_index + st.session_state.num_emails_to_send, len(emails_df))

            if start_index >= len(emails_df):
                # All emails sent, reset for next cycle or stop
                st.session_state.status_message_placeholder.success("All emails sent! Resetting index to start from beginning.")
                st.session_state.last_sent_index = 0
                # Optionally stop the scheduler here if you only want one full run
                # st.session_state.scheduler_running = False
                time.sleep(2) # Allow user to see the message
                st.rerun() # Rerun to update UI and potentially restart from 0
                st.stop() # Stop execution until next user interaction
            else:
                emails_to_send_now = emails_df.iloc[start_index:end_index]
                sent_count_this_batch = 0
                for idx, row in emails_to_send_now.iterrows():
                    email = row['Email']
                    # In a real application, you would use a library like 'smtplib' here
                    # to connect to an SMTP server and send the email.
                    # You would construct the full email with subject, body (HTML), and attachments.
                    # Example (conceptual):
                    # from email.mime.text import MIMEText
                    # from email.mime.multipart import MIMEMultipart
                    # from email.mime.application import MIMEApplication
                    #
                    # msg = MIMEMultipart()
                    # msg['From'] = 'your_email@example.com'
                    # msg['To'] = email
                    # msg['Subject'] = email_subject
                    # msg.attach(MIMEText(email_body_html, 'html'))
                    #
                    # # Attach PDF (replace with your actual PDF path)
                    # # with open("path/to/NYC_LL_144_Details.pdf", "rb") as f:
                    # #     attach = MIMEApplication(f.read(), _subtype="pdf")
                    # #     attach.add_header('Content-Disposition', 'attachment', filename="NYC_LL_144_Details.pdf")
                    # #     msg.attach(attach)
                    #
                    # # Then send via smtplib:
                    # # server = smtplib.SMTP('smtp.your-email-provider.com', 587)
                    # # server.starttls()
                    # # server.login('your_email@example.com', 'your_password')
                    # # server.send_message(msg)
                    # # server.quit()
                    # --------------------------------
                    st.session_state.status_message_placeholder.write(
                        f"Simulating sending to: **{email}** (Index: {idx})"
                        f"<br>Subject: **{email_subject}**"
                        f"<br>Body (HTML): <div style='border: 1px solid #ccc; padding: 10px; max-height: 150px; overflow-y: auto;'>{email_body_html}</div>",
                        unsafe_allow_html=True
                    )
                    sent_count_this_batch += 1
                    time.sleep(0.05) # Small delay for visual effect of sending

                st.session_state.last_sent_index = end_index
                st.session_state.last_run_time = current_time
                st.session_state.status_message_placeholder.success(
                    f"Sent {sent_count_this_batch} emails. Next batch will start from index **{st.session_state.last_sent_index}**."
                )
                time.sleep(1) # Give user a moment to see the success message
                st.rerun() # Trigger next check after a short pause
        else:
            st.session_state.status_message_placeholder.warning("No emails loaded to send. Stopping scheduler.")
            st.session_state.scheduler_running = False
    else:
        # Countdown
        time_to_wait = required_interval_seconds - time_elapsed
        minutes_left = int(time_to_wait // 60)
        seconds_left = int(time_to_wait % 60)
        st.session_state.status_message_placeholder.info(
            f"Next send in: **{minutes_left:02d}** minutes and **{seconds_left:02d}** seconds."
        )
        time.sleep(1) # Wait 1 second before next rerun to update countdown
        st.rerun() # Trigger rerun to update countdown

st.markdown("---")
st.info(f"Current Scheduler Status: {'**Running**' if st.session_state.scheduler_running else '**Paused**'}")
st.info(f"Next email to send from index: **{st.session_state.last_sent_index}**")
