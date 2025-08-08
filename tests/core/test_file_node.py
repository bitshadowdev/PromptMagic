import unittest
from src.core.file_tree import FileNode

class TestFileNode(unittest.TestCase):

    def test_file_node_selection(self):
        node = FileNode("test.txt", "/path/to/test.txt", 100, ".txt", "📄")
        self.assertFalse(node.is_selected)
        node.is_selected = True
        self.assertTrue(node.is_selected)

if __name__ == '__main__':
    unittest.main()
