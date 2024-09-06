# src/services/model_info_service.py
import os
import torch
import json
import hashlib
from utils.custom_logging import logger
from configs.app_config import MODEL_SETTINGS_FILE, MODEL_PATH

class ModelInfoService:
    @staticmethod
    def get_model_info():
        return {
            "model_name": "Meta-Llama-3.1-8B",
            "model_path": MODEL_PATH,
            "model_type": "llama",
            "tokenizer_path": MODEL_PATH,
            "max_seq_len": 2048,
            "max_batch_size": 32,
            "device": "cuda" if torch.cuda.is_available() else "cpu",
            "load_in_8bit": False,
            "trust_remote_code": False,
            "use_auth_token": False,
        }

    @staticmethod
    def generate_model_hash(settings):
        model_string = f"{settings['model_name']}{settings['model_path']}{settings['model_type']}{settings['max_seq_len']}{settings['max_batch_size']}{settings['device']}{settings['load_in_8bit']}{settings['trust_remote_code']}{settings['use_auth_token']}"
        return hashlib.md5(model_string.encode()).hexdigest()

    @classmethod
    def save_model_info(cls, settings):
        settings['model_hash'] = cls.generate_model_hash(settings)
        os.makedirs(os.path.dirname(MODEL_SETTINGS_FILE), exist_ok=True)
        with open(MODEL_SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
        logger.info(f"Model settings saved to {MODEL_SETTINGS_FILE}")

    @staticmethod
    def load_model_info():
        if os.path.exists(MODEL_SETTINGS_FILE):
            try:
                with open(MODEL_SETTINGS_FILE, 'r') as f:
                    if content := f.read().strip():
                        return json.loads(content)
                    else:
                        logger.warning(f"The file {MODEL_SETTINGS_FILE} is empty.")
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON from {MODEL_SETTINGS_FILE}: {e}")
            except Exception as e:
                logger.error(f"Unexpected error reading {MODEL_SETTINGS_FILE}: {e}")
        else:
            logger.warning(f"The file {MODEL_SETTINGS_FILE} does not exist.")
        return None

    @classmethod
    def update_model_info_if_needed(cls):
        current_settings = cls.get_model_info()
        current_hash = cls.generate_model_hash(current_settings)

        saved_settings = cls.load_model_info()

        if saved_settings is None:
            cls.save_model_info(current_settings)
            logger.info("Model settings initialized and saved.")
            return current_settings
        elif saved_settings.get('model_hash') != current_hash:
            for key, value in current_settings.items():
                if key not in saved_settings:
                    saved_settings[key] = value
            saved_settings['model_hash'] = current_hash
            cls.save_model_info(saved_settings)
            logger.info("Model settings updated and saved.")
            return saved_settings
        else:
            for key in current_settings:
                if key not in saved_settings:
                    saved_settings[key] = current_settings[key]
                    logger.info(f"Added missing key '{key}' to saved model settings.")
            logger.info("Using saved model settings.")
            return saved_settings