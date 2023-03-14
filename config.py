from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
HOUR = int(os.getenv('HOURS'))
MIN = int(os.getenv('MINS'))
CHANNEL_TO_POST = int(os.getenv('CHANNEL_ID'))
FEMALE_ROLE_ID = int(os.getenv('FEMALE_ROLE'))
PATH_TO_DB = os.getenv('PATH_TO_DB')
PATH_TO_TEMPLATES = os.getenv('PATH_TO_TEMPLATES')
