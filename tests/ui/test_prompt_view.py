import unittest
import tkinter as tk
from tkinter import ttk
from src.ui.prompt_view import PromptView


class TestPromptView(unittest.TestCase):
    def test_prompt_view_creation(self):
        root = tk.Tk()
        root.title = "Prompt Magic"
        view = PromptView(root)
        self.assertEqual(view.parent, root)
        self.assertIsInstance(view.frame, ttk.Frame)
        self.assertIsInstance(view.text_area, tk.Text)
        root.destroy()


if __name__ == "__main__":
    unittest.main()
