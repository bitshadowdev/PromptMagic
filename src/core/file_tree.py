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
                with open(self.path, 'r', encoding='utf-8') as f:
                    self.content = f.read()
            except Exception as e:
                self.content = f"Error reading file: {e}"

    def to_markdown(self) -> str:
        if self.is_directory:
            return f"***/{self.path}*** (Directory)"
        else:
            print("Llamaddo")
            if self.content is None:
                self.load_content() # Load content if not already loaded
            return f'***/{self.path}***\n\n```{self.extension}\n{self.content}\n```'

class FileTree:
    def __init__(self):
        self.root: Optional[FileNode] = None
        self.nodes_by_path = {} # To quickly access nodes by their path

    def add_node(self, name: str, path: str, is_directory: bool, parent_path: Optional[str] = None, size: int = 0, extension: str = "", emoji: str = "") -> FileNode:
        node = FileNode(name, path, is_directory, size, extension, emoji)
        self.nodes_by_path[path] = node

        if parent_path is None:
            self.root = node
        else:
            parent_node = self.nodes_by_path.get(parent_path)
            if parent_node:
                parent_node.children.append(node)
        return node

    def get_selected_files(self) -> List[FileNode]:
        selected_files = []
        def _traverse(node: FileNode):
            if node.is_selected and not node.is_directory:
                selected_files.append(node)
            for child in node.children:
                _traverse(child)
        if self.root:
            _traverse(self.root)
        return selected_files

    def get_node_by_path(self, path: str) -> Optional[FileNode]:
        return self.nodes_by_path.get(path)

    def get_selected_files_markdown(self) -> str:
        """
        Returns a string containing markdown of all selected files, separated by double newlines.
        """
        selected_files = self.get_selected_files()
        markdown_parts = [file_node.to_markdown() for file_node in selected_files]
        return "\n\n".join(markdown_parts)
