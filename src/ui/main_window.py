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

        menubar = tk.Menu(root)
        root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Folder...", command=self.open_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)

        self.file_selection_view = FileSelectionView(self.notebook)
        self.openapi_view = OpenAPIView(self.notebook)

        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(fill="x", padx=10, pady=(0, 5), side="bottom")
        
        filter_label = ttk.Label(filter_frame, text="Extension filter (ignore):")
        filter_label.pack(side="left")

        self.filter_entry = ttk.Entry(filter_frame)
        self.filter_entry.pack(fill="x", expand=True, side="left", padx=5)
        
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5, side="bottom")

        self.next_button = ttk.Button(button_frame, text="Siguiente", command=self.show_prompt_view)
        self.next_button.pack(side="right")

    def open_folder(self):
        """Función del menú para abrir un nuevo directorio."""
        self.file_selection_view.open_folder_dialog()

    def show_prompt_view(self):
        """
        Transición a la vista del prompt, aplicando el filtro y generando el contenido.
        """
        originally_selected_files = self.state.file_tree.get_selected_files()
        filter_text = self.filter_entry.get().strip()
        extensions_to_filter = {ext.strip() for ext in filter_text.split(',') if ext.strip()}
        
        final_selected_files = [
            node for node in originally_selected_files 
            if node.extension not in extensions_to_filter
        ]
        
        if not final_selected_files:
            messagebox.showwarning("No Selection", "No files selected after applying the filter.")
            return
        
        # --- ¡Cambio Clave! Generamos el markdown aquí, con la lista filtrada ---
        print(f"DEBUG: Generando markdown desde {len(final_selected_files)} archivos filtrados.")
        markdown_parts = [node.to_markdown() for node in final_selected_files]
        context_content = "\n\n".join(markdown_parts)

        # Guardamos las rutas de la lista filtrada para la función de "Refrescar"
        self.state.temp_storage.save_selected_paths(final_selected_files)
        
        self.root.withdraw()
        top = Toplevel(self.root)
        top.title("Compose Prompt")
        top.geometry("800x600")
        
        # Pasamos el contenido ya generado a PromptView
        prompt_view = PromptView(top, context_content, self.root, self)
        prompt_view.frame.pack(fill="both", expand=True)

        def on_close():
            self.root.deiconify()
            top.destroy()

        top.protocol("WM_DELETE_WINDOW", on_close)