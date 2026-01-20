from database import save_journal_entry as db_save_journal_entry, load_journal_entries as db_load_journal_entries

def save_journal_entry(username, entry_text):
    """Saves a new journal entry to the database."""
    db_save_journal_entry(username, entry_text)

def load_journal_entries(username):
    """Loads all journal entries for a user from the database."""
    return db_load_journal_entries(username)
