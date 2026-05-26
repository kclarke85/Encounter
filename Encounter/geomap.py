import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import time

# --- Configuration ---
st.set_page_config(layout="wide", page_title="NYC 2025 Hiring Trends")

# --- Data Simulation ---
# Define NYC borough coordinates for pin placement
NYC_BOROUGH_COORDS = {
    "Manhattan": {"lat": 40.7831, "lon": -73.9712},
    "Brooklyn": {"lat": 40.6782, "lon": -73.9442},
    "Queens": {"lat": 40.7282, "lon": -73.7949},
    "The Bronx": {"lat": 40.8448, "lon": -73.8648},
    "Staten Island": {"lat": 40.5795, "lon": -74.1502},
}

# Define industries and their approximate base hiring trends (simulated for 2025)
# Based on general trends and search results (e.g., healthcare/education growing, manufacturing declining)
INDUSTRY_BASE_HIRES = {
    "Healthcare & Education": 1500,
    "Tech & Information": 1200,
    "Finance": 900,
    "Retail": 700,
    "Hospitality & Leisure": 1000,
    "Professional Services": 800,
    "Manufacturing & Construction": 300,
}

# Define colors for each industry for visual distinction on the map and chart
INDUSTRY_COLORS = {
    "Healthcare & Education": [255, 99, 71, 160],  # Tomato
    "Tech & Information": [60, 179, 113, 160],  # MediumSeaGreen
    "Finance": [65, 105, 225, 160],  # RoyalBlue
    "Retail": [255, 165, 0, 160],  # Orange
    "Hospitality & Leisure": [218, 112, 214, 160],  # Orchid
    "Professional Services": [0, 191, 255, 160],  # DeepSkyBlue
    "Manufacturing & Construction": [139, 69, 19, 160],  # SaddleBrown
}


def generate_hiring_data(year=2025):
    """Generates simulated monthly hiring data for NYC industries."""
    data = []
    months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    boroughs = list(NYC_BOROUGH_COORDS.keys())
    industries = list(INDUSTRY_BASE_HIRES.keys())

    for i, month_name in enumerate(months):
        month_num = i + 1
        for industry in industries:
            # Base hires for the industry
            base_hires = INDUSTRY_BASE_HIRES[industry]

            # Add monthly fluctuation (e.g., slight dip in summer, rise towards year-end)
            # This is a simplified model for demonstration
            monthly_factor = 1.0
            if month_num in [7, 8]:  # Summer dip
                monthly_factor = 0.9
            elif month_num in [11, 12]:  # Year-end surge
                monthly_factor = 1.1

            # Add random noise for variability
            hires = int(base_hires * monthly_factor + np.random.randint(-150, 150))
            hires = max(50, hires)  # Ensure hires are at least 50

            # Distribute hires across boroughs, weighted by a simple random choice
            # For simplicity, each industry's hires for a month are assigned to one random borough
            # In a real scenario, you'd have more granular location data per hire
            chosen_borough = np.random.choice(boroughs)
            borough_coords = NYC_BOROUGH_COORDS[chosen_borough]

            data.append({
                "MonthNum": month_num,
                "Month": month_name,
                "Industry": industry,
                "Hires": hires,
                "Latitude": borough_coords["lat"] + (np.random.rand() - 0.5) * 0.05,  # Small random offset
                "Longitude": borough_coords["lon"] + (np.random.rand() - 0.5) * 0.05,  # Small random offset
                "Borough": chosen_borough,
                "Color": INDUSTRY_COLORS[industry]
            })

    df = pd.DataFrame(data)
    return df


# Generate the data once and store it
@st.cache_data
def load_data():
    return generate_hiring_data()


df_hiring = load_data()

# --- Streamlit App Layout ---
st.title("🏙️ NYC 2025 Hiring Trends by Industry")
st.markdown(
    """
    This interactive dashboard visualizes simulated monthly hiring data across various industries in New York City for 2025.
    Explore the trends month by month using the slider or click 'Play Animation' to see the timeline unfold.
    """
)

# Create two columns for layout: one for controls, one for data display
col1, col2 = st.columns([1, 3])

# Initialize session state for animation control
if 'play_animation' not in st.session_state:
    st.session_state.play_animation = False
if 'animation_month_index' not in st.session_state:
    st.session_state.animation_month_index = 1

