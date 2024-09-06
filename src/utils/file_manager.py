# src/utils/file_manager.py
import os
from configs.app_config import get_env_path, TXT_OUTPUT_DIRECTORY
from src.utils.custom_logging import logger

def save_text_file(content, filename, directory=None):
    if directory is None:
        directory = get_env_path(TXT_OUTPUT_DIRECTORY)
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def save_parsed_data(parsed_data, output_directory=None):
    if output_directory is None:
        output_directory = get_env_path(TXT_OUTPUT_DIRECTORY)
    os.makedirs(output_directory, exist_ok=True)
    for filename, content in parsed_data.items():
        output_filename = f"{os.path.splitext(filename)[0]}.txt"
        output_path = os.path.join(output_directory, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Saved parsed content to: {output_path}")