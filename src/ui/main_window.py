import ttkbootstrap as tkb
from tkinter import Menu
from ttkbootstrap.dialogs import Messagebox
from src.ui.file_selection_view import FileSelectionView
from src.ui.ui_plugins.openapi_view import OpenAPIView
from src.ui.prompt_view import PromptView
from src.core.app_state import AppState
from src.core.language_manager import LanguageManager
import os

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.lang = LanguageManager()
        self.root.title(self.lang.get_string("TITLE_MAIN"))
        self.root.geometry("800x600")
        self.state = AppState()

        menubar = Menu(root)
        root.config(menu=menubar)
        
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.lang.get_string("MENU_FILE"), menu=file_menu)
        file_menu.add_command(label=self.lang.get_string("MENU_OPEN_FOLDER"), command=self.open_folder)
        file_menu.add_separator()
        file_menu.add_command(label=self.lang.get_string("MENU_EXIT"), command=root.quit)

        self.notebook = tkb.Notebook(self.root)
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)

        self.file_selection_view = FileSelectionView(self.notebook)
        self.openapi_view = OpenAPIView(self.notebook)

        filter_frame = tkb.Frame(self.root)
        filter_frame.pack(fill="x", padx=10, pady=(0, 5), side="bottom")
        
        filter_label = tkb.Label(filter_frame, text=self.lang.get_string("LABEL_EXTENSION_FILTER"))
        filter_label.pack(side="left")

        self.filter_entry = tkb.Entry(filter_frame)
        self.filter_entry.pack(fill="x", expand=True, side="left", padx=5)
        
        button_frame = tkb.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5, side="bottom")

        self.next_button = tkb.Button(button_frame, text=self.lang.get_string("BUTTON_NEXT"), command=self.show_prompt_view, bootstyle="primary")
        self.next_button.pack(side="right")

    def open_folder(self):
        self.file_selection_view.open_folder_dialog()

    def show_prompt_view(self):
        originally_selected_files = self.state.file_tree.get_selected_files()
        filter_text = self.filter_entry.get().strip()
        extensions_to_filter = {ext.strip() for ext in filter_text.split(',') if ext.strip()}
        
        final_selected_files = [
            node for node in originally_selected_files 
            if node.extension not in extensions_to_filter
        ]
        
        if not final_selected_files:
            Messagebox.show_warning(
                parent=self.root,
                title=self.lang.get_string("MSG_NO_FILES_TITLE"),
                message=self.lang.get_string("MSG_NO_FILES_AFTER_FILTER_CONTENT")
            )
            return
        
        markdown_parts = [node.to_markdown() for node in final_selected_files]
        context_content = "\n\n".join(markdown_parts)

        self.state.temp_storage.save_selected_paths(final_selected_files)
        
        self.root.withdraw()
        top = tkb.Toplevel(self.root)
        
        # Aplicamos el ícono a la nueva ventana
        if self.state.icon_path and os.path.exists(self.state.icon_path):
            top.iconbitmap(self.state.icon_path)
            
        top.title(self.lang.get_string("TITLE_COMPOSE_PROMPT"))
        top.geometry("800x600")
        
        prompt_view = PromptView(top, context_content, self.root, self)
        prompt_view.frame.pack(fill="both", expand=True)

        def on_close():
            self.root.deiconify()
            top.destroy()

        top.protocol("WM_DELETE_WINDOW", on_close)