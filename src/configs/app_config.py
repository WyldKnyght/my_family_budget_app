# src/configs/app_config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_env_path(env_var):
    if path := os.getenv(env_var):
        return os.path.abspath(path)
    else:
        raise ValueError(f"{env_var} not set in .env file")

# Model variables
MODEL_DIR= get_env_path('MODEL_DIR')
MODEL_SETTINGS_FILE= get_env_path('MODEL_SETTINGS_FILE')
MODEL_PATH = get_env_path('MODEL_PATH')

# System variables
SYSTEM_SETTINGS_FILE = get_env_path('SYSTEM_SETTINGS_FILE')

# Input/Output variables
PDF_INPUT_DIRECTORY = get_env_path('PDF_INPUT_DIRECTORY')
TXT_OUTPUT_DIRECTORY = get_env_path('TXT_OUTPUT_DIRECTORY')

# Database variables
DATABASE_DIR = get_env_path('DATABASE_DIR')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_PATH = os.path.join(DATABASE_DIR, DATABASE_NAME)

# Parsing patterns
BRANCH_ADDRESS_PATTERN = r"Branch Address:\s*(.*)"
OUR_ADDRESS_PATTERN = r"Our Address:\s*(.*)"
STATEMENT_PERIOD_PATTERN = r"Statement Period:\s*(.*)"
ACCOUNT_SUMMARY_PATTERN = r"Account Summary:(.*?)(?=\n\n)"

# Default values
DEFAULT_NEED_MORE_DETAILS = "Need more details"

# UI settings
WINDOW_TITLE = "Family Budget Assistant"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800