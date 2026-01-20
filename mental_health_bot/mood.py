from database import save_mood_entry as db_save_mood_entry, load_mood_entries as db_load_mood_entries

def save_mood_entry(username, mood_score):
    """Saves a new mood entry to the database."""
    db_save_mood_entry(username, mood_score)

def load_mood_entries(username):
    """Loads all mood entries for a user from the database."""
    return db_load_mood_entries(username)
