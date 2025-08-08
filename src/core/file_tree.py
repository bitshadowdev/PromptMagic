import os
from typing import Optional, List

class FileNode:
    def __init__(self, name: str, path: str, is_directory: bool, size: int = 0, extension: str = "", emoji: str = ""):
        self.name = name
        self.path = path
        self.is_directory = is_directory
        self.size = size
        self.extension = extension
        self.emoji = emoji
        self.is_selected = False
        self.content: Optional[str] = None
        self.children: List[FileNode] = []

    def load_content(self):
        if not self.is_directory and self.content is None:
            try:
                with open(self.path, 'r', encoding='utf-8', errors='ignore') as f:
                    self.content = f.read()
            except Exception as e:
                self.content = f"Error reading file: {e}"

    def to_markdown(self) -> str:
        if self.is_directory:
            return "" # Los directorios no aportan contenido
        
        # Asegurarse de que el contenido está cargado
        if self.content is None:
            self.load_content()
            
        return f'**`{self.path}`**\n\n```{self.extension.lstrip(".")}\n{self.content}\n```'

class FileTree:
    def __init__(self):
        self.root: Optional[FileNode] = None
        self.nodes_by_path = {} # Para acceder rápidamente a los nodos por su ruta

    def add_node(self, name: str, path: str, is_directory: bool, parent_path: Optional[str] = None, size: int = 0, extension: str = "", emoji: str = "") -> FileNode:
        node = FileNode(name, path, is_directory, size, extension, emoji)
        self.nodes_by_path[path] = node

        if parent_path is None:
            # Aunque no tenemos una raíz única, este método maneja la estructura
            pass
        else:
            parent_node = self.nodes_by_path.get(parent_path)
            if parent_node:
                parent_node.children.append(node)
        return node

    def get_selected_files(self) -> List[FileNode]:
        """Recorre el árbol y devuelve una lista de todos los archivos seleccionados."""
        selected_files = []
        for node in self.nodes_by_path.values():
            if node.is_selected and not node.is_directory:
                selected_files.append(node)
        return selected_files

    def get_node_by_path(self, path: str) -> Optional[FileNode]:
        return self.nodes_by_path.get(path)

    def get_selected_files_markdown(self) -> str:
        """
        Devuelve un string con el contenido en formato markdown de todos los archivos seleccionados.
        """
        selected_files = self.get_selected_files()
        markdown_parts = [file_node.to_markdown() for file_node in selected_files]
        return "\n\n".join(markdown_parts)