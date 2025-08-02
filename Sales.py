import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urljoin, urlparse
import time


def extract_emails(text):
    """Extract email addresses from text using regex"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return list(set(re.findall(email_pattern, text)))


def extract_names(soup):
    """Extract potential names from various HTML elements"""
    names = []

    # Common selectors where names might appear
    name_selectors = [
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        '.name', '.author', '.contact-name', '.person-name',
        '[class*="name"]', '[class*="author"]', '[class*="contact"]',
        'strong', 'b', 'em'
    ]

    for selector in name_selectors:
        elements = soup.select(selector)
        for elem in elements:
            text = elem.get_text().strip()
            # Simple heuristic: if text contains 2-4 words and looks like a name
            words = text.split()
            if 2 <= len(words) <= 4 and all(word.replace('-', '').replace("'", "").isalpha() for word in words):
                names.append(text)

    return list(set(names))


def extract_company_info(soup, url):
    """Extract company information from the webpage"""
    companies = []

    # Try to get company from title tag
    title = soup.find('title')
    if title:
        companies.append(title.get_text().strip())

    # Look for company-related selectors
    company_selectors = [
        '.company', '.organization', '.org', '.business',
        '[class*="company"]', '[class*="organization"]',
        'meta[property="og:site_name"]', 'meta[name="author"]'
    ]

    for selector in company_selectors:
        elements = soup.select(selector)
        for elem in elements:
            if elem.name == 'meta':
                content = elem.get('content', '')
                if content:
                    companies.append(content)
            else:
                text = elem.get_text().strip()
                if text:
                    companies.append(text)

    # Extract domain name as potential company
    domain = urlparse(url).netloc.replace('www.', '')
    companies.append(domain)

    return list(set(companies))


def parse_name(full_name):
    """Parse full name into first and last name"""
    parts = full_name.strip().split()
    if len(parts) >= 2:
        first_name = parts[0]
        last_name = ' '.join(parts[1:])
        return first_name, last_name
    elif len(parts) == 1:
        return parts[0], ''
    else:
        return '', ''


def scrape_contact_info(url):
    """Main scraping function"""
    try:
        # Set headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Make request with timeout
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract information
        emails = extract_emails(response.text)
        names = extract_names(soup)
        companies = extract_company_info(soup, url)

        # Combine information into contacts
        contacts = []

        # If we have both names and emails, try to pair them
        if names and emails:
            max_contacts = max(len(names), len(emails))
            for i in range(max_contacts):
                name = names[i] if i < len(names) else names[0] if names else ''
                email = emails[i] if i < len(emails) else emails[0] if emails else ''
                company = companies[0] if companies else ''

                first_name, last_name = parse_name(name)

                contacts.append({
                    'First Name': first_name,
                    'Last Name': last_name,
                    'Email': email,
                    'Company': company,
                    'Source URL': url
                })

        # If we only have emails, create entries for each email
        elif emails:
            company = companies[0] if companies else ''
            for email in emails:
                contacts.append({
                    'First Name': '',
                    'Last Name': '',
                    'Email': email,
                    'Company': company,
                    'Source URL': url
                })

        # If we only have names, create entries for each name
        elif names:
            company = companies[0] if companies else ''
            for name in names:
                first_name, last_name = parse_name(name)
                contacts.append({
                    'First Name': first_name,
                    'Last Name': last_name,
                    'Email': '',
                    'Company': company,
                    'Source URL': url
                })

        # If nothing found, at least show the company/domain
        else:
            company = companies[0] if companies else ''
            contacts.append({
                'First Name': '',
                'Last Name': '',
                'Email': '',
                'Company': company,
                'Source URL': url
            })

        return contacts, None

    except requests.exceptions.RequestException as e:
        return [], f"Error fetching URL: {str(e)}"
    except Exception as e:
        return [], f"Error processing page: {str(e)}"


def main():
    st.set_page_config(
        page_title="Contact Information Scraper",
        page_icon="🔍",
        layout="wide"
    )

    st.title("🔍 Contact Information Web Scraper")
    st.markdown("Extract contact information (names, emails, companies) from web pages")

    # Sidebar with instructions
    with st.sidebar:
        st.header("📋 Instructions")
        st.markdown("""
        1. Enter a URL in the input field
        2. Click 'Scrape Contact Info'
        3. View extracted information in the table
        4. Download results as CSV if needed

        **Note:** Please ensure you comply with website terms of service and robots.txt when scraping.
        """)

        st.header("⚙️ Settings")
        show_source = st.checkbox("Show Source URL in results", value=True)

    # Main input area
    col1, col2 = st.columns([3, 1])

    with col1:
        url = st.text_input(
            "Enter URL to scrape:",
            placeholder="https://example.com/contact",
            help="Enter the full URL including http:// or https://"
        )

    with col2:
        st.write("")  # Spacing
        scrape_button = st.button("🔍 Scrape Contact Info", type="primary")

    # Initialize session state for results
    if 'contacts' not in st.session_state:
        st.session_state.contacts = []

    # Process scraping request
    if scrape_button and url:
        if not url.startswith(('http://', 'https://')):
            st.error("Please enter a valid URL starting with http:// or https://")
        else:
            with st.spinner(f"Scraping {url}..."):
                contacts, error = scrape_contact_info(url)

                if error:
                    st.error(error)
                else:
                    st.session_state.contacts = contacts
                    st.success(f"Found {len(contacts)} contact entries!")

    # Display results
    if st.session_state.contacts:
        st.header("📊 Extracted Contact Information")

        # Convert to DataFrame
        df = pd.DataFrame(st.session_state.contacts)

        # Remove Source URL column if not requested
        if not show_source and 'Source URL' in df.columns:
            df = df.drop('Source URL', axis=1)

        # Display table
        st.dataframe(df, use_container_width=True)

        # Download option
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="contact_info.csv",
            mime="text/csv"
        )

        # Clear results button
        if st.button("🗑️ Clear Results"):
            st.session_state.contacts = []
            st.rerun()

    # Example URLs section
    st.header("💡 Example URLs to Try")
    example_urls = [
        "https://about.linkedin.com/contact-us",
        "https://www.example.com/contact",
        "https://www.example.com/about",
        "https://www.example.com/team"
    ]

    cols = st.columns(len(example_urls))
    for i, example_url in enumerate(example_urls):
        with cols[i]:
            if st.button(f"Try: {example_url.split('//')[-1]}", key=f"example_{i}"):
                st.session_state.example_url = example_url
                st.rerun()

    # Set example URL if clicked
    if 'example_url' in st.session_state:
        st.info(f"Click the input field above and paste: {st.session_state.example_url}")
        del st.session_state.example_url


if __name__ == "__main__":
    main()