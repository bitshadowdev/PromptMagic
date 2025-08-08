# src/core/language_manager.py

from src.config.strings import STRINGS

class LanguageManager:
    """
    Clase Singleton para gestionar los textos de la interfaz.
    """
    _instance = None
    
    def __new__(cls, language="es"):
        if cls._instance is None:
            cls._instance = super(LanguageManager, cls).__new__(cls)
            cls._instance.load_language(language)
        return cls._instance
        
    def load_language(self, language: str):
        """Carga el diccionario de textos para el idioma especificado."""
        self.lang_map = STRINGS.get(language, STRINGS["es"]) # Carga 'es' por defecto
        
    def get_string(self, key: str) -> str:
        """Obtiene un texto por su clave."""
        return self.lang_map.get(key, f"_{key}_") # Devuelve la clave si no se encuentra
