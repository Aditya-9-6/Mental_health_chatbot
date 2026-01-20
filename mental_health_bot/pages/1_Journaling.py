import streamlit as st
from journal import save_journal_entry, load_journal_entries

def journaling_page():
    st.title("My Journal")

    st.write("Use this space to write down your thoughts and feelings.")

    # Get the username from the session state
    username = st.session_state["username"]

    entry_text = st.text_area("New Journal Entry", height=200)

    if st.button("Save Entry"):
        if entry_text:
            save_journal_entry(username, entry_text)
            st.success("Journal entry saved!")
            # Clear the text area after saving
            st.rerun()
        else:
            st.warning("Please enter some text before saving.")

    st.divider()

    st.header("Past Entries")

    entries = load_journal_entries(username)
    if entries:
        # Sort entries by timestamp in descending order
        entries.sort(key=lambda x: x["timestamp"], reverse=True)
        for entry in entries:
            st.write(f"**{entry['timestamp']}**")
            st.write(entry["entry"])
            st.divider()
    else:
        st.write("No journal entries yet.")

if 'authentication_status' in st.session_state and st.session_state["authentication_status"]:
    journaling_page()
else:
    st.warning("Please login to access this page.")
