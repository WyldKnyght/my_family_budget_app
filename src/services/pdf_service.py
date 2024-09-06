# src/services/pdf_service.py
import os
import re
import PyPDF2
import json
from PyPDF2 import PdfReader
from utils.custom_logging import logger
from configs.app_config import (
    get_env_path, TXT_OUTPUT_DIRECTORY, BRANCH_ADDRESS_PATTERN,
    OUR_ADDRESS_PATTERN, STATEMENT_PERIOD_PATTERN, ACCOUNT_SUMMARY_PATTERN
)
from data_structures.pdf_info import PDFInfo

class PDFService:
    def __init__(self):
        self.reader = None
        self.pdf_path = None

    def load_pdf(self, pdf_path):
        """Load the PDF file."""
        self.pdf_path = pdf_path
        try:
            self.reader = PdfReader(self.pdf_path)
            logger.info(f"Successfully loaded PDF: {self.pdf_path}")
        except Exception as e:
            logger.error(f"Error loading PDF {self.pdf_path}: {str(e)}")
            raise

    def get_pdf_files(self, directory_path):
        """Get all PDF files in the given directory."""
        return [f for f in os.listdir(directory_path) if f.lower().endswith('.pdf')]

    def save_processed_files(self, processed_files, processed_files_path):
        """Save the list of processed files."""
        with open(processed_files_path, 'w') as f:
            json.dump(processed_files, f, indent=4)

    def load_processed_files(self, processed_files_path):
        """Load the list of processed files."""
        if os.path.exists(processed_files_path):
            with open(processed_files_path, 'r') as f:
                return json.load(f)
        return {}

    def process_pdf(self, pdf_path):
        self.load_pdf(pdf_path)
        parsed_info = self.parse_pdf_content(pdf_path)  # Changed from text to pdf_path
        self.save_pdf_info(parsed_info)
        
        # Save the parsed text to a file
        filename = os.path.basename(pdf_path)
        txt_filename = f"{os.path.splitext(filename)[0]}.txt"
        txt_path = os.path.join(TXT_OUTPUT_DIRECTORY, txt_filename)
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(str(parsed_info))

    def parse_pdf_directory(self, directory):
        parsed_data = {}
        for filename in os.listdir(directory):
            if filename.endswith(".pdf"):
                file_path = os.path.join(directory, filename)
                pdf_info = self.parse_pdf_content(file_path)
                pdf_info["filename"] = filename
                self.insert_pdf_info(pdf_info)
                parsed_data[filename] = pdf_info
        return parsed_data

    def parse_pdf_content(self, pdf_path):
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = "".join(page.extract_text() for page in reader.pages)
        
        # Extract information
        branch_address = self.extract_info(text, BRANCH_ADDRESS_PATTERN)
        our_address = self.extract_info(text, OUR_ADDRESS_PATTERN)
        statement_period = self.extract_info(text, STATEMENT_PERIOD_PATTERN)
        account_summary = self.extract_info(text, ACCOUNT_SUMMARY_PATTERN, re.DOTALL)

        return PDFInfo(
            filename=os.path.basename(pdf_path),
            branch_address=branch_address,
            our_address=our_address,
            statement_period=statement_period,
            account_summary=account_summary,
            additional_info=text
        )

    @staticmethod
    def extract_info(text, pattern, flags=0):
        match = re.search(pattern, text, flags)
        return match[1].strip() if match else None

    def save_parsed_data(self, parsed_data, output_directory=None):
        if output_directory is None:
            output_directory = get_env_path(TXT_OUTPUT_DIRECTORY)

        os.makedirs(output_directory, exist_ok=True)

        for filename, content in parsed_data.items():
            output_filename = f"{os.path.splitext(filename)[0]}.txt"
            output_path = os.path.join(output_directory, output_filename)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(str(content))  # Convert dict to string for writing

            logger.info(f"Saved parsed content to: {output_path}")

    def extract_text(self):
        """Extract text from all pages of the PDF."""
        if not self.reader:
            self.load_pdf(self.pdf_path)

        text = "".join(page.extract_text() + "\n" for page in self.reader.pages)
        logger.info(f"Successfully extracted text from PDF: {self.pdf_path}")
        return text

    def extract_text_from_page(self, page_num):
        """Extract text from a specific page of the PDF."""
        if not self.reader:
            self.load_pdf(self.pdf_path)

        if page_num < 0 or page_num >= len(self.reader.pages):
            logger.error(f"Invalid page number {page_num} for PDF {self.pdf_path}")
            return ""

        text = self.reader.pages[page_num].extract_text()
        logger.info(f"Successfully extracted text from page {page_num} of PDF: {self.pdf_path}")
        return text

    def get_parsed_status(self, pdf_files, output_directory):
        parsed_status = {}
        for filename in pdf_files:
            txt_filename = f"{os.path.splitext(filename)[0]}.txt"
            txt_path = os.path.join(output_directory, txt_filename)
            parsed_status[filename] = "Parsed" if os.path.exists(txt_path) else "Not Parsed"
        return parsed_status

    def process_pdfs(self, pdf_files):
        for pdf_file in pdf_files:
            self.process_pdf(pdf_file)