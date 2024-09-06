# src/views/pdf_tab.py

import os
from PyQt6.QtWidgets import (QWidget, QPushButton, QMessageBox,
                             QVBoxLayout, QHBoxLayout, QLabel, QFileDialog,
                             QTableWidget, QTableWidgetItem, QHeaderView)
from controllers.pdf_manager import PDFManager
from configs.app_config import PDF_INPUT_DIRECTORY, TXT_OUTPUT_DIRECTORY
from configs.ui_config import NOT_PARSED, PARSED, PDF_TAB_COLUMNS
from utils.custom_logging import logger
from exceptions.pdf_exceptions import PDFParsingError

class PDFTab(QWidget):
    def __init__(self, model, tokenizer):
        super().__init__()
        self.model = model
        self.tokenizer = tokenizer
        self.pdf_manager = PDFManager()
        self.pdf_files = []
        self.parsed_data = {}
        self.init_ui()
        self.load_default_pdfs()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addLayout(self.create_pdf_selection_layout())
        layout.addWidget(self.create_file_table())
        self.setLayout(layout)
        logger.info("PDF tab UI initialized")

    def create_pdf_selection_layout(self):
        pdf_layout = QHBoxLayout()
        self.pdf_label = QLabel("No PDFs selected")
        pdf_button = QPushButton("Select PDFs")
        pdf_button.clicked.connect(self.select_pdfs)
        pdf_layout.addWidget(self.pdf_label)
        pdf_layout.addWidget(pdf_button)
        return pdf_layout

    def create_file_table(self):
        self.file_table = QTableWidget()
        self.file_table.setColumnCount(len(PDF_TAB_COLUMNS))
        self.file_table.setHorizontalHeaderLabels(PDF_TAB_COLUMNS)
        self.file_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        return self.file_table

    def load_default_pdfs(self):
        try:
            self.pdf_files = self.pdf_manager.get_pdf_files(PDF_INPUT_DIRECTORY)
            self.update_pdf_list_ui()
        except Exception as e:
            logger.error(f"Error loading default PDFs: {str(e)}")
            QMessageBox.warning(self, "Error", f"Failed to load default PDFs: {str(e)}")

    def update_pdf_list_ui(self):
        if self.pdf_files:
            self.pdf_label.setText(f"Found {len(self.pdf_files)} PDF(s)")
            self.check_parsed_status()
            self.update_file_table()
        else:
            self.pdf_label.setText("No PDF files found.")

    def check_parsed_status(self):
        try:
            self.parsed_data = self.pdf_manager.get_parsed_status(self.pdf_files, TXT_OUTPUT_DIRECTORY)
        except Exception as e:
            logger.error(f"Error checking parsed status: {str(e)}")
            QMessageBox.warning(self, "Error", f"Failed to check parsed status: {str(e)}")

    def update_file_table(self):
        self.file_table.setRowCount(len(self.pdf_files))
        for row, filename in enumerate(self.pdf_files):
            self.file_table.setItem(row, 0, QTableWidgetItem(filename))
            status = self.parsed_data.get(filename, NOT_PARSED)
            self.file_table.setItem(row, 1, QTableWidgetItem(status))
            
            parse_button = QPushButton("Parse" if status == NOT_PARSED else "Re-parse")
            parse_button.clicked.connect(lambda _, f=filename: self.parse_single_pdf(f))
            self.file_table.setCellWidget(row, 2, parse_button)

    def parse_single_pdf(self, filename):
        try:
            if not self.pdf_manager.parse_single_pdf(
                filename, PDF_INPUT_DIRECTORY, TXT_OUTPUT_DIRECTORY
            ):
                raise PDFParsingError(f"Failed to parse {filename}")
            self.parsed_data[filename] = PARSED
            self.update_file_table()
            logger.info(f"Successfully parsed {filename}")
            QMessageBox.information(self, "Success", f"Successfully parsed {filename}")
        except Exception as e:
            logger.error(f"Failed to parse {filename}: {str(e)}")
            QMessageBox.warning(self, "Error", f"Failed to parse {filename}: {str(e)}")

    def select_pdfs(self):
        try:
            files, _ = QFileDialog.getOpenFileNames(self, "Select PDF Files", PDF_INPUT_DIRECTORY, "PDF Files (*.pdf)")
            if files:
                self.pdf_files = [os.path.basename(f) for f in files]
                self.pdf_manager.process_pdfs(files)
                self.update_pdf_list_ui()
        except Exception as e:
            logger.error(f"Error selecting PDFs: {str(e)}")
            QMessageBox.warning(self, "Error", f"Failed to select PDFs: {str(e)}")