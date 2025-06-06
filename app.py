#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import random
import plotly.graph_objects as go

# --- Utility: Responsive chart size ---
def is_mobile():
    return st.session_state.get("force_mobile", False)

# Optional: Manual toggle (left sidebar if you want control)
# st.sidebar.checkbox("Force Mobile Mode", value=False, key="force_mobile")

# --- UI HEADER ---
st.image("https://raw.githubusercontent.com/koso9/Streamlit-Dashboard/main/streamlit_pic.png", use_container_width=True)


# --- Section Toggle ---
selected_section = st.radio("Navigate:", ["Summary", "Production", "Operations", "Secondary"], horizontal=True)

# --- Show Institution Filter (not on Summary) ---
if selected_section != "Summary":
    institution_type = st.selectbox("Select Institution Type", ["IMB", "Bank", "Credit Union"])

# --- SUMMARY PAGE ---
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

    # --- NEW MEMBERS MAP ---
    st.markdown("### We Love Our Members!")
    st.write(
    "We’re excited to welcome new members to our growing community of over 200 mortgage institutions. "
    "Members gain access to benchmark insights, collaboration opportunities, and innovative technology partners. "
    "Our network spans across the U.S., including IMBs, Banks, and Credit Unions — all organized by their annual production volume."
)

    volume_filter = st.selectbox("Volume", ["All", "Under $500M", "$500M–$1B", "Over $1B"])

    def volume_category(volume):
        if volume < 500:
            return "Under $500M"
        elif 500 <= volume <= 1000:
            return "$500M–$1B"
        else:
            return "Over $1B"

    types = ["IMB", "Bank", "CU"]
    colors = {"IMB": "#19D3F3", "Bank": "#1E3A8A", "CU": "#C5F500"}

    cities = [
        ("Seattle", 47.61, -122.33), ("San Francisco", 37.77, -122.42), ("San Diego", 32.72, -117.16),
        ("Denver", 39.74, -104.99), ("Phoenix", 33.44, -112.07), ("Salt Lake City", 40.76, -111.89),
        ("Dallas", 32.77, -96.79), ("Houston", 29.76, -95.36), ("Atlanta", 33.75, -84.39),
        ("Miami", 25.76, -80.19), ("Nashville", 36.16, -86.78), ("Charlotte", 35.22, -80.84),
        ("Chicago", 41.87, -87.62), ("Minneapolis", 44.98, -93.26), ("Detroit", 42.33, -83.05),
        ("Boston", 42.36, -71.06), ("Philadelphia", 39.95, -75.16), ("New York", 40.71, -74.00),
        ("Washington DC", 38.90, -77.03), ("Pittsburgh", 40.44, -79.99)
    ]

    member_data = []
    for i in range(200):
        city, base_lat, base_lon = random.choice(cities)
        jitter_lat = base_lat + random.uniform(-0.5, 0.5)
        jitter_lon = base_lon + random.uniform(-0.5, 0.5)
        m_type = random.choice(types)
        volume = random.randint(100, 1500)
        member_data.append({
            "Name": f"Company {i+1}",
            "City": city,
            "Lat": jitter_lat,
            "Lon": jitter_lon,
            "Type": m_type,
            "Color": colors[m_type],
            "Volume": volume,
            "Category": volume_category(volume)
        })

    if volume_filter != "All":
        member_data = [m for m in member_data if m["Category"] == volume_filter]

    fig = go.Figure()
    for t in types:
        df_subset = [m for m in member_data if m["Type"] == t]
        fig.add_trace(go.Scattergeo(
            lon=[m["Lon"] for m in df_subset],
            lat=[m["Lat"] for m in df_subset],
            mode='markers',
            marker=dict(
                size=[max(6, m["Volume"] // 100) for m in df_subset],
                color=colors[t],
                opacity=0.6,
                line=dict(width=0)
            ),
            name=t,
            text=[f"{m['Name']}<br>{m['City']}<br>Volume: ${m['Volume']}M" for m in df_subset],
            hoverinfo='text'
        ))

    fig.update_layout(
        geo=dict(
            scope='usa',
            projection_type='albers usa',
            showland=True,
            landcolor="white",
            subunitcolor="lightgray",
            countrycolor="lightgray",
            showlakes=False,
            showcoastlines=False,
            showframe=False,
            bgcolor="rgba(0,0,0,0)"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=20, b=0, l=0, r=0),
    )

    st.plotly_chart(fig, use_container_width=True)

# --- OPERATIONS PAGE ---
if selected_section == "Operations":
    st.markdown("## March Performance Overview")

    df_kpi = pd.DataFrame({
        "Metric": ["CTC Days", "Margin", "Pull%"],
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

    st.subheader("How efficient was your Operations vs Peers?")

    st.write(
        "March marked a turning point in operational efficiency across many lending institutions. "
        "Cycle times, after months of fluctuation, have begun to stabilize—suggesting process improvements and better pipeline management. "
        "Gross margins showed modest but meaningful improvement, a positive sign as lenders continue to adapt to compressed market conditions. "
        "Notably, pull-through rates remained resilient, indicating stronger borrower commitment and possibly more strategic rate lock behavior. "
        "This snapshot helps benchmark your position against peers and track month-over-month momentum across the past 6 months. "
        "Use it to identify operational strengths, uncover emerging gaps, and prioritize focus areas as the spring market builds momentum."
    )

    st.markdown("### 🔥 Momentum Tracker: Ops Metrics Over Time")

    # Generate data for heatmap
    months = ["Sep", "Oct", "Nov", "Dec", "Jan", "Feb"]

    metrics = ["CTC Days", "Margin", "Pull%"]
    values = {
    "CTC Days": [36, 34, 33, 32, 34, 33],        # Last 6 from original
    "Margin":   [229, 228, 226, 227, 221, 223],
    "Pull%":    [75, 74, 75, 76, 70, 71]
}


    df = pd.DataFrame([
        {"Month": m, "Metric": metric, "Value": values[metric][i]}
        for metric in metrics
        for i, m in enumerate(months)
    ])

    # Classify performance
    def classify(series):
        baseline = series.mean()
        return [
            "Strong" if x > baseline + 1 else
            "Weak" if x < baseline - 1 else
            "Neutral" for x in series
        ]

    df["Category"] = df.groupby("Metric")["Value"].transform(classify)
    df["Value Display"] = df.apply(
        lambda row: f"{int(row['Value'])}%" if row["Metric"] == "Pull%" else f"{int(row['Value'])}",
        axis=1
    )

    color_scale = alt.Scale(
        domain=["Strong", "Neutral", "Weak"],
        range=["#00F5A0", "#E5E7EB", "#FF6B6B"]
    )

    base = alt.Chart(df).encode(
        x=alt.X("Month:O", sort=months, axis=alt.Axis(labelFontSize=11, title="2024–2025")),
        y=alt.Y("Metric:N", axis=alt.Axis(labelFontSize=12, title=None)),
    )

    heat = base.mark_rect().encode(
        color=alt.Color("Category:N", scale=color_scale, legend=alt.Legend(title=None)),
        tooltip=["Metric", "Month", "Value"]
    )

    text = base.mark_text(baseline="middle", fontSize=11).encode(
        text="Value Display:N",
        color=alt.value("black")
    )

    # Render chart
    st.altair_chart((heat + text).properties(width=360, height=180), use_container_width=True)

# --- Production Section ---
if selected_section == "Production":
    st.subheader("What's Driving Loan Volume Trends?")

    st.write(
        "Loan production patterns often tell the story of borrower behavior, market volatility, and lender strategy. "
        "This section highlights year-long trends in volume and units by loan type—Conventional, Government, Jumbo, and Other—"
        "to help identify where your institution stands compared to peers."
    )

    st.markdown(
        "Across the last 12 months, we've seen notable shifts: conventional loans continue to dominate overall volume, "
        "while government-backed loans experience steeper fluctuations likely tied to changing rate sensitivity among FHA/VA borrowers. "
        "Jumbo loans saw a late-year rebound, suggesting renewed confidence in high-balance lending. "
        "Use the filters below to explore how your performance compares and spot pockets of opportunity or concern."
    )

    # Loan type dropdown
    loan_types = ["Conventional", "Government", "Jumbo", "Other"]
    selected_loan = st.selectbox("Select Loan Type", loan_types)

    # Units vs Volume toggle
    view_option = st.radio("Select View", ["Units", "Volume"], horizontal=True)

    # Color mapping
    loan_colors = {
        "Conventional": "#D5FF00",  # Neon green-yellow
        "Government": "#19D3F3",    # Turquoise
        "Jumbo": "#AEE6FF",         # Bright baby blue
        "Other": "#FF6B6B"          # Bright coral
    }
    peer_gray = "#B0B0B0"

    # Generate synthetic data
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    np.random.seed(42)
    data = []
    for month in months:
        for loan in loan_types:
            peer_units = np.random.randint(80, 130)
            peer_volume = peer_units * np.random.randint(250000, 500000)
            my_units = int(peer_units * np.random.uniform(0.4, 0.8))
            my_volume = int(my_units * np.random.randint(250000, 500000))
            data.append([month, loan, peer_units, peer_volume, my_units, my_volume])

    df = pd.DataFrame(data, columns=["Month", "Loan Type", "Peer Units", "Peer Volume", "My Units", "My Volume"])
    df_filtered = df[df["Loan Type"] == selected_loan].copy()

    # Choose metric
    if view_option == "Units":
        y_data = "My Units"
        peer_data = "Peer Units"
        y_label = "Loan Units"
    else:
        y_data = "My Volume"
        peer_data = "Peer Volume"
        y_label = "Loan Volume ($M)"
        df_filtered[y_data] = df_filtered[y_data] / 1e6
        df_filtered[peer_data] = df_filtered[peer_data] / 1e6

    # Create Plotly figure
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=df_filtered["Month"],
        x=df_filtered[peer_data],
        name="Peer Avg",
        orientation='h',
        marker=dict(color=peer_gray),
        hovertemplate='Peer Avg: %{x:.2f}<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        y=df_filtered["Month"],
        x=df_filtered[y_data],
        name="My Company",
        orientation='h',
        marker=dict(color=loan_colors[selected_loan]),
        hovertemplate='My Co: %{x:.2f}<extra></extra>'
    ))

    # Properly apply layout AFTER fig is created
    fig.update_layout(
        barmode='overlay',
        title=f"12-Month Trend – {selected_loan} Loans",
        xaxis_title=y_label,
        yaxis=dict(autorange='reversed'),
        margin=dict(t=40, b=40, l=20, r=20),
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
        plot_bgcolor='white',
        height=500,
        modebar_remove=["zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d"]
    )

    # Optional: small spacing to avoid overlap with select boxes
    st.markdown("<br>", unsafe_allow_html=True)

    st.plotly_chart(fig, use_container_width=True)
