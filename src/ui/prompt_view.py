import ttkbootstrap as tkb
from tkinter import Text
from src.core.app_state import AppState
from src.ui.result_view import ResultView
from src.core.language_manager import LanguageManager
import os

class PromptView:
    def __init__(self, parent, context_content, main_root, main_window_instance):
        self.parent = parent
        self.context_content = context_content
        self.main_root = main_root
        self.main_window_instance = main_window_instance
        self.frame = tkb.Frame(parent)
        self.state = AppState()
        self.lang = LanguageManager()

        self.text_area = Text(self.frame, wrap="word", relief="flat")
        self.text_area.pack(padx=10, pady=10, fill="both", expand=True)
        self.text_area.insert("1.0", self.lang.get_string("PROMPT_TEMPLATE_PLACEHOLDER"))

        button_frame = tkb.Frame(self.frame)
        button_frame.pack(fill="x", padx=10, pady=5)

        prev_button = tkb.Button(button_frame, text=self.lang.get_string("BUTTON_PREVIOUS"), command=self.go_back)
        prev_button.pack(side="left")

        get_prompt_button = tkb.Button(button_frame, text=self.lang.get_string("BUTTON_GET_PROMPT"), command=self.show_result_view, bootstyle="success")
        get_prompt_button.pack(side="right")

    def go_back(self):
        self.main_root.deiconify()
        self.parent.destroy()

    def show_result_view(self):
        prompt_template = self.text_area.get(tkb.END, "1.0").strip()
        final_prompt_content = prompt_template.replace("{context}", self.context_content)

        self.parent.destroy()

        top = tkb.Toplevel(self.main_root)

        # Aplicamos el ícono a la nueva ventana
        if self.state.icon_path and os.path.exists(self.state.icon_path):
            top.iconbitmap(self.state.icon_path)
            
        top.title(self.lang.get_string("TITLE_PROMPT_RESULT"))
        top.geometry("900x700")
        
        result_view = ResultView(top, final_prompt_content, prompt_template, self.main_root, self.main_window_instance)
        result_view.frame.pack(fill="both", expand=True)