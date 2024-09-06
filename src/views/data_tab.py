# src/views/data_tab.py
import sqlite3
from PyQt6.QtWidgets import (QWidget, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                             QListWidget, QSplitter, QMessageBox)
from PyQt6.QtCore import Qt
from utils.custom_logging import logger
from configs.app_config import DATABASE_PATH

class DataTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
        self.init_database()

    def init_ui(self):
        layout = QHBoxLayout()
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.create_file_list())
        splitter.addWidget(self.create_content_explanation_widget())
        layout.addWidget(splitter)
        self.setLayout(layout)

    def init_database(self):
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS explanations
                (filename TEXT PRIMARY KEY, explanation TEXT)
            ''')
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
            QMessageBox.warning(self, "Error", f"Failed to initialize database: {e}")

    def save_explanation(self):
        if not (current_file := self.file_list.currentItem()):
            return
        filename = current_file.text()
        explanation = self.explanation_input.toPlainText()

        try:
            self.save_explanation_to_database(filename, explanation)
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            QMessageBox.warning(self, "Error", f"Failed to save explanation: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            QMessageBox.warning(self, "Error", f"An unexpected error occurred: {e}")

    def save_explanation_to_database(self, filename, explanation):
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO explanations (filename, explanation)
            VALUES (?, ?)
        ''', (filename, explanation))

        conn.commit()
        conn.close()

        logger.info(f"Saved explanation for {filename}")
        QMessageBox.information(self, "Success", f"Explanation saved for {filename}")
        self.main_window.pdf_tab.chat_history.append(f"System: Explanation saved for {filename}")

    def display_file_content(self, item):
        filename = item.text()
        self.file_content.setText(self.main_window.pdf_tab.parsed_data.get(filename, ""))

        try:
            self.load_explanation_from_database(filename)
        except sqlite3.Error as e:
            logger.error(f"Database error when loading explanation: {e}")
            self.explanation_input.clear()

    def load_explanation_from_database(self, filename):
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT explanation FROM explanations WHERE filename = ?', (filename,))
        result = cursor.fetchone()
        conn.close()

        if result:
            self.explanation_input.setText(result[0])
        else:
            self.explanation_input.clear()

    def create_file_list(self):
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.display_file_content)
        return self.file_list

    def create_content_explanation_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.file_content = QTextEdit()
        self.file_content.setReadOnly(True)
        self.explanation_input = QTextEdit()
        self.explanation_input.setPlaceholderText("Enter explanation here...")
        save_explanation_button = QPushButton("Save Explanation")
        save_explanation_button.clicked.connect(self.save_explanation)

        layout.addWidget(QLabel("File Content:"))
        layout.addWidget(self.file_content)
        layout.addWidget(QLabel("Explanation:"))
        layout.addWidget(self.explanation_input)
        layout.addWidget(save_explanation_button)

        widget.setLayout(layout)
        return widget

    def update_file_list(self, filenames):
        self.file_list.clear()
        self.file_list.addItems(filenames)