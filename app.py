import streamlit as st
import pandas as pd
import numpy as np
import os

# ----------------- PAGE CONFIG & STYLING -----------------
st.set_page_config(
    page_title="75-Day Waffle Tracker",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premium dark theme styling with HSL tailored gradients, Inter/Outfit typography,
# glassmorphism, and responsive waffle grid adjustments.
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Global styles (Scandinavian Minimalist Light Mode) */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMain"], .main, section.main {
        font-family: 'Outfit', sans-serif;
        background-color: #f7f6f5 !important;
        color: #1e1e24;
    }
    
    /* Remove default Streamlit top whitespace */
    [data-testid="block-container"] {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Glassmorphic border container overrides (KPI and participant cards) */
    div[data-testid="stVerticalBlockBorderEffect"] {
        background-color: rgba(255, 255, 255, 0.75) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(0, 0, 0, 0.05) !important;
        border-radius: 20px !important;
        padding: 1.2rem !important;
        box-shadow: 0 8px 24px -10px rgba(0, 0, 0, 0.04) !important;
        transition: border-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease !important;
    }
    div[data-testid="stVerticalBlockBorderEffect"]:hover {
        border-color: rgba(16, 185, 129, 0.2) !important;
        box-shadow: 0 12px 30px -10px rgba(16, 185, 129, 0.06) !important;
    }
    
    /* Header Styling */
    .title-container {
        text-align: center;
        padding: 0.8rem 0 0.5rem 0;
        margin-bottom: 0.75rem;
        background: radial-gradient(circle at top, rgba(16, 185, 129, 0.04) 0%, rgba(252, 251, 250, 0) 70%);
    }
    .main-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.6rem;
        font-weight: 700;
        letter-spacing: -0.04em;
        background: linear-gradient(135deg, #0f766e 0%, #0d9488 50%, #4f46e5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .subtitle {
        font-size: 0.8rem;
        color: #6b7280;
        margin-top: 0.3rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    
    /* Waffle Grid customization */
    div[data-testid="stColumn"] {
        padding: 0px !important;
    }
    
    /* Target only the 15-column rows of the waffle grid to set a compact gap and max-width */
    div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) {
        max-width: 470px !important;
        gap: 4px !important;
        margin-bottom: 4px !important;
        flex-wrap: nowrap !important;
        overflow: visible !important;
    }
    
    /* Style only the nested waffle columns to be exactly 28px wide to prevent deforming */
    div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) > div[data-testid="stColumn"] {
        width: 28px !important;
        min-width: 28px !important;
        max-width: 28px !important;
        flex: 0 0 28px !important;
    }
    
    /* Style only waffle grid selectbox containers */
    div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) div.stSelectbox {
        width: 28px !important;
        height: 28px !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Hide the selectbox label to maximize grid alignment */
    div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) div.stSelectbox label {
        display: none !important;
    }
    
    /* Default group styling for waffle cells */
    div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) div.stSelectbox div[role="group"] {
        width: 28px !important;
        height: 28px !important;
        border-radius: 6px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        overflow: hidden !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: none !important;
        background-color: rgba(0, 0, 0, 0.035) !important;
        border: 1px dashed rgba(0, 0, 0, 0.12) !important;
    }
    
    /* Hover transitions: translation and glow shadow */
    div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) div.stSelectbox div[role="group"]:hover {
        transform: translateY(-2px) scale(1.08) !important;
        border-color: rgba(0, 0, 0, 0.3) !important;
        cursor: pointer !important;
    }
    
    /* Green status cell: Done */
    div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) div.stSelectbox div[role="group"]:has(input[value="✅"]) {
        background-color: rgba(16, 185, 129, 0.08) !important;
        border: 1.5px solid #10b981 !important;
        box-shadow: 0 2px 6px rgba(16, 185, 129, 0.12) !important;
    }
    div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) div.stSelectbox div[role="group"]:has(input[value="✅"]):hover {
        border-color: #059669 !important;
        box-shadow: 0 4px 10px rgba(5, 150, 105, 0.25) !important;
    }
    
    /* Red status cell: Failed */
    div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) div.stSelectbox div[role="group"]:has(input[value="❌"]) {
        background-color: rgba(239, 68, 68, 0.06) !important;
        border: 1.5px solid #ef4444 !important;
        box-shadow: 0 2px 6px rgba(239, 68, 68, 0.08) !important;
    }
    div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) div.stSelectbox div[role="group"]:has(input[value="❌"]):hover {
        border-color: #dc2626 !important;
        box-shadow: 0 4px 10px rgba(220, 38, 38, 0.2) !important;
    }
    
    /* Style the input inside the waffle cell */
    div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) div.stSelectbox input {
        width: 28px !important;
        height: 26px !important;
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        text-align: center !important;
        font-size: 1.1rem !important;
        line-height: 26px !important;
        cursor: pointer !important;
        caret-color: transparent !important;
    }
    
    /* Hide the ⬜ emoji text in empty cells to reveal a clean dashed slot background */
    div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) div.stSelectbox div[role="group"]:has(input[value="⬜"]) input {
        color: transparent !important;
    }
    
    /* Hide the default dropdown SVG arrow/button inside the grid cell */
    div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) div.stSelectbox button {
        display: none !important;
        width: 0px !important;
        height: 0px !important;
        padding: 0 !important;
    }
    
    /* Ensure the selectbox dropdown container has a horizontal, aesthetic width with breathing room */
    div[data-testid="stSelectboxVirtualDropdown"] {
        width: 132px !important;
        min-width: 132px !important;
        height: 44px !important;
        background-color: transparent !important;
    }
    
    /* Target the listbox elements inside the dropdown container and force flexrow with spacious layout */
    div[data-testid="stSelectboxVirtualDropdown"] div[role="listbox"] {
        width: 132px !important;
        min-width: 132px !important;
        height: 44px !important;
        background-color: #ffffff !important; /* Pure white background in light mode */
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        border-radius: 12px !important;
        padding: 4px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1) !important;
        display: flex !important;
        flex-direction: row !important; /* Lay items horizontally */
        align-items: center !important;
        justify-content: space-around !important; /* Distribute items evenly */
        overflow: visible !important;
    }
    
    /* Force all descendants of the listbox to lay out horizontally and statically, overriding absolute positioning and containment */
    div[data-testid="stSelectboxVirtualDropdown"] [role="listbox"] * {
        position: static !important;
        display: flex !important;
        flex-direction: row !important;
        width: auto !important;
        height: auto !important;
        top: auto !important;
        left: auto !important;
        transform: none !important;
        box-shadow: none !important;
        contain: none !important; /* Disable React Aria layout containment optimizations */
    }
    
    /* Style each option item to be a clean spacious square to prevent squishing */
    div[data-testid="stSelectboxVirtualDropdown"] [role="option"] {
        width: 36px !important;
        height: 36px !important;
        min-width: 36px !important;
        max-width: 36px !important;
        min-height: 36px !important;
        max-height: 36px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        border-radius: 8px !important;
        cursor: pointer !important;
        margin: 0 !important;
        padding: 0 !important;
        transition: background-color 0.15s ease !important;
    }
    div[data-testid="stSelectboxVirtualDropdown"] [role="option"]:hover {
        background-color: rgba(0, 0, 0, 0.04) !important;
    }
    
    /* Force text/emojis inside options to be centered, fully visible, and keep native colors */
    div[data-testid="stSelectboxVirtualDropdown"] [role="option"] * {
        background-color: transparent !important;
        color: #1c1917 !important; /* Dark text contrast for light mode */
        font-size: 1.25rem !important; /* Beautiful large emoji size */
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        height: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
        overflow: visible !important; /* Prevent child clipping */
    }
    
    /* Expander customizations */
    div[data-testid="stExpander"] {
        background-color: rgba(255, 255, 255, 0.6) !important;
        border: 1px solid rgba(0, 0, 0, 0.05) !important;
        border-radius: 12px !important;
        margin-top: 1rem !important;
    }
    
    /* Quirky, modern button style */
    .stButton>button {
        background: linear-gradient(135deg, #10b981, #06b6d4) !important;
        color: #ffffff !important; /* Clean white text on gradient */
        border: none !important;
        border-radius: 10px !important;
        padding: 0.55rem 1.6rem !important;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600 !important;
        width: 100%;
        box-shadow: 0 4px 15px 0 rgba(16, 185, 129, 0.2) !important;
        transition: all 0.25s ease-in-out !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 22px 0 rgba(16, 185, 129, 0.3) !important;
    }
    
    /* Hide sidebar and toggle control */
    section[data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Custom Micro Stats Badge Styling */
    .stats-row {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 0.8rem;
    }
    .member-header {
        margin: 0 0 0.5rem 0 !important;
        font-family: "Space Grotesk", sans-serif !important;
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        color: #1c1917 !important;
    }
    .habit-title {
        font-size: 0.85rem !important;
        color: #4b5563 !important;
        font-weight: 600 !important;
        margin-bottom: 0.4rem !important;
        font-family: "Space Grotesk", sans-serif !important;
    }
    .habit-category {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-bottom: 2px !important;
        display: block !important;
    }
    .habit-category.do-category {
        color: #0f766e !important; /* Teal */
    }
    .habit-category.drop-category {
        color: #be123c !important; /* Rose */
    }
    .stat-tag {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.76rem;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 6px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        border: 1px solid transparent;
    }
    .stat-tag.success {
        background-color: rgba(16, 185, 129, 0.08);
        color: #065f46;
        border-color: rgba(16, 185, 129, 0.15);
    }
    .stat-tag.streak {
        background-color: rgba(245, 158, 11, 0.08);
        color: #92400e;
        border-color: rgba(245, 158, 11, 0.15);
    }
    .stat-tag.danger {
        background-color: rgba(239, 68, 68, 0.06);
        color: #991b1b;
        border-color: rgba(239, 68, 68, 0.12);
    }
    
    /* Modern minimalist commitment quote box */
    .mission-quote-box {
        background-color: rgba(245, 245, 244, 0.65) !important;
        border-left: 3px solid #0f766e !important; /* Elegant deep teal */
        padding: 8px 12px !important;
        border-radius: 4px 8px 8px 4px !important;
        margin: -0.4rem 0 1rem 0 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    .mission-quote-title {
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: #0f766e !important;
        display: block !important;
        margin-bottom: 2px !important;
    }
    .mission-quote-text {
        font-size: 0.88rem !important;
        font-style: italic !important;
        font-weight: 500 !important;
        color: #44403c !important;
        margin: 0 !important;
        line-height: 1.25 !important;
    }
    
    /* Tiny visual day watermark for empty cells */
    .waffle-watermark {
        position: absolute !important;
        font-size: 8px !important;
        font-weight: 600 !important;
        color: rgba(0, 0, 0, 0.22) !important;
        pointer-events: none !important;
        bottom: 2px !important;
        right: 3px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        transition: opacity 0.2s ease !important;
        z-index: 10 !important;
    }
    
    /* Hide watermark when cell is checked */
    div[role="group"]:has(input[value="✅"]) .waffle-watermark,
    div[role="group"]:has(input[value="❌"]) .waffle-watermark {
        opacity: 0 !important;
    }
    
    /* Mobile-first responsive styling overrides */
    @media (max-width: 500px) {
        /* Mobile cell watermark adjustments */
        .waffle-watermark {
            font-size: 6.5px !important;
            bottom: 1px !important;
            right: 2px !important;
        }
        /* Scale down the main title and subtitle */
        .main-title {
            font-size: 1.8rem !important;
        }
        .subtitle {
            font-size: 0.8rem !important;
        }
        
        /* Scale down member header */
        .member-header {
            font-size: 1.15rem !important;
            margin-bottom: 0.35rem !important;
        }
        
        /* Scale down habit labels */
        .habit-title {
            font-size: 0.78rem !important;
            margin-bottom: 0.3rem !important;
        }
        /* Scale down habit category labels */
        .habit-category {
            font-size: 0.64rem !important;
            margin-bottom: 1px !important;
        }
        /* Compact stats tags to fit narrow phone screens side-by-side */
        .stat-tag {
            font-size: 0.68rem !important;
            padding: 2px 6px !important;
            border-radius: 5px !important;
        }
        
        /* Tighten commitment quote box space */
        .mission-quote-box {
            padding: 6px 10px !important;
            margin-bottom: 0.8rem !important;
        }
        .mission-quote-text {
            font-size: 0.8rem !important;
        }
        
        /* Adjust card padding to save screen space */
        div[data-testid="stVerticalBlockBorderEffect"] {
            padding: 0.9rem !important;
            border-radius: 16px !important;
        }
        
        /* Scale down the waffle grid cells to fit mobile viewports */
        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) > div[data-testid="stColumn"] {
            width: 20px !important;
            min-width: 20px !important;
            max-width: 20px !important;
            flex: 0 0 20px !important;
        }
        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) div.stSelectbox {
            width: 20px !important;
            height: 20px !important;
        }
        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) div.stSelectbox div[role="group"] {
            width: 20px !important;
            height: 20px !important;
            border-radius: 4px !important;
        }
        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) div.stSelectbox input {
            width: 20px !important;
            height: 18px !important;
            font-size: 0.85rem !important;
            line-height: 18px !important;
        }
        
        /* Set grid wrapper bounds for mobile */
        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) {
            max-width: 350px !important;
            gap: 2.5px !important;
            margin-bottom: 2.5px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ----------------- LOCAL DATA SETUP -----------------
LOCAL_FILE = "data.csv"

def clean_dataframe(df):
    """Ensures standard structure for Member, HabitType, and all 75 day columns."""
    if df is None:
        df = pd.DataFrame()
    # Rename "Name" column to "Member" for internal consistency if present
    if "Name" in df.columns:
        df = df.rename(columns={"Name": "Member"})
    if "Member" not in df.columns:
        df["Member"] = ""
    if "HabitType" not in df.columns:
        df["HabitType"] = ""
    
    # Fill NaN and convert to clean strings
    df["Member"] = df["Member"].fillna("").astype(str).str.strip()
    df["HabitType"] = df["HabitType"].fillna("").astype(str).str.strip()
    
    # Ensure all Day columns exist and are clean
    for i in range(1, 76):
        col = f"Day {i}"
        if col not in df.columns:
            df[col] = ""
        df[col] = df[col].fillna("").astype(str).str.strip()
        
    return df

def init_mock_data():
    """Initializes a local data.csv with sample members and random progress if it doesn't exist."""
    if not os.path.exists(LOCAL_FILE):
        days_cols = [f"Day {i}" for i in range(1, 76)]
        columns = ["Member", "HabitType"] + days_cols
        
        # Sample members
        members_sample = ["Rohit", "Sarah", "Alex"]
        data = []
        
        # Seed deterministic sample data
        np.random.seed(42)
        choices = ["", "Done", "Failed"]
        probabilities = [0.4, 0.5, 0.1]
        
        for m in members_sample:
            for habit in ["Do", "Drop"]:
                row = [m, habit]
                for day in range(75):
                    # Fill first 15-22 days, leave remaining empty
                    if day < 22:
                        row.append(np.random.choice(choices, p=probabilities))
                    else:
                        row.append("")
                data.append(row)
                
        df = pd.DataFrame(data, columns=columns)
        df = clean_dataframe(df)
        df.to_csv(LOCAL_FILE, index=False)
    else:
        df = pd.read_csv(LOCAL_FILE)
        df = clean_dataframe(df)
    return df

# ----------------- DATA LOADING -----------------
SHEET_URL = "https://docs.google.com/spreadsheets/d/1PGNxcmcZtpG3XtnPyynBacZbMRX-xS1bjLlLR0QJmm4/edit?usp=sharing"
CSV_URL = "https://docs.google.com/spreadsheets/d/1PGNxcmcZtpG3XtnPyynBacZbMRX-xS1bjLlLR0QJmm4/export?format=csv"
MISSIONS_FILE = "missions.csv"
MISSIONS_CSV_URL = "https://docs.google.com/spreadsheets/d/1PGNxcmcZtpG3XtnPyynBacZbMRX-xS1bjLlLR0QJmm4/export?format=csv&gid=718170288"

# Auto-sync from Google Sheets on initial page load / browser refresh
if "has_synced" not in st.session_state:
    st.session_state["has_synced"] = True
    
    # Sync main waffle tracker data
    try:
        df = pd.read_csv(CSV_URL)
        df = clean_dataframe(df)
        df.to_csv(LOCAL_FILE, index=False)
        st.toast("🔄 Auto-synced latest progress from Google Sheet!", icon="🔄")
    except Exception as e:
        st.toast(f"⚠️ Failed to auto-sync from Sheet: {e}", icon="⚠️")
        if os.path.exists(LOCAL_FILE):
            df = pd.read_csv(LOCAL_FILE)
            df = clean_dataframe(df)
        else:
            df = init_mock_data()
            
    # Sync missions data
    try:
        missions_df = pd.read_csv(MISSIONS_CSV_URL)
        missions_df.columns = [c.strip() for c in missions_df.columns]
        missions_df["Name"] = missions_df["Name"].fillna("").astype(str).str.strip()
        missions_df["Mission"] = missions_df["Mission"].fillna("").astype(str).str.strip()
        missions_df.to_csv(MISSIONS_FILE, index=False)
    except Exception as e:
        if os.path.exists(MISSIONS_FILE):
            missions_df = pd.read_csv(MISSIONS_FILE)
        else:
            missions_df = pd.DataFrame(columns=["Name", "Mission"])
else:
    # Read main waffle tracker data
    if os.path.exists(LOCAL_FILE):
        df = pd.read_csv(LOCAL_FILE)
        df = clean_dataframe(df)
    else:
        df = init_mock_data()
        
    # Read missions data
    if os.path.exists(MISSIONS_FILE):
        missions_df = pd.read_csv(MISSIONS_FILE)
    else:
        missions_df = pd.DataFrame(columns=["Name", "Mission"])

# Check if Streamlit GSheets secrets are configured
def is_gsheets_configured():
    try:
        if "connections" in st.secrets and "gsheets" in st.secrets["connections"]:
            return True
    except:
        pass
    return False

# ----------------- MAIN PAGE HEADER -----------------
st.markdown("""
<div class="title-container" style="padding: 1rem 0 0.5rem 0; margin-bottom: 1rem;">
    <h1 class="main-title" style="font-size: 2.2rem;">🔥 75-Day Challenge</h1>
    <div class="subtitle" style="font-size: 0.95rem; margin-top: 0.2rem;">Waffle Habit Tracker & Streak Dashboard</div>
</div>
""", unsafe_allow_html=True)

# ----------------- CLOUD CONFIGURATION -----------------
GSCRIPT_FILE = "gscript_url.txt"

# Load saved Google Apps Script URL if it exists
if "gscript_url" not in st.session_state:
    if os.path.exists(GSCRIPT_FILE):
        try:
            with open(GSCRIPT_FILE, "r") as f:
                st.session_state["gscript_url"] = f.read().strip()
        except:
            st.session_state["gscript_url"] = ""
    else:
        st.session_state["gscript_url"] = ""

# ----------------- AUTO-SAVE SYNCHRONIZATION -----------------
import threading

def run_cloud_sync_in_background(df_to_save, gscript_url):
    try:
        if gscript_url:
            import requests
            import json
            payload = {
                "headers": df_to_save.columns.tolist(),
                "rows": df_to_save.values.tolist()
            }
            requests.post(
                gscript_url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=25
            )
        elif is_gsheets_configured():
            from streamlit_gsheets import GSheetsConnection
            conn = st.connection("gsheets", type=GSheetsConnection)
            conn.update(
                spreadsheet=SHEET_URL,
                data=df_to_save
            )
    except Exception as e:
        import logging
        logging.error(f"Background cloud sync failed: {e}")

def save_and_sync():
    try:
        # Load the latest local copy to update
        df_to_update = pd.read_csv(LOCAL_FILE)
        df_to_update = clean_dataframe(df_to_update)
        
        reverse_map = {"⬜": "", "✅": "Done", "❌": "Failed"}
        members_list = df_to_update["Member"].unique() if not df_to_update.empty else []
        for m in members_list:
            for habit in ["Do", "Drop"]:
                match = df_to_update[(df_to_update["Member"] == m) & (df_to_update["HabitType"].str.lower().str.startswith(habit.lower()))]
                if not match.empty:
                    idx = match.index[0]
                    for day_num in range(1, 76):
                        key = f"{m}_{habit}_{day_num}"
                        if key in st.session_state:
                            val = st.session_state[key]
                            df_to_update.at[idx, f"Day {day_num}"] = reverse_map.get(val, "")
        
        df_to_update.to_csv(LOCAL_FILE, index=False)
        st.toast("Progress saved locally & syncing to cloud...", icon="💾")
        
        # Dispatch cloud sync to background thread to prevent UI freezing
        gscript_url = st.session_state.get("gscript_url", "").strip()
        df_to_save = df_to_update.rename(columns={"Member": "Name"}).fillna("")
        
        if gscript_url or is_gsheets_configured():
            thread = threading.Thread(
                target=run_cloud_sync_in_background,
                args=(df_to_save, gscript_url)
            )
            thread.daemon = True
            thread.start()
            
    except Exception as e:
        st.error(f"Failed to auto-save: {e}")

# Main page action buttons (Save button removed, auto-save active)
with st.container(border=True):
    col_sync, col_status = st.columns([2.5, 9.5])
    
    with col_sync:
        if st.button("🔄 Sync from Sheet"):
            try:
                df_cloud = pd.read_csv(CSV_URL)
                df_cloud = clean_dataframe(df_cloud)
                df_cloud.to_csv(LOCAL_FILE, index=False)
                st.toast("Synchronized with Google Sheet!", icon="🔄")
                st.rerun()
            except Exception as e:
                st.error(f"Sync failed: {e}")
    
    with col_status:
        gscript_url = st.session_state.get("gscript_url", "").strip()
        if gscript_url:
            st.markdown("<div style='font-size: 0.85rem; color: #10b981; padding-top: 0.65rem; font-weight: 600;'>☁️ Auto-sync active (Cloud Web App Mode)</div>", unsafe_allow_html=True)
        elif is_gsheets_configured():
            st.markdown("<div style='font-size: 0.85rem; color: #10b981; padding-top: 0.65rem; font-weight: 600;'>☁️ Auto-sync active (Secrets Mode)</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='font-size: 0.85rem; color: #f59e0b; padding-top: 0.65rem;'>📂 Auto-save active (Local Mode - configure cloud settings below to sync)</div>", unsafe_allow_html=True)

# Google Sheet Cloud Settings Expander
with st.expander("⚙️ Google Sheet Cloud Sync Settings"):
    gscript_input = st.text_input(
        "Google Apps Script Web App URL",
        value=st.session_state.get("gscript_url", ""),
        placeholder="https://script.google.com/macros/s/.../exec",
        help="Paste the deployed Apps Script URL here to enable automatic write-backs to Google Sheets."
    )
    if gscript_input != st.session_state.get("gscript_url", ""):
        st.session_state["gscript_url"] = gscript_input
        try:
            with open(GSCRIPT_FILE, "w") as f:
                f.write(gscript_input)
        except Exception as file_err:
            st.error(f"Failed to save settings file: {file_err}")
        st.toast("Google Sheets Web App URL updated!", icon="🔗")
        st.rerun()
        
    st.markdown("""
    ### How to set up zero-config cloud sync:
    1. Open your [Google Sheet](https://docs.google.com/spreadsheets/d/1PGNxcmcZtpG3XtnPyynBacZbMRX-xS1bjLlLR0QJmm4/edit?usp=sharing).
    2. Click **Extensions > Apps Script** in the top menu.
    3. Delete any boilerplate code and paste the following Google Apps Script:
    ```javascript
    function doPost(e) {
      try {
        var data = JSON.parse(e.postData.contents);
        var ss = SpreadsheetApp.getActiveSpreadsheet();
        var sheet = ss.getSheets()[0]; // Targets the first sheet
        
        sheet.clearContents();
        sheet.getRange(1, 1, 1, data.headers.length).setValues([data.headers]);
        if (data.rows && data.rows.length > 0) {
          sheet.getRange(2, 1, data.rows.length, data.headers.length).setValues(data.rows);
        }
        return ContentService.createTextOutput(JSON.stringify({status: "success"}))
          .setMimeType(ContentService.MimeType.JSON);
      } catch (err) {
        return ContentService.createTextOutput(JSON.stringify({status: "error", message: err.toString()}))
          .setMimeType(ContentService.MimeType.JSON);
      }
    }
    ```
    4. Click the **Save** icon (disk icon).
    5. Click **Deploy > New deployment** in the top-right.
    6. Click the gear icon next to "Select type" and select **Web app**.
    7. Configure:
       - **Execute as:** `Me (your email)`
       - **Who has access:** `Anyone`
    8. Click **Deploy** and authorize permissions (click *Advanced* and *Go to Untitled project (unsafe)* if prompted).
    9. Copy the **Web app URL** and paste it in the box above!
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

# ----------------- METRICS DASHBOARD -----------------
def compute_stats(rows, habit_type):
    habit_row = rows[rows["HabitType"].str.lower().str.startswith(habit_type.lower())]
    if habit_row.empty:
        return 0, 0, 0
    row_vals = [habit_row.iloc[0][f"Day {i}"] for i in range(1, 76)]
    row_vals = ["" if pd.isna(v) or str(v).lower() == "nan" else str(v) for v in row_vals]
    
    done_count = sum(1 for v in row_vals if v == "Done")
    failed_count = sum(1 for v in row_vals if v == "Failed")
    
    max_streak = 0
    curr_streak = 0
    for v in row_vals:
        if v == "Done":
            curr_streak += 1
            max_streak = max(max_streak, curr_streak)
        else:
            curr_streak = 0
            
    return done_count, failed_count, max_streak

# ----------------- Waffle Grid Rendering -----------------
def render_waffle(member, member_rows, habit_type, title, emoji_prefix):
    # Extract the row corresponding to this specific habit type
    habit_rows = member_rows[member_rows["HabitType"].str.lower().str.startswith(habit_type.lower())]
    
    if habit_rows.empty:
        st.markdown(f"<div style='font-size: 0.9rem; color: #94a3b8; font-weight: 600; margin-bottom: 0.25rem;'>{title} (No data)</div>", unsafe_allow_html=True)
        return
        
    row_data = habit_rows.iloc[0]
    actual_habit_description = row_data["HabitType"]
    
    # Clean up redundant prefix Do: / Drop:
    desc = actual_habit_description
    for prefix in ["do:", "drop:"]:
        if desc.lower().startswith(prefix):
            desc = desc[len(prefix):].strip()
            
    icon = "🟢" if habit_type.lower() == "do" else "🔴"
    category_label = "Things I'll Do" if habit_type.lower() == "do" else "Things I'll Drop"
    category_class = "do-category" if habit_type.lower() == "do" else "drop-category"
    
    st.markdown(f"""
    <div class="habit-category {category_class}">{category_label}</div>
    <div class='habit-title'>{icon} {desc}</div>
    """, unsafe_allow_html=True)
    
    options_map = {"": "⬜", "Done": "✅", "Failed": "❌"}
    
    for r in range(5):
        cols = st.columns(15)
        for c in range(15):
            day_num = (r * 15) + c + 1
            col_name = f"Day {day_num}"
            
            # Read current database value (fallback to blank if nan)
            current_val = row_data.get(col_name, "")
            if pd.isna(current_val) or str(current_val).lower() == "nan":
                current_val = ""
            
            # Normalize casing and remove whitespace
            current_val = str(current_val).strip()
            if current_val.lower() == "done":
                current_val = "Done"
            elif current_val.lower() == "failed":
                current_val = "Failed"
            else:
                current_val = ""
                
            default_emoji = options_map.get(current_val, "⬜")
            
            with cols[c]:
                st.selectbox(
                    f"D{day_num}",
                    options=["⬜", "✅", "❌"],
                    index=["⬜", "✅", "❌"].index(default_emoji),
                    key=f"{member}_{habit_type}_{day_num}",
                    label_visibility="collapsed",
                    on_change=save_and_sync
                )

# Display each participant's grids inside modern glass containers
members_list = sorted(df["Member"].unique()) if not df.empty else []

for member in members_list:
    with st.container(border=True):
        st.markdown(f"<h3 class='member-header'>👤 {member}</h3>", unsafe_allow_html=True)
        
        # Display the commitment mission as an elegant quote box
        if 'missions_df' in globals() and not missions_df.empty:
            match = missions_df[missions_df["Name"].str.lower().str.strip() == member.lower().strip()]
            if not match.empty:
                mission_text = match.iloc[0]["Mission"]
                if pd.notna(mission_text) and str(mission_text).strip():
                    st.markdown(f"""
                    <div class="mission-quote-box">
                        <p class="mission-quote-text">“{mission_text}”</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        member_rows = df[df["Member"] == member]
        
        # Calculate stats
        do_done, do_failed, do_streak = compute_stats(member_rows, "Do")
        drop_done, drop_failed, drop_streak = compute_stats(member_rows, "Drop")
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown(f"""
            <div class="stats-row">
                <span class="stat-tag success">🟢 {do_done}/75d</span>
                <span class="stat-tag streak">🔥 Streak: {do_streak}d</span>
                <span class="stat-tag danger">❌ Failed: {do_failed}</span>
            </div>
            """, unsafe_allow_html=True)
            render_waffle(member, member_rows, "Do", "Daily DO", "do")
            
        with col2:
            st.markdown(f"""
            <div class="stats-row">
                <span class="stat-tag success">🔴 {drop_done}/75d</span>
                <span class="stat-tag streak">🔥 Streak: {drop_streak}d</span>
                <span class="stat-tag danger">❌ Failed: {drop_failed}</span>
            </div>
            """, unsafe_allow_html=True)
            render_waffle(member, member_rows, "Drop", "Daily DROP", "drop")
        
    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

# ----------------- HOVER INTERACTIONS JS INJECTION -----------------
import streamlit.components.v1 as components
components.html("""
<script>
    (function() {
        const parentDoc = window.parent.document;
        let isHoveringDropdown = false;
        
        // Helper function to close dropdown cleanly
        function closeDropdown(input) {
            if (!input) return;
            const escEvent = new KeyboardEvent('keydown', {
                key: 'Escape',
                code: 'Escape',
                keyCode: 27,
                which: 27,
                bubbles: true,
                cancelable: true
            });
            input.dispatchEvent(escEvent);
            input.blur();
        }
        
        // Mobile-friendly outside tap handler to prevent overlapping option bars
        function handleOutsideTap(e) {
            const activeInput = parentDoc.activeElement;
            if (activeInput && activeInput.tagName === 'INPUT' && activeInput.getAttribute('aria-expanded') === 'true') {
                const clickedSelectbox = e.target.closest('div.stSelectbox');
                const clickedDropdown = e.target.closest('div[data-testid="stSelectboxVirtualDropdown"]');
                
                // If they tapped outside the currently active selectbox and its popover dropdown, close it immediately
                if (!clickedSelectbox || clickedSelectbox.querySelector('input') !== activeInput) {
                    if (!clickedDropdown) {
                        closeDropdown(activeInput);
                    }
                }
            }
        }
        
        // Listen to mousedown and touchstart in the capture phase to dismiss old popovers before new ones open
        parentDoc.addEventListener('mousedown', handleOutsideTap, true);
        parentDoc.addEventListener('touchstart', handleOutsideTap, true);
        
        // Track hover state on the dropdown container globally in the parent document
        parentDoc.addEventListener('mouseover', function(e) {
            const dropdown = e.target.closest('div[data-testid="stSelectboxVirtualDropdown"]');
            if (dropdown) {
                isHoveringDropdown = true;
            }
        }, true);
        
        parentDoc.addEventListener('mouseout', function(e) {
            const dropdown = e.target.closest('div[data-testid="stSelectboxVirtualDropdown"]');
            if (dropdown) {
                if (!e.relatedTarget || !dropdown.contains(e.relatedTarget)) {
                    isHoveringDropdown = false;
                    // If mouse left the dropdown, close the active input after a short delay
                    setTimeout(() => {
                        const activeInput = parentDoc.activeElement;
                        if (activeInput && activeInput.tagName === 'INPUT' && activeInput.getAttribute('aria-expanded') === 'true') {
                            if (!isHoveringDropdown) {
                                closeDropdown(activeInput);
                            }
                        }
                    }, 150);
                }
            }
        }, true);
        
        function setupHoverListeners() {
            // Find all waffle selectbox elements in the grid
            const grids = parentDoc.querySelectorAll('div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) div.stSelectbox');
            
            grids.forEach(grid => {
                const input = grid.querySelector('input');
                if (!input) return;
                
                // Read aria-label to get day number (e.g., "D15")
                const ariaLabel = input.getAttribute('aria-label') || "";
                const dayNum = ariaLabel.replace('D', '');
                
                if (dayNum) {
                    input.title = "Day " + dayNum;
                }
                
                // Avoid double-binding event listeners
                if (grid.dataset.hoverBound) return;
                grid.dataset.hoverBound = "true";
                
                // Add tiny visual day watermark inside the cell
                if (dayNum) {
                    const group = grid.querySelector('div[role="group"]');
                    if (group) {
                        const watermark = parentDoc.createElement('span');
                        watermark.className = 'waffle-watermark';
                        watermark.innerText = dayNum;
                        group.appendChild(watermark);
                    }
                }
                
                // When mouse enters the cell
                grid.addEventListener('mouseenter', function() {
                    // Immediately close any other open dropdown before opening this one
                    const activeInput = parentDoc.activeElement;
                    if (activeInput && activeInput.tagName === 'INPUT' && activeInput.getAttribute('aria-expanded') === 'true' && activeInput !== input) {
                        closeDropdown(activeInput);
                    }
                    
                    const isExpanded = input.getAttribute('aria-expanded') === 'true';
                    if (!isExpanded) {
                        // Focus and click the input to trigger dropdown open
                        input.focus();
                        input.click();
                    }
                });
                
                // When mouse leaves the cell
                grid.addEventListener('mouseleave', function() {
                    // Wait a short grace period to allow the mouse to transition to the dropdown popover
                    setTimeout(() => {
                        if (isHoveringDropdown) return; // Keep open if mouse is now on the dropdown options
                        
                        const isExpanded = input.getAttribute('aria-expanded') === 'true';
                        if (isExpanded) {
                            closeDropdown(input);
                        }
                    }, 150);
                });
            });
        }
        
        // Run immediately and on a delay to capture rendering
        setupHoverListeners();
        setTimeout(setupHoverListeners, 300);
        setTimeout(setupHoverListeners, 1000);
        
        // Also listen for scroll events to auto-dismiss open dropdowns
        parentDoc.addEventListener('scroll', function() {
            const activeInput = parentDoc.activeElement;
            if (activeInput && activeInput.tagName === 'INPUT' && activeInput.getAttribute('aria-expanded') === 'true') {
                closeDropdown(activeInput);
            }
        }, true); // Use capture phase to catch all scrolls
    })();
</script>
""", height=0)
