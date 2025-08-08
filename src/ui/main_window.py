import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
from src.ui.file_selection_view import FileSelectionView
from src.ui.ui_plugins.openapi_view import OpenAPIView
from src.ui.prompt_view import PromptView
from src.core.app_state import AppState

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Prompt Magic")
        self.root.geometry("800x600")
        self.state = AppState()

        # Create menu bar
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Folder...", command=self.open_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)

        self.file_selection_view = FileSelectionView(self.notebook)
        self.openapi_view = OpenAPIView(self.notebook)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5, side="bottom")

        self.next_button = ttk.Button(button_frame, text="Siguiente", command=self.show_prompt_view)
        self.next_button.pack(side="right")

    def open_folder(self):
        """Open folder dialog from menu"""
        self.file_selection_view.open_folder_dialog()

    def show_prompt_view(self):
        """Transition to prompt view with temporary storage"""
        # Save selected files to temporary storage
        selected_files = self.state.file_tree.get_selected_files()
        if not selected_files:
            messagebox.showwarning("No Selection", "Please select at least one file before proceeding.")
            return
        
        # Save content to temporary storage
        print(f"DEBUG: Saving {len(selected_files)} selected files...")
        markdown_content = self.state.save_selected_content()
        print(f"DEBUG: Saved markdown content size: {len(markdown_content)}")
        
        # Hide main window and show prompt view
        self.root.withdraw()
        top = Toplevel(self.root)
        top.title("Compose Prompt")
        top.geometry("800x600")
        prompt_view = PromptView(top)
        prompt_view.frame.pack(fill="both", expand=True)

        def on_close():
            self.root.deiconify()  # Show the main window again
            top.destroy()

        top.protocol("WM_DELETE_WINDOW", on_close)