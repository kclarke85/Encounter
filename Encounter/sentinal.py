import streamlit as st
import pandas as pd
import numpy as np
import time


# --- 1. STUBBED DATA GENERATION ---
def get_device_data():
    # Hypothetical fleet of 20 devices in "Base Camp Alpha"
    devices = [f"Unit-{i:03d}" for i in range(1, 21)]
    data = {
        "Device_ID": devices,
        "Temp_C": np.random.uniform(22, 32, 20),
        "Water_Level": np.random.uniform(5, 100, 20),
        "Signal_dBm": np.random.uniform(-110, -50, 20)
    }
    return pd.DataFrame(data)


# --- 2. SET THEORY ENGINE ---
def run_triage_logic(df):
    # Defining the Negative Sets
    s_heat = set(df[df['Temp_C'] > 28]['Device_ID'])
    s_dry = set(df[df['Water_Level'] < 15]['Device_ID'])
    s_dark = set(df[df['Signal_dBm'] < -95]['Device_ID'])

    # UNIONS & INTERSECTIONS (The Alert Triggers)
    # Logistics Alert: Union of Dry or Dark
    a_logistics = s_dry.union(s_dark)

    # Medical Alert: Heat is high AND it's not a dry/dark issue (S_heat ∩ complement(S_dry))
    # This identifies units that are failing despite having resources.
    a_medical = s_heat.difference(s_dry)

    # Success Set: Everything NOT in a negative state
    all_negatives = s_heat.union(s_dry).union(s_dark)
    s_success = set(df['Device_ID']).difference(all_negatives)

    return s_heat, s_dry, s_dark, a_logistics, a_medical, s_success


# --- 3. STREAMLIT DASHBOARD UI ---
st.set_page_config(page_title="Sentinel Network Dashboard", layout="wide")
st.title("🌍 Sentinel Network: Base Camp Alpha")
st.subheader("Nocturnal Heat-Recovery Triage (Set Theory Logic)")

# Refresh Button
if st.button('Refresh Field Data'):
    df = get_device_data()
    s_heat, s_dry, s_dark, a_logistics, a_medical, s_success = run_triage_logic(df)

    # Top Level Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Operational (Success Set)", f"{len(s_success)} Units", delta=f"{len(s_success) - 15} vs Last Hour")
    col2.metric("Logistics Alerts (Union)", len(a_logistics), delta_color="inverse")
    col3.metric("Medical Crisis (Intersection)", len(a_medical), delta_color="inverse")

    st.divider()

    # Dashboard Layout
    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.write("### 🛰️ Live Fleet Status")


        # Color coding the data for the UI
        def color_triage(val):
            color = 'red' if val > 28 else 'green'
            return f'color: {color}'


        st.dataframe(df.style.applymap(color_triage, subset=['Temp_C']))

    with right_col:
        st.write("### 🚨 Actionable Triage")

        with st.expander("🔴 MEDICAL INTERVENTION REQUIRED", expanded=True):
            if a_medical:
                for unit in a_medical:
                    st.error(f"**{unit}**: Patient Safety Risk. System failing to cool.")
            else:
                st.success("No active medical crises.")

        with st.expander("🟠 LOGISTICS / MAINTENANCE", expanded=False):
            if a_logistics:
                for unit in a_logistics:
                    reason = []
                    if unit in s_dry: reason.append("Low Water")
                    if unit in s_dark: reason.append("Low Signal")
                    st.warning(f"**{unit}**: Check {' & '.join(reason)}")
            else:
                st.success("Supplies & Connectivity Optimal.")

    # Mathematical Proof for Grant Officers
    st.divider()
    st.write("### 🧮 Set Theory Operational Proof")
    st.latex(r"Success = (S_{heat} \cup S_{dry} \cup S_{dark})^c")
    st.write(f"**Current Operational Efficiency:** {(len(s_success) / len(df)) * 100}%")

else:
    st.info("Click 'Refresh Field Data' to simulate incoming LoRa/Cellular telemetry.")