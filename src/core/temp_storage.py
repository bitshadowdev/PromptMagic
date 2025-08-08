import os
import tempfile
import json
from typing import List
from src.core.file_tree import FileNode

class TempStorage:
    """Maneja el almacenamiento temporal de las rutas de los archivos seleccionados."""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="prompt_magic_")
        self.paths_file = os.path.join(self.temp_dir, "selected_paths.json")
        print(f"DEBUG: Directorio temporal creado en: {self.temp_dir}")
        
    def save_selected_paths(self, file_nodes: List[FileNode]):
        """Guarda las rutas de los nodos de archivo seleccionados en un archivo JSON."""
        paths = [node.path for node in file_nodes]
        print(f"DEBUG: Guardando {len(paths)} rutas en {self.paths_file}")
        with open(self.paths_file, 'w', encoding='utf-8') as f:
            json.dump(paths, f)
            
    def load_selected_paths(self) -> List[str]:
        """Carga las rutas de los archivos desde el archivo JSON temporal."""
        try:
            with open(self.paths_file, 'r', encoding='utf-8') as f:
                paths = json.load(f)
                print(f"DEBUG: Cargando {len(paths)} rutas desde {self.paths_file}")
                return paths
        except FileNotFoundError:
            print("DEBUG: No se encontró el archivo de rutas temporales.")
            return []
        except Exception as e:
            print(f"DEBUG: Error al cargar las rutas temporales: {e}")
            return []
            
    def cleanup(self):
        """Limpia los archivos y el directorio temporal."""
        try:
            if os.path.exists(self.paths_file):
                os.remove(self.paths_file)
            os.rmdir(self.temp_dir)
            print(f"DEBUG: Directorio temporal {self.temp_dir} limpiado.")
        except Exception as e:
            print(f"DEBUG: Error al limpiar los archivos temporales: {e}")