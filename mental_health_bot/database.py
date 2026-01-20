import sqlite3
from logging_config import get_logger

logger = get_logger(__name__)
DB_FILE = "mental_health.db"

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
    return conn

def create_tables():
    """Create the tables in the database."""
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS journal_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    entry TEXT NOT NULL
                );
            """)
            c.execute("""
                CREATE TABLE IF NOT EXISTS mood_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    mood INTEGER NOT NULL
                );
            """)
            c.execute("""
                CREATE TABLE IF NOT EXISTS goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    goal TEXT NOT NULL,
                    completed INTEGER NOT NULL
                );
            """)
            logger.info("Tables created successfully.")
        except sqlite3.Error as e:
            logger.error(f"Error creating tables: {e}")
        finally:
            conn.close()

def save_journal_entry(username, entry_text):
    """Saves a new journal entry to the database."""
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("INSERT INTO journal_entries (username, timestamp, entry) VALUES (?, ?, ?)",
                      (username, sqlite3.datetime.datetime.now().isoformat(), entry_text))
            conn.commit()
            logger.info(f"Journal entry saved for user '{username}'.")
        except sqlite3.Error as e:
            logger.error(f"Error saving journal entry for user '{username}': {e}")
        finally:
            conn.close()

def load_journal_entries(username):
    """Loads all journal entries for a user from the database."""
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT timestamp, entry FROM journal_entries WHERE username = ?", (username,))
            logger.info(f"Journal entries loaded for user '{username}'.")
            return [{"timestamp": row[0], "entry": row[1]} for row in c.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Error loading journal entries for user '{username}': {e}")
        finally:
            conn.close()
    return []

def save_mood_entry(username, mood_score):
    """Saves a new mood entry to the database."""
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("INSERT INTO mood_entries (username, timestamp, mood) VALUES (?, ?, ?)",
                      (username, sqlite3.datetime.datetime.now().isoformat(), mood_score))
            conn.commit()
            logger.info(f"Mood entry saved for user '{username}'.")
        except sqlite3.Error as e:
            logger.error(f"Error saving mood entry for user '{username}': {e}")
        finally:
            conn.close()

def load_mood_entries(username):
    """Loads all mood entries for a user from the database."""
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT timestamp, mood FROM mood_entries WHERE username = ?", (username,))
            logger.info(f"Mood entries loaded for user '{username}'.")
            return [{"timestamp": row[0], "mood": row[1]} for row in c.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Error loading mood entries for user '{username}': {e}")
        finally:
            conn.close()
    return []

def save_goal(username, goal_text):
    """Saves a new goal to the database."""
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("INSERT INTO goals (username, goal, completed) VALUES (?, ?, ?)", (username, goal_text, 0))
            conn.commit()
            logger.info(f"Goal saved for user '{username}'.")
        except sqlite3.Error as e:
            logger.error(f"Error saving goal for user '{username}': {e}")
        finally:
            conn.close()

def load_goals(username):
    """Loads all goals for a user from the database."""
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT goal, completed FROM goals WHERE username = ?", (username,))
            logger.info(f"Goals loaded for user '{username}'.")
            return [{"goal": row[0], "completed": bool(row[1])} for row in c.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Error loading goals for user '{username}': {e}")
        finally:
            conn.close()
    return []

def update_goal_status(username, goal_text, completed):
    """Updates the status of a goal for a user."""
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("UPDATE goals SET completed = ? WHERE username = ? AND goal = ?", (1 if completed else 0, username, goal_text))
            conn.commit()
            logger.info(f"Goal status updated for user '{username}'.")
        except sqlite3.Error as e:
            logger.error(f"Error updating goal status for user '{username}': {e}")
        finally:
            conn.close()
