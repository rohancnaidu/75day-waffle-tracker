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
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    /* Global styles */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Outfit', sans-serif;
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    
    /* Remove default Streamlit top whitespace */
    [data-testid="block-container"] {
        padding-top: 1.2rem !important;
        padding-bottom: 1rem !important;
    }
    
    /* Header Styling */
    .title-container {
        text-align: center;
        padding: 2rem 0 1rem 0;
        margin-bottom: 1.5rem;
        background: linear-gradient(180deg, rgba(99, 102, 241, 0.05) 0%, rgba(11, 15, 25, 0) 100%);
        border-radius: 20px;
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.05em;
        background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* Glassmorphic Cards */
    .card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(12px);
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.2);
        transition: transform 0.2s, border-color 0.2s;
    }
    .card:hover {
        border-color: rgba(99, 102, 241, 0.2);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #f8fafc;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Waffle Grid customization */
    div[data-testid="stColumn"] {
        padding: 0px !important;
    }
    
    /* Target only the 15-column rows of the waffle grid to set a compact gap and max-width */
    div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) {
        max-width: 470px !important;
        gap: 3px !important;
        margin-bottom: 3px !important;
        flex-wrap: nowrap !important;
        overflow: visible !important;
    }
    
    /* Style only the nested waffle columns to be exactly 28px wide to prevent stretching/deforming */
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
    
    /* Style the React-Aria ComboBox Group wrapper */
    div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) div.stSelectbox div[role="group"] {
        width: 28px !important;
        height: 28px !important;
        background-color: #1e293b !important; /* Solid dark slate cell */
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 4px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        overflow: hidden !important;
        transition: border-color 0.2s, background-color 0.2s;
        box-shadow: none !important;
    }
    div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) div.stSelectbox div[role="group"]:hover {
        border-color: rgba(99, 102, 241, 0.5) !important;
        background-color: #2d3748 !important;
    }
    
    /* Style the input element that displays the emoji */
    div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(15)) div.stSelectbox input {
        width: 28px !important;
        height: 26px !important;
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        text-align: center !important;
        font-size: 1.15rem !important; /* Large, crisp emoji rendering */
        line-height: 26px !important;
        cursor: pointer !important;
        caret-color: transparent !important; /* Hide input cursor */
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
        background-color: #1e293b !important; /* Solid dark slate dropdown card */
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        padding: 4px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5) !important;
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
        border-radius: 6px !important;
        cursor: pointer !important;
        margin: 0 !important;
        padding: 0 !important;
        transition: background-color 0.15s ease !important;
    }
    div[data-testid="stSelectboxVirtualDropdown"] [role="option"]:hover {
        background-color: rgba(255, 255, 255, 0.08) !important;
    }
    
    /* Force text/emojis inside options to be centered, fully visible, and keep native colors */
    div[data-testid="stSelectboxVirtualDropdown"] [role="option"] * {
        background-color: transparent !important;
        color: #f8fafc !important; /* Ensure light text contrast */
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
    
    /* Custom buttons */
    .stButton>button {
        background: linear-gradient(95deg, #4f46e5, #7c3aed) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        width: 100%;
        box-shadow: 0 4px 14px 0 rgba(79, 70, 229, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px 0 rgba(79, 70, 229, 0.5) !important;
        background: linear-gradient(95deg, #5b52f9, #8b4bfb) !important;
    }
    
    /* Hide sidebar and toggle control */
    section[data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
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

# Force load from cloud if local file is missing or contains old mock data (e.g. Rohit)
force_load_cloud = False
if os.path.exists(LOCAL_FILE):
    try:
        temp_df = pd.read_csv(LOCAL_FILE)
        if "Member" in temp_df.columns and any(name in temp_df["Member"].values for name in ["Rohit", "Sarah", "Alex"]):
            force_load_cloud = True
    except:
        force_load_cloud = True

if os.path.exists(LOCAL_FILE) and not force_load_cloud:
    df = pd.read_csv(LOCAL_FILE)
    df = clean_dataframe(df)
else:
    try:
        df = pd.read_csv(CSV_URL)
        df = clean_dataframe(df)
        df.to_csv(LOCAL_FILE, index=False)
        st.toast("🔗 Loaded fresh data from Google Sheet!", icon="🔗")
    except Exception as e:
        st.toast(f"⚠️ Google Sheets failed. Using mock data: {e}", icon="⚠️")
        df = init_mock_data()

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
        
        # Attempt to write back to Google Sheets
        gscript_url = st.session_state.get("gscript_url", "").strip()
        
        if gscript_url:
            try:
                import requests
                import json
                df_to_save = df_to_update.rename(columns={"Member": "Name"})
                df_to_save = df_to_save.fillna("")
                payload = {
                    "headers": df_to_save.columns.tolist(),
                    "rows": df_to_save.values.tolist()
                }
                res = requests.post(
                    gscript_url,
                    data=json.dumps(payload),
                    headers={"Content-Type": "application/json"},
                    timeout=15
                )
                if res.status_code == 200:
                    st.toast("Progress auto-saved and synced to Google Sheets!", icon="💾")
                else:
                    st.toast(f"Auto-saved locally (Cloud sync HTTP error: {res.status_code})", icon="⚠️")
            except Exception as g_err:
                st.toast(f"Auto-saved locally (Cloud sync connection failed: {g_err})", icon="⚠️")
        elif is_gsheets_configured():
            try:
                from streamlit_gsheets import GSheetsConnection
                conn = st.connection("gsheets", type=GSheetsConnection)
                df_to_save = df_to_update.rename(columns={"Member": "Name"})
                df_to_save = df_to_save.fillna("")
                conn.update(
                    spreadsheet=SHEET_URL,
                    data=df_to_save
                )
                st.toast("Progress auto-saved and synced to Google Sheets!", icon="💾")
            except Exception as g_err:
                st.toast(f"Auto-saved locally (Cloud sync failed: {g_err})", icon="⚠️")
        else:
            st.toast("Progress auto-saved locally!", icon="💾")
    except Exception as e:
        st.error(f"Failed to auto-save: {e}")

# Main page action buttons (Save button removed, auto-save active)
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
    st.markdown(f"<div style='font-size: 0.9rem; color: #94a3b8; font-weight: 600; margin-bottom: 0.25rem;'>{emoji_prefix.upper()} - {actual_habit_description}</div>", unsafe_allow_html=True)
    
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

# Display each participant's grids one below the other
members_list = sorted(df["Member"].unique()) if not df.empty else []

for member in members_list:
    st.markdown(f"<h3 style='margin: 1.5rem 0 0.5rem 0; font-size: 1.3rem; font-weight: 700; color: #f8fafc;'>👤 {member}</h3>", unsafe_allow_html=True)
    
    member_rows = df[df["Member"] == member]
    
    # Calculate stats
    do_done, do_failed, do_streak = compute_stats(member_rows, "Do")
    drop_done, drop_failed, drop_streak = compute_stats(member_rows, "Drop")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown(f"<div style='font-size: 0.85rem; color: #10b981; margin-bottom: 0.4rem;'><b>🟢 Daily DO:</b> {do_done}/75 days &nbsp;|&nbsp; <b>🔥 Max Streak:</b> {do_streak} days &nbsp;|&nbsp; <b>❌ Failed:</b> {do_failed}</div>", unsafe_allow_html=True)
        render_waffle(member, member_rows, "Do", "Daily DO", "do")
        
    with col2:
        st.markdown(f"<div style='font-size: 0.85rem; color: #ef4444; margin-bottom: 0.4rem;'><b>🔴 Daily DROP:</b> {drop_done}/75 days &nbsp;|&nbsp; <b>🔥 Max Streak:</b> {drop_streak} days &nbsp;|&nbsp; <b>❌ Failed:</b> {drop_failed}</div>", unsafe_allow_html=True)
        render_waffle(member, member_rows, "Drop", "Daily DROP", "drop")
        
    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
    st.divider()
