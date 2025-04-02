#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Mortgage Benchmark | TMC",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.image("https://raw.githubusercontent.com/koso9/Streamlit-Dashboard/main/streamlit_pic.png", use_container_width=True)


# ---- TITLE & KPIs ----
st.title("Mortgage Benchmark Summary")
st.subheader("March 2025")
st.write(
    "March brought continued market headwinds, with application volume dropping 12% as buyers faced persistent rate volatility. "
    "Government loan activity softened notably, while conventional margins rebounded slightly. Lenders are watching lock pull-through and CTC timelines closely "
    "as seasonal momentum builds heading into spring."
)


st.markdown ("#### Top Insight:")
st.info("**Application volume dropped 12%** month-over-month, led by a 19% decline in Government products. Likely driven by rate volatility and buyer hesitation.")

# KPI metrics
col1, col2, col3 = st.columns(3)
col1.metric("📥 App Volume MoM", "↓ 12%", "-12% vs Feb")
col2.metric("📊 Gross Margin", "227 bps", "+6 bps vs Feb")
col3.metric("📆 Avg CTC Days", "34", "± 0 vs Feb")

# Expandable insights
with st.expander(" See Additional Insights"):
    st.markdown("""
    - 🔻 Jumbo margins fell for the second straight month.
    - 🟢 Conventional margin recovery suggests stronger rate locks.
    - ⚠️ Southeast region saw the biggest volume drop (15%).
    """)

#st.markdown("---")

# ---- CHART 1: GROSS MARGIN ----
# ---- INTERACTIVE CHART 1: GROSS MARGIN FILTER ----
st.header("Product Margins in Motion")

data = {
    "Product": ["Conventional", "Government", "Jumbo", "Other"],
    "January (bps)": [208, 234, 164, 230],
    "February (bps)": [230, 275, 204, 214]
}
df = pd.DataFrame(data)

# Interactive dropdown
selected_product = st.selectbox("Choose a Product Type", df["Product"])

# Filter data
filtered_df = df[df["Product"] == selected_product]

# Plot
fig, ax = plt.subplots()
ax.bar(["January", "February"], [filtered_df["January (bps)"].values[0], filtered_df["February (bps)"].values[0]],
       color=["lightgreen", "orange"])
ax.set_title(f"Gross Margin for {selected_product}")
ax.set_ylabel("Basis Points (bps)")

st.pyplot(fig)
st.markdown("---")
st.info(
    "Conventional and Government products saw margin improvements in February, with gains of 22 and 41 basis points respectively.\n"
    "This likely reflects increased pricing power due to early spring demand and a more favorable secondary market."
)



# ---- CHART 2: APPLICATION & LOAN VOLUME % CHANGE ----
st.header("Momentum Check: Apps to Closing Snapshot")
#"Application and Loan Volume - MoM % Change")

#"Application and Loan Volume - MoM % Change")

# Sample extended data
volume_data = {
    "Channel": ["Retail", "Retail", "Wholesale", "Wholesale"],
    "Category": ["Application Volume", "Sold Loan Volume", "Application Volume", "Sold Loan Volume"],
    "Percent Change": [6, 7, 4, 5]
}
df = pd.DataFrame(volume_data)

# Filter dropdown
selected_channel = st.selectbox("Choose a Channel", df["Channel"].unique())

# Filter data by selected channel
filtered_df = df[df["Channel"] == selected_channel]

# Plot
# Corrected Chart 2 snippet
fig, ax = plt.subplots()
bars = ax.bar(filtered_df["Category"], filtered_df["Percent Change"], color=["skyblue", "salmon"])
ax.set_ylabel("Percent Change (%)")
ax.set_title(f"MoM Volume Change – {selected_channel}")

for bar in bars:
    height = bar.get_height()
    ax.annotate(f"{height}%",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 8),
                textcoords="offset points",
                ha='center', va='bottom')

ax.set_ylim(0, max(filtered_df["Percent Change"]) + 2)

st.pyplot(fig)
st.markdown("---")
st.info(
    "Despite market volatility, application volume climbed 6% month-over-month while sold loan volume outpaced it with a 7% increase.\n"
    "This signals lenders are improving pull-through or pricing strategies are driving more locks to funding."
)

# ---- CHART 3: APPLICATION TO CTC TIMELINE ----
st.header("Speed to Close: Operational Efficiency Check")

# Extended data with Loan Purpose
timeline_data = {
    "Month": ["Feb '24", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan '25", "Feb '25"] * 2,
    "Purpose": ["Purchase"] * 13 + ["Refinance"] * 13,
    "Days": [33, 31, 33, 33, 36, 36, 34, 34, 34, 34, 34, 37, 34,
             38, 36, 37, 39, 40, 40, 39, 38, 37, 36, 36, 37, 38]
}

timeline_df = pd.DataFrame(timeline_data)

# Dropdown filter
selected_purpose = st.selectbox("Select Loan Purpose", timeline_df["Purpose"].unique())

# Filter data
filtered_df = timeline_df[timeline_df["Purpose"] == selected_purpose]

# Plot
fig3, ax3 = plt.subplots()
ax3.plot(filtered_df["Month"], filtered_df["Days"], marker='o', linestyle='-', color='mediumslateblue')
ax3.set_ylabel("Days")
ax3.set_xlabel("Month")
ax3.set_title(f"Avg Time from App to Clear-to-Close ({selected_purpose})")
ax3.grid(False)

# Show every 2nd month label
ax3.set_xticks(range(0, len(filtered_df["Month"]), 2))
ax3.set_xticklabels(filtered_df["Month"][::2], rotation=45)

st.pyplot(fig3)
st.markdown("---")
st.info(
    "Average time from application to clear-to-close remained steady at 34 days, suggesting operational consistency.\n"
    "The January spike to 37 days now appears to be an outlier, likely driven by holiday pipeline delays."
)
