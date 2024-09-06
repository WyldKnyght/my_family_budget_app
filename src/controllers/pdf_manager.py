# src/controllers/pdf_manager.py
import os
from services.pdf_service import PDFService
from utils.custom_logging import logger

class PDFManager:
    def __init__(self):
        self.pdf_service = PDFService()

    def get_pdf_files(self, directory):
        return self.pdf_service.get_pdf_files(directory)

    def get_parsed_status(self, pdf_files, output_directory):
        return self.pdf_service.get_parsed_status(pdf_files, output_directory)

    def parse_single_pdf(self, filename, input_directory):
        try:
            pdf_path = os.path.join(input_directory, filename)
            self.pdf_service.process_pdf(pdf_path)
            return True
        except Exception as e:
            logger.error(f"Error parsing {filename}: {str(e)}")
            return False

    def process_pdfs(self, files):
        self.pdf_service.process_pdfs(files)