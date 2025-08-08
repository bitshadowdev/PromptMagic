import unittest
import tkinter as tk
from tkinter import ttk
from unittest.mock import MagicMock
from src.ui.main_window import MainWindow

class TestMainWindow(unittest.TestCase):

    def test_main_window_creation(self):
        root = tk.Tk()
        app = MainWindow(root)
        self.assertEqual(app.root, root)
        self.assertIsInstance(app.notebook, ttk.Notebook)
        root.destroy()

    def test_navigation_to_prompt_view(self):
        root = tk.Tk()
        app = MainWindow(root)
        app.show_prompt_view = MagicMock() # Mock the method here
        app.next_button.invoke()
        app.show_prompt_view.assert_called_once()
        root.destroy()

if __name__ == '__main__':
    unittest.main()
