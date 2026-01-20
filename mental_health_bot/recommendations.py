import os
from langchain_google_genai import ChatGoogleGenerativeAI
from journal import load_journal_entries
from mood import load_mood_entries
from logging_config import get_logger

logger = get_logger(__name__)

def generate_recommendations():
    """Generates personalized recommendations based on mood and journal entries."""
    
    logger.info("Generating recommendations...")
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.error("No API key found.")
        return "No API key found. Please set the GOOGLE_API_KEY environment variable."
        
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
    
    journal_entries = load_journal_entries(st.session_state["username"])
    mood_entries = load_mood_entries(st.session_state["username"])
    
    if not journal_entries and not mood_entries:
        logger.warning("Not enough data to generate recommendations.")
        return "Not enough data to generate recommendations. Please add journal and mood entries."
        
    prompt = "Based on the following journal and mood entries, please provide some personalized recommendations for improving mental well-being:\n\n"
    
    if journal_entries:
        prompt += "Journal Entries:\n"
        for entry in journal_entries:
            prompt += f"- {entry['entry']}\n"
            
    if mood_entries:
        prompt += "\nMood Entries:\n"
        for entry in mood_entries:
            prompt += f"- Mood: {entry['mood']}/10 on {entry['timestamp']}\n"
            
    try:
        response = llm.invoke(prompt)
        logger.info("Recommendations generated successfully.")
        return response.content
    except Exception as e:
        logger.error(f"An error occurred while generating recommendations: {e}")
        return f"An error occurred while generating recommendations: {e}"