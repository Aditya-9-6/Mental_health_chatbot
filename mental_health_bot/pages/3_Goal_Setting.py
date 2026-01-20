import streamlit as st
from goals import save_goal, load_goals, update_goal_status

def goal_setting_page():
    st.title("Goal Setting")

    st.write("Use this page to set and track your mental health goals.")

    # Get the username from the session state
    username = st.session_state["username"]

    goal_text = st.text_input("New Goal")

    if st.button("Save Goal"):
        if goal_text:
            save_goal(username, goal_text)
            st.success("Goal saved!")
            st.rerun()
        else:
            st.warning("Please enter a goal before saving.")

    st.divider()

    st.header("My Goals")

    goals = load_goals(username)
    if goals:
        for i, goal in enumerate(goals):
            checkbox_state = st.checkbox(goal["goal"], value=goal["completed"], key=f"goal_{i}")
            if checkbox_state != goal["completed"]:
                update_goal_status(username, goal["goal"], checkbox_state)
                st.rerun()
    else:
        st.write("No goals set yet.")

if 'authentication_status' in st.session_state and st.session_state["authentication_status"]:
    goal_setting_page()
else:
    st.warning("Please login to access this page.")
