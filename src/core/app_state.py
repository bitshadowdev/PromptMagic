from src.core.file_tree import FileTree
from src.core.temp_storage import TempStorage

class AppState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppState, cls).__new__(cls)
            cls._instance.file_tree = FileTree()
            cls._instance.prompt_template = ""
            cls._instance.temp_storage = TempStorage()
            cls._instance._initialized = True
        return cls._instance
    
    def save_selected_content(self):
        """Save selected files to temporary storage and return markdown content"""
        return self.temp_storage.save_selected_files(self.file_tree)
    
    def load_markdown_content(self) -> str:
        """Load markdown content from temporary storage"""
        return self.temp_storage.load_markdown_content()
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        if hasattr(self, 'temp_storage'):
            self.temp_storage.cleanup()
            # Create new temp storage for next use
            self.temp_storage = TempStorage()
    
    def reset(self):
        """Reset the app state (useful for creating new prompt)"""
        self.cleanup_temp_files()
        self.file_tree = FileTree()
        self.prompt_template = ""