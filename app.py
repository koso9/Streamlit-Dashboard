#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import plotly.graph_objects as go

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

    st.markdown("#### Top Insight:")
    st.info("**Application volume dropped 12%** month-over-month, led by a 19% decline in Government products. Likely driven by rate volatility and buyer hesitation.")

    col1, col2, col3 = st.columns(3)
    col1.metric("App Volume MoM", "↓ 12%", "-12% vs Feb")
    col2.metric("Gross Margin", "227 bps", "+6 bps vs Feb")
    col3.metric("Avg CTC Days", "34", "± 0 vs Feb")

    with st.expander(" See Additional Insights"):
        st.markdown('''
        - Jumbo margins fell for the second straight month.
        - Conventional margin recovery suggests stronger rate locks.
        - Southeast region saw the biggest volume drop (15%).
        ''')

    st.markdown("---")

# --- Operations Section ---
elif selected_section == "Operations":
    st.subheader("Operational Trends by KPI")

    # --- Salary by Role ---
    st.markdown("## 💼 Salary Comparison by Role")

    salary_data = {
        "Closer": {"My Company": 16000, "Peer Group": 58000},
        "Processor": {"My Company": 26000, "Peer Group": 60000},
        "Underwriter": {"My Company": 35000, "Peer Group": 92000},
    }

    selected_role = st.selectbox("Select a Role to Compare Salaries:", list(salary_data.keys()))
    selected = salary_data[selected_role]

    def draw_salary_icons(salary, color="#009CA6", total_icons=10):
        full_units = int(salary // 10000)
        partial_fill = (salary % 10000) / 10000
        shapes = []

        for i in range(total_icons):
            x0 = i
            x1 = i + 0.8

            shapes.append(dict(type="rect", x0=x0, x1=x1, y0=0, y1=1, line=dict(width=0), fillcolor="#D9EDF7"))
            shapes.append(dict(type="circle", x0=x0 + 0.25, x1=x0 + 0.55, y0=1.05, y1=1.35, line=dict(width=0), fillcolor="#D9EDF7"))

            if i < full_units:
                shapes.append(dict(type="rect", x0=x0, x1=x1, y0=0, y1=1, line=dict(width=0), fillcolor=color))
                shapes.append(dict(type="circle", x0=x0 + 0.25, x1=x0 + 0.55, y0=1.05, y1=1.35, line=dict(width=0), fillcolor=color))
            elif i == full_units and partial_fill > 0:
                shapes.append(dict(type="rect", x0=x0, x1=x1, y0=0, y1=partial_fill, line=dict(width=0), fillcolor=color))

        fig = go.Figure()
        fig.update_layout(shapes=shapes, height=160, width=70 * total_icons, margin=dict(l=0, r=0, t=0, b=0),
                          xaxis=dict(visible=False), yaxis=dict(visible=False))
        fig.update_yaxes(range=[-0.5, 1.6])
        fig.update_xaxes(range=[-0.5, total_icons])
        return fig

    st.markdown(f"### {selected_role}")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**My Company Salary**")
        st.markdown(f"${selected['My Company']:,}")
        fig1 = draw_salary_icons(selected['My Company'])
        st.plotly_chart(fig1, use_container_width=False)

    with col2:
        st.markdown("**Peer Group Salary**")
        st.markdown(f"${selected['Peer Group']:,}")
        fig2 = draw_salary_icons(selected['Peer Group'])
        st.plotly_chart(fig2, use_container_width=False)

    st.caption("*Each person icon represents ~$10,000 in salary.*")
    st.markdown("<div style='margin-top: 40px'></div>", unsafe_allow_html=True)

    # --- Operational KPI Summary ---
    st.markdown("## 📊 Operational KPI Overview")

    df_kpi = pd.DataFrame({
        "Metric": ["CTC Days", "Margins (bps)", "Pull-Through"],
        "MyCo": [32, 227, 75],
        "Peer Avg": [34, 225, 73],
        "Change": [-2, 6, 2],
        "Unit": [" days", " bps", "%"]
    })

    col1, col2, col3 = st.columns(3)
    for i, col in enumerate([col1, col2, col3]):
        metric = df_kpi.loc[i, "Metric"]
        myco_val = df_kpi.loc[i, "MyCo"]
        peer_val = df_kpi.loc[i, "Peer Avg"]
        delta = df_kpi.loc[i, "Change"]
        unit = df_kpi.loc[i, "Unit"]

        arrow = "↑" if delta > 0 else "↓" if delta < 0 else "→"
        delta_text = f"{arrow}{abs(delta)}{unit}"

        col.metric(label=metric, value=f"{myco_val}{unit}", delta=delta_text + f" vs Peer: {peer_val}{unit}")

    st.markdown("<div style='margin-top: 20px'></div>", unsafe_allow_html=True)

    # --- 12-Month KPI Performance Grid ---
    st.markdown("### 12-Month KPI Performance Grid")

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    metrics = ["CTC Days", "Margins (bps)", "Pull-Through"]
    values = {
        "CTC Days":       [34, 33, 32, 31, 34, 35, 36, 37, 36, 34, 33, 32],
        "Margins (bps)":  [221, 223, 222, 220, 224, 225, 226, 227, 229, 228, 226, 227],
        "Pull-Through":   [70, 71, 72, 71, 73, 72, 74, 75, 75, 74, 75, 76]
    }

    df = pd.DataFrame([
        {"Month": m, "Metric": metric, "Value": values[metric][i]}
        for metric in metrics
        for i, m in enumerate(months)
    ])

    def classify(series):
        baseline = series.mean()
        return [
            "Strong" if x > baseline + 1 else
            "Weak" if x < baseline - 1 else
            "Neutral" for x in series
        ]

    df["Category"] = df.groupby("Metric")["Value"].transform(classify)
    df["Value Display"] = df.apply(
        lambda row: f"{int(row['Value'])}%" if "Pull" in row["Metric"] else f"{int(row['Value'])}", axis=1
    )

    color_scale = alt.Scale(
        domain=["Strong", "Neutral", "Weak"],
        range=["#00F5A0", "#D9EDF7", "#FF6B6B"]
    )

    heat = alt.Chart(df).mark_rect().encode(
        x=alt.X("Month:O", title="Month", sort=months, axis=alt.Axis(labelAngle=0, labelFontSize=14)),
        y=alt.Y("Metric:N", title="", axis=alt.Axis(labelFontSize=15)),
        color=alt.Color("Category:N", scale=color_scale, legend=alt.Legend(title="Performance", labelFontSize=13, titleFontSize=14)),
        tooltip=["Metric", "Month", "Value"]
    ).properties(width=1000, height=300)

    text = alt.Chart(df).mark_text(
        baseline="middle",
        fontSize=14
    ).encode(
        x="Month:O",
        y="Metric:N",
        text="Value Display:N",
        color=alt.value("black")
    )

    st.altair_chart(heat + text, use_container_width=True)

# --- Production Section Placeholder ---
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
    st.markdown("### 📊 Quarterly Product Comparison")
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
    ax_q.set_title("Quarterly Comparison")
    ax_q.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig_q)

    # --- Monthly Drilldown by Selector ---
    st.markdown("### 📅 Monthly Product Breakdown")
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
    ax_m.set_title(f"Loan Breakdown – {selected_month}")
    st.pyplot(fig_m)

    st.markdown("---")


# --- Secondary Section Placeholder ---
elif selected_section == "Secondary":
    st.subheader("Secondary Market Trends")
    st.markdown("Coming soon...")
