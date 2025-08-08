import tkinter as tk
from tkinter import ttk, Toplevel
from src.ui.file_selection_view import FileSelectionView
from src.ui.ui_plugins.openapi_view import OpenAPIView
from src.ui.prompt_view import PromptView

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Prompt Magic")
        self.root.geometry("800x600")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)

        self.file_selection_view = FileSelectionView(self.notebook)
        self.openapi_view = OpenAPIView(self.notebook)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5, side="bottom")

        self.next_button = ttk.Button(button_frame, text="Siguiente", command=self.show_prompt_view)
        self.next_button.pack(side="right")

    def show_prompt_view(self):
        self.root.withdraw() # Hide the main window
        top = Toplevel(self.root)
        top.title("Compose Prompt")
        top.geometry("800x600")
        prompt_view = PromptView(top)
        prompt_view.frame.pack(fill="both", expand=True)

        def on_close():
            self.root.deiconify() # Show the main window again
            top.destroy()

        top.protocol("WM_DELETE_WINDOW", on_close)