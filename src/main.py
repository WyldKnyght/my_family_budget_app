# src/main.py

from utils.custom_logging import setup_logging, logger
from controllers.model_manager import ModelManager
from views.main_window import MainWindow
from PyQt6.QtWidgets import QApplication
import sys

def main():
    setup_logging()
    logger.info("Initializing application...")

    try:
        initialize_and_run_application()
    except Exception as e:
        logger.error(f"An error occurred during application initialization: {str(e)}")
        sys.exit(1)

def initialize_and_run_application():
    model_manager = ModelManager()
    model, tokenizer = model_manager.get_model_and_tokenizer()
    app = QApplication(sys.argv)
    main_window = MainWindow(model, tokenizer)
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()