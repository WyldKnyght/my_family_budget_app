# src/services/system_info_service.py
import platform
import psutil
import torch
import json
import hashlib
import os
import wmi
from utils.custom_logging import logger
from configs.app_config import SYSTEM_SETTINGS_FILE, MODEL_PATH

class SystemInfoService:
    @staticmethod
    def get_system_info():
        total_ram = psutil.virtual_memory().total
        gpu_memory = []
        if torch.cuda.is_available():
            gpu_memory.extend(
                torch.cuda.get_device_properties(i).total_memory
                for i in range(torch.cuda.device_count())
            )
        settings = {
            "os": platform.system(),
            "os_version": platform.release(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(logical=False),
            "total_ram": total_ram / (1024 ** 3),  # in GB
            "cuda_available": torch.cuda.is_available(),
            "cuda_version": torch.version.cuda if torch.cuda.is_available() else None,
            "gpu_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
            "gpu_names": [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())] if torch.cuda.is_available() else [],
            "gpu_memory": [mem / (1024 ** 3) for mem in gpu_memory],  # in GB
            "default_device": "cuda" if torch.cuda.is_available() else "cpu",
            "model_path": os.path.normpath(MODEL_PATH),
        }

        try:
            c = wmi.WMI()
            intel_gpu = c.Win32_VideoController(AdapterCompatibility="Intel Corporation")[0]
            settings["intel_gpu"] = {
                "name": intel_gpu.Name,
                "memory": intel_gpu.AdapterRAM,
                "driver_version": intel_gpu.DriverVersion,
            }
        except IndexError:
            logger.info("No Intel GPU detected.")
            settings["intel_gpu"] = None
        except Exception as e:
            logger.error(f"Error detecting Intel GPU: {str(e)}")
            settings["intel_gpu"] = None

        if settings["cuda_available"] and settings["gpu_memory"]:
            settings["max_memory"] = min(settings["gpu_memory"]) * 0.9
        else:
            settings["max_memory"] = settings["total_ram"] * 0.8

        return settings

    @staticmethod
    def generate_system_hash(settings):
        system_string = f"{settings['os']}{settings['os_version']}{settings['python_version']}{settings['cpu_count']}{settings['total_ram']}{settings['cuda_available']}{settings['cuda_version']}{settings['gpu_count']}{','.join(settings['gpu_names'])}{','.join(map(str, settings['gpu_memory']))}"
        return hashlib.md5(system_string.encode()).hexdigest()

    @classmethod
    def save_system_info(cls, settings):
        settings['system_hash'] = cls.generate_system_hash(settings)
        os.makedirs(os.path.dirname(SYSTEM_SETTINGS_FILE), exist_ok=True)
        with open(SYSTEM_SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
        logger.info(f"System settings saved to {SYSTEM_SETTINGS_FILE}")

    @staticmethod
    def load_system_info():
        if os.path.exists(SYSTEM_SETTINGS_FILE):
            try:
                with open(SYSTEM_SETTINGS_FILE, 'r') as f:
                    if content := f.read().strip():
                        return json.loads(content)
                    else:
                        logger.warning(f"The file {SYSTEM_SETTINGS_FILE} is empty.")
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON from {SYSTEM_SETTINGS_FILE}: {e}")
            except Exception as e:
                logger.error(f"Unexpected error reading {SYSTEM_SETTINGS_FILE}: {e}")
        else:
            logger.warning(f"The file {SYSTEM_SETTINGS_FILE} does not exist.")
        return None

    @classmethod
    def update_system_info_if_needed(cls):
        current_settings = cls.get_system_info()
        current_hash = cls.generate_system_hash(current_settings)

        saved_settings = cls.load_system_info()

        if saved_settings is None:
            cls.save_system_info(current_settings)
            logger.info("System settings initialized and saved.")
            return current_settings
        elif saved_settings.get('system_hash') != current_hash:
            for key, value in current_settings.items():
                if key not in saved_settings:
                    saved_settings[key] = value
            saved_settings['system_hash'] = current_hash
            cls.save_system_info(saved_settings)
            logger.info("System settings updated and saved.")
            return saved_settings
        else:
            for key in current_settings:
                if key not in saved_settings:
                    saved_settings[key] = current_settings[key]
                    logger.info(f"Added missing key '{key}' to saved settings.")
            logger.info("Using saved system settings.")
            return saved_settings