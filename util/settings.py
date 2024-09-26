import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    USERS = os.getenv('USERS').split(',')
    USERNAMES = os.getenv('USERNAMES').split(',')
    ADMINS = os.getenv('ADMINS').split(',')
    MESSAGES = os.getenv('MESSAGES').split('|')
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')