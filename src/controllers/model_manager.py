# src/controllers/model_manager.py
from services.system_info_service import SystemInfoService
from services.model_info_service import ModelInfoService
from services.model_optimization_service import ModelOptimizationService
from services.model_loader_service import ModelLoaderService
from utils.custom_logging import logger

class ModelManager:
    def __init__(self):
        self.system_info_service = SystemInfoService()
        self.model_info_service = ModelInfoService()
        self.model_optimization_service = ModelOptimizationService()
        self.model_loader_service = ModelLoaderService()
        self.model = None
        self.tokenizer = None

    def initialize(self):
        logger.info("Initializing ModelManager...")
        self._update_system_and_model_info()
        self._load_model()
        logger.info("ModelManager initialization complete.")

    def _update_system_and_model_info(self):
        logger.info("Updating system and model information...")
        self.system_info_service.update_system_info_if_needed()
        self.model_info_service.update_model_info_if_needed()

    def _load_model(self):
        logger.info("Loading model...")
        optimal_settings = self.model_optimization_service.get_optimal_model_settings()
        self.tokenizer, self.model = self.model_loader_service.load_model(optimal_settings)

    def get_model_and_tokenizer(self):
        if self.model is None or self.tokenizer is None:
            self.initialize()
        return self.model, self.tokenizer