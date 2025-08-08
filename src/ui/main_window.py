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

        # Es importante que FileSelectionView se cree para que el menú "Open Folder" funcione
        self.file_selection_view = FileSelectionView(self.notebook)
        self.openapi_view = OpenAPIView(self.notebook)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5, side="bottom")

        self.next_button = ttk.Button(button_frame, text="Siguiente", command=self.show_prompt_view)
        self.next_button.pack(side="right")

    def open_folder(self):
        """Función del menú para abrir un nuevo directorio."""
        self.file_selection_view.open_folder_dialog()

    def show_prompt_view(self):
        """
        Transición a la vista del prompt.
        ¡Aquí está la corrección! No guardamos nada, solo verificamos.
        """
        # 1. Obtiene los archivos seleccionados directamente desde el estado en memoria.
        selected_files = self.state.file_tree.get_selected_files()
        
        # 2. Si no hay nada seleccionado, muestra la advertencia.
        if not selected_files:
            messagebox.showwarning("No Selection", "Please select at least one file before proceeding.")
            return
        
        # 3. Si hay selección, simplemente procede a la siguiente ventana.
        #    La información ya está en AppState, lista para ser usada.
        print(f"DEBUG: Proceeding to next view with {len(selected_files)} files selected in memory.")
        self.root.withdraw()
        top = Toplevel(self.root)
        top.title("Compose Prompt")
        top.geometry("800x600")
        
        prompt_view = PromptView(top, self.root) # Pasamos la raíz para poder volver
        prompt_view.frame.pack(fill="both", expand=True)

        def on_close():
            self.root.deiconify()
            top.destroy()

        top.protocol("WM_DELETE_WINDOW", on_close)