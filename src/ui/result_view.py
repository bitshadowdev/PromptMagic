import tkinter as tk
from tkinter import ttk
from src.core.app_state import AppState

class ResultView:
    def __init__(self, parent, content):
        self.parent = parent
        self.frame = ttk.Frame(parent)

        # Get the markdown content of all selected files
        app_state = AppState()
        selected_files_markdown = app_state.file_tree.get_selected_files_markdown()
        
        # Create a text area to display the result
        self.text_area = tk.Text(self.frame, wrap="word")
        self.text_area.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Insert the content with the selected files markdown
        final_content = content.replace("{context}", selected_files_markdown)
        self.text_area.insert("1.0", final_content)
        self.text_area.config(state="disabled")

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill="x", padx=10, pady=5, side="bottom")

        exit_button = ttk.Button(button_frame, text="Salir")
        exit_button.pack(side="right")

        new_prompt_button = ttk.Button(button_frame, text="Crear otro prompt")
        new_prompt_button.pack(side="left")

        prev_button = ttk.Button(button_frame, text="Anterior")
        prev_button.pack(side="left", padx=5)

        copy_button = ttk.Button(button_frame, text="Copiar")
        copy_button.pack(side="left")
