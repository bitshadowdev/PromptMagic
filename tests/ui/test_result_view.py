import unittest
import tkinter as tk
from tkinter import ttk
from src.ui.result_view import ResultView


class TestResultView(unittest.TestCase):
    def test_result_view_creation(self):
        root = tk.Tk()
        view = ResultView(root, "Test content")
        root.title = "Prompt Magic"

        self.assertEqual(view.parent, root)
        self.assertIsInstance(view.frame, ttk.Frame)
        self.assertIsInstance(view.text_area, tk.Text)
        self.assertEqual(view.text_area.get("1.0", tk.END), "Test content\n")
        root.destroy()


if __name__ == "__main__":
    unittest.main()
