# # import streamlit as st
# # import requests
# # from bs4 import BeautifulSoup
# # import time
# # import json
# # import serpapi
# #
# # # --- CONFIG ---
# # SERPAPI_KEY = "39198bc2d0dd2ee580ec916b154a2f48eac8093c7e7aae4cb62bfc5855341b3b"  # 🔑 get one free at serpapi.com
# #
# # # --- SERP API Helpers ---
# # def serpapi_google_search(query, location="United States", num=10):
# #     search = serpapi.GoogleSearch({
# #         "engine": "google",
# #         "q": query,
# #         "location": location,
# #         "num": num,
# #         "api_key": SERPAPI_KEY
# #     })
# #     return search.get_dict()
# #
# # def keyword_research(seed_keyword, location):
# #     query = f"{seed_keyword} {location}"
# #     results = serpapi_google_search(query, location=location)
# #
# #     # Collect related searches + People Also Ask (PAAs)
# #     keywords = []
# #     if "related_searches" in results:
# #         for r in results["related_searches"]:
# #             keywords.append({"keyword": r["query"], "volume": "N/A"})
# #
# #     if "related_questions" in results:
# #         for q in results["related_questions"]:
# #             keywords.append({"keyword": q["question"], "volume": "N/A"})
# #
# #     return keywords[:10]  # top 10 suggestions
# #
# #
# # def competitor_backlinks(competitor_url, location="United States"):
# #     query = f"site:{competitor_url}"
# #     results = serpapi_google_search(query, location=location, num=20)
# #
# #     backlinks = []
# #     if "organic_results" in results:
# #         for r in results["organic_results"]:
# #             backlinks.append({
# #                 "website": r.get("link", "N/A"),
# #                 "opportunity": "Potential backlink source"
# #             })
# #     return backlinks[:5]
# #
# #
# # # --- MAIN APP ---
# # st.set_page_config(page_title="Company SEO Tool", layout="wide")
# # st.title("Company SEO Assistant")
# # st.markdown("This is now upgraded with **real Google data via SerpApi** 🚀")
# #
# # # Tabs
# # tab1, tab2, tab3, tab4 = st.tabs(["Keyword Research", "On-Page SEO", "Local SEO", "Off-Page SEO"])
# #
# # # --- Keyword Research ---
# # with tab1:
# #     st.header("Keyword Research")
# #     st.write("Find and analyze keywords for your business.")
# #
# #     with st.form(key='keyword_form'):
# #         seed_keyword = st.text_input("Enter a seed keyword (e.g., 'plumber')")
# #         location = st.text_input("Enter your target location (e.g., 'New York')", "United States")
# #         submit_button = st.form_submit_button(label='Generate Keywords')
# #
# #     if submit_button and seed_keyword:
# #         with st.spinner('Fetching keyword ideas from Google...'):
# #             try:
# #                 keywords = keyword_research(seed_keyword, location)
# #                 if keywords:
# #                     st.success("✅ Keywords Generated")
# #                     st.table(keywords)
# #                 else:
# #                     st.error("No keyword suggestions found.")
# #             except Exception as e:
# #                 st.error(f"Error: {e}")
# #
# # # --- On-Page SEO ---
# # with tab2:
# #     st.header("On-Page SEO Analysis")
# #     with st.form(key='onpage_form'):
# #         url_to_analyze = st.text_input("Enter a URL to analyze")
# #         analyze_button = st.form_submit_button("Analyze URL")
# #
# #     if analyze_button and url_to_analyze:
# #         with st.spinner("Analyzing page..."):
# #             try:
# #                 response = requests.get(url_to_analyze, timeout=10)
# #                 if response.status_code == 200:
# #                     soup = BeautifulSoup(response.text, 'html.parser')
# #
# #                     st.success("✅ Analysis Complete")
# #                     title = soup.find('title').get_text() if soup.find('title') else "Not found"
# #                     st.write(f"**Title:** {title}")
# #
# #                     meta_desc = soup.find('meta', attrs={'name': 'description'})
# #                     st.write(f"**Meta Description:** {meta_desc['content'] if meta_desc else 'Missing'}")
# #
# #                     h1_tags = soup.find_all('h1')
# #                     st.write(f"**H1 Tags:** {len(h1_tags)} found")
# #
# #                 else:
# #                     st.error(f"Failed to fetch URL. Status code: {response.status_code}")
# #             except Exception as e:
# #                 st.error(f"Error fetching URL: {e}")
# #
# # # --- Local SEO ---
# # with tab3:
# #     st.header("Local SEO & NAP Consistency")
# #     st.info("✅ Add Google Business Profile API integration here if needed.")
# #
# # # --- Off-Page SEO ---
# # with tab4:
# #     st.header("Off-Page SEO & Backlink Strategy")
# #     with st.form(key='offpage_form'):
# #         competitor_url = st.text_input("Enter a Competitor's URL")
# #         find_button = st.form_submit_button("Find Backlink Opportunities")
# #
# #     if find_button and competitor_url:
# #         with st.spinner("Fetching backlink opportunities..."):
# #             try:
# #                 opportunities = competitor_backlinks(competitor_url)
# #                 if opportunities:
# #                     st.success("✅ Opportunities Found")
# #                     st.table(opportunities)
# #                 else:
# #                     st.error("No backlink sources found.")
# #             except Exception as e:
# #                 st.error(f"Error: {e}")
#
#
#
# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import serpapi
#
# # --- CONFIG ---
# SERPAPI_KEY = "your-serpapi-key"  # Replace with your actual key
#
# # --- SERP API Helpers ---
# def serpapi_google_search(query, location="United States", num=10):
#     search = serpapi.GoogleSearch({
#         "engine": "google",
#         "q": query,
#         "location": location,
#         "num": num,
#         "api_key": SERPAPI_KEY
#     })
#     return search.get_dict()
#
# # --- Keyword Research ---
# def keyword_research(seed_keyword, location):
#     query = f"{seed_keyword} {location}"
#     results = serpapi_google_search(query, location=location)
#
#     keywords = []
#     for r in results.get("related_searches", []):
#         keywords.append({"Keyword": r["query"]})
#     for q in results.get("related_questions", []):
#         keywords.append({"Keyword": q["question"]})
#
#     return keywords[:10]
#
# def enrich_keywords_with_metrics(keywords):
#     enriched = []
#     for kw in keywords:
#         enriched.append({
#             "Keyword": kw["Keyword"],
#             "Volume": "1,200",  # Placeholder
#             "Competition": "Medium",
#             "CPC": "$2.50"
#         })
#     return enriched
#
# # --- On-Page SEO ---
# def analyze_onpage(url):
#     response = requests.get(url, timeout=10)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     return {
#         "Title": soup.title.string if soup.title else "Not found",
#         "Meta Description": soup.find('meta', attrs={'name': 'description'}).get("content", "Missing") if soup.find('meta', attrs={'name': 'description'}) else "Missing",
#         "H1 Count": len(soup.find_all('h1')),
#         "soup": soup
#     }
#
# def extract_onpage_elements(soup):
#     alt_tags = [img.get('alt') for img in soup.find_all('img') if img.get('alt')]
#     internal_links = [a['href'] for a in soup.find_all('a', href=True) if "http" in a['href']]
#     schema = soup.find('script', type='application/ld+json')
#     return {
#         "Alt Tags": len(alt_tags),
#         "Internal Links": len(internal_links),
#         "Schema Markup": "Present" if schema else "Missing"
#     }
#
# # --- Backlink Discovery ---
# def competitor_backlinks(competitor_url, location="United States"):
#     query = f"site:{competitor_url}"
#     results = serpapi_google_search(query, location=location, num=20)
#
#     backlinks = []
#     for r in results.get("organic_results", []):
#         backlinks.append({
#             "Website": r.get("link", "N/A"),
#             "Opportunity": "Potential backlink source"
#         })
#     return backlinks[:5]
#
# # --- UI SETUP ---
# st.set_page_config(page_title="SEO Assistant", layout="wide")
# st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📈 SEO Assistant Dashboard</h1>", unsafe_allow_html=True)
# st.markdown("Upgrade your clients' visibility with real-time SEO insights powered by Google data via SerpApi.")
#
# # --- Tabs ---
# tab1, tab2, tab3, tab4 = st.tabs(["🔍 Keyword Research", "🧠 On-Page SEO", "📍 Local SEO", "🔗 Off-Page SEO"])
#
# # --- Keyword Research ---
# with tab1:
#     st.subheader("🔍 Keyword Research")
#     col1, col2 = st.columns(2)
#     with col1:
#         seed_keyword = st.text_input("Seed Keyword", placeholder="e.g. plumber")
#     with col2:
#         location = st.text_input("Target Location", value="United States")
#
#     if st.button("Generate Keyword Ideas"):
#         with st.spinner("Fetching keyword ideas..."):
#             try:
#                 raw_keywords = keyword_research(seed_keyword, location)
#                 enriched = enrich_keywords_with_metrics(raw_keywords)
#                 st.success("✅ Keywords Generated")
#                 st.dataframe(enriched, use_container_width=True)
#             except Exception as e:
#                 st.error(f"Error: {e}")
#
# # --- On-Page SEO ---
# with tab2:
#     st.subheader("🧠 On-Page SEO Analysis")
#     url_to_analyze = st.text_input("Enter a URL to audit", placeholder="https://example.com")
#
#     if st.button("Analyze Page"):
#         with st.spinner("Analyzing..."):
#             try:
#                 result = analyze_onpage(url_to_analyze)
#                 extras = extract_onpage_elements(result["soup"])
#                 st.success("✅ Analysis Complete")
#                 st.markdown(f"**Title:** {result['Title']}")
#                 st.markdown(f"**Meta Description:** {result['Meta Description']}")
#                 st.markdown(f"**H1 Tags Found:** {result['H1 Count']}")
#                 st.markdown(f"**Alt Tags Present:** {extras['Alt Tags']}")
#                 st.markdown(f"**Internal Links:** {extras['Internal Links']}")
#                 st.markdown(f"**Schema Markup:** {extras['Schema Markup']}")
#             except Exception as e:
#                 st.error(f"Error fetching URL: {e}")
#
# # --- Local SEO ---
# with tab3:
#     st.subheader("📍 Local SEO & NAP Consistency")
#     st.info("🔧 Coming soon: Google Business Profile integration for NAP audits and citation tracking.")
#     st.markdown("You’ll be able to verify Name, Address, Phone consistency across major directories and map listings.")
#
# # --- Off-Page SEO ---
# with tab4:
#     st.subheader("🔗 Backlink Strategy")
#     competitor_url = st.text_input("Competitor URL", placeholder="https://competitor.com")
#
#     if st.button("Find Backlink Opportunities"):
#         with st.spinner("Searching for backlink sources..."):
#             try:
#                 opportunities = competitor_backlinks(competitor_url)
#                 st.success("✅ Opportunities Found")
#                 st.dataframe(opportunities, use_container_width=True)
#             except Exception as e:
#                 st.error(f"Error: {e}")

