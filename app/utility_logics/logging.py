from datetime import datetime
from database.db import db  # Import the database instance

def log_utility_usage(user_id: str, utility_name: str, parameters: dict):
    """
    Logs the usage of a utility in the database.

    Args:
        user_id (str): ID of the user who executed the utility.
        utility_name (str): Name of the utility executed.
        parameters (dict): Parameters passed to the utility.
    """
    log_entry = {
        "user_id": user_id,
        "utility_name": utility_name,
        "parameters": parameters,
        "timestamp": datetime.utcnow(),
    }
    db["utility_logs"].insert_one(log_entry)  # Use the imported `db` instance
