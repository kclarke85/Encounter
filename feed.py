import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

# Streamlit setup
st.set_page_config(page_title="NYC Employment Top 10 Categories", layout="centered")

# Centered caption
st.markdown(
    "<div style='text-align: center; font-size: 16px; color: gray;'>"
    "Source: BLS NYC Nonagricultural Employment (000's) | Jun 2024 - Jun 2025"
    "</div>",
    unsafe_allow_html=True
)

data = {
    "Category": [
        "Total Nonfarm",
        "Total Private",
        "Goods Producing",
        "Service Providing",
        "Government",
        "Professional and Business Services",
        "Health Care and Social Assistance",
        "Accommodation and Food Services",
        "Trade, Transportation, and Utilities",
        "Financial Activities",
    ],
    "Jun 2024": [4790.7, 4201.8, 200.5, 4590.2, 588.9, 808.3, 995.6, 365.2, 580.8, 513.3],
    "May 2025": [4854.6, 4255.6, 194.2, 4660.4, 599.0, 795.1, 1059.7, 364.0, 576.0, 501.5],
    "Jun 2025": [4871.6, 4275.5, 196.3, 4675.3, 596.1, 808.1, 1064.0, 368.8, 580.0, 514.2],
}

df = pd.DataFrame(data)

# Descriptions for each category
category_descriptions = {
    "Total Nonfarm": "All jobs except farm workers, private household employees, and nonprofit employees.",
    "Total Private": "Jobs in private-sector businesses and organizations.",
    "Goods Producing": "Jobs producing goods including manufacturing, construction, and mining.",
    "Service Providing": "Jobs providing services rather than goods such as healthcare, education, finance, etc.",
    "Government": "Jobs in federal, state, and local government agencies.",
    "Professional and Business Services": "Jobs in professional, scientific, technical services, management, and administrative support.",
    "Health Care and Social Assistance": "Jobs in hospitals, clinics, social services, and related fields.",
    "Accommodation and Food Services": "Jobs in hotels, restaurants, bars, and hospitality services.",
    "Trade, Transportation, and Utilities": "Jobs in wholesale/retail trade, transportation, warehousing, and utilities.",
    "Financial Activities": "Jobs in finance, insurance, real estate, and related sectors.",
}

# Separate 'Goods Producing' category
goods_producing = df[df["Category"] == "Goods Producing"]
others = df[df["Category"] != "Goods Producing"]

# Sort others descending by Jun 2025 and take top 9
others_sorted = others.sort_values(by="Jun 2025", ascending=False).head(9)

# Combine others + Goods Producing at bottom
df_sorted = pd.concat([others_sorted, goods_producing], ignore_index=True)

# Prepare DataFrame for animation
df_anim = df_sorted.set_index("Category").T.reset_index().rename(columns={"index": "Month"})
months = df_anim["Month"].tolist()
categories = df_sorted["Category"].tolist()

positions = list(range(len(months)))

colors = [
    "#1f77b4", "#2ca02c", "#ff7f0e", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
]

placeholder = st.empty()

for frame in range(1, len(months) + 1):
    fig, ax = plt.subplots(figsize=(14, 7))

    for i, category in enumerate(categories):
        y = [len(categories) - 1 - i] * frame
        x = positions[:frame]
        vals = df_anim[category].values[:frame]

        ax.plot(x, y, marker='o', color=colors[i], linewidth=2)
        for j, val in enumerate(vals):
            ax.text(x[j], y[j] + 0.15, f"{val:.1f}k", ha='center', fontsize=10, color=colors[i])

    ax.set_yticks(range(len(categories)))
    ax.set_yticklabels(list(reversed(categories)))
    ax.set_xticks(positions[:frame])
    ax.set_xticklabels(months[:frame])
    ax.set_xlim(-0.5, len(months) - 0.5)
    ax.set_ylim(-1, len(categories))
    ax.set_title("Top 10 NYC Employment Categories by Jun 2025 (Goods Producing at Bottom)", fontsize=18)
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    plt.tight_layout()

    placeholder.pyplot(fig)
    time.sleep(3)

# Description Table (Centered Header)
st.markdown("---")
st.markdown(
    "<h2 style='text-align: center;'>Industry Categories and Descriptions</h2>",
    unsafe_allow_html=True
)

desc_df = pd.DataFrame({
    "Category": list(category_descriptions.keys()),
    "Description": list(category_descriptions.values())
})

st.table(desc_df)
