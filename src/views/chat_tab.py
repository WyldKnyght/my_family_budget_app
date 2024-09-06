# src/views/chat_tab.py
from PyQt6.QtWidgets import QWidget, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import QThread, pyqtSignal
from utils.custom_logging import logger
from services.ai_service import AIService

class AIResponseThread(QThread):
    response_ready = pyqtSignal(str)

    def __init__(self, ai_service, user_message):
        super().__init__()
        self.ai_service = ai_service
        self.user_message = user_message

    def run(self):
        response = self.ai_service.generate_response(self.user_message)
        self.response_ready.emit(response)

class ChatTab(QWidget):
    def __init__(self, model, tokenizer):
        super().__init__()
        self.ai_service = AIService(model, tokenizer)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.create_chat_interface())
        self.setLayout(layout)
        logger.info("Chat tab UI initialized")

    def create_chat_interface(self):
        chat_widget = QWidget()
        chat_layout = QVBoxLayout()

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        chat_layout.addWidget(self.chat_history)

        input_layout = QHBoxLayout()
        self.user_input = QTextEdit()
        self.user_input.setFixedHeight(50)
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.user_input)
        input_layout.addWidget(send_button)
        chat_layout.addLayout(input_layout)

        chat_widget.setLayout(chat_layout)
        return chat_widget

    def send_message(self):
        if user_message := self.user_input.toPlainText().strip():
            self.chat_history.append(f"You: {user_message}")
            self.user_input.clear()

            self.ai_thread = AIResponseThread(self.ai_service, user_message)
            self.ai_thread.response_ready.connect(self.handle_ai_response)
            self.ai_thread.start()

    def handle_ai_response(self, response):
        self.chat_history.append(f"AI: {response}")
        logger.info("AI response received and displayed")

