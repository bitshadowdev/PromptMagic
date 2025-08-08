import tkinter as tk
from tkinter import ttk
from src.core.app_state import AppState

class PromptView:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)

        self.text_area = tk.Text(self.frame, wrap="word")
        self.text_area.pack(padx=10, pady=10, fill="both", expand=True)
        self.text_area.insert("1.0", "Sigue las intrucciones de manera precisa\n\n{context}\n")

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill="x", padx=10, pady=5)

        prev_button = ttk.Button(button_frame, text="Previous")
        prev_button.pack(side="left")

        get_prompt_button = ttk.Button(button_frame, text="Get Prompt", command=self.show_result_view)
        get_prompt_button.pack(side="right")

    def show_result_view(self):
        from src.ui.result_view import ResultView
        prompt_template = self.text_area.get("1.0", tk.END)

        # Get selected files content
        app_state = AppState()
        context_content = ""
        selected_files = app_state.file_tree.get_selected_files()
        for file_node in selected_files:
            context_content += file_node.to_markdown() + "\n\n"

        final_prompt_content = prompt_template.replace("{context}", context_content)

        self.parent.destroy() # Close the current Toplevel window

        top = tk.Toplevel(self.parent.master) # Use master to get the root window
        top.title("Prompt Result")
        top.geometry("800x600")
        result_view = ResultView(top, final_prompt_content)
        result_view.frame.pack(fill="both", expand=True)

        def on_close():
            top.destroy()
            # Optionally, you might want to re-show the main window or go back to file selection
            # For now, just close the result view
        top.protocol("WM_DELETE_WINDOW", on_close)
