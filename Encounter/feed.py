import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# --------------------
# 🔑 BLS API Settings
# --------------------
API_KEY = "3a6a384cf3b30494e7cc6657d3b2ed8d5305e39c"
BASE_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# --------------------
# 📘 Sample Series IDs
# --------------------
# Replace these with actual demographic-industry codes from CPS (if available)
SERIES_IDS = {
    'Total - All Workers': 'LNS12000000',  # total employed (CPS)
    'Men, 20 years and over': 'LNS12000031',
    'Women, 20 years and over': 'LNS12000032',
    'Black or African American': 'LNS12000006',
    'White': 'LNS12000003',
    'Asian': 'LNU02032183',
    '16 to 19 years': 'LNS12000012',
    '20 to 24 years': 'LNS12000016'
}

# --------------------
# 📥 Get BLS API Data
# --------------------
def get_bls_data(series_id, start_year, end_year):
    headers = {'Content-type': 'application/json'}
    payload = {
        "seriesid": [series_id],
        "startyear": str(start_year),
        "endyear": str(end_year),
        "registrationKey": API_KEY
    }
    response = requests.post(BASE_URL, json=payload, headers=headers)
    json_data = response.json()
    try:
        data = json_data['Results']['series'][0]['data']
        df = pd.DataFrame(data)
        df['value'] = pd.to_numeric(df['value'])
        df['year'] = df['year'].astype(int)
        df['periodName'] = pd.Categorical(df['periodName'], categories=[
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'],
            ordered=True)
        df['date'] = pd.to_datetime(df['year'].astype(str) + ' ' + df['periodName'].astype(str))
        return df[['date', 'value']]
    except KeyError:
        return pd.DataFrame()

# --------------------
# 🎛️ Streamlit UI
# --------------------
st.title("📊 NYC Employment by Race, Gender, and Age (CPS / BLS API)")
st.write("Data Source: U.S. Bureau of Labor Statistics (CPS)")

start_year = st.sidebar.selectbox("Start Year", list(range(2010, 2026)), index=10)
end_year = st.sidebar.selectbox("End Year", list(range(2010, 2026)), index=15)

selected_series = st.multiselect("Select Demographic Groups", options=list(SERIES_IDS.keys()),
                                 default=['Total - All Workers', 'Men, 20 years and over', 'Women, 20 years and over'])

# --------------------
# 📊 Display Results
# --------------------
chart_data = pd.DataFrame()

for name in selected_series:
    sid = SERIES_IDS[name]
    df = get_bls_data(sid, start_year, end_year)
    df['Group'] = name
    chart_data = pd.concat([chart_data, df], ignore_index=True)

if not chart_data.empty:
    fig = px.line(chart_data, x='date', y='value', color='Group',
                  title='Employment by Demographic Group',
                  labels={'value': 'Employment (000s)', 'date': 'Date'})
    st.plotly_chart(fig, use_container_width=True)

    # Add Table
    st.dataframe(chart_data.pivot_table(index='date', columns='Group', values='value'))
else:
    st.warning("No data returned from BLS API. Check your API key or series IDs.")

