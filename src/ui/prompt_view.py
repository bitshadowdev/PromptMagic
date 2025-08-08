import tkinter as tk
from tkinter import ttk
from src.core.app_state import AppState

class PromptView:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.state = AppState()

        # Instruction label
        instruction_label = ttk.Label(self.frame, text="Customize your prompt template:")
        instruction_label.pack(padx=10, pady=(10, 5), anchor='w')

        # Text area for prompt template
        self.text_area = tk.Text(self.frame, wrap="word", height=15)
        self.text_area.pack(padx=10, pady=5, fill="both", expand=True)
        
        # Insert default template
        default_template = "Sigue las instrucciones de manera precisa\n\n{context}\n"
        self.text_area.insert("1.0", default_template)

        # Info label
        info_label = ttk.Label(
            self.frame, 
            text="Note: {context} will be replaced with the content of your selected files.",
            font=('TkDefaultFont', 8)
        )
        info_label.pack(padx=10, pady=(0, 5), anchor='w')

        # Button frame
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill="x", padx=10, pady=10)

        prev_button = ttk.Button(button_frame, text="Previous", command=self.go_back)
        prev_button.pack(side="left")

        get_prompt_button = ttk.Button(button_frame, text="Get Prompt", command=self.show_result_view)
        get_prompt_button.pack(side="right")

    def go_back(self):
        """Return to the main window"""
        self.parent.master.deiconify()  # Show main window
        self.parent.destroy()  # Close this window

    def show_result_view(self):
        """Generate final prompt and show result view"""
        from src.ui.result_view import ResultView
        
        # Get the prompt template
        prompt_template = self.text_area.get("1.0", tk.END).strip()
        
        # Load markdown content from temporary storage
        print("DEBUG: Loading markdown content from temp storage...")
        context_content = self.state.load_markdown_content()
        
        if not context_content:
            context_content = "No files were selected or content could not be loaded."
            print("DEBUG: No content loaded from temp storage!")
        else:
            print(f"DEBUG: Loaded {len(context_content)} characters of content")
        
        # Replace {context} with actual content
        final_prompt_content = prompt_template.replace("{context}", context_content)
        
        print(f"DEBUG: Final prompt length: {len(final_prompt_content)} characters")
        
        # Close current window
        self.parent.destroy()

        # Create result view
        top = tk.Toplevel(self.parent.master)
        top.title("Prompt Result")
        top.geometry("900x700")
        result_view = ResultView(top, final_prompt_content)
        result_view.frame.pack(fill="both", expand=True)

        def on_close():
            # Clean up temp files when closing result view
            self.state.cleanup_temp_files()
            top.destroy()

        top.protocol("WM_DELETE_WINDOW", on_close)