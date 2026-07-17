# 🔥 75-Day Challenge Waffle Habit Tracker

A highly polished, premium Streamlit dashboard to track your 75-day challenges. It features interactive waffle grids to record daily progress, live streak calculations, statistics cards, and dual-mode storage (Google Sheets cloud sync or local CSV storage).

## ✨ Features
- 🟢 **Daily DO Grid**: Visualize and record the habits you are building.
- 🔴 **Daily DROP Grid**: Visualize and record the habits you are quitting.
- 🔥 **Live Streak & Success Tracking**: Real-time stats calculation including max streaks and overall success rates.
- ➕ **Add Participants**: Easily add new challenge participants directly from the sidebar.
- 🔗 **Dual Storage Modes**:
  - **Local Mode (Default)**: Automatically reads and writes to a local `data.csv`. Perfect for playing around immediately!
  - **Cloud Mode**: Connects directly to Google Sheets for collaboration.

---

## 🚀 Getting Started

### 1. Prerequisites
Make sure you have **Python 3.8+** installed.

### 2. Installation
Navigate to this project directory and install the required dependencies:
```bash
# Optional: Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Run the App
Start the Streamlit application:
```bash
streamlit run app.py
```
This will launch the app in your browser (typically at `http://localhost:8501`).

---

## 📊 Google Sheets Setup Guide

If you want to sync your tracker with a Google Sheet:

### Step A: Prepare the Spreadsheet
1. Create a new Google Sheet.
2. Name the first worksheet/tab as `Data`.
3. In the first row of the `Data` worksheet, add the following headers:
   - Column A: `Member`
   - Column B: `HabitType`
   - Column C through BY: `Day 1`, `Day 2`, `Day 3`, ..., `Day 75`
4. Populate a row for yourself to start:
   - Row 2: `Your Name`, `Do`, followed by empty cells for the days.
   - Row 3: `Your Name`, `Drop`, followed by empty cells for the days.

### Step B: Share the Sheet
1. Click **Share** on your Google Sheet.
2. Under "General access", change it to **Anyone with the link can view** (for public reading) or set up service account credentials for editing.
3. Copy the URL of your Google Sheet.

### Step C: Connect the App
1. Paste the URL into the **Google Sheet URL** field in the application sidebar.
2. Save progress to write updates directly to the Google Sheet!

> 💡 **Note on writing permissions:** For secure writing without opening access to everyone, configure service account credentials in a `.streamlit/secrets.toml` file under the `[connections.gsheets]` section as described in the `streamlit-gsheets` documentation.
