import tkinter as tk
from tkinter import ttk
from src.core.app_state import AppState

class ResultView:
    def __init__(self, parent, content, main_root, main_window_instance):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.content = content
        self.state = AppState()
        self.main_root = main_root # Referencia a la ventana raíz (Tk)
        self.main_window_instance = main_window_instance # Referencia a la clase MainWindow
        
        # Área de texto para mostrar el resultado
        self.text_area = tk.Text(self.frame, wrap="word")
        self.text_area.pack(padx=10, pady=10, fill="both", expand=True)
        self.text_area.insert("1.0", self.content)
        self.text_area.config(state="disabled") # Lo hacemos de solo lectura

        # Frame para los botones de acción
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill="x", padx=10, pady=5, side="bottom")

        # --- Conexión de todos los botones ---
        exit_button = ttk.Button(button_frame, text="Salir", command=self.exit_app)
        exit_button.pack(side="right")

        new_prompt_button = ttk.Button(button_frame, text="Crear otro prompt", command=self.create_new_prompt)
        new_prompt_button.pack(side="left")

        # Importamos PromptView aquí para evitar importación circular
        from src.ui.prompt_view import PromptView
        prev_button = ttk.Button(button_frame, text="Anterior", command=self.go_back)
        prev_button.pack(side="left", padx=5)

        copy_button = ttk.Button(button_frame, text="Copiar", command=self.copy_to_clipboard)
        copy_button.pack(side="left")
        
    def copy_to_clipboard(self):
        """Copia el contenido del prompt al portapapeles."""
        print("DEBUG: Botón 'Copiar' presionado.")
        self.parent.clipboard_clear()
        self.parent.clipboard_append(self.content)
        print("DEBUG: Contenido copiado al portapapeles.")

    def go_back(self):
        """Regresa a la vista anterior (PromptView)."""
        from src.ui.prompt_view import PromptView # Importación local para la función
        print("DEBUG: Botón 'Anterior' presionado. Volviendo a PromptView.")
        
        self.parent.destroy() # Cierra la ventana actual de resultados
        
        # Crea y muestra de nuevo la ventana de Prompt
        top = tk.Toplevel(self.main_root)
        top.title("Compose Prompt")
        top.geometry("800x600")
        prompt_view = PromptView(top, self.main_root, self.main_window_instance)
        prompt_view.frame.pack(fill="both", expand=True)

    def create_new_prompt(self):
        """Reinicia el estado y regresa a la pantalla principal de selección."""
        print("DEBUG: Botón 'Crear otro prompt' presionado. Reiniciando estado.")
        
        # 1. Resetea el estado de la aplicación
        self.state.reset()
        
        # 2. Refresca el árbol de archivos en la ventana principal para que se vea vacío
        current_path = self.main_window_instance.file_selection_view.path_input.get()
        self.main_window_instance.file_selection_view.populate_tree(current_path)
        
        # 3. Muestra de nuevo la ventana principal
        self.main_root.deiconify()
        
        # 4. Cierra la ventana actual de resultados
        self.parent.destroy()
        
    def exit_app(self):
        """Cierra toda la aplicación."""
        print("DEBUG: Botón 'Salir' presionado. Cerrando la aplicación.")
        self.main_root.quit()