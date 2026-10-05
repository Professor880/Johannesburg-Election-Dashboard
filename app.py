import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Johannesburg 2026 Election Analytics",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PROFESSIONAL CSS
# ============================================================

st.markdown("""
<style>

/* Main page */
.stApp {
    background-color: #f5f7fb;
}

/* Main container */
.block-container {
    padding-top: 1.8rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* Main headings */
h1, h2, h3 {
    font-family: Arial, sans-serif;
}

/* KPI cards */
div[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #e5e7eb;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: white;
}

/* Tables */
div[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 10px;
}

/* Professional information box */
.info-box {
    background: white;
    border-left: 5px solid #2563eb;
    padding: 18px 22px;
    border-radius: 8px;
    margin-top: 15px;
    margin-bottom: 20px;
    box-shadow: 0 2px 7px rgba(0,0,0,0.04);
}

/* Header */
.dashboard-header {
    background: linear-gradient(90deg, #111827, #1f2937);
    padding: 28px;
    border-radius: 14px;
    margin-bottom: 25px;
}

.dashboard-header h1 {
    color: white;
    margin: 0;
    font-size: 34px;
}

.dashboard-header p {
    color: #d1d5db;
    margin-top: 8px;
    margin-bottom: 0;
    font-size: 16px;
}

/* Footer */
.footer {
    text-align: center;
    color: #6b7280;
    font-size: 13px;
    padding-top: 35px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


@st.cache_data
def load_data():

    party = pd.read_csv(
        BASE_DIR / "Johannesburg_2026_Party_Projections.csv"
    )

    ward = pd.read_csv(
        BASE_DIR / "Johannesburg_2026_Ward_Projections.csv"
    )

    summary = pd.read_csv(
        BASE_DIR / "Johannesburg_2026_Final_Summary.csv"
    )

    return party, ward, summary


try:
    party_df, ward_df, summary_df = load_data()

except FileNotFoundError:

    st.error(
        "Dashboard data files could not be found. "
        "Place all three CSV files in the same folder as app.py."
    )

    st.stop()


# ============================================================
# CLEAN DATA
# ============================================================

party_df["Projected_2026_Votes"] = pd.to_numeric(
    party_df["Projected_2026_Votes"],
    errors="coerce"
)

party_df["Projected_2026_Share"] = pd.to_numeric(
    party_df["Projected_2026_Share"],
    errors="coerce"
)

party_df["Baseline_2021_Share"] = pd.to_numeric(
    party_df["Baseline_2021_Share"],
    errors="coerce"
)

party_df["Projected_Rank"] = pd.to_numeric(
    party_df["Projected_Rank"],
    errors="coerce"
)

ward_df["Projected_Vote_Share"] = pd.to_numeric(
    ward_df["Projected_Vote_Share"],
    errors="coerce"
)

ward_df["Projected_Votes"] = pd.to_numeric(
    ward_df["Projected_Votes"],
    errors="coerce"
)

ward_df["Ward_Code"] = ward_df["Ward_Code"].astype(str)


# ============================================================
# IMPORTANT VALUES
# ============================================================

leader = party_df.sort_values(
    "Projected_Rank"
).iloc[0]

leading_party = leader["Party"]

leading_share = leader["Projected_2026_Share"]

leading_votes = leader["Projected_2026_Votes"]

projected_voters = 994670
historical_voters = 947305

voter_change = (
    (projected_voters - historical_voters)
    / historical_voters
) * 100


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🗳️ Election Analytics")

    st.markdown(
        "### City of Johannesburg"
    )

    st.caption(
        "2026 Local Government Election"
    )

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "Executive Overview",
            "Party Projections",
            "Ward Analysis",
            "Turnout Analysis",
            "Coalition Analysis",
            "Methodology",
            "Data Explorer"
        ]
    )

    st.markdown("---")

    st.caption(
        "Election Analytics Dashboard"
    )

    st.caption(
        "04 November 2026"
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="dashboard-header">
        <h1>Johannesburg 2026 Election Analytics</h1>
        <p>
        Data-driven analysis of projected electoral outcomes
        for the City of Johannesburg Metropolitan Municipality
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    st.subheader("Executive Overview")

    st.write(
        "This dashboard presents the 2026 Johannesburg local "
        "government election scenario using the 2021 election "
        "baseline, demographic indicators and analytical "
        "projection assumptions."
    )

    st.markdown("### Key Election Indicators")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Projected Leading Party",
            leading_party
        )

    with col2:
        st.metric(
            "Projected Vote Share",
            f"{leading_share:.2f}%"
        )

    with col3:
        st.metric(
            "Projected Party Votes",
            f"{leading_votes:,.0f}"
        )

    with col4:
        st.metric(
            "Projected Voters",
            f"{projected_voters:,}",
            f"{voter_change:.1f}% vs 2021"
        )

    st.markdown("---")

    col1, col2 = st.columns([1.6, 1])

    # PARTY SHARE CHART
    with col1:

        st.markdown("### 2026 Projected Party Support")

        chart_data = party_df.sort_values(
            "Projected_2026_Share",
            ascending=True
        )

        fig = px.bar(
            chart_data,
            x="Projected_2026_Share",
            y="Party",
            orientation="h",
            text="Projected_2026_Share",
            labels={
                "Projected_2026_Share":
                "Projected Vote Share (%)",
                "Party": ""
            }
        )

        fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside"
        )

        fig.update_layout(
            height=420,
            margin=dict(l=20, r=50, t=20, b=20),
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # RANKING
    with col2:

        st.markdown("### Projected Ranking")

        ranking = party_df[
            [
                "Projected_Rank",
                "Party",
                "Projected_2026_Share"
            ]
        ].sort_values("Projected_Rank")

        ranking.columns = [
            "Rank",
            "Party",
            "Projected Share (%)"
        ]

        st.dataframe(
            ranking,
            hide_index=True,
            use_container_width=True
        )

    st.markdown("### Election Outlook")

    if leading_share < 50:

        st.markdown(
            f"""
            <div class="info-box">
            <strong>{leading_party}</strong> records the largest
            projected vote share at <strong>{leading_share:.2f}%</strong>.
            No analysed party reaches an outright majority of the
            projected vote, making the scenario relevant for
            post-election coalition analysis.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.success(
            f"{leading_party} exceeds 50% of projected support."
        )


# ============================================================
# PARTY PROJECTIONS
# ============================================================

elif page == "Party Projections":

    st.subheader("Party Projection Analysis")

    st.write(
        "Comparison between the 2021 Johannesburg election "
        "baseline and the 2026 analytical projection."
    )

    st.markdown("### 2021 vs 2026 Vote Share")

    comparison = party_df[
        [
            "Party",
            "Baseline_2021_Share",
            "Projected_2026_Share"
        ]
    ].copy()

    comparison_long = comparison.melt(
        id_vars="Party",
        value_vars=[
            "Baseline_2021_Share",
            "Projected_2026_Share"
        ],
        var_name="Election",
        value_name="Vote Share"
    )

    comparison_long["Election"] = comparison_long[
        "Election"
    ].replace(
        {
            "Baseline_2021_Share":
            "2021 Baseline",
            "Projected_2026_Share":
            "2026 Projection"
        }
    )

    fig = px.bar(
        comparison_long,
        x="Party",
        y="Vote Share",
        color="Election",
        barmode="group",
        text_auto=".1f",
        labels={
            "Vote Share": "Vote Share (%)"
        }
    )

    fig.update_layout(
        height=480,
        legend_title_text=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # CHANGE ANALYSIS
    st.markdown("### Projected Change in Party Support")

    change_df = party_df.copy()

    change_df["Change_pp"] = (
        change_df["Projected_2026_Share"]
        - change_df["Baseline_2021_Share"]
    )

    fig_change = px.bar(
        change_df.sort_values("Change_pp"),
        x="Change_pp",
        y="Party",
        orientation="h",
        text="Change_pp",
        labels={
            "Change_pp":
            "Change from 2021 (percentage points)"
        }
    )

    fig_change.update_traces(
        texttemplate="%{text:+.2f}",
        textposition="outside"
    )

    fig_change.update_layout(
        height=400,
        showlegend=False
    )

    st.plotly_chart(
        fig_change,
        use_container_width=True
    )

    # VOTES
    st.markdown("### Projected Vote Totals")

    vote_chart = party_df.sort_values(
        "Projected_2026_Votes",
        ascending=True
    )

    fig_votes = px.bar(
        vote_chart,
        x="Projected_2026_Votes",
        y="Party",
        orientation="h",
        text="Projected_2026_Votes",
        labels={
            "Projected_2026_Votes":
            "Projected Votes"
        }
    )

    fig_votes.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )

    fig_votes.update_layout(
        height=420,
        showlegend=False
    )

    st.plotly_chart(
        fig_votes,
        use_container_width=True
    )

    # TABLE
    st.markdown("### Projection Table")

    display_party = party_df.copy()

    display_party.columns = [
        "Party",
        "2021 Share (%)",
        "2026 Projected Share (%)",
        "2026 Projected Votes",
        "Projected Rank"
    ]

    st.dataframe(
        display_party.sort_values("Projected Rank"),
        hide_index=True,
        use_container_width=True
    )


# ============================================================
# WARD ANALYSIS
# ============================================================

elif page == "Ward Analysis":

    st.subheader("Selected Ward Analysis")

    st.write(
        "The ward analysis compares three Johannesburg wards "
        "selected to represent different demographic and "
        "population characteristics."
    )

    selected_ward = st.selectbox(
        "Select a ward",
        ward_df["Ward_Code"].unique()
    )

    selected = ward_df[
        ward_df["Ward_Code"] == selected_ward
    ].iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Ward",
            selected_ward
        )

    with col2:
        st.metric(
            "Projected Leading Party",
            selected["Projected_Leading_Party"]
        )

    with col3:
        st.metric(
            "Projected Vote Share",
            f"{selected['Projected_Vote_Share']:.2f}%"
        )

    st.metric(
        "Projected Votes for Leading Party",
        f"{selected['Projected_Votes']:,.0f}"
    )

    st.markdown("---")

    st.markdown("### Comparison of Selected Wards")

    ward_chart = ward_df.sort_values(
        "Projected_Vote_Share",
        ascending=False
    )

    fig = px.bar(
        ward_chart,
        x="Ward_Code",
        y="Projected_Vote_Share",
        color="Projected_Leading_Party",
        text="Projected_Vote_Share",
        labels={
            "Ward_Code": "Ward",
            "Projected_Vote_Share":
            "Projected Leading Share (%)",
            "Projected_Leading_Party":
            "Leading Party"
        }
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%"
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("### Ward Projection Results")

    display_wards = ward_df.rename(
        columns={
            "Ward_Code": "Ward",
            "Projected_Leading_Party":
            "Projected Leading Party",
            "Projected_Vote_Share":
            "Projected Vote Share (%)",
            "Projected_Votes":
            "Projected Leading Party Votes"
        }
    )

    st.dataframe(
        display_wards,
        hide_index=True,
        use_container_width=True
    )

    st.markdown("### Ward Selection Rationale")

    st.markdown(
        """
        The three wards were selected to capture contrasting
        characteristics within Johannesburg:

        - **Ward 79800060** — selected for its relatively high
          proportion of residents aged 15–34.
        - **Ward 79800083** — selected for its relatively high
          proportion of residents aged 60 and above.
        - **Ward 79800100** — selected because it has the largest
          estimated population among the analysed Johannesburg wards.

        This provides a geographic comparison across wards with
        different demographic profiles.
        """
    )


# ============================================================
# TURNOUT ANALYSIS
# ============================================================

elif page == "Turnout Analysis":

    st.subheader("Voter Participation Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "2021 Participating Voters",
            f"{historical_voters:,}"
        )

    with col2:
        st.metric(
            "2026 Projected Voters",
            f"{projected_voters:,}"
        )

    with col3:
        st.metric(
            "Projected Change",
            f"{voter_change:.2f}%"
        )

    turnout_df = pd.DataFrame(
        {
            "Election": [
                "2021 Observed",
                "2026 Projected"
            ],
            "Participating Voters": [
                historical_voters,
                projected_voters
            ]
        }
    )

    fig = px.bar(
        turnout_df,
        x="Election",
        y="Participating Voters",
        text="Participating Voters"
    )

    fig.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )

    fig.update_layout(
        height=430,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("### Participation Sensitivity Analysis")

    sensitivity = pd.DataFrame(
        {
            "Scenario": [
                "Lower Participation",
                "Base Projection",
                "Higher Participation"
            ],
            "Factor": [
                0.95,
                1.05,
                1.15
            ]
        }
    )

    sensitivity["Projected Voters"] = (
        historical_voters
        * sensitivity["Factor"]
    ).round().astype(int)

    st.dataframe(
        sensitivity,
        hide_index=True,
        use_container_width=True
    )

    st.info(
        "The projected voter figure represents an estimated "
        "number of participating voters. A formal turnout "
        "percentage requires a reliable registered-voter "
        "denominator for the corresponding election geography."
    )


# ============================================================
# COALITION ANALYSIS
# ============================================================

elif page == "Coalition Analysis":

    st.subheader("Coalition-Relevance Analysis")

    st.write(
        "This section evaluates whether any analysed party "
        "reaches an outright majority of projected vote support."
    )

    max_share = party_df[
        "Projected_2026_Share"
    ].max()

    majority_gap = 50 - max_share

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Leading Party",
            leading_party
        )

    with col2:
        st.metric(
            "Leading Share",
            f"{max_share:.2f}%"
        )

    with col3:
        st.metric(
            "Gap to 50%",
            f"{majority_gap:.2f} pp"
        )

    # Majority line chart
    fig = go.Figure()

    ordered = party_df.sort_values(
        "Projected_2026_Share",
        ascending=False
    )

    fig.add_trace(
        go.Bar(
            x=ordered["Party"],
            y=ordered["Projected_2026_Share"],
            text=ordered["Projected_2026_Share"],
            texttemplate="%{text:.2f}%",
            textposition="outside",
            name="Projected Support"
        )
    )

    fig.add_hline(
        y=50,
        line_dash="dash",
        annotation_text="50% Majority Threshold"
    )

    fig.update_layout(
        height=470,
        yaxis_title="Projected Vote Share (%)",
        xaxis_title="",
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    if max_share < 50:

        st.info(
            "No analysed party reaches 50% of projected vote "
            "support. The scenario is therefore coalition-relevant. "
            "This does not determine which parties would form a "
            "governing coalition because council seats and "
            "post-election negotiations also matter."
        )

    else:

        st.success(
            "At least one analysed party exceeds the 50% "
            "projected vote-share threshold."
        )


# ============================================================
# METHODOLOGY
# ============================================================

elif page == "Methodology":

    st.subheader("Methodology and Analytical Framework")

    st.markdown("### 1. Historical Baseline")

    st.write(
        "The analysis uses the official 2021 Johannesburg "
        "local government election results as the historical "
        "electoral baseline."
    )

    st.markdown("### 2. Demographic Variables")

    st.write(
        "Ward-level demographic indicators were derived from "
        "Statistics South Africa data. Variables considered "
        "include age composition, sex and population-group "
        "characteristics."
    )

    st.markdown("### 3. 2026 Projection Approach")

    st.write(
        "The 2026 results are produced using a transparent "
        "scenario-based projection framework. Party vote shares "
        "are adjusted from the 2021 baseline using explicit "
        "analytical assumptions."
    )

    st.markdown("### 4. Ward-Level Analysis")

    st.write(
        "Ward-level scenarios use selected demographic "
        "characteristics to compare potential differences in "
        "party support across the three selected wards."
    )

    st.markdown("### 5. Geographic Comparability")

    st.write(
        "Johannesburg wards were identified using the 798 "
        "municipal ward-code prefix. The analysed demographic "
        "dataset contains 135 Johannesburg wards."
    )

    st.markdown("### Analytical Classification")

    classification = pd.DataFrame(
        {
            "Category": [
                "Historical Observation",
                "Derived Variable",
                "Scenario Assumption",
                "2026 Projection"
            ],
            "Examples": [
                "2021 party vote shares and participating voters",
                "Age and population-group percentages",
                "Party-share adjustments and participation factor",
                "Projected shares, votes and ward leaders"
            ]
        }
    )

    st.dataframe(
        classification,
        hide_index=True,
        use_container_width=True
    )

    st.markdown("### Limitations")

    st.markdown(
        """
        - Only one metro-level historical election baseline is used.
        - Comparable historical ward-level election observations
          were not available for supervised model training.
        - Demographic characteristics should not be interpreted
          as deterministic predictors of political behaviour.
        - The participation projection is assumption-based.
        - A registered-voter denominator is required for a formal
          turnout-rate calculation.
        - Ward-level adjustments are analytical scenario rules
          rather than coefficients learned by a supervised model.
        - Ward and voting-district boundaries may change between
          election cycles and require formal geographic crosswalks
          for stronger longitudinal analysis.
        - Coalition outcomes depend on council seats and political
          negotiations and cannot be inferred solely from projected
          vote shares.
        """
    )


# ============================================================
# DATA EXPLORER
# ============================================================

elif page == "Data Explorer":

    st.subheader("Data Explorer")

    dataset = st.selectbox(
        "Select dataset",
        [
            "Party Projections",
            "Ward Projections",
            "Final Summary"
        ]
    )

    if dataset == "Party Projections":

        st.dataframe(
            party_df,
            hide_index=True,
            use_container_width=True
        )

        csv = party_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "Download Party Projection CSV",
            csv,
            "Johannesburg_2026_Party_Projections.csv",
            "text/csv"
        )

    elif dataset == "Ward Projections":

        st.dataframe(
            ward_df,
            hide_index=True,
            use_container_width=True
        )

        csv = ward_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "Download Ward Projection CSV",
            csv,
            "Johannesburg_2026_Ward_Projections.csv",
            "text/csv"
        )

    else:

        st.dataframe(
            summary_df,
            hide_index=True,
            use_container_width=True
        )

        csv = summary_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "Download Final Summary CSV",
            csv,
            "Johannesburg_2026_Final_Summary.csv",
            "text/csv"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div class="footer">
    Johannesburg 2026 Local Government Election Analytics<br>
    City of Johannesburg Metropolitan Municipality |
    Data Analytics Project
    </div>
    """,
    unsafe_allow_html=True
)