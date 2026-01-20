import streamlit as st
from recommendations import generate_recommendations

def recommendations_page():
    st.title("Personalized Recommendations")

    st.write("Here are some personalized recommendations based on your journal and mood entries.")

    if st.button("Generate Recommendations"):
        with st.spinner("Generating recommendations..."):
            recommendations = generate_recommendations()
            st.markdown(recommendations)

if __name__ == "__main__":
    recommendations_page()
