# src/configs/model_config.py

import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv('MODEL_NAME', 'Meta-Llama-3.1-8B')
MODEL_PATH = os.path.abspath(os.getenv('MODEL_PATH', 'models/Meta-Llama-3.1-8B'))
MODEL_TYPE = os.getenv('MODEL_TYPE', 'llama')
MAX_SEQ_LEN = int(os.getenv('MAX_SEQ_LEN', 2048))
MAX_BATCH_SIZE = int(os.getenv('MAX_BATCH_SIZE', 32))
TRUST_REMOTE_CODE = os.getenv('TRUST_REMOTE_CODE', 'False').lower() == 'true'
LOAD_IN_8BIT = os.getenv('LOAD_IN_8BIT', 'False').lower() == 'true'
USE_AUTH_TOKEN = os.getenv('USE_AUTH_TOKEN', 'False').lower() == 'true'

MODEL_SETTINGS_FILE = os.path.abspath(os.getenv('MODEL_SETTINGS_FILE', 'src/configs/model_settings.json'))

# Text Generation
MAX_INPUT_LENGTH = int(os.getenv('MAX_INPUT_LENGTH', 512))
MAX_OUTPUT_LENGTH = int(os.getenv('MAX_OUTPUT_LENGTH', 200))
AI_TEMPERATURE = float(os.getenv('AI_TEMPERATURE', 0.7))

