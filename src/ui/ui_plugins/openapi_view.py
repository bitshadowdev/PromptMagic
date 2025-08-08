import tkinter as tk
from tkinter import ttk, Toplevel, Entry, Button
from src.plugins.openapi.openapi_plugin import OpenAPIPlugin
from src.core.language_manager import LanguageManager

class OpenAPIView:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.lang = LanguageManager()
        self.listbox = tk.Listbox(self.frame)
        self.listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.plugin = OpenAPIPlugin()

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=5)

        add_button = ttk.Button(button_frame, text=self.lang.get_string("BUTTON_ADD"), command=self.add_spec)
        add_button.pack(side=tk.LEFT, padx=5)

        remove_button = ttk.Button(button_frame, text=self.lang.get_string("BUTTON_REMOVE"), command=self.remove_spec)
        remove_button.pack(side=tk.LEFT)

        parent.add(self.frame, text=self.lang.get_string("TAB_OPENAPI"))

    def add_spec(self):
        top = Toplevel(self.frame)
        top.title(self.lang.get_string("TITLE_ADD_SPEC"))
        entry = Entry(top, width=50)
        entry.pack(padx=10, pady=10)

        def add():
            url = entry.get()
            if url:
                spec = self.plugin.get_openapi_spec(url)
                if spec:
                    self.listbox.insert(tk.END, url)
                    top.destroy()

        add_button = Button(top, text=self.lang.get_string("BUTTON_ADD"), command=add)
        add_button.pack(pady=5)

    def remove_spec(self):
        selected_indices = self.listbox.curselection()
        for i in reversed(selected_indices):
            self.listbox.delete(i)