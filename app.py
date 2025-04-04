#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import seaborn as sns
import os

st.set_page_config(
    page_title="Mortgage Benchmark | TMC",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.image("https://raw.githubusercontent.com/koso9/Streamlit-Dashboard/main/streamlit_pic.png", use_container_width=True)

# --- Institution Type Filter ---
institution_type = st.selectbox("Select Institution Type", ["IMB", "Bank", "Credit Union"])

# --- Section Toggle ---
selected_section = st.radio("Navigate:", ["Summary", "Production", "Operations", "Secondary"], horizontal=True)

# --- Summary Section ---
if selected_section == "Summary":
    st.title("Mortgage Benchmark Summary")
    st.subheader("March 2025")
    st.write(
        "March brought continued market headwinds, with application volume dropping 12% as buyers faced persistent rate volatility. "
        "Government loan activity softened notably, while conventional margins rebounded slightly. Lenders are watching lock pull-through and CTC timelines closely "
        "as seasonal momentum builds heading into spring."
    )

    st.markdown ("#### Top Insight:")
    st.info("**Application volume dropped 12%** month-over-month, led by a 19% decline in Government products. Likely driven by rate volatility and buyer hesitation.")

    col1, col2, col3 = st.columns(3)
    col1.metric("App Volume MoM", "↓ 12%", "-12% vs Feb")
    col2.metric("Gross Margin", "227 bps", "+6 bps vs Feb")
    col3.metric("Avg CTC Days", "34", "± 0 vs Feb")

    with st.expander(" See Additional Insights"):
        st.markdown ('''
        - Jumbo margins fell for the second straight month.
        - Conventional margin recovery suggests stronger rate locks.
        - Southeast region saw the biggest volume drop (15%).
        ''')

    st.markdown("---")

# --- Operations Section with Sparkline KPI Cards (Enhanced) ---
elif selected_section == "Operations":
    st.subheader("Operational Trends by KPI")

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    metrics = ["CTC Days", "Margin (bps)", "Pull-Through Rate"]

    data_peer = {
        "IMB": [
            [34, 33, 32, 32, 33, 34, 34, 35, 34, 33, 34, 34],
            [210, 212, 214, 216, 218, 221, 223, 224, 225, 226, 228, 229],
            [66, 67, 68, 69, 69, 70, 71, 72, 73, 74, 73, 72],
        ]
    }

    data_myco = {
        "IMB": [
            [36, 35, 34, 33, 32, 34, 36, 37, 38, 36, 35, 34],
            [215, 217, 218, 220, 222, 225, 227, 228, 229, 230, 231, 229],
            [68, 69, 70, 72, 71, 72, 74, 73, 74, 75, 74, 73],
        ]
    }

    df_peer = pd.DataFrame(data_peer[institution_type], index=metrics, columns=months)
    df_myco = pd.DataFrame(data_myco[institution_type], index=metrics, columns=months)

    st.write(f"**Institution: {institution_type}**")

    def sparkline_comparison(metric, my_values, peer_values, my_color, peer_color):
        fig, ax = plt.subplots(figsize=(10, 2))
        ax.plot(months, my_values, marker='o', linewidth=2, label='My Company', color=my_color)
        ax.plot(months, peer_values, marker='x', linestyle='--', linewidth=2, label='Peer Group', color=peer_color)
        ax.set_ylabel(metric)
        ax.set_xticks(range(len(months)))
        ax.set_xticklabels(months, fontsize=8, rotation=45)
        ax.legend(loc='upper left')
        ax.set_title(f"{metric} — My Co: {my_values[-1]} | Peer: {peer_values[-1]}", fontsize=11, weight='bold')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', linestyle='--', alpha=0.3)
        st.pyplot(fig)

    st.markdown("### Monthly Sparkline Comparison")
    sparkline_comparison("CTC Days", df_myco.loc["CTC Days"].values, df_peer.loc["CTC Days"].values, "#1E3A8A", "#90CAF9")
    sparkline_comparison("Margin (bps)", df_myco.loc["Margin (bps)"].values, df_peer.loc["Margin (bps)"].values, "#2892D7", "#81D4FA")
    sparkline_comparison("Pull-Through Rate", df_myco.loc["Pull-Through Rate"].values, df_peer.loc["Pull-Through Rate"].values, "#F72585", "#F48FB1")

    st.caption("Each chart compares monthly performance over 12 months for your company vs. the peer group. Dashed line indicates peer trend.")



    st.markdown("---")
    st.subheader("Salary by Role")

    salary_data = {
        "Closer": {"My Company": 16000, "Peer Group": 58000},
        "Processor": {"My Company": 26000, "Peer Group": 60000},
        "Underwriter": {"My Company": 35000, "Peer Group": 92000},
    }

    selected_role = st.selectbox("Select a Role to Compare Salaries:", list(salary_data.keys()))
    selected = salary_data[selected_role]

    def draw_people_chart(filled_count, total=10):
        fig, ax = plt.subplots(figsize=(total, 1))
        for i in range(total):
            icon_color = '#009CA6' if i < filled_count else '#D9EDF7'
            ax.add_patch(plt.Rectangle((i, 0), 0.8, 1, color=icon_color))
        ax.set_xlim(0, total)
        ax.set_ylim(0, 1)
        ax.axis('off')
        return fig

    st.markdown(f"### {selected_role}")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**My Company Salary**")
        st.markdown(f"${selected['My Company']:,}")
        fig1 = draw_people_chart(int(selected['My Company'] // 10000))
        st.pyplot(fig1)

    with col2:
        st.markdown("**Peer Group Salary**")
        st.markdown(f"${selected['Peer Group']:,}")
        fig2 = draw_people_chart(int(selected['Peer Group'] // 10000))
        st.pyplot(fig2)

    st.caption("*Each person shape represents approximately $10,000 in salary. Color indicates the amount filled versus target scale of 10 icons.*")

# --- Production Section with Refined Quarterly View and Monthly Selector ---
elif selected_section == "Production":
    st.subheader("Loan Type Comparison")

    # Generate 12 months of fake data
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    quarters = {"Jan": "Q1", "Feb": "Q1", "Mar": "Q1",
                "Apr": "Q2", "May": "Q2", "Jun": "Q2",
                "Jul": "Q3", "Aug": "Q3", "Sep": "Q3",
                "Oct": "Q4", "Nov": "Q4", "Dec": "Q4"}
    loan_types = ["Conventional", "Government", "Jumbo", "Other"]

    # Dual-tone color palette
    peer_colors = {
        "Conventional": "#19D3F3",
        "Government": "#F72585",
        "Jumbo": "#7209B7",
        "Other": "#3A0CA3"
    }
    myco_colors = {
        "Conventional": "#126782",
        "Government": "#9D174D",
        "Jumbo": "#4B0082",
        "Other": "#1E1B5E"
    }

    np.random.seed(42)
    data = []
    for month in months:
        for loan in loan_types:
            peer_units = np.random.randint(40, 120)
            peer_volume = peer_units * np.random.randint(200000, 500000)
            my_units = int(peer_units * np.random.uniform(0.4, 0.7))
            my_volume = int(my_units * np.random.randint(200000, 500000))
            data.append([month, quarters[month], loan, peer_units, peer_volume, my_units, my_volume])

    df = pd.DataFrame(data, columns=["Month", "Quarter", "Loan Type", "Peer Units", "Peer Volume", "My Units", "My Volume"])

    # --- Toggle between Units and Volume ---
    view = st.radio("Select View", ["Units", "Volume"], horizontal=True)

    # --- Quarterly Grouped Bar Chart ---
    st.markdown("### Quarterly View")
    df_q = df.groupby(["Quarter", "Loan Type"]).agg({
        "Peer Units": "sum", "Peer Volume": "sum",
        "My Units": "sum", "My Volume": "sum"
    }).reset_index()

    fig_q, ax_q = plt.subplots(figsize=(10, 6))
    x = np.arange(len(["Q1", "Q2", "Q3", "Q4"]))
    width = 0.35

    for i, loan in enumerate(loan_types):
        q_vals_peer = []
        q_vals_my = []
        for q in ["Q1", "Q2", "Q3", "Q4"]:
            row = df_q[(df_q["Quarter"] == q) & (df_q["Loan Type"] == loan)]
            if view == "Units":
                q_vals_peer.append(row["Peer Units"].values[0])
                q_vals_my.append(row["My Units"].values[0])
            else:
                q_vals_peer.append(row["Peer Volume"].values[0] / 1e6)
                q_vals_my.append(row["My Volume"].values[0] / 1e6)

        offset = (i - 1.5) * (width / len(loan_types))
        ax_q.bar(x + offset, q_vals_peer, width=width / 2, label=f"Peer – {loan}", color=peer_colors[loan])
        ax_q.bar(x + offset + width / 2, q_vals_my, width=width / 2, label=f"My Co – {loan}", color=myco_colors[loan])

    ax_q.set_xticks(x)
    ax_q.set_xticklabels(["Q1", "Q2", "Q3", "Q4"])
    ax_q.set_ylabel("Loan Units" if view == "Units" else "Loan Volume ($M)")
    ax_q.set_title("Quarterly Product Comparison")
    ax_q.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig_q)

    # --- Monthly Drilldown by Selector ---
    st.markdown("### Monthly Drilldown by Product")
    selected_month = st.selectbox("Select a Month", months)
    df_month = df[df["Month"] == selected_month]

    fig_m, ax_m = plt.subplots(figsize=(10, 5))
    x = np.arange(len(loan_types))
    width = 0.35

    if view == "Units":
        peer_vals = df_month.groupby("Loan Type")["Peer Units"].sum().reindex(loan_types)
        my_vals = df_month.groupby("Loan Type")["My Units"].sum().reindex(loan_types)
    else:
        peer_vals = df_month.groupby("Loan Type")["Peer Volume"].sum().reindex(loan_types) / 1e6
        my_vals = df_month.groupby("Loan Type")["My Volume"].sum().reindex(loan_types) / 1e6

    for i, loan in enumerate(loan_types):
        ax_m.bar(i - width / 2, peer_vals[loan], width=width, label=f"Peer – {loan}" if i == 0 else "", color=peer_colors[loan])
        ax_m.bar(i + width / 2, my_vals[loan], width=width, label=f"My Co – {loan}" if i == 0 else "", color=myco_colors[loan])

    ax_m.set_xticks(x)
    ax_m.set_xticklabels(loan_types)
    ax_m.set_ylabel("Loan Units" if view == "Units" else "Loan Volume ($M)")
    ax_m.set_title(f"Loan Type Breakdown – {selected_month}")
    st.pyplot(fig_m)