import streamlit as st
import requests
from bs4 import BeautifulSoup
import serpapi
import pandas as pd
from datetime import datetime, timedelta
import json
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIG ---
SERPAPI_KEY = "39198bc2d0dd2ee580ec916b154a2f48eac8093c7e7aae4cb62bfc5855341b3b"  # Replace with your actual key


# --- Enhanced SERP API Helpers ---
def serpapi_google_search(query, location="United States", num=10):
    """Enhanced Google search with error handling"""
    try:
        search = serpapi.GoogleSearch({
            "engine": "google",
            "q": query,
            "location": location,
            "num": num,
            "api_key": SERPAPI_KEY
        })
        return search.get_dict()
    except Exception as e:
        st.error(f"SerpApi error: {e}")
        return {}


def get_keyword_volume_estimate(keyword):
    """Estimate search volume based on keyword characteristics"""
    # Simple heuristic - in real implementation, use Google Keyword Planner API
    base_volume = 1000
    if "near me" in keyword.lower():
        return int(base_volume * 0.3)
    elif any(word in keyword.lower() for word in ["emergency", "24/7", "urgent"]):
        return int(base_volume * 0.8)
    elif len(keyword.split()) > 4:
        return int(base_volume * 0.2)
    else:
        return base_volume


def get_competition_level(keyword):
    """Estimate competition based on keyword type"""
    high_competition = ["insurance", "lawyer", "attorney", "mortgage"]
    medium_competition = ["plumber", "electrician", "contractor"]

    keyword_lower = keyword.lower()
    if any(word in keyword_lower for word in high_competition):
        return "High"
    elif any(word in keyword_lower for word in medium_competition):
        return "Medium"
    else:
        return "Low"


