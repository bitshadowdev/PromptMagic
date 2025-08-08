import ttkbootstrap as tkb
from tkinter import Listbox # ¡Importamos Listbox directamente desde tkinter!
from src.core.language_manager import LanguageManager
from src.core.app_state import AppState
from src.plugins.openapi.openapi_plugin import OpenAPIPlugin
import os

class OpenAPIView:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tkb.Frame(parent)
        self.lang = LanguageManager()
        self.state = AppState()
        
        # --- ¡Corrección! Usamos el Listbox de tkinter ---
        # ttkbootstrap aplicará el estilo del tema automáticamente.
        self.listbox = Listbox(self.frame) 
        self.listbox.pack(pady=10, padx=10, fill="both", expand=True)

        self.plugin = OpenAPIPlugin()

        button_frame = tkb.Frame(self.frame)
        button_frame.pack(fill="x", side="bottom", pady=5)

        add_button = tkb.Button(button_frame, text=self.lang.get_string("BUTTON_ADD"), command=self.add_spec, bootstyle="primary")
        add_button.pack(side="left", padx=5)

        remove_button = tkb.Button(button_frame, text=self.lang.get_string("BUTTON_REMOVE"), command=self.remove_spec, bootstyle="danger")
        remove_button.pack(side="left")

        parent.add(self.frame, text=self.lang.get_string("TAB_OPENAPI"))

    def add_spec(self):
        top = tkb.Toplevel(self.frame)
        
        if self.state.icon_path and os.path.exists(self.state.icon_path):
            top.iconbitmap(self.state.icon_path)
            
        top.title(self.lang.get_string("TITLE_ADD_SPEC"))
        entry = tkb.Entry(top, width=50)
        entry.pack(padx=10, pady=10)

        def add():
            url = entry.get()
            if url:
                spec = self.plugin.get_openapi_spec(url)
                if spec:
                    self.listbox.insert(tkb.END, url)
                    top.destroy()

        add_button = tkb.Button(top, text=self.lang.get_string("BUTTON_ADD"), command=add, bootstyle="success")
        add_button.pack(pady=5)

    def remove_spec(self):
        selected_indices = self.listbox.curselection()
        for i in reversed(selected_indices):
            self.listbox.delete(i)