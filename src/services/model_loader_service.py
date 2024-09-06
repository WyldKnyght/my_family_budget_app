# src/services/model_loader_service.py
import accelerate
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
from utils.custom_logging import logger

_ = accelerate.__version__  # Dummy line to satisfy linter

class ModelLoaderService:
    @staticmethod
    def load_model(settings):
        logger.info(f"Loading model on {settings['device']}")

        tokenizer = AutoTokenizer.from_pretrained(settings["model_path"])
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        config = AutoConfig.from_pretrained(
            settings["model_path"],
            trust_remote_code=settings["trust_remote_code"]
        )
        config.pad_token_id = tokenizer.pad_token_id

        model = AutoModelForCausalLM.from_pretrained(
            settings["model_path"],
            config=config,
            torch_dtype=settings["torch_dtype"],
            low_cpu_mem_usage=settings["low_cpu_mem_usage"],
            device_map=settings["device_map"],
            trust_remote_code=settings["trust_remote_code"],
            max_memory=settings["max_memory"],
            load_in_8bit=settings["load_in_8bit"],
        )

        model.to(settings["device"])
        logger.info("Model loaded successfully!")

        return tokenizer, model