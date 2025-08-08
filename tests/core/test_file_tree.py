
import unittest
from unittest.mock import MagicMock
from src.core.file_tree import FileNode, FileTree

class TestFileTree(unittest.TestCase):

    def test_file_node_creation(self):
        node = FileNode("test.txt", "/path/to/test.txt", 100, ".txt", "📄")
        self.assertEqual(node.name, "test.txt")
        self.assertEqual(node.path, "/path/to/test.txt")
        self.assertEqual(node.size, 100)
        self.assertEqual(node.extension, ".txt")
        self.assertEqual(node.emoji, "📄")

    def test_file_node_to_markdown(self):
        node = FileNode("test.txt", "/path/to/test.txt", 100, ".txt", "📄")
        node.content = "Hello, world!"
        expected_markdown = f'***/{node.path}***\n\n```{node.extension}\n{node.content}\n```'
        self.assertEqual(node.to_markdown(), expected_markdown)

    def test_file_tree_creation(self):
        tree = FileTree()
        self.assertIsNone(tree.root)

    def test_file_tree_insert(self):
        tree = FileTree()
        tree.insert("test.txt", "/path/to/test.txt", 100, ".txt", "📄")
        self.assertIsNotNone(tree.root)
        self.assertEqual(tree.root.name, "test.txt")

if __name__ == '__main__':
    unittest.main()