with col1:
    st.header("Controls")

    # Determine the initial value for the slider
    # If animation is playing, use the animation_month_index
    # Otherwise, let the slider manage its own value
    slider_value = st.session_state.animation_month_index if st.session_state.play_animation else 1

    # Month slider
    selected_month_num = st.slider(
        "Select Month",
        min_value=1,
        max_value=12,
        value=slider_value,  # Use slider_value to control its initial position
        step=1,
        format="Month %d",
        key="month_slider"
    )

    # Play/Stop button for animation
    if st.button("Play Animation"):
        # Toggle animation state
        st.session_state.play_animation = not st.session_state.play_animation
        # If starting animation, reset month index to 1
        if st.session_state.play_animation:
            st.session_state.animation_month_index = 1
        st.rerun()  # Rerun to apply the new animation state immediately

    animation_speed = st.slider(
        "Animation Speed (seconds per month)",
        min_value=0.1,
        max_value=3.0,
        value=0.8,
        step=0.1
    )

    st.markdown("---")
    st.subheader("Industry Colors")
    for industry, color_rgba in INDUSTRY_COLORS.items():
        # Convert RGBA to hex for display in Markdown
        hex_color = '#%02x%02x%02x' % (color_rgba[0], color_rgba[1], color_rgba[2])
        st.markdown(f"<span style='color:{hex_color};'>■</span> {industry}", unsafe_allow_html=True)

with col2:
    # Use the slider's current value for display, or the animation index if playing
    display_month_num = st.session_state.animation_month_index if st.session_state.play_animation else selected_month_num
    st.header(
        f"Hiring Overview for Month {display_month_num} ({pd.to_datetime(f'2025-{display_month_num}-01').strftime('%B %Y')})")

    # Placeholder for dynamic content
    map_placeholder = st.empty()
    chart_placeholder = st.empty()

    # Animation loop logic
    if st.session_state.play_animation:
        # If animation is active, update the month index for the next run
        # This will be picked up by the slider's 'value' in the next rerun
        if st.session_state.animation_month_index < 12:
            st.session_state.animation_month_index += 1
        else:
            st.session_state.animation_month_index = 1  # Loop back to January

        # Filter data for the current animation month index
        current_month_data = df_hiring[df_hiring["MonthNum"] == st.session_state.animation_month_index]

        # Sleep and rerun to create the animation effect
        time.sleep(animation_speed)
        st.rerun()
    else:
        # If not playing, use the month selected by the slider
        current_month_data = df_hiring[df_hiring["MonthNum"] == selected_month_num]

    # --- Map Visualization (PyDeck) ---
    # Initial view state centered on NYC
    view_state = pdk.ViewState(
        latitude=40.7128,
        longitude=-74.0060,
        zoom=9.5,
        pitch=45,
    )

    # Create a ScatterplotLayer for hiring pins
    # Size of pin based on number of hires, color based on industry
    layer = pdk.Layer(
        "ScatterplotLayer",
        current_month_data,
        get_position=["Longitude", "Latitude"],
        get_color="Color",
        get_radius="Hires * 0.5",  # Scale radius based on hires
        pickable=True,
        auto_highlight=True,
        tooltip={
            "html": "<b>Industry:</b> {Industry}<br/>"
                    "<b>Borough:</b> {Borough}<br/>"
                    "<b>Hires:</b> {Hires}",
            "style": {"backgroundColor": "steelblue", "color": "white"}
        }
    )

    # Create a PyDeck Deck object
    r = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",  # Light map style
        initial_view_state=view_state,
        layers=[layer],
    )

    # Display the map in the placeholder
    map_placeholder.pydeck_chart(r)

    # --- Hiring Summary Bar Chart ---
    # Aggregate hires by industry for the current month
    hiring_by_industry = current_month_data.groupby("Industry")["Hires"].sum().reset_index()
    hiring_by_industry = hiring_by_industry.sort_values(by="Hires", ascending=False)

    # Create a dictionary to map industry names to their RGB color strings
    color_map = {
        industry: f'rgb({color_rgba[0]}, {color_rgba[1]}, {color_rgba[2]})'
        for industry, color_rgba in INDUSTRY_COLORS.items()
    }

    chart_placeholder.subheader("Monthly Hiring by Industry")
    chart_placeholder.bar_chart(
        hiring_by_industry,
        x="Industry",
        y="Hires",
        # Use the 'Industry' column for coloring and provide the color_discrete_map
        color="Industry",
        color_discrete_map=color_map
    )

st.markdown("---")
st.info("Note: The hiring data presented is simulated and does not reflect actual 2025 hiring figures.")

