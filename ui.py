import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# CSV file to store data
DATA_FILE = "challenge_scores.csv"

# Load data
def load_data():
    try:
        return pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "var36 Status", "var36 Score", "HOLA_MIGO Status", "HOLA_MIGO Score"])

# Save data
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Score calculation
def calculate_score(status):
    return 4 if status == "Completed" else -0.25

st.set_page_config(page_title="LeetCode Challenge Tracker", layout="centered")
st.title("📊 LeetCode Daily Challenge Tracker")

df = load_data()

# ---- Select Who is Using Page ----
user = st.selectbox("Select User", ["var36", "HOLA_MIGO"])

# ---- Input Section ----
st.subheader("Add Daily Record")
col1, col2 = st.columns(2)

with col1:
    selected_date = st.date_input("Date", date.today())

# Get latest saved status of the other person
existing = df[df["Date"] == str(selected_date)]
if not existing.empty:
    existing = existing.iloc[0]
else:
    existing = None

if user == "var36":
    your_status = st.selectbox("var36 Status", ["Completed", "Missed"])
    friend_status_display = existing["HOLA_MIGO Status"] if existing is not None else "Not Set"
    st.text_input("HOLA_MIGO Status (read-only)", value=friend_status_display, disabled=True)

else:  # HOLA_MIGO
    your_status = st.selectbox("HOLA_MIGO Status", ["Completed", "Missed"])
    friend_status_display = existing["var36 Status"] if existing is not None else "Not Set"
    st.text_input("var36 Status (read-only)", value=friend_status_display, disabled=True)

if st.button("Add / Update Record"):
    # Calculate scores
    your_score = calculate_score(your_status)

    # Prepare default scores
    var36_status = friend_status = None
    var36_score = hola_score = None

    # If record for this date exists, load the old one
    if existing is not None:
        var36_status = existing["var36 Status"]
        var36_score = existing["var36 Score"]
        friend_status = existing["HOLA_MIGO Status"]
        hola_score = existing["HOLA_MIGO Score"]

    # Update corresponding user data
    if user == "var36":
        var36_status = your_status
        var36_score = your_score
    else:
        friend_status = your_status
        hola_score = your_score

    # Remove old entry if exists
    df = df[df["Date"] != str(selected_date)]
    df = pd.concat(
        [df, pd.DataFrame(
            {
                "Date": [str(selected_date)],
                "var36 Status": [var36_status],
                "var36 Score": [var36_score],
                "HOLA_MIGO Status": [friend_status],
                "HOLA_MIGO Score": [hola_score],
            }
        )],
        ignore_index=True
    )

    save_data(df)
    st.success("✅ Record saved successfully!")

# ---- Display table ----
st.subheader("📅 Daily Scores")
st.dataframe(df.sort_values("Date"))

# ---- Total scores ----
total_var36 = df["var36 Score"].sum()
total_hola = df["HOLA_MIGO Score"].sum()

st.metric("var36 Total Score", f"{total_var36:.2f}")
st.metric("HOLA_MIGO Total Score", f"{total_hola:.2f}")

# ---- Plotly graph ----
if not df.empty:
    st.subheader("📈 Progress Over Time")
    fig = px.line(
        df.sort_values("Date"),
        x="Date",
        y=["var36 Score", "HOLA_MIGO Score"],
        markers=True,
        title="Daily Challenge Scores",
        labels={"value": "Score", "variable": "Player"},
    )
    st.plotly_chart(fig, use_container_width=True)
