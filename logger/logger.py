import logging
import sys
import csv
import os
from datetime import datetime

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)

    # StreamHandler for console output
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(stream_handler)

    return logger

def log_user_action(action, from_user, action_details=None):
    app_language = from_user.language_code
    user_id = from_user.id
    username = from_user.username
    first_name = from_user.first_name
    last_name = from_user.last_name
    is_premium = getattr(from_user, 'is_premium', False)  # Check if user is a premium user
    file_exists = os.path.isfile('user_actions.csv')
    with open('user_actions.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'timestamp', 'user_id', 'username', 'first_name', 'last_name',
            'is_premium', 'app_language', 'action', 'action_details'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames) # type: ignore
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': user_id,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'is_premium': is_premium,
            'app_language': app_language,
            'action': action,
            'action_details': action_details
        })
