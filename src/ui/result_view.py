import tkinter as tk
from tkinter import ttk
import os
from src.core.app_state import AppState

class ResultView:
    def __init__(self, parent, content, prompt_template, main_root, main_window_instance):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.content = content
        self.prompt_template = prompt_template # Guardamos la plantilla original
        self.state = AppState()
        self.main_root = main_root
        self.main_window_instance = main_window_instance
        
        self.text_area = tk.Text(self.frame, wrap="word")
        self.text_area.pack(padx=10, pady=10, fill="both", expand=True)
        self.text_area.insert("1.0", self.content)
        self.text_area.config(state="disabled")

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill="x", padx=10, pady=5, side="bottom")

        exit_button = ttk.Button(button_frame, text="Salir", command=self.exit_app)
        exit_button.pack(side="right")

        new_prompt_button = ttk.Button(button_frame, text="Crear otro prompt", command=self.create_new_prompt)
        new_prompt_button.pack(side="left")

        prev_button = ttk.Button(button_frame, text="Anterior", command=self.go_back)
        prev_button.pack(side="left", padx=5)

        copy_button = ttk.Button(button_frame, text="Copiar", command=self.copy_to_clipboard)
        copy_button.pack(side="left")
        
        # --- ¡Nuevo! Botón de Refrescar ---
        refresh_button = ttk.Button(button_frame, text="Refrescar", command=self.refresh_prompt)
        refresh_button.pack(side="left", padx=5)
        
    def refresh_prompt(self):
        """Recarga el contenido de los archivos seleccionados y actualiza el prompt."""
        print("DEBUG: Botón 'Refrescar' presionado.")
        
        # 1. Cargar las rutas desde el archivo temporal
        paths = self.state.temp_storage.load_selected_paths()
        if not paths:
            print("DEBUG: No hay rutas para refrescar.")
            return
            
        # 2. Volver a leer cada archivo y construir el contenido markdown
        markdown_parts = []
        for path in paths:
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                _, ext = os.path.splitext(path)
                ext = ext.lstrip('.')
                markdown_parts.append(f'**`{path}`**\n\n```{ext}\n{content}\n```')
            except Exception as e:
                print(f"DEBUG: No se pudo refrescar el archivo {path}: {e}")
                markdown_parts.append(f'**`{path}`**\n\n```\nError al refrescar el archivo: {e}\n```')

        # 3. Reconstruir el prompt final
        new_context = "\n\n".join(markdown_parts)
        self.content = self.prompt_template.replace("{context}", new_context)
        
        # 4. Actualizar el área de texto
        self.text_area.config(state="normal")
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", self.content)
        self.text_area.config(state="disabled")
        print("DEBUG: El prompt ha sido refrescado con el contenido actualizado de los archivos.")

    def copy_to_clipboard(self):
        print("DEBUG: Botón 'Copiar' presionado.")
        self.parent.clipboard_clear()
        self.parent.clipboard_append(self.content)
        print("DEBUG: Contenido copiado al portapapeles.")

    def go_back(self):
        from src.ui.prompt_view import PromptView
        print("DEBUG: Botón 'Anterior' presionado.")
        self.parent.destroy()
        top = tk.Toplevel(self.main_root)
        top.title("Compose Prompt")
        top.geometry("800x600")
        prompt_view = PromptView(top, self.main_root, self.main_window_instance)
        prompt_view.frame.pack(fill="both", expand=True)

    def create_new_prompt(self):
        print("DEBUG: Botón 'Crear otro prompt' presionado.")
        self.state.reset()
        current_path = self.main_window_instance.file_selection_view.path_input.get()
        self.main_window_instance.file_selection_view.populate_tree(current_path)
        self.main_root.deiconify()
        self.parent.destroy()
        
    def exit_app(self):
        print("DEBUG: Botón 'Salir' presionado.")
        self.state.temp_storage.cleanup() # Asegurarse de limpiar al salir
        self.main_root.quit()