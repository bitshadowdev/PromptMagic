from src.core.file_tree import FileTree

class AppState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppState, cls).__new__(cls)
            cls._instance.file_tree = FileTree()
            cls._instance.prompt_template = ""
        return cls._instance
