### Project Folder Structure

Below is a comprehensive summary of the folder structure for your project, along with descriptions of the purpose of each directory and file.

```
src/
├── __init__.py                  # Initialization file for the src package
├── main.py                       # Main entry point of the application
├── configs/                      # Configuration management
│   ├── __init__.py              # Initialization file for the configs package
│   └── app_config.py            # Centralized configuration management, including environment variables and constants
├── controllers/                  # High-level management of operations
│   ├── __init__.py              # Initialization file for the controllers package
│   ├── data_manager.py           # (Removed) Previously managed data operations; no longer needed
│   └── pdf_manager.py            # Manages PDF processing operations, coordinating between services
├── data_structures/              # Defines data structures used in the application
│   ├── __init__.py              # Initialization file for the data_structures package
│   └── pdf_info.py               # Defines the PDFInfo data structure for storing PDF-related information
├── services/                     # Handles specific functionalities related to PDF processing
│   ├── __init__.py              # Initialization file for the services package
│   ├── pdf_service.py           # Handles PDF loading and text extraction
│   ├── parsing_service.py        # Parses extracted text and manages PDF information
│   └── database_service.py       # (To be implemented) Manages database operations for storing PDF information
├── utils/                        # Contains utility functions and configurations
│   ├── __init__.py              # Initialization file for the utils package
│   ├── custom_logging.py         # Configures logging for the application
│   ├── file_manager.py           # General file operations, including saving and loading files
│   └── text_manager.py           # (Removed) Previously handled text processing; functionality moved to services
└── views/                        # Manages the UI components of the application
    ├── __init__.py              # Initialization file for the views package
    ├── main_window.py            # Main application window UI
    ├── chat_tab.py               # UI for the chat interface
    ├── data_tab.py               # UI for displaying parsed PDF information
    └── pdf_tab.py                # UI for managing PDF uploads and processing
```

### Key Points

- **configs/**: This directory contains configuration files that manage application settings and environment variables, allowing for easy customization and flexibility.

- **controllers/**: This directory contains high-level classes that manage the flow of operations in the application. The `pdf_manager.py` coordinates PDF processing tasks.

- **data_structures/**: This directory defines the data structures used in the application, specifically the `pdf_info.py` file that structures PDF-related information.

- **services/**: This directory contains service classes that encapsulate specific functionalities, such as loading PDFs, parsing text, and managing database operations.

- **utils/**: This directory includes utility functions that provide common functionalities, such as logging and file operations.

- **views/**: This directory manages the user interface components of the application, providing the necessary UI for interacting with the PDF processing features.
