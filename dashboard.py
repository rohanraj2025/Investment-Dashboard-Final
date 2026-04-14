import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="MSH Interactive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background: #f3eef9;
    }

    .block-container {
        padding-top: 0.15rem !important;
        padding-bottom: 0.6rem !important;
        padding-left: 0.7rem !important;
        padding-right: 0.7rem !important;
        max-width: 100% !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 2.2rem !important;
    }

    div[data-testid="stToolbar"] {
        top: 0.05rem !important;
        right: 0.4rem !important;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #6f3db8 0%, #7f52c7 100%);
        border-top-right-radius: 22px;
        border-bottom-right-radius: 22px;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    .sidebar-logo-wrap {
        background: rgba(255,255,255,0.10);
        border-radius: 14px;
        padding: 8px;
        margin-bottom: 12px;
    }

    .title-bar {
        background: linear-gradient(90deg, #6b39b4 0%, #4e287f 100%);
        color: white;
        text-align: center;
        font-size: 22px;
        font-weight: 900;
        padding: 8px 14px;
        border-radius: 16px;
        margin-top: 0px;
        margin-bottom: 8px;
        line-height: 1.15;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
    }

    .kpi-card {
        background: white;
        border-radius: 14px;
        padding: 12px 10px;
        border: 1px solid #e6dcf5;
        border-top: 6px solid #6b39b4;
        box-shadow: 0 3px 12px rgba(0,0,0,0.05);
        min-height: 98px;
    }

    .kpi-title {
        font-size: 12px;
        font-weight: 800;
        color: #54416f;
        text-align: center;
        margin-bottom: 6px;
        line-height: 1.15;
    }

    .kpi-value {
        font-size: 18px;
        font-weight: 900;
        color: #271443;
        text-align: center;
        line-height: 1.15;
    }

    .kpi-sub {
        font-size: 10px;
        color: #7a6d92;
        text-align: center;
        margin-top: 5px;
        line-height: 1.1;
    }

    .panel-card {
        background: white;
        border-radius: 14px;
        padding: 10px;
        border: 1px solid #e6dcf5;
        box-shadow: 0 3px 12px rgba(0,0,0,0.05);
        margin-top: 6px;
        margin-bottom: 8px;
        overflow: hidden;
    }

    .panel-title {
        font-size: 16px;
        font-weight: 900;
        color: #2b1748;
        text-align: center;
        margin-bottom: 8px;
        line-height: 1.2;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e6dcf5;
        padding: 8px;
        border-radius: 12px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    }

    .stRadio > label, .stMultiSelect > label {
        font-weight: 800 !important;
    }

    .stMultiSelect > div > div {
        border-radius: 8px !important;
    }

    hr {
        margin-top: 0.4rem !important;
        margin-bottom: 0.4rem !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_excel("Investment data.xlsx")
    df.columns = [str(c).strip() for c in df.columns]

    if "State" in df.columns:
        df["State"] = (
            df["State"]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .str.title()
        )
        df["State"] = df["State"].replace("Nan", pd.NA)

    if "Total Funds Raised" in df.columns:
        df["Total Funds Raised Num"] = pd.to_numeric(df["Total Funds Raised"], errors="coerce")

    if "Revenue Generated (FY 24-25)" in df.columns:
        df["Revenue FY Num"] = pd.to_numeric(df["Revenue Generated (FY 24-25)"], errors="coerce")

    if "Revenue Generated Apr 25 - Feb 26" in df.columns:
        df["Revenue AprFeb Num"] = pd.to_numeric(df["Revenue Generated Apr 25 - Feb 26"], errors="coerce")

    if "Current Valuation of the Company in INR Cr." in df.columns:
        df["Valuation Num"] = pd.to_numeric(df["Current Valuation of the Company in INR Cr."], errors="coerce")

    number_cols = [
        "Total No. of Customers",
        "Customers Served",
        "Total Number of Employment Generated Till Date",
        "Total No. of IPRs Published",
        "Total No. of IPRs Granted",
        "No. of Patents Published",
        "No. Patents Granted",
        "No. of Trademarks",
        "No. of Copyrights"
    ]

    for col in number_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

df = load_data()

with st.sidebar:
    st.markdown('<div class="sidebar-logo-wrap">', unsafe_allow_html=True)
    st.image("MSH logoo temo.png", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("## Dashboard Menu")
    page = st.radio(
        "Go to",
        [
            "Overview",
            "Funding & Revenue",
            "Sector Analysis",
            "Geography & Tier",
            "IPR & Valuation"
        ]
    )

    st.markdown("---")
    st.markdown("## Filters")

    filtered_df = df.copy()

    if "State" in df.columns:
        state_options = sorted([x for x in df["State"].dropna().astype(str).unique() if x.strip() != ""])
        selected_states = st.multiselect("State", state_options)
        if selected_states:
            filtered_df = filtered_df[filtered_df["State"].astype(str).isin(selected_states)]

    if "Sector" in df.columns:
        sector_options = sorted([x for x in df["Sector"].dropna().astype(str).unique() if x.strip() != ""])
        selected_sectors = st.multiselect("Sector", sector_options)
        if selected_sectors:
            filtered_df = filtered_df[filtered_df["Sector"].astype(str).isin(selected_sectors)]

    tier_col = "Tier Classification (Startup Based out of)"
    if tier_col in df.columns:
        tier_options = sorted([x for x in df[tier_col].dropna().astype(str).unique() if x.strip() != ""])
        selected_tiers = st.multiselect("Tier", tier_options)
        if selected_tiers:
            filtered_df = filtered_df[filtered_df[tier_col].astype(str).isin(selected_tiers)]

    inc_col = "Name of Enabling Partner / Incubation Center"
    if inc_col in df.columns:
        inc_options = sorted([x for x in df[inc_col].dropna().astype(str).unique() if x.strip() != ""])
        selected_inc = st.multiselect("Incubation Center", inc_options)
        if selected_inc:
            filtered_df = filtered_df[filtered_df[inc_col].astype(str).isin(selected_inc)]

st.markdown('<div class="title-bar">Startup Investment Dashboard</div>', unsafe_allow_html=True)

TOTAL_FUNDS_CR = (
    filtered_df["Total Funds Raised Num"].sum(skipna=True) / 100
    if "Total Funds Raised Num" in filtered_df.columns else 0
)

REV_FY_CR = (
    filtered_df["Revenue FY Num"].sum(skipna=True)
    if "Revenue FY Num" in filtered_df.columns else 0
)

REV_APR_FEB_CR = (
    filtered_df["Revenue AprFeb Num"].sum(skipna=True)
    if "Revenue AprFeb Num" in filtered_df.columns else 0
)

total_startups = len(filtered_df)

total_customers = (
    filtered_df["Total No. of Customers"].sum(skipna=True)
    if "Total No. of Customers" in filtered_df.columns else 0
)

employment = (
    filtered_df["Total Number of Employment Generated Till Date"].sum(skipna=True)
    if "Total Number of Employment Generated Till Date" in filtered_df.columns else 0
)

avg_valuation = (
    filtered_df["Valuation Num"].mean(skipna=True)
    if "Valuation Num" in filtered_df.columns and len(filtered_df) > 0 else 0
)

ipr_total = 0
for col in [
    "Total No. of IPRs Published",
    "Total No. of IPRs Granted",
    "No. of Patents Published",
    "No. Patents Granted",
    "No. of Trademarks",
    "No. of Copyrights"
]:
    if col in filtered_df.columns:
        ipr_total += filtered_df[col].sum(skipna=True)

if page == "Overview":
    k1, k2, k3, k4, k5 = st.columns(5)

    cards = [
        ("Total Records", f"{total_startups}", "Filtered startups"),
        ("Funding Raised", f"₹ {TOTAL_FUNDS_CR:.2f} Cr", "Excel numeric sum"),
        ("Revenue FY 24-25", f"₹ {REV_FY_CR:.2f} Cr", "Excel numeric sum"),
        ("Revenue Apr 25 - Feb 26", f"₹ {REV_APR_FEB_CR:.2f} Cr", "Excel numeric sum"),
        ("Employment", f"{int(employment):,}", "Jobs generated")
    ]

    for col, (title, value, sub) in zip([k1, k2, k3, k4, k5], cards):
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">{title}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">State-wise Startup Distribution</div>', unsafe_allow_html=True)
    if "State" in filtered_df.columns:
        state_df = (
            filtered_df[filtered_df["State"].astype(str).str.strip() != ""]
            .groupby("State")
            .size()
            .reset_index(name="Count")
            .sort_values("Count", ascending=False)
            .head(12)
        )
        if not state_df.empty:
            state_df = state_df.sort_values("Count", ascending=True)

            fig = px.bar(
                state_df,
                x="Count",
                y="State",
                orientation="h",
                text="Count"
            )
            fig.update_traces(marker_color="#6b39b4", textposition="outside")
            fig.update_layout(
                height=320,
                margin=dict(l=6, r=20, t=6, b=6),
                xaxis_title="Startup Count",
                yaxis_title="State",
                plot_bgcolor="white",
                paper_bgcolor="white"
            )
            st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Funding Raised by Sector</div>', unsafe_allow_html=True)
    if "Sector" in filtered_df.columns and "Total Funds Raised Num" in filtered_df.columns:
        fs_df = (
            filtered_df.groupby("Sector", as_index=False)["Total Funds Raised Num"]
            .sum()
            .sort_values("Total Funds Raised Num", ascending=False)
            .head(10)
        )
        if not fs_df.empty:
            fs_df["Funding Cr"] = fs_df["Total Funds Raised Num"] / 100

            fig = px.treemap(
                fs_df,
                path=["Sector"],
                values="Funding Cr",
                color="Funding Cr",
                color_continuous_scale="Purples"
            )
            fig.update_layout(
                height=340,
                margin=dict(l=6, r=6, t=6, b=6)
            )
            st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Funding & Revenue":
    k1, k2, k3 = st.columns(3)
    k1.metric("Funding Raised", f"₹ {TOTAL_FUNDS_CR:.2f} Cr")
    k2.metric("Revenue FY 24-25", f"₹ {REV_FY_CR:.2f} Cr")
    k3.metric("Revenue Apr 25 - Feb 26", f"₹ {REV_APR_FEB_CR:.2f} Cr")

    c1, c2 = st.columns([1.1, 1.4])

    with c1:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Revenue Comparison by Sector</div>', unsafe_allow_html=True)
        if "Sector" in filtered_df.columns:
            grp = filtered_df.groupby("Sector", as_index=False).agg({
                "Revenue FY Num": "sum",
                "Revenue AprFeb Num": "sum"
            }).head(10)

            if not grp.empty:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    y=grp["Sector"],
                    x=grp["Revenue FY Num"],
                    name="FY 24-25",
                    orientation="h",
                    marker_color="#5b2d90"
                ))
                fig.add_trace(go.Bar(
                    y=grp["Sector"],
                    x=grp["Revenue AprFeb Num"],
                    name="Apr 25 - Feb 26",
                    orientation="h",
                    marker_color="#b39ddb"
                ))
                fig.update_layout(
                    barmode="group",
                    height=340,
                    margin=dict(l=6, r=6, t=6, b=6),
                    yaxis={"categoryorder": "total ascending"}
                )
                st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Funding Raised by Sector</div>', unsafe_allow_html=True)
        if "Sector" in filtered_df.columns and "Total Funds Raised Num" in filtered_df.columns:
            fs_df = (
                filtered_df.groupby("Sector", as_index=False)["Total Funds Raised Num"]
                .sum()
                .sort_values("Total Funds Raised Num", ascending=False)
                .head(10)
            )
            if not fs_df.empty:
                fs_df["Funding Cr"] = fs_df["Total Funds Raised Num"] / 100
                fs_df = fs_df.sort_values("Funding Cr", ascending=True)

                fig = px.bar(
                    fs_df,
                    x="Funding Cr",
                    y="Sector",
                    orientation="h",
                    text="Funding Cr"
                )
                fig.update_traces(
                    marker_color="#5b2d90",
                    texttemplate="%{text:.2f} Cr",
                    textposition="outside"
                )
                fig.update_layout(
                    height=340,
                    margin=dict(l=6, r=25, t=6, b=6),
                    xaxis_title="Funding Raised (Cr)",
                    yaxis_title="Sector",
                    plot_bgcolor="#f8f4fc",
                    paper_bgcolor="white"
                )
                st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Sector Analysis":
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Sector Analysis</div>', unsafe_allow_html=True)

    if "Sector" in filtered_df.columns:
        sector_summary = filtered_df.groupby("Sector", as_index=False).agg({
            "Total Funds Raised Num": "sum",
            "Revenue FY Num": "sum",
            "Revenue AprFeb Num": "sum"
        }).sort_values("Total Funds Raised Num", ascending=False)

        sector_summary["Funding Cr"] = (sector_summary["Total Funds Raised Num"] / 100).round(2)

        fig = px.bar(sector_summary.head(10), x="Sector", y="Funding Cr", text="Funding Cr")
        fig.update_traces(
            marker_color="#6b39b4",
            texttemplate="%{text:.2f}",
            textposition="outside"
        )
        fig.update_layout(height=360, margin=dict(l=6, r=6, t=6, b=6))
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(sector_summary, use_container_width=True, height=240)

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Geography & Tier":
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">State-wise Distribution</div>', unsafe_allow_html=True)
        if "State" in filtered_df.columns:
            state_df = (
                filtered_df[filtered_df["State"].astype(str).str.strip() != ""]
                .groupby("State")
                .size()
                .reset_index(name="Count")
                .sort_values("Count", ascending=False)
                .head(15)
            )
            if not state_df.empty:
                fig = px.bar(state_df, x="State", y="Count", text="Count")
                fig.update_traces(marker_color="#6b39b4")
                fig.update_layout(height=340, margin=dict(l=6, r=6, t=6, b=6))
                st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Tier-wise Distribution</div>', unsafe_allow_html=True)
        if tier_col in filtered_df.columns:
            tier_df = (
                filtered_df[filtered_df[tier_col].astype(str).str.strip() != ""]
                .groupby(tier_col)
                .size()
                .reset_index(name="Count")
            )
            if not tier_df.empty:
                fig = px.pie(tier_df, names=tier_col, values="Count", hole=0.5)
                fig.update_traces(textinfo="percent+label")
                fig.update_layout(height=340, margin=dict(l=6, r=6, t=6, b=6))
                st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "IPR & Valuation":
    iprs_published = (
        filtered_df["Total No. of IPRs Published"].sum(skipna=True)
        if "Total No. of IPRs Published" in filtered_df.columns else 0
    )
    iprs_granted = (
        filtered_df["Total No. of IPRs Granted"].sum(skipna=True)
        if "Total No. of IPRs Granted" in filtered_df.columns else 0
    )
    patents_published = (
        filtered_df["No. of Patents Published"].sum(skipna=True)
        if "No. of Patents Published" in filtered_df.columns else 0
    )
    patents_granted = (
        filtered_df["No. Patents Granted"].sum(skipna=True)
        if "No. Patents Granted" in filtered_df.columns else 0
    )
    trademarks = (
        filtered_df["No. of Trademarks"].sum(skipna=True)
        if "No. of Trademarks" in filtered_df.columns else 0
    )
    copyrights = (
        filtered_df["No. of Copyrights"].sum(skipna=True)
        if "No. of Copyrights" in filtered_df.columns else 0
    )

    m1, m2, m3 = st.columns(3)
    m1.metric("IPRs Published", f"{int(iprs_published):,}")
    m2.metric("IPRs Granted", f"{int(iprs_granted):,}")
    m3.metric("Patents Published", f"{int(patents_published):,}")

    m4, m5, m6 = st.columns(3)
    m4.metric("Patents Granted", f"{int(patents_granted):,}")
    m5.metric("Trademarks", f"{int(trademarks):,}")
    m6.metric("Copyrights", f"{int(copyrights):,}")

    m7, m8 = st.columns(2)
    m7.metric("Avg Valuation", f"₹ {avg_valuation:.2f} Cr")
    m8.metric("Total Customers", f"{int(total_customers):,}")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">IPR Overview</div>', unsafe_allow_html=True)

        ipr_data = {
            "Published IPRs": iprs_published,
            "Granted IPRs": iprs_granted,
            "Patents Published": patents_published,
            "Patents Granted": patents_granted,
            "Trademarks": trademarks,
            "Copyrights": copyrights,
        }

        ipr_df = pd.DataFrame({"Category": list(ipr_data.keys()), "Count": list(ipr_data.values())})
        fig = px.bar(ipr_df, x="Category", y="Count", text="Count")
        fig.update_traces(marker_color="#6b39b4")
        fig.update_layout(height=340, margin=dict(l=6, r=6, t=6, b=6))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Top Startups by Valuation</div>', unsafe_allow_html=True)

        startup_col = "Startup Registered Name"
        val_col = "Valuation Num"

        if startup_col in filtered_df.columns and val_col in filtered_df.columns:
            top_val_df = (
                filtered_df[[startup_col, val_col]]
                .copy()
                .dropna(subset=[val_col])
                .sort_values(val_col, ascending=False)
                .head(10)
            )
            if not top_val_df.empty:
                fig = px.bar(top_val_df, x=val_col, y=startup_col, orientation="h", text=val_col)
                fig.update_traces(marker_color="#6b39b4")
                fig.update_layout(
                    height=340,
                    margin=dict(l=6, r=6, t=6, b=6),
                    yaxis={"categoryorder": "total ascending"}
                )
                st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="panel-card">', unsafe_allow_html=True)
st.markdown(f'<div class="panel-title">Filtered Data - {page}</div>', unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True, height=280)
st.markdown('</div>', unsafe_allow_html=True)
