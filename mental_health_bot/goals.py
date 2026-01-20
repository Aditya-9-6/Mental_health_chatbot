from database import save_goal as db_save_goal, load_goals as db_load_goals, update_goal_status as db_update_goal_status

def save_goal(username, goal_text):
    """Saves a new goal to the database."""
    db_save_goal(username, goal_text)

def load_goals(username):
    """Loads all goals for a user from the database."""
    return db_load_goals(username)

def update_goal_status(username, goal_text, completed):
    """Updates the status of a goal for a user."""
    db_update_goal_status(username, goal_text, completed)