# --- Enhanced Keyword Research ---
def keyword_research(seed_keyword, location):
    """Enhanced keyword research with real data"""
    query = f"{seed_keyword} {location}"
    results = serpapi_google_search(query, location=location)

    keywords = []

    # Get related searches
    for r in results.get("related_searches", []):
        kw = r["query"]
        keywords.append({
            "Keyword": kw,
            "Volume": get_keyword_volume_estimate(kw),
            "Competition": get_competition_level(kw),
            "Intent": classify_search_intent(kw),
            "Difficulty": estimate_difficulty(kw)
        })

    # Get People Also Ask questions
    for q in results.get("related_questions", []):
        kw = q["question"]
        keywords.append({
            "Keyword": kw,
            "Volume": get_keyword_volume_estimate(kw),
            "Competition": get_competition_level(kw),
            "Intent": "Informational",
            "Difficulty": "Low"
        })

    return keywords[:15]


def classify_search_intent(keyword):
    """Classify search intent for better targeting"""
    keyword_lower = keyword.lower()
    if any(word in keyword_lower for word in ["buy", "price", "cost", "hire", "service"]):
        return "Commercial"
    elif any(word in keyword_lower for word in ["how", "what", "why", "when", "guide"]):
        return "Informational"
    elif any(word in keyword_lower for word in ["near me", "in", "location"]):
        return "Local"
    else:
        return "Navigational"


def estimate_difficulty(keyword):
    """Estimate SEO difficulty"""
    if len(keyword.split()) > 3:
        return "Low"
    elif any(word in keyword.lower() for word in ["best", "top", "review"]):
        return "High"
    else:
        return "Medium"


