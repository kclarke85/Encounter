import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import date, timedelta

# --- Configuration and Setup ---

# Use st.session_state for persistence, as Streamlit re-runs the script on every interaction
if 'boycotts' not in st.session_state:
    # Initialize the list of boycott campaigns
    # Each entry is a dictionary: {'company': ticker, 'date': date_object}
    st.session_state.boycotts = []


# --- Main App Functions ---

def fetch_stock_data(ticker, start_date, end_date):
    """Fetches historical stock data using yfinance and caches it."""
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            st.error(f"Could not fetch data for ticker: **{ticker}**. Please check the symbol.")
            return None
        return data
    except Exception as e:
        st.error(f"An error occurred while fetching data for {ticker}: {e}")
        return None


def add_boycott_campaign(company_name, ticker, boycott_date):
    """Adds a new boycott campaign to the session state."""
    if ticker and boycott_date:
        # Check for duplicates before adding
        if not any(b['ticker'] == ticker and b['date'] == boycott_date for b in st.session_state.boycotts):
            st.session_state.boycotts.append({
                'company': company_name,
                'ticker': ticker.upper(),
                'date': boycott_date
            })
            st.toast(f"Boycott campaign added for **{company_name}** starting {boycott_date.strftime('%Y-%m-%d')}! ✊")
        else:
            st.warning(f"A boycott for **{company_name}** on this date is already logged.")


def plot_boycott_effect(df, ticker, boycott_date):
    """Creates an interactive chart showing the stock price and the boycott date."""

    # 1. Calculate a simple 20-day Moving Average (MA) for trend
    df['20-Day MA'] = df['Close'].rolling(window=20).mean()

    # 2. Create the line chart using Plotly Express
    fig = px.line(
        df.reset_index(),
        x='Date',
        y=['Close', '20-Day MA'],
        title=f'Stock Price Trend for {ticker}',
        labels={'Close': 'Closing Price (USD)', 'Date': 'Date'},
        height=500
    )

    # 3. Add a vertical line for the Boycott Start Date
    fig.add_vline(
        x=boycott_date,
        line_width=3,
        line_dash="dash",
        line_color="red",
        annotation_text="**BOYCOTT START**",
        annotation_position="bottom right"
    )

    # 4. Customize the legend and tooltips
    fig.update_layout(legend_title_text='Metric')
    fig.update_traces(hovertemplate='Date: %{x}<br>Price: $%{y:.2f}<extra></extra>')

    st.plotly_chart(fig, use_container_width=True)


# --- Streamlit UI Layout ---

st.set_page_config(
    page_title="Boycott Impact Tracker",
    page_icon="✊",
    layout="wide"
)

st.title("✊ The Boycott Impact Tracker")
st.markdown(
    "Use this tool to log a boycott campaign and visually assess its potential effect on a company's stock price (a common proxy for financial health).")

# --- Sidebar for Adding Campaigns ---

with st.sidebar:
    st.header("➕ Log a New Boycott")
    st.markdown("Enter the details of the company and the boycott start date.")

    company_input = st.text_input("Company Name (e.g., Starbucks)", key="company_name_input")
    ticker_input = st.text_input("Stock Ticker (e.g., SBUX, MSFT)", key="ticker_input")

    # Set default date to today for convenience
    today = date.today()
    boycott_date_input = st.date_input(
        "Boycott Start Date",
        value=today,
        max_value=today,
        key="boycott_date_input"
    )

    if st.button("Log Campaign", type="primary"):
        if ticker_input and company_input:
            add_boycott_campaign(company_input, ticker_input, boycott_date_input)
        else:
            st.error("Please enter both the Company Name and Stock Ticker.")

# --- Main Content Area for Tracking ---

st.header("📈 Active Boycott Campaigns & Impact")

if not st.session_state.boycotts:
    st.info("No boycott campaigns have been logged yet. Use the sidebar to start tracking one!")
else:
    # Reverse the list so the most recent boycott is at the top
    for campaign in reversed(st.session_state.boycotts):
        company = campaign['company']
        ticker = campaign['ticker']
        boycott_date = campaign['date']

        # Calculate a date range for the chart: 6 months before to 3 months after (or today)
        start_chart_date = boycott_date - timedelta(days=180)
        end_chart_date = min(today, boycott_date + timedelta(days=90))

        # Use Streamlit Expander for a clean look
        with st.expander(f"**{company}** ({ticker}) - Boycott Started: {boycott_date.strftime('%Y-%m-%d')}",
                         expanded=True):

            # Use columns for layout and a key metric display
            col1, col2, col3 = st.columns(3)

            col1.metric("Boycott Start", f"{boycott_date.strftime('%b %d, %Y')}")
            col2.metric("Analysis Period",
                        f"{start_chart_date.strftime('%b %Y')} to {end_chart_date.strftime('%b %Y')}")
            col3.metric("Stock Ticker", ticker)

            # Fetch the data
            stock_df = fetch_stock_data(ticker, start_chart_date, end_chart_date)

            if stock_df is not None:
                st.subheader("Stock Price vs. Boycott Start Date")
                st.markdown(
                    "The red dashed line marks the start of the boycott campaign. Check if the stock's closing price or 20-Day Moving Average trend changed significantly after this date.")

                # Plot the data
                plot_boycott_effect(stock_df, ticker, boycott_date)