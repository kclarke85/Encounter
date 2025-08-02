# import streamlit as st
# import pandas as pd
# import io
#
# # Set the page configuration for a wider layout
# st.set_page_config(layout="wide", page_title="Email Resolver")
#
# st.title("Email Resolution and Uniqueness Checker")
#
# st.write("""
# This application allows you to paste a single column of email addresses.
# It will then display the original list and a 'resolved' list containing only unique emails, side by side.
# """)
#
# # Input area for data
# st.subheader("1. Paste Your Email Data Here")
# st.info("Please paste a single column of email addresses, one per line.")
# data_input = st.text_area(
#     "Paste your email addresses",
#     height=300,
#     placeholder="email1@example.com\nemail2@example.com\nemail1@example.com\nemail3@example.com"
# )
#
# # Process data when input is provided
# if data_input:
#     # Read the input as a single column DataFrame
#     # Using io.StringIO to treat the string as a file
#     try:
#         # Split by newlines and create a DataFrame
#         emails = [line.strip() for line in data_input.split('\n') if line.strip()]
#         df_emails = pd.DataFrame(emails, columns=['Email Address'])
#
#     except Exception as e:
#         st.error(f"Could not parse data. Please ensure it's a single column of email addresses. Error: {e}")
#         df_emails = None
#
#     if df_emails is not None and not df_emails.empty:
#         st.subheader("2. Email Lists")
#
#         # Create the 'Resolved Emails' list (unique emails)
#         # For now, "resolved" means unique. If you need more complex resolution (e.g., validation),
#         # please specify.
#         resolved_emails = df_emails['Email Address'].drop_duplicates().reset_index(drop=True)
#         resolved_emails_df = resolved_emails.to_frame(name='Resolved Email')
#
#
#         # Use columns for adjacent display
#         col1, col2 = st.columns(2)
#
#         with col1:
#             st.write("#### Original Emails")
#             # Add 'Row Number' to the original DataFrame
#             df_emails_display = df_emails.copy()
#             df_emails_display.insert(0, 'Row Number', range(1, len(df_emails_display) + 1))
#             st.dataframe(df_emails_display)
#             st.write(f"Total original emails: **{len(df_emails)}**")
#
#
#         with col2:
#             st.write("#### Resolved Emails (Unique)")
#             # Add 'Row Number' to the resolved DataFrame
#             resolved_emails_display = resolved_emails_df.copy()
#             resolved_emails_display.insert(0, 'Row Number', range(1, len(resolved_emails_display) + 1))
#             st.dataframe(resolved_emails_display)
#             st.write(f"Total unique emails: **{len(resolved_emails)}**")
#             st.write(f"Found **{len(df_emails) - len(resolved_emails)}** duplicate entries.")
#
#             # Add a button to copy resolved emails
#             if not resolved_emails.empty:
#                 # Prepare the text to be copied
#                 emails_to_copy = "\n".join(resolved_emails.tolist())
#
#                 # JavaScript to copy text to clipboard
#                 # We use document.execCommand('copy') for better compatibility in iframes
#                 # and provide a fallback message.
#                 copy_script = f"""
#                 <script>
#                 function copyToClipboard(text) {{
#                     const textarea = document.createElement('textarea');
#                     textarea.value = text;
#                     document.body.appendChild(textarea);
#                     textarea.select();
#                     try {{
#                         document.execCommand('copy');
#                         alert('Emails copied to clipboard!');
#                     }} catch (err) {{
#                         alert('Failed to copy emails. Please copy manually: ' + text);
#                     }}
#                     document.body.removeChild(textarea);
#                 }}
#                 </script>
#                 <button onclick="copyToClipboard(`{emails_to_copy}`)">Copy All Resolved Emails</button>
#                 """
#                 st.components.v1.html(copy_script, height=50)
#             else:
#                 st.info("No unique emails to copy.")
#
#     elif df_emails is not None and df_emails.empty:
#         st.info("No email addresses were detected from your paste. Please try again.")
# else:
#     st.info("Paste your email data into the text area above to get started.")
#
# st.markdown("---")
# st.write("Developed with Streamlit and Pandas.")

import streamlit as st
import pandas as pd
import dns.resolver
import time

# ---------- DNS check functions ----------

