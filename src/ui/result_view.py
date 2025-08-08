import ttkbootstrap as tkb
from tkinter import Text
import os
from src.core.app_state import AppState
from src.core.language_manager import LanguageManager

class ResultView:
    def __init__(self, parent, content, prompt_template, main_root, main_window_instance):
        self.parent = parent
        self.frame = tkb.Frame(parent)
        self.content = content
        self.prompt_template = prompt_template
        self.state = AppState()
        self.lang = LanguageManager()
        self.main_root = main_root
        self.main_window_instance = main_window_instance
        
        self.text_area = Text(self.frame, wrap="word", relief="flat")
        self.text_area.pack(padx=10, pady=10, fill="both", expand=True)
        self.text_area.insert("1.0", self.content)
        self.text_area.config(state="disabled")

        button_frame = tkb.Frame(self.frame)
        button_frame.pack(fill="x", padx=10, pady=5, side="bottom")

        exit_button = tkb.Button(button_frame, text=self.lang.get_string("BUTTON_EXIT"), command=self.exit_app, bootstyle="danger")
        exit_button.pack(side="right")

        new_prompt_button = tkb.Button(button_frame, text=self.lang.get_string("BUTTON_CREATE_NEW"), command=self.create_new_prompt, bootstyle="success")
        new_prompt_button.pack(side="left")

        prev_button = tkb.Button(button_frame, text=self.lang.get_string("BUTTON_PREVIOUS"), command=self.go_back)
        prev_button.pack(side="left", padx=5)

        copy_button = tkb.Button(button_frame, text=self.lang.get_string("BUTTON_COPY"), command=self.copy_to_clipboard, bootstyle="info")
        copy_button.pack(side="left")
        
        refresh_button = tkb.Button(button_frame, text=self.lang.get_string("BUTTON_REFRESH"), command=self.refresh_prompt)
        refresh_button.pack(side="left", padx=5)
        
    def refresh_prompt(self):
        print("DEBUG: Botón 'Refrescar' presionado.")
        
        paths = self.state.temp_storage.load_selected_paths()
        if not paths:
            print("DEBUG: No hay rutas para refrescar.")
            return
            
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

        new_context = "\n\n".join(markdown_parts)
        self.content = self.prompt_template.replace("{context}", new_context)
        
        self.text_area.config(state="normal")
        self.text_area.delete("1.0", tkb.END)
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
        top = tkb.Toplevel(self.main_root)

        # Aplicamos el ícono a la nueva ventana
        if self.state.icon_path and os.path.exists(self.state.icon_path):
            top.iconbitmap(self.state.icon_path)

        top.title(self.lang.get_string("TITLE_COMPOSE_PROMPT"))
        top.geometry("800x600")
        
        final_selected_files = self.state.file_tree.get_selected_files()
        markdown_parts = [node.to_markdown() for node in final_selected_files]
        context_content = "\n\n".join(markdown_parts)

        prompt_view = PromptView(top, context_content, self.main_root, self.main_window_instance)
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
        self.state.temp_storage.cleanup()
        self.main_root.quit()