from src.core.file_tree import FileTree

class AppState:
    """
    Clase Singleton para mantener el estado global de la aplicación en memoria.
    Almacena el árbol de archivos y la plantilla del prompt.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppState, cls).__new__(cls)
            # Inicializamos el estado una sola vez
            cls._instance.file_tree = FileTree()
            cls._instance.prompt_template = ""
        return cls._instance
    
    def reset(self):
        """
        Reinicia el estado de la aplicación para generar un nuevo prompt.
        Esto es útil para el botón "Crear otro prompt".
        """
        self.file_tree = FileTree()
        self.prompt_template = ""