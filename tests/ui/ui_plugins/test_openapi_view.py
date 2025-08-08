import unittest
import tkinter as tk
from tkinter import ttk
from src.ui.ui_plugins.openapi_view import OpenAPIView


class TestOpenAPIView(unittest.TestCase):
    def test_openapi_view_creation(self):
        root = tk.Tk()
        root.title = "Open Api View"
        notebook = ttk.Notebook(root)
        view = OpenAPIView(notebook)
        self.assertEqual(view.parent, notebook)
        self.assertIsInstance(view.frame, ttk.Frame)
        self.assertIsInstance(view.listbox, tk.Listbox)
        root.destroy()


if __name__ == "__main__":
    unittest.main()
