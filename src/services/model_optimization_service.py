# src/services/model_optimization_service.py
import torch
from services.system_info_service import SystemInfoService
from services.model_info_service import ModelInfoService

class ModelOptimizationService:
    @staticmethod
    def get_optimal_model_settings():
        system_settings = SystemInfoService.load_system_info()
        model_settings = ModelInfoService.load_model_info()

        return {
            "model_name": model_settings["model_name"],
            "model_path": model_settings["model_path"],
            "device": "cuda" if system_settings["cuda_available"] else "cpu",
            "torch_dtype": torch.float16 if system_settings["cuda_available"] else torch.float32,
            "low_cpu_mem_usage": True,
            "device_map": "auto" if system_settings["cuda_available"] else None,
            "trust_remote_code": model_settings["trust_remote_code"],
            "max_memory": {0: f"{int(system_settings['max_memory'])}GB"} if system_settings["cuda_available"] else None,
            "load_in_8bit": model_settings["load_in_8bit"] if system_settings["cuda_available"] else False,
            "max_seq_len": model_settings["max_seq_len"],
            "max_batch_size": min(model_settings["max_batch_size"], system_settings["cpu_count"]),
        }