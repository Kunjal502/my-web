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
        return pd.DataFrame(columns=["Date", "Your Status", "Your Score", "Friend Status", "Friend Score"])

# Save data
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Score calculation
def calculate_score(status):
    return 4 if status == "Completed" else -0.25

st.set_page_config(page_title="LeetCode Challenge Tracker", layout="centered")
st.title("📊 LeetCode Daily Challenge Tracker")

df = load_data()

# Input section
st.subheader("Add Daily Record")
col1, col2 = st.columns(2)
with col1:
    selected_date = st.date_input("Date", date.today())
    your_status = st.selectbox("Your Status", ["Completed", "Missed"])
with col2:
    friend_status = st.selectbox("Friend's Status", ["Completed", "Missed"])

if st.button("Add / Update Record"):
    your_score = calculate_score(your_status)
    friend_score = calculate_score(friend_status)

    # Remove old entry if exists
    df = df[df["Date"] != str(selected_date)]
    df = pd.concat([df, pd.DataFrame({
        "Date": [str(selected_date)],
        "Your Status": [your_status],
        "Your Score": [your_score],
        "Friend Status": [friend_status],
        "Friend Score": [friend_score]
    })], ignore_index=True)

    save_data(df)
    st.success("✅ Record saved successfully!")

# Display table
st.subheader("📅 Daily Scores")
st.dataframe(df.sort_values("Date"))

# Total scores
total_you = df["Your Score"].sum()
total_friend = df["Friend Score"].sum()

st.metric("Your Total Score", f"{total_you:.2f}")
st.metric("Friend's Total Score", f"{total_friend:.2f}")

# Plotly graph
if not df.empty:
    st.subheader("📈 Progress Over Time")
    fig = px.line(df.sort_values("Date"), x="Date", y=["Your Score", "Friend Score"],
                  markers=True, title="Daily Challenge Scores",
                  labels={"value": "Score", "variable": "Player"})
    st.plotly_chart(fig, use_container_width=True)
