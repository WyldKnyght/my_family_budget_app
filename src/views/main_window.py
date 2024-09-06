from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel
from .pdf_tab import PDFTab
from .data_tab import DataTab
from .chat_tab import ChatTab
from utils.custom_logging import logger
from configs.app_config import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT

class MainWindow(QMainWindow):
    def __init__(self, model, tokenizer):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)

        self.model = model
        self.tokenizer = tokenizer
        
        self.init_ui()
        logger.info("Main window initialized")

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.tab_widget = QTabWidget()
        
        dashboard_tab = self.create_dashboard_tab()
        self.tab_widget.addTab(dashboard_tab, "Dashboard")

        self.pdf_tab = PDFTab(self.model, self.tokenizer)
        self.tab_widget.addTab(self.pdf_tab, "PDFs")

        self.chat_tab = ChatTab(self.model, self.tokenizer)
        self.tab_widget.addTab(self.chat_tab, "Chat")

        self.data_tab = DataTab(self)
        self.tab_widget.addTab(self.data_tab, "Data")

        layout.addWidget(self.tab_widget)
        central_widget.setLayout(layout)

        logger.info("UI components initialized")

    def create_dashboard_tab(self):
        dashboard_tab = QWidget()
        dashboard_layout = QVBoxLayout()
        dashboard_layout.addWidget(QLabel("Dashboard - To be implemented"))
        dashboard_tab.setLayout(dashboard_layout)
        logger.info("Dashboard tab created")
        return dashboard_tab