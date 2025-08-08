import unittest
import tkinter as tk
from tkinter import ttk
from src.ui.file_selection_view import FileSelectionView

class TestFileSelectionView(unittest.TestCase):

    def test_file_selection_view_creation(self):
        root = tk.Tk()
        notebook = ttk.Notebook(root)
        view = FileSelectionView(notebook)
        self.assertEqual(view.parent, notebook)
        self.assertIsInstance(view.frame, ttk.Frame)
        self.assertIsInstance(view.tree, ttk.Treeview)
        self.assertIsInstance(view.path_input, ttk.Entry)
        root.destroy()

if __name__ == '__main__':
    unittest.main()