def check_spf(domain):
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        for rdata in answers:
            for txt_string in rdata.strings:
                if txt_string.decode().startswith("v=spf1"):
                    return True
    except Exception:
        pass
    return False

def check_dkim(domain, selector='default'):
    dkim_domain = f"{selector}._domainkey.{domain}"
    try:
        answers = dns.resolver.resolve(dkim_domain, 'TXT')
        for rdata in answers:
            for txt_string in rdata.strings:
                if txt_string.decode().startswith("v=DKIM1"):
                    return True
    except Exception:
        pass
    return False

def check_dmarc(domain):
    dmarc_domain = f"_dmarc.{domain}"
    try:
        answers = dns.resolver.resolve(dmarc_domain, 'TXT')
        for rdata in answers:
            for txt_string in rdata.strings:
                if txt_string.decode().startswith("v=DMARC1"):
                    return True
    except Exception:
        pass
    return False

# ---------- Streamlit App ----------

st.set_page_config(layout="wide", page_title="Email Resolver & DNS Auth Checker")
st.title("Email Resolution, Uniqueness, and SPF/DKIM/DMARC Checker")

st.write("""
Paste your email addresses below.
This app removes duplicates, extracts domains, checks SPF, DKIM, and DMARC, and shows you the results.
""")

st.subheader("1️⃣ Paste Your Email Data")
st.info("One email per line.")

data_input = st.text_area(
    "Paste your emails",
    height=300,
    placeholder="email1@example.com\nemail2@company.com\nemail1@example.com"
)

if data_input:
    emails = [line.strip() for line in data_input.split('\n') if line.strip()]
    df_emails = pd.DataFrame(emails, columns=['Email Address'])

    if not df_emails.empty:
        st.subheader("2️⃣ Original vs Resolved Emails")

        resolved_emails = df_emails['Email Address'].drop_duplicates().reset_index(drop=True)
        resolved_emails_df = resolved_emails.to_frame(name='Resolved Email')

        # Extract domains
        resolved_emails_df['Domain'] = resolved_emails_df['Resolved Email'].apply(lambda x: x.split('@')[-1])

        # Drop duplicate domains for checks
        unique_domains = resolved_emails_df['Domain'].drop_duplicates().tolist()

        st.info("Checking SPF, DKIM, DMARC for each domain — please wait...")

        # Progress bar & status text
        progress_bar = st.progress(0)
        status_text = st.empty()

        domain_checks = []
        total = len(unique_domains)

        for i, domain in enumerate(unique_domains):
            status_text.text(f"Checking ({i+1}/{total}): {domain}")
            spf = check_spf(domain)
            dkim = check_dkim(domain)
            dmarc = check_dmarc(domain)
            domain_checks.append({'Domain': domain, 'SPF': spf, 'DKIM': dkim, 'DMARC': dmarc})
            progress_bar.progress((i + 1) / total)
            # Force UI to update
            time.sleep(0.1)

        status_text.text("✅ Checks complete.")
        progress_bar.empty()

        df_domain_checks = pd.DataFrame(domain_checks)

        # Merge DNS results back to resolved_emails_df
        resolved_emails_df = resolved_emails_df.merge(df_domain_checks, on='Domain', how='left')

        # Use columns for side-by-side display
        col1, col2 = st.columns(2)

        with col1:
            st.write("### 📥 Original Emails")
            df_emails_display = df_emails.copy()
            df_emails_display.insert(0, 'Row Number', range(1, len(df_emails_display) + 1))
            st.dataframe(df_emails_display)
            st.write(f"Total original emails: **{len(df_emails)}**")

        with col2:
            st.write("### ✅ Resolved Emails with Domain Checks")
            resolved_display = resolved_emails_df.copy()
            resolved_display.insert(0, 'Row Number', range(1, len(resolved_display) + 1))
            st.dataframe(resolved_display)
            st.write(f"Total unique emails: **{len(resolved_emails)}**")
            st.write(f"Unique domains checked: **{len(unique_domains)}**")

        # Download link for results
        csv = resolved_emails_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Resolved Emails with DNS Checks",
            data=csv,
            file_name='resolved_emails_dns.csv',
            mime='text/csv'
        )
    else:
        st.info("No email addresses detected. Please paste valid emails.")
else:
    st.info("Paste your emails above to get started.")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit, Pandas, and dnspython.")
