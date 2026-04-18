import streamlit as st
import pandas as pd

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(
    page_title="Business Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------
# HIDE STREAMLIT UI ELEMENTS
# ---------------------------
st.markdown("""
<style>
/* Hide Streamlit default UI */
#MainMenu, header, footer {
    visibility: hidden;
}

/* Hide newer toolbar / decorations */
.stAppToolbar,
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    display: none !important;
}

/* App background */
[data-testid="stAppViewContainer"] {
    background-color: #f6f8fb;
}

/* Remove padding issues */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* Headings */
h1, h2, h3 {
    color: #1f2937;
}

/* Tabs styling */
button[data-baseweb="tab"] {
    font-size: 15px;
    font-weight: 500;
    color: #555;
}

button[aria-selected="true"] {
    color: #2563eb !important;
    border-bottom: 3px solid #2563eb !important;
}

/* Dataframe styling */
[data-testid="stDataFrame"] {
    border: 1px solid #e5e7eb;
    border-radius: 10px;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# CSV LINKS
# ---------------------------
CSV_FILES = {
    "Dental clinic": "https://docs.google.com/spreadsheets/d/1ktUxErd0fS5bdjT4lAkIa6v4tOmRmm9hysTXSpp_mK4/export?format=csv",
    "Hospital": "https://docs.google.com/spreadsheets/d/1xZ2pqjm8RHBWlVIimvBuXPq6UFe4-bL8C4CLfjJHIYA/export?format=csv",
    "Law firm or Advocate firm": "https://docs.google.com/spreadsheets/d/12I5HbsV3d3bDmzM_jUSBlGe1awYfRmW37juPWK0bjhg/export?format=csv",
    "Real Estate": "https://docs.google.com/spreadsheets/d/1j3wnQ25wog9QB_wUoXyXYRAWUUESzHfeRelvwYVahOM/export?format=csv",
    "Coaching Classes/Tutions": "https://docs.google.com/spreadsheets/d/10_Y-GEXHApcWO7Y9ddbTiUvOZv3aWQ_XIjk-ydJFC0s/export?format=csv",
    "CA Firms": "https://docs.google.com/spreadsheets/d/1dxhtJ47-3sh1ab4vvHhrxF904rCvxf63n-UpV2ZO85I/export?format=csv"
}

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data
def load_data(url):
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

# ---------------------------
# GOOGLE SHEET LINK
# ---------------------------
def get_sheet_url(csv_url):
    return csv_url.replace("/export?format=csv", "/edit")

# ---------------------------
# TITLE
# ---------------------------
st.title("Business Leads Dashboard")
st.caption("By A Rehman")

# ---------------------------
# CARD UI
# ---------------------------
def card(col, title, value, color):
    with col:
        st.markdown(
            f"""
            <div style="
                background: {color};
                padding: 16px;
                border-radius: 14px;
                border: 1px solid #e5e7eb;
                box-shadow: 0 2px 6px rgba(0,0,0,0.04);
                text-align: center;
            ">
                <div style="font-size: 13px; color: #374151; margin-bottom: 6px;">
                    {title}
                </div>
                <div style="font-size: 24px; font-weight: 700; color: #111827;">
                    {value}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------------------
# TABS
# ---------------------------
tabs = st.tabs(list(CSV_FILES.keys()))

# ---------------------------
# MAIN LOOP
# ---------------------------
for tab, (name, url) in zip(tabs, CSV_FILES.items()):
    with tab:

        df = load_data(url)

        if df.empty:
            st.warning("⚠️ Data not available (check CSV link or sharing settings)")
            continue

        # ---------------------------
        # SIDEBAR FILTERS
        # ---------------------------
        st.sidebar.markdown("## 🔍 Filters")
        st.sidebar.markdown(f"### {name}")

        search = st.sidebar.text_input("Search", key=f"{name}_search")

        if search:
            df = df[df.apply(lambda row: search.lower() in str(row).lower(), axis=1)]

        if "Buisness Domain" in df.columns:
            domains = ["All"] + sorted(df["Buisness Domain"].dropna().unique().tolist())
            selected_domain = st.sidebar.selectbox(
                "Business Domain", domains, key=f"{name}_domain"
            )

            if selected_domain != "All":
                df = df[df["Buisness Domain"] == selected_domain]

        if "City, State" in df.columns:
            cities = ["All"] + sorted(df["City, State"].dropna().unique().tolist())
            selected_city = st.sidebar.selectbox(
                "City", cities, key=f"{name}_city"
            )

            if selected_city != "All":
                df = df[df["City, State"] == selected_city]

        # ---------------------------
        # STATS
        # ---------------------------
        st.markdown("### 📊 Dashboard Overview")

        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

        card(col1, "Total Records", len(df), "#eef2ff")

        card(col2, "Business Domains",
             df["Buisness Domain"].nunique() if "Buisness Domain" in df.columns else 0,
             "#ecfeff")

        card(col3, "Cities Covered",
             df["City, State"].nunique() if "City, State" in df.columns else 0,
             "#f0fdf4")

        card(col4, "With Email",
             df["Email"].notna().sum() if "Email" in df.columns else 0,
             "#fff7ed")

        card(col5, "With Contact",
             df["Contact No"].notna().sum() if "Contact No" in df.columns else 0,
             "#fef2f2")

        card(col6, "G-Map Count",
             df["Link Of Google Map"].notna().sum()
             if "Link Of Google Map" in df.columns else 0,
             "#f5f3ff")

        card(col7, "Website / Social Count",
             df["Website / Social"].notna().sum()
             if "Website / Social" in df.columns else 0,
             "#f0f9ff")

        st.divider()

        # ---------------------------
        # TABLE
        # ---------------------------
        st.markdown("### 📋 Business Data")
        st.dataframe(df, use_container_width=True, hide_index=True)

        # ---------------------------
        # SHEET BUTTON
        # ---------------------------
        sheet_url = get_sheet_url(url)

        st.link_button(
            f"🔗 Open {name} Sheet",
            sheet_url,
            use_container_width=True
        )