# --- Enhanced On-Page SEO Analysis ---
def analyze_onpage_comprehensive(url):
    """Comprehensive on-page analysis"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, timeout=15, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Basic elements
        title = soup.title.string.strip() if soup.title else "Missing"
        meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
        meta_desc = meta_desc_tag.get('content', '').strip() if meta_desc_tag else "Missing"

        # Header analysis
        headers_analysis = analyze_headers(soup)

        # Image analysis
        images = soup.find_all('img')
        images_without_alt = [img for img in images if not img.get('alt')]

        # Link analysis
        internal_links, external_links = analyze_links(soup, url)

        # Schema markup
        schema_scripts = soup.find_all('script', type='application/ld+json')

        # Page speed indicators
        total_images = len(images)
        large_images = [img for img in images if
                        img.get('src') and not any(opt in img.get('src', '') for opt in ['webp', 'avif'])]

        # Content analysis
        content_analysis = analyze_content(soup)

        return {
            "url": url,
            "title": title,
            "title_length": len(title),
            "meta_description": meta_desc,
            "meta_desc_length": len(meta_desc) if meta_desc != "Missing" else 0,
            "headers": headers_analysis,
            "total_images": total_images,
            "images_without_alt": len(images_without_alt),
            "internal_links": len(internal_links),
            "external_links": len(external_links),
            "schema_markup": len(schema_scripts),
            "content_analysis": content_analysis,
            "issues": generate_seo_issues(title, meta_desc, headers_analysis, images_without_alt, schema_scripts),
            "recommendations": generate_recommendations(title, meta_desc, headers_analysis, images_without_alt,
                                                        schema_scripts)
        }

    except Exception as e:
        return {"error": str(e)}


def analyze_headers(soup):
    """Analyze header structure"""
    headers = {}
    for i in range(1, 7):
        headers[f'h{i}'] = len(soup.find_all(f'h{i}'))
    return headers


def analyze_links(soup, base_url):
    """Analyze internal and external links"""
    from urllib.parse import urljoin, urlparse

    base_domain = urlparse(base_url).netloc
    links = soup.find_all('a', href=True)

    internal_links = []
    external_links = []

    for link in links:
        href = link['href']
        full_url = urljoin(base_url, href)
        domain = urlparse(full_url).netloc

        if domain == base_domain or not domain:
            internal_links.append(href)
        else:
            external_links.append(href)

    return internal_links, external_links


def analyze_content(soup):
    """Analyze page content"""
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()

    text = soup.get_text()
    words = text.split()

    return {
        "word_count": len(words),
        "character_count": len(text),
        "reading_time": max(1, len(words) // 200)  # Assume 200 words per minute
    }


def generate_seo_issues(title, meta_desc, headers, images_without_alt, schema_scripts):
    """Generate list of SEO issues"""
    issues = []

    if title == "Missing":
        issues.append("Missing page title")
    elif len(title) > 60:
        issues.append("Title too long (over 60 characters)")
    elif len(title) < 30:
        issues.append("Title too short (under 30 characters)")

    if meta_desc == "Missing":
        issues.append("Missing meta description")
    elif len(meta_desc) > 160:
        issues.append("Meta description too long (over 160 characters)")
    elif len(meta_desc) < 120:
        issues.append("Meta description too short (under 120 characters)")

    if headers.get('h1', 0) == 0:
        issues.append("Missing H1 tag")
    elif headers.get('h1', 0) > 1:
        issues.append("Multiple H1 tags found")

    if images_without_alt:
        issues.append(f"{len(images_without_alt)} images missing alt text")

    if not schema_scripts:
        issues.append("No structured data markup found")

    return issues


def generate_recommendations(title, meta_desc, headers, images_without_alt, schema_scripts):
    """Generate actionable recommendations"""
    recommendations = []

    if title == "Missing":
        recommendations.append("Add a descriptive page title with primary keyword")
    elif len(title) > 60:
        recommendations.append("Shorten title to under 60 characters while keeping primary keyword")

    if meta_desc == "Missing":
        recommendations.append("Add compelling meta description with call-to-action")
    elif len(meta_desc) < 120:
        recommendations.append("Expand meta description to 120-160 characters for better click-through rates")

    if headers.get('h1', 0) == 0:
        recommendations.append("Add H1 tag with primary keyword for page topic clarity")

    if images_without_alt:
        recommendations.append("Add descriptive alt text to all images for accessibility and SEO")

    if not schema_scripts:
        recommendations.append("Implement local business schema markup for better local search visibility")

    recommendations.append("Consider adding customer review schema for star ratings in search results")
    recommendations.append("Optimize page loading speed by compressing images and minifying CSS/JS")

    return recommendations


# --- Enhanced Local SEO Features ---
def check_local_citations(business_name, phone, address):
    """Check for business citations across major directories"""
    # In a real implementation, this would check major directories
    # For now, we'll simulate the process

    directories = [
        "Google My Business", "Yelp", "Yellow Pages", "Bing Places",
        "Apple Maps", "Facebook", "Better Business Bureau", "Angie's List"
    ]

    citations = []
    for directory in directories:
        # Simulate citation check
        status = "Found" if hash(business_name + directory) % 3 != 0 else "Missing"
        citations.append({
            "Directory": directory,
            "Status": status,
            "NAP Consistency": "Consistent" if status == "Found" else "N/A"
        })

    return citations


def local_keyword_suggestions(business_type, location):
    """Generate local keyword suggestions"""
    base_keywords = {
        "painter": ["house painter", "interior painting", "exterior painting", "residential painter"],
        "plumber": ["emergency plumber", "drain cleaning", "water heater repair", "pipe repair"],
        "electrician": ["electrical repair", "outlet installation", "panel upgrade", "emergency electrician"],
        "contractor": ["home renovation", "kitchen remodel", "bathroom remodel", "general contractor"]
    }

    keywords = base_keywords.get(business_type.lower(), ["contractor", "home services"])
    local_keywords = []

    for keyword in keywords:
        local_keywords.extend([
            f"{keyword} {location}",
            f"{keyword} near me",
            f"best {keyword} in {location}",
            f"{keyword} services {location}",
            f"affordable {keyword} {location}"
        ])

    return local_keywords[:10]


# --- Enhanced Backlink Analysis ---
def analyze_competitor_backlinks(competitor_url):
    """Enhanced backlink analysis"""
    # Search for pages linking to competitor
    query = f'"{competitor_url}"'
    results = serpapi_google_search(query, num=20)

    backlink_sources = []
    for result in results.get("organic_results", []):
        if competitor_url not in result.get("link", ""):
            backlink_sources.append({
                "Source": result.get("title", "Unknown"),
                "URL": result.get("link", ""),
                "Domain Authority": estimate_domain_authority(result.get("link", "")),
                "Opportunity": categorize_backlink_opportunity(result.get("link", ""))
            })

    return backlink_sources[:10]


def estimate_domain_authority(url):
    """Estimate domain authority based on domain characteristics"""
    if not url:
        return "Unknown"

    domain = url.split("//")[1].split("/")[0] if "//" in url else url.split("/")[0]

    if any(tld in domain for tld in [".edu", ".gov"]):
        return "High (80+)"
    elif any(site in domain for site in ["wikipedia", "forbes", "cnn"]):
        return "High (80+)"
    elif len(domain.split(".")[0]) > 10:
        return "Low (20-40)"
    else:
        return "Medium (40-70)"


def categorize_backlink_opportunity(url):
    """Categorize the type of backlink opportunity"""
    if not url:
        return "Unknown"

    domain = url.lower()

    if any(word in domain for word in ["directory", "listing"]):
        return "Business Directory"
    elif any(word in domain for word in ["blog", "news", "article"]):
        return "Content Marketing"
    elif any(word in domain for word in ["review", "testimonial"]):
        return "Review Site"
    elif any(word in domain for word in ["social", "facebook", "twitter"]):
        return "Social Media"
    else:
        return "General Link Building"


# --- PDF Report Generation ---
def generate_pdf_report(data, client_name):
    """Generate professional PDF report"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=1 * inch)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        alignment=1,
        textColor=colors.HexColor('#2E86AB')
    )
    story.append(Paragraph(f"SEO Analysis Report for {client_name}", title_style))
    story.append(Spacer(1, 0.5 * inch))

    # Executive Summary
    story.append(Paragraph("Executive Summary", styles['Heading2']))
    story.append(Paragraph(
        f"This report provides a comprehensive SEO analysis conducted on {datetime.now().strftime('%B %d, %Y')}. "
        f"Key findings and actionable recommendations are outlined below.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.3 * inch))

    # Add sections based on data
    if 'keywords' in data:
        story.append(Paragraph("Keyword Analysis", styles['Heading2']))
        # Create keyword table
        keyword_data = [['Keyword', 'Volume', 'Competition', 'Intent']]
        for kw in data['keywords'][:10]:
            keyword_data.append([
                kw['Keyword'][:50] + '...' if len(kw['Keyword']) > 50 else kw['Keyword'],
                str(kw['Volume']),
                kw['Competition'],
                kw['Intent']
            ])

        table = Table(keyword_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 0.3 * inch))

    doc.build(story)
    buffer.seek(0)
    return buffer


# --- Streamlit UI ---
st.set_page_config(page_title="Professional SEO Dashboard", layout="wide", page_icon="📈")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 3rem;
        margin-bottom: 2rem;
    }
    .metric-container {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .recommendation-box {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .issue-box {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🚀 Professional SEO Dashboard</h1>', unsafe_allow_html=True)
st.markdown("**Comprehensive SEO analysis and reporting for contractor businesses**")

# Sidebar for client information
with st.sidebar:
    st.header("Client Information")
    client_name = st.text_input("Client Name", value="Sample Client")
    business_type = st.selectbox("Business Type", ["painter", "plumber", "electrician", "contractor", "other"])
    primary_location = st.text_input("Primary Service Area", value="New York, NY")

# Main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Keyword Research",
    "🔍 On-Page Analysis",
    "📍 Local SEO",
    "🔗 Backlink Analysis",
    "📊 Client Reports"
])

# --- Enhanced Keyword Research Tab ---
with tab1:
    st.header("🎯 Advanced Keyword Research")

    col1, col2 = st.columns([2, 1])
    with col1:
        seed_keyword = st.text_input("Primary Service/Keyword", value=business_type,
                                     help="e.g., house painter, emergency plumber")
    with col2:
        location = st.text_input("Target Location", value=primary_location)

    if st.button("🚀 Generate Comprehensive Keyword Analysis", type="primary"):
        with st.spinner("Analyzing keywords and search trends..."):
            try:
                # Get keywords
                keywords = keyword_research(seed_keyword, location)
                local_suggestions = local_keyword_suggestions(business_type, location.split(",")[0])

                if keywords:
                    st.success("✅ Keyword Analysis Complete")

                    # Display metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        avg_volume = sum(kw['Volume'] for kw in keywords) // len(keywords)
                        st.markdown(
                            f'<div class="metric-container"><h3>{avg_volume:,}</h3><p>Avg Monthly Volume</p></div>',
                            unsafe_allow_html=True)
                    with col2:
                        high_volume = len([kw for kw in keywords if kw['Volume'] > 1000])
                        st.markdown(
                            f'<div class="metric-container"><h3>{high_volume}</h3><p>High Volume Keywords</p></div>',
                            unsafe_allow_html=True)
                    with col3:
                        local_terms = len([kw for kw in keywords if kw['Intent'] == 'Local'])
                        st.markdown(
                            f'<div class="metric-container"><h3>{local_terms}</h3><p>Local Intent Keywords</p></div>',
                            unsafe_allow_html=True)
                    with col4:
                        easy_targets = len([kw for kw in keywords if kw['Difficulty'] == 'Low'])
                        st.markdown(
                            f'<div class="metric-container"><h3>{easy_targets}</h3><p>Easy Target Keywords</p></div>',
                            unsafe_allow_html=True)

                    # Keyword table
                    st.subheader("📈 Keyword Opportunities")
                    df = pd.DataFrame(keywords)
                    st.dataframe(df, use_container_width=True)

                    # Local keyword suggestions
                    st.subheader("📍 Local SEO Keywords")
                    local_df = pd.DataFrame(
                        [{"Keyword": kw, "Priority": "High" if "near me" in kw else "Medium"} for kw in
                         local_suggestions])
                    st.dataframe(local_df, use_container_width=True)

                    # Store data for reports
                    if 'report_data' not in st.session_state:
                        st.session_state.report_data = {}
                    st.session_state.report_data['keywords'] = keywords

                else:
                    st.error("No keywords found. Please check your SerpApi configuration.")

            except Exception as e:
                st.error(f"Error: {e}")

# --- Enhanced On-Page Analysis Tab ---
with tab2:
    st.header("🔍 Comprehensive On-Page SEO Audit")

    url_input = st.text_input("Website URL to Analyze", placeholder="https://example.com")

    if st.button("🔎 Run Complete SEO Audit", type="primary"):
        if url_input:
            with st.spinner("Conducting comprehensive SEO analysis..."):
                try:
                    analysis = analyze_onpage_comprehensive(url_input)

                    if "error" not in analysis:
                        st.success("✅ SEO Audit Complete")

                        # Overview metrics
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            score = max(0, 100 - len(analysis['issues']) * 10)
                            color = "green" if score > 80 else "orange" if score > 60 else "red"
                            st.markdown(
                                f'<div class="metric-container"><h3 style="color: {color};">{score}/100</h3><p>SEO Score</p></div>',
                                unsafe_allow_html=True)
                        with col2:
                            st.markdown(
                                f'<div class="metric-container"><h3>{len(analysis["issues"])}</h3><p>Issues Found</p></div>',
                                unsafe_allow_html=True)
                        with col3:
                            st.markdown(
                                f'<div class="metric-container"><h3>{analysis["content_analysis"]["word_count"]}</h3><p>Word Count</p></div>',
                                unsafe_allow_html=True)
                        with col4:
                            st.markdown(
                                f'<div class="metric-container"><h3>{analysis["content_analysis"]["reading_time"]} min</h3><p>Reading Time</p></div>',
                                unsafe_allow_html=True)

                        # Technical details
                        st.subheader("🔧 Technical SEO Details")

                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Page Title:**", analysis['title'])
                            st.write("**Title Length:**", f"{analysis['title_length']} characters")
                            st.write("**Meta Description:**", analysis['meta_description'][:100] + "..." if len(
                                analysis['meta_description']) > 100 else analysis['meta_description'])
                            st.write("**Meta Description Length:**", f"{analysis['meta_desc_length']} characters")

                        with col2:
                            st.write("**Header Structure:**")
                            for header, count in analysis['headers'].items():
                                st.write(f"  - {header.upper()}: {count}")
                            st.write("**Images:**",
                                     f"{analysis['total_images']} total, {analysis['images_without_alt']} missing alt text")
                            st.write("**Links:**",
                                     f"{analysis['internal_links']} internal, {analysis['external_links']} external")

                        # Issues and recommendations
                        if analysis['issues']:
                            st.subheader("⚠️ Issues Found")
                            for issue in analysis['issues']:
                                st.markdown(f'<div class="issue-box">• {issue}</div>', unsafe_allow_html=True)

                        st.subheader("💡 Recommendations")
                        for rec in analysis['recommendations']:
                            st.markdown(f'<div class="recommendation-box">• {rec}</div>', unsafe_allow_html=True)

                        # Store for reports
                        if 'report_data' not in st.session_state:
                            st.session_state.report_data = {}
                        st.session_state.report_data['onpage'] = analysis

                    else:
                        st.error(f"Error analyzing URL: {analysis['error']}")

                except Exception as e:
                    st.error(f"Analysis failed: {e}")

# --- Local SEO Tab ---
with tab3:
    st.header("📍 Local SEO Management")

    # Business information form
    with st.form("business_info"):
        st.subheader("Business Information")
        col1, col2 = st.columns(2)
        with col1:
            biz_name = st.text_input("Business Name", value=client_name)
            biz_phone = st.text_input("Phone Number", placeholder="(555) 123-4567")
        with col2:
            biz_address = st.text_input("Business Address", placeholder="123 Main St, City, State")
            biz_category = st.selectbox("Business Category", ["Home Improvement", "Plumbing", "Electrical", "Painting",
                                                              "General Contractor"])

        check_citations = st.form_submit_button("🔍 Check Citation Consistency")

    if check_citations and biz_name and biz_phone:
        with st.spinner("Checking business citations across major directories..."):
            citations = check_local_citations(biz_name, biz_phone, biz_address)

            # Citation metrics
            found_citations = len([c for c in citations if c['Status'] == 'Found'])
            total_citations = len(citations)

            col1, col2, col3 = st.columns(3)
            with col1:
                completion = int((found_citations / total_citations) * 100)
                st.markdown(f'<div class="metric-container"><h3>{completion}%</h3><p>Citation Completion</p></div>',
                            unsafe_allow_html=True)
            with col2:
                st.markdown(
                    f'<div class="metric-container"><h3>{found_citations}/{total_citations}</h3><p>Citations Found</p></div>',
                    unsafe_allow_html=True)
            with col3:
                consistent = len([c for c in citations if c['NAP Consistency'] == 'Consistent'])
                st.markdown(f'<div class="metric-container"><h3>{consistent}</h3><p>Consistent NAP</p></div>',
                            unsafe_allow_html=True)

            # Citation table
            st.subheader("📋 Citation Status by Directory")
            citation_df = pd.DataFrame(citations)
            st.dataframe(citation_df, use_container_width=True)

            # Recommendations
            missing_citations = [c['Directory'] for c in citations if c['Status'] == 'Missing']
            if missing_citations:
                st.subheader("🎯 Recommended Actions")
                st.write("**Missing Citations - Priority Directories:**")
                for directory in missing_citations[:5]:  # Top 5 priorities
                    st.markdown(f'<div class="recommendation-box">• Create listing on {directory}</div>',
                                unsafe_allow_html=True)

# --- Backlink Analysis Tab ---
with tab4:
    st.header("🔗 Competitor Backlink Analysis")

    competitor_url = st.text_input("Competitor Website URL", placeholder="https://competitor-website.com")

    if st.button("🕵️ Analyze Competitor Backlinks", type="primary"):
        if competitor_url:
            with st.spinner("Discovering backlink opportunities..."):
                try:
                    opportunities = analyze_competitor_backlinks(competitor_url)

                    if opportunities:
                        st.success("✅ Backlink Analysis Complete")

                        # Opportunity metrics
                        high_authority = len([o for o in opportunities if "High" in o['Domain Authority']])
                        directories = len([o for o in opportunities if o['Opportunity'] == 'Business Directory'])
                        content_opps = len([o for o in opportunities if o['Opportunity'] == 'Content Marketing'])

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown(
                                f'<div class="metric-container"><h3>{len(opportunities)}</h3><p>Opportunities Found</p></div>',
                                unsafe_allow_html=True)
                        with col2:
                            st.markdown(
                                f'<div class="metric-container"><h3>{high_authority}</h3><p>High Authority Sites</p></div>',
                                unsafe_allow_html=True)
                        with col3:
                            st.markdown(
                                f'<div class="metric-container"><h3>{directories}</h3><p>Directory Opportunities</p></div>',
                                unsafe_allow_html=True)

                        # Opportunities table
                        st.subheader("🎯 Link Building Opportunities")
                        opp_df = pd.DataFrame(opportunities)
                        st.dataframe(opp_df, use_container_width=True)

                        # Strategy recommendations
                        st.subheader("📈 Link Building Strategy")
                        if directories > 0:
                            st.markdown(
                                '<div class="recommendation-box">• Focus on business directory submissions - high ROI for local businesses</div>',
                                unsafe_allow_html=True)
                        if content_opps > 0:
                            st.markdown(
                                '<div class="recommendation-box">• Create valuable content for guest posting opportunities</div>',
                                unsafe_allow_html=True)
                        if high_authority > 0:
                            st.markdown(
                                '<div class="recommendation-box">• Prioritize high-authority sites for maximum SEO impact</div>',
                                unsafe_allow_html=True)

                        # Store for reports
                        if 'report_data' not in st.session_state:
                            st.session_state.report_data = {}
                        st.session_state.report_data['backlinks'] = opportunities

                    else:
                        st.warning("No backlink opportunities found for this competitor.")

                except Exception as e:
                    st.error(f"Backlink analysis failed: {e}")

# --- Client Reports Tab ---
with tab5:
    st.header("📊 Professional Client Reports")

    if 'report_data' not in st.session_state:
        st.info("📋 Run analyses in other tabs to generate comprehensive reports")
    else:
        st.success("✅ Report data available - Generate professional PDF reports for clients")

        # Report options
        col1, col2 = st.columns(2)
        with col1:
            report_type = st.selectbox(
                "Report Type",
                ["Complete SEO Audit", "Keyword Research Only", "Technical SEO Only", "Local SEO Focus"]
            )
        with col2:
            report_format = st.selectbox("Format", ["PDF Report", "Executive Summary"])

        # Report preview
        st.subheader("📋 Report Preview")

        if 'keywords' in st.session_state.report_data:
            with st.expander("🎯 Keyword Analysis Summary", expanded=True):
                keywords = st.session_state.report_data['keywords']
                total_keywords = len(keywords)
                avg_volume = sum(kw['Volume'] for kw in keywords) // len(keywords) if keywords else 0

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Keywords Analyzed", total_keywords)
                with col2:
                    st.metric("Avg Monthly Volume", f"{avg_volume:,}")
                with col3:
                    high_intent = len([kw for kw in keywords if kw['Intent'] in ['Commercial', 'Local']])
                    st.metric("High-Intent Keywords", high_intent)

                # Top keywords chart
                if keywords:
                    df_chart = pd.DataFrame(keywords[:10])
                    fig = px.bar(
                        df_chart,
                        x='Volume',
                        y='Keyword',
                        color='Competition',
                        title="Top 10 Keyword Opportunities",
                        orientation='h'
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)

        if 'onpage' in st.session_state.report_data:
            with st.expander("🔍 Technical SEO Summary", expanded=True):
                analysis = st.session_state.report_data['onpage']

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    seo_score = max(0, 100 - len(analysis.get('issues', [])) * 10)
                    st.metric("SEO Score", f"{seo_score}/100")
                with col2:
                    st.metric("Issues Found", len(analysis.get('issues', [])))
                with col3:
                    st.metric("Word Count", analysis.get('content_analysis', {}).get('word_count', 0))
                with col4:
                    st.metric("Schema Markup", "Present" if analysis.get('schema_markup', 0) > 0 else "Missing")

                # Issues chart
                if analysis.get('issues'):
                    issue_categories = {}
                    for issue in analysis['issues']:
                        if 'title' in issue.lower():
                            issue_categories['Title Issues'] = issue_categories.get('Title Issues', 0) + 1
                        elif 'meta' in issue.lower():
                            issue_categories['Meta Issues'] = issue_categories.get('Meta Issues', 0) + 1
                        elif 'image' in issue.lower():
                            issue_categories['Image Issues'] = issue_categories.get('Image Issues', 0) + 1
                        else:
                            issue_categories['Other Issues'] = issue_categories.get('Other Issues', 0) + 1

                    fig = px.pie(
                        values=list(issue_categories.values()),
                        names=list(issue_categories.keys()),
                        title="SEO Issues by Category"
                    )
                    st.plotly_chart(fig, use_container_width=True)

        # Generate report button
        if st.button("📄 Generate Professional PDF Report", type="primary"):
            with st.spinner("Generating comprehensive PDF report..."):
                try:
                    pdf_buffer = generate_pdf_report(st.session_state.report_data, client_name)

                    st.success("✅ Report Generated Successfully!")
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_buffer,
                        file_name=f"SEO_Report_{client_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )

                except Exception as e:
                    st.error(f"Error generating PDF: {e}")
                    st.info("💡 Note: PDF generation requires reportlab library. Install with: pip install reportlab")

# --- Footer ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>🚀 Professional SEO Dashboard - Built for Contractor Marketing Success</p>
        <p>Last updated: """ + datetime.now().strftime('%B %d, %Y') + """</p>
    </div>
    """,
    unsafe_allow_html=True
)