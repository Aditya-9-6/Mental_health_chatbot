import streamlit as st
import plotly.express as px
import pandas as pd
from mood import save_mood_entry, load_mood_entries

def mood_tracking_page():
    st.title("Mood Tracking")

    st.write("Use the slider to select your current mood.")

    # Get the username from the session state
    username = st.session_state["username"]

    mood_score = st.slider("Mood", 1, 10, 5)

    if st.button("Save Mood"):
        save_mood_entry(username, mood_score)
        st.success("Mood entry saved!")
        st.rerun()

    st.divider()

    st.header("Mood History")

    entries = load_mood_entries(username)
    if entries:
        df = pd.DataFrame(entries)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        
        fig = px.line(df, x="timestamp", y="mood", title="Mood Over Time")
        st.plotly_chart(fig)
    else:
        st.write("No mood entries yet.")

if 'authentication_status' in st.session_state and st.session_state["authentication_status"]:
    mood_tracking_page()
else:
    st.warning("Please login to access this page.")
