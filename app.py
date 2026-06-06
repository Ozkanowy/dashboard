import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Analytics Pro | Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Dark gradient background */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* Metric cards */
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 20px;
    backdrop-filter: blur(8px);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.4);
}

/* Section headers */
h1, h2, h3 {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* Tab styling */
button[data-baseweb="tab"] {
    background: transparent !important;
    color: rgba(255,255,255,0.6) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: rgba(99, 102, 241, 0.3) !important;
    color: #ffffff !important;
    border-bottom: 2px solid #6366f1 !important;
}

/* Selectbox & sliders */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: white !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.5); border-radius: 10px; }

/* Custom card */
.glass-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(10px);
    margin-bottom: 16px;
}

.gradient-text {
    background: linear-gradient(90deg, #6366f1, #a78bfa, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.4rem;
    font-weight: 700;
    line-height: 1.2;
}

.badge {
    display: inline-block;
    background: rgba(99,102,241,0.25);
    color: #a78bfa;
    border: 1px solid rgba(99,102,241,0.4);
    border-radius: 999px;
    padding: 2px 12px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}

.stat-row {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
}
</style>
""", unsafe_allow_html=True)


# ── Data Generation ─────────────────────────────────────────────────────────────
@st.cache_data
def generate_sales_data(days=180, seed=42):
    np.random.seed(seed)
    dates = [datetime(2025, 1, 1) + timedelta(days=i) for i in range(days)]
    categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books"]
    regions = ["North America", "Europe", "Asia Pacific", "Latin America"]

    records = []
    for d in dates:
        for cat in categories:
            for reg in regions:
                base = {"Electronics": 8000, "Clothing": 4000,
                        "Home & Garden": 3000, "Sports": 2500, "Books": 1200}[cat]
                trend = 1 + (dates.index(d) / days) * 0.3
                seasonality = 1 + 0.15 * np.sin(2 * np.pi * dates.index(d) / 30)
                revenue = base * trend * seasonality * np.random.uniform(0.8, 1.2)
                records.append({
                    "date": d, "category": cat, "region": reg,
                    "revenue": round(revenue, 2),
                    "units": int(revenue / random.uniform(20, 80)),
                    "profit_margin": round(np.random.uniform(0.12, 0.45), 3),
                })
    return pd.DataFrame(records)


@st.cache_data
def generate_user_data(seed=42):
    np.random.seed(seed)
    n = 500
    df = pd.DataFrame({
        "user_id": range(1, n + 1),
        "age": np.random.normal(35, 10, n).clip(18, 70).astype(int),
        "spend": np.random.exponential(300, n).clip(5, 2000).round(2),
        "sessions": np.random.poisson(12, n),
        "satisfaction": np.random.choice([1, 2, 3, 4, 5],
                                         p=[0.05, 0.10, 0.20, 0.35, 0.30], size=n),
        "segment": np.random.choice(["Premium", "Standard", "Basic"],
                                    p=[0.20, 0.50, 0.30], size=n),
        "country": np.random.choice(["USA", "UK", "Germany", "Japan", "Brazil",
                                      "Canada", "Australia", "France"],
                                    p=[0.30, 0.15, 0.12, 0.10, 0.08,
                                       0.10, 0.08, 0.07], size=n),
    })
    return df


df_sales = generate_sales_data()
df_users = generate_user_data()

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.03)",
    font_color="#e2e8f0",
    font_family="Inter",
    xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.1)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.1)"),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.1)"),
    margin=dict(l=10, r=10, t=40, b=10),
)
COLOR_SEQ = px.colors.qualitative.Vivid


# ── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="gradient-text">Analytics Pro</div>', unsafe_allow_html=True)
    st.markdown('<span class="badge">✦ LIVE DASHBOARD</span>', unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["📊 Overview", "📈 Sales Deep Dive", "👥 User Insights", "🌍 Regional Map"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### ⚙️ Filters")

    date_range = st.slider(
        "Date Range (days back)",
        min_value=30, max_value=180, value=90, step=10,
    )

    categories = st.multiselect(
        "Categories",
        ["Electronics", "Clothing", "Home & Garden", "Sports", "Books"],
        default=["Electronics", "Clothing", "Home & Garden"],
    )

    regions = st.multiselect(
        "Regions",
        ["North America", "Europe", "Asia Pacific", "Latin America"],
        default=["North America", "Europe", "Asia Pacific", "Latin America"],
    )

    st.markdown("---")
    st.markdown(
        '<div style="color:rgba(255,255,255,0.4);font-size:0.75rem;">Last updated: '
        + datetime.now().strftime("%b %d, %Y %H:%M")
        + "</div>",
        unsafe_allow_html=True,
    )

# ── Filter data ─────────────────────────────────────────────────────────────────
cutoff = datetime(2025, 1, 1) + timedelta(days=180 - date_range)
mask = (
    (df_sales["date"] >= cutoff)
    & (df_sales["category"].isin(categories if categories else ["Electronics"]))
    & (df_sales["region"].isin(regions if regions else ["North America"]))
)
df_f = df_sales[mask].copy()

total_rev = df_f["revenue"].sum()
total_units = df_f["units"].sum()
avg_margin = df_f["profit_margin"].mean()
prev_rev = df_f["revenue"].sum() * 0.87  # simulated prior period


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Overview
# ══════════════════════════════════════════════════════════════════════════════
if page == "📊 Overview":
    st.markdown('<h1 class="gradient-text">Business Overview</h1>', unsafe_allow_html=True)
    st.markdown(
        f'<span class="badge">📅 Last {date_range} days</span>&nbsp;'
        f'<span class="badge">🗂 {len(categories)} categories</span>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Total Revenue", f"${total_rev:,.0f}",
              f"+{((total_rev - prev_rev) / prev_rev * 100):.1f}%")
    c2.metric("📦 Units Sold", f"{total_units:,}",
              f"+{np.random.randint(5, 20)}%")
    c3.metric("📊 Avg Profit Margin", f"{avg_margin:.1%}",
              f"+{np.random.uniform(0.5, 2.5):.1f}%")
    c4.metric("🛒 Orders", f"{len(df_f):,}",
              f"+{np.random.randint(3, 15)}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # Revenue trend
    col_l, col_r = st.columns([2, 1])

    with col_l:
        st.markdown("#### Revenue Trend by Category")
        daily = (
            df_f.groupby(["date", "category"])["revenue"]
            .sum()
            .reset_index()
        )
        fig_trend = px.area(
            daily, x="date", y="revenue", color="category",
            color_discrete_sequence=COLOR_SEQ,
        )
        fig_trend.update_layout(**PLOTLY_LAYOUT, height=340)
        fig_trend.update_traces(line_width=2)
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_r:
        st.markdown("#### Revenue Share")
        by_cat = df_f.groupby("category")["revenue"].sum().reset_index()
        fig_pie = px.pie(
            by_cat, names="category", values="revenue",
            hole=0.55, color_discrete_sequence=COLOR_SEQ,
        )
        fig_pie.update_layout(**PLOTLY_LAYOUT, height=340,
                               showlegend=True)
        fig_pie.update_traces(textinfo="percent", textfont_size=12)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Margin heatmap
    st.markdown("#### Profit Margin Heatmap (Category × Region)")
    pivot = df_f.pivot_table(
        index="category", columns="region",
        values="profit_margin", aggfunc="mean"
    )
    fig_heat = px.imshow(
        pivot,
        text_auto=".1%",
        color_continuous_scale="Viridis",
        aspect="auto",
    )
    fig_heat.update_layout(**PLOTLY_LAYOUT, height=280,
                            coloraxis_showscale=False)
    st.plotly_chart(fig_heat, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Sales Deep Dive
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📈 Sales Deep Dive":
    st.markdown('<h1 class="gradient-text">Sales Deep Dive</h1>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📅 Weekly Aggregation", "📦 Category Comparison", "🔍 Distribution"])

    with tab1:
        df_f["week"] = df_f["date"].dt.to_period("W").apply(lambda r: r.start_time)
        weekly = df_f.groupby(["week", "region"]).agg(
            revenue=("revenue", "sum"),
            units=("units", "sum"),
        ).reset_index()

        fig_bar = px.bar(
            weekly, x="week", y="revenue", color="region",
            barmode="group", color_discrete_sequence=COLOR_SEQ,
            labels={"revenue": "Revenue ($)", "week": "Week"},
        )
        fig_bar.update_layout(**PLOTLY_LAYOUT, height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

    with tab2:
        cat_summary = df_f.groupby("category").agg(
            revenue=("revenue", "sum"),
            units=("units", "sum"),
            margin=("profit_margin", "mean"),
        ).reset_index()

        fig_bubble = px.scatter(
            cat_summary, x="revenue", y="margin",
            size="units", color="category",
            text="category", size_max=60,
            color_discrete_sequence=COLOR_SEQ,
            labels={"revenue": "Total Revenue ($)", "margin": "Avg Profit Margin"},
        )
        fig_bubble.update_layout(**PLOTLY_LAYOUT, height=420)
        fig_bubble.update_traces(textposition="top center")
        st.plotly_chart(fig_bubble, use_container_width=True)

    with tab3:
        metric = st.selectbox("Select metric", ["revenue", "units", "profit_margin"])
        fig_box = px.box(
            df_f, x="category", y=metric, color="category",
            color_discrete_sequence=COLOR_SEQ,
            points="outliers",
        )
        fig_box.update_layout(**PLOTLY_LAYOUT, height=420, showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: User Insights
# ══════════════════════════════════════════════════════════════════════════════
elif page == "👥 User Insights":
    st.markdown('<h1 class="gradient-text">User Insights</h1>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("👤 Total Users", f"{len(df_users):,}")
    c2.metric("💵 Avg Spend", f"${df_users['spend'].mean():.2f}")
    c3.metric("⭐ Avg Satisfaction", f"{df_users['satisfaction'].mean():.2f} / 5")

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Age vs. Spend by Segment")
        fig_sc = px.scatter(
            df_users, x="age", y="spend", color="segment",
            opacity=0.65, size_max=8,
            color_discrete_sequence=["#6366f1", "#ec4899", "#10b981"],
            labels={"age": "Age", "spend": "Spend ($)"},
        )
        fig_sc.update_layout(**PLOTLY_LAYOUT, height=360)
        st.plotly_chart(fig_sc, use_container_width=True)

    with col_b:
        st.markdown("#### Satisfaction Distribution")
        sat_counts = df_users["satisfaction"].value_counts().sort_index().reset_index()
        sat_counts.columns = ["rating", "count"]
        colors = ["#ef4444", "#f97316", "#eab308", "#22c55e", "#6366f1"]
        fig_sat = px.bar(
            sat_counts, x="rating", y="count",
            color="rating", color_discrete_sequence=colors,
            labels={"rating": "Rating (1–5)", "count": "Users"},
        )
        fig_sat.update_layout(**PLOTLY_LAYOUT, height=360, showlegend=False)
        st.plotly_chart(fig_sat, use_container_width=True)

    st.markdown("#### User Segment Breakdown")
    seg = df_users.groupby("segment").agg(
        users=("user_id", "count"),
        avg_spend=("spend", "mean"),
        avg_sessions=("sessions", "mean"),
    ).reset_index()

    fig_seg = make_subplots(rows=1, cols=3, subplot_titles=["Users", "Avg Spend ($)", "Avg Sessions"])
    for i, (col, label) in enumerate(zip(["users", "avg_spend", "avg_sessions"],
                                          ["Users", "Avg Spend", "Avg Sessions"]), 1):
        fig_seg.add_trace(
            go.Bar(x=seg["segment"], y=seg[col],
                   marker_color=["#6366f1", "#ec4899", "#10b981"],
                   showlegend=False, name=label),
            row=1, col=i,
        )
    fig_seg.update_layout(**PLOTLY_LAYOUT, height=320)
    st.plotly_chart(fig_seg, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Regional Map
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🌍 Regional Map":
    st.markdown('<h1 class="gradient-text">Regional Analysis</h1>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Country-level user data
    country_data = df_users.groupby("country").agg(
        users=("user_id", "count"),
        avg_spend=("spend", "mean"),
        avg_satisfaction=("satisfaction", "mean"),
    ).reset_index()

    iso_map = {
        "USA": "USA", "UK": "GBR", "Germany": "DEU", "Japan": "JPN",
        "Brazil": "BRA", "Canada": "CAN", "Australia": "AUS", "France": "FRA",
    }
    country_data["iso_alpha"] = country_data["country"].map(iso_map)

    metric_choice = st.selectbox(
        "Map metric",
        ["users", "avg_spend", "avg_satisfaction"],
        format_func=lambda x: {"users": "👤 Users", "avg_spend": "💵 Avg Spend",
                                "avg_satisfaction": "⭐ Satisfaction"}[x],
    )

    fig_map = px.choropleth(
        country_data,
        locations="iso_alpha",
        color=metric_choice,
        hover_name="country",
        hover_data={"users": True, "avg_spend": ":.2f", "avg_satisfaction": ":.2f"},
        color_continuous_scale="Viridis",
        projection="natural earth",
    )
    fig_map.update_layout(
        **PLOTLY_LAYOUT,
        height=480,
        geo=dict(
            bgcolor="rgba(0,0,0,0)",
            showframe=False,
            showcoastlines=True,
            coastlinecolor="rgba(255,255,255,0.2)",
            landcolor="rgba(255,255,255,0.05)",
            oceancolor="rgba(0,0,0,0)",
            showocean=True,
        ),
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Country table
    st.markdown("#### Country Performance Table")
    display = country_data.drop(columns=["iso_alpha"]).rename(columns={
        "country": "Country", "users": "Users",
        "avg_spend": "Avg Spend ($)", "avg_satisfaction": "Satisfaction ⭐",
    })
    display["Avg Spend ($)"] = display["Avg Spend ($)"].round(2)
    display["Satisfaction ⭐"] = display["Satisfaction ⭐"].round(2)
    st.dataframe(
        display.sort_values("Users", ascending=False).reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
    )
