import tkinter as tk
from tkinter import ttk
from src.core.app_state import AppState
from src.ui.result_view import ResultView

class PromptView:
    def __init__(self, parent, main_root, main_window_instance):
        self.parent = parent
        self.main_root = main_root
        self.main_window_instance = main_window_instance # Guardamos la instancia
        self.frame = ttk.Frame(parent)
        self.state = AppState()

        self.text_area = tk.Text(self.frame, wrap="word")
        self.text_area.pack(padx=10, pady=10, fill="both", expand=True)
        self.text_area.insert("1.0", "Sigue las intrucciones de manera precisa\n\n{context}\n")

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill="x", padx=10, pady=5)

        prev_button = ttk.Button(button_frame, text="Previous", command=self.go_back)
        prev_button.pack(side="left")

        get_prompt_button = ttk.Button(button_frame, text="Get Prompt", command=self.show_result_view)
        get_prompt_button.pack(side="right")

    def go_back(self):
        """Regresa a la ventana principal de selección de archivos."""
        self.main_root.deiconify()
        self.parent.destroy()

    def show_result_view(self):
        """Genera el prompt final y muestra la vista de resultados."""
        prompt_template = self.text_area.get("1.0", tk.END).strip()
        context_content = self.state.file_tree.get_selected_files_markdown()

        if not context_content:
            context_content = "WARNING: No files were selected or content could not be loaded."
        
        final_prompt_content = prompt_template.replace("{context}", context_content)

        self.parent.destroy()

        top = tk.Toplevel(self.main_root)
        top.title("Prompt Result")
        top.geometry("900x700")
        
        # Le pasamos la instancia de MainWindow a ResultView
        result_view = ResultView(top, final_prompt_content, self.main_root, self.main_window_instance)
        result_view.frame.pack(fill="both", expand=True)