#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---- TITLE ----
st.title( "Benchmark Summary")
st.subheader("March 2025 ")
st.write("Top Insight: 45% decrease of X !")

st.markdown("---")

# ---- CHART 1: GROSS MARGIN ----
# ---- INTERACTIVE CHART 1: GROSS MARGIN FILTER ----
st.header("Gross Margin by Product Type")

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
st.info("Are my margins in line with peers? suggestion: add percentile rankings")


# ---- CHART 2: APPLICATION & LOAN VOLUME % CHANGE ----
st.header("Application and Loan Volume - MoM % Change")

volume_data = {
    "Category": ["Application Volume", "Sold Loan Volume"],
    "Percent Change": [6, 7]
}
vol_df = pd.DataFrame(volume_data)

fig2, ax2 = plt.subplots()
bars = ax2.bar(vol_df["Category"], vol_df["Percent Change"], color=["skyblue", "salmon"])
ax2.set_ylabel("Percent Change (%)")
ax2.set_title("Month-over-Month Change in Volume")

for bar in bars:
    height = bar.get_height()
    ax2.annotate(f"{height}%",
                 xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3),
                 textcoords="offset points",
                 ha='center', va='bottom')

st.pyplot(fig2)
st.markdown("---")
st.info("How does this compare to others in my region/volume tier? Suggestion: add peer comparison, seasonality.")

# ---- CHART 3: APPLICATION TO CTC TIMELINE ----
st.header("Average Time from Application to Clear-to-Close")

timeline_data = {
    "Month": [
        "Feb '24", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan '25", "Feb '25"
    ],
    "Days": [33, 31, 33, 33, 36, 36, 34, 34, 34, 34, 34, 37, 34]
}
timeline_df = pd.DataFrame(timeline_data)

fig3, ax3 = plt.subplots()
ax3.plot(timeline_df["Month"], timeline_df["Days"], marker='o', linestyle='-', color='mediumslateblue')
ax3.set_ylabel("Days")
ax3.set_xlabel("Month")
ax3.set_title("Avg Time from App to Clear-to-Close (in Days)")
ax3.grid(True)

# Rotate and reduce ticks
ax3.set_xticks(range(0, len(timeline_df["Month"]), 2))  # Show every 2nd label
ax3.set_xticklabels(timeline_df["Month"][::2], rotation=45)
         
st.pyplot(fig3)
st.markdown("---")
st.info("What is my average app to ctc turn-time?: suggestion: add filter by channel or compare with 25% of perfomers")




