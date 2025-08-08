import tkinter as tk
from tkinter import ttk, filedialog
import os
from src.core.emoji_assigner import EmojiAssigner
from src.core.app_state import AppState
from src.core.file_tree import FileTree

class FileSelectionView:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.state = AppState()
        self.path_to_item_id = {}

        path_frame = ttk.Frame(self.frame)
        path_frame.pack(fill=tk.X, padx=5, pady=5)

        self.path_input = ttk.Entry(path_frame)
        self.path_input.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=(0, 5))

        browse_button = ttk.Button(path_frame, text="Browse...", command=self.open_folder_dialog)
        browse_button.pack(side=tk.LEFT)
        
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

        self.tree = ttk.Treeview(tree_frame, columns=('selected',), show='tree headings')
        self.tree.heading('#0', text='Name')
        self.tree.column("#0", width=400, anchor='w')
        
        self.tree.heading('selected', text='Selected')
        self.tree.column("selected", width=80, anchor='center', stretch=tk.NO)

        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        parent.add(self.frame, text="Select Files")

        self.tree.bind("<Button-1>", self.on_tree_click)
        
        self.populate_tree(os.path.abspath('.'))
    
    # El método deselect_by_extensions se elimina de aquí, ya que no es necesario.

    def open_folder_dialog(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.populate_tree(folder_path)

    def on_tree_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            item_id = self.tree.identify_row(event.y)
            if item_id:
                self.toggle_item_selection(item_id)

    def toggle_item_selection(self, item_id):
        tags = self.tree.item(item_id, 'tags')
        if not tags: return

        file_path = tags[0]
        file_node = self.state.file_tree.get_node_by_path(file_path)
        
        if file_node:
            file_node.is_selected = not file_node.is_selected
            if file_node.is_selected and not file_node.is_directory:
                file_node.load_content()
            
            self.update_tree_item_selection(item_id, file_node.is_selected)

            if file_node.is_directory:
                self._toggle_children_selection(item_id, file_node.is_selected)

    def _toggle_children_selection(self, parent_id, selected):
        for child_id in self.tree.get_children(parent_id):
            tags = self.tree.item(child_id, 'tags')
            if not tags: continue
            child_path = tags[0]
            child_node = self.state.file_tree.get_node_by_path(child_path)
            if child_node:
                child_node.is_selected = selected
                if selected and not child_node.is_directory:
                    child_node.load_content()
                self.update_tree_item_selection(child_id, selected)
                if child_node.is_directory:
                    self._toggle_children_selection(child_id, selected)

    def update_tree_item_selection(self, item_id, is_selected):
        self.tree.set(item_id, 'selected', '✔' if is_selected else '')

    def populate_tree(self, path):
        self.path_input.delete(0, tk.END)
        self.path_input.insert(0, path)
        self.tree.delete(*self.tree.get_children())
        self.emoji_assigner = EmojiAssigner()
        
        self.state.file_tree = FileTree()
        self.path_to_item_id = {}
        
        self._populate_tree("", path, None)

    def _populate_tree(self, parent_tree_id, current_path, parent_node_path):
        try:
            items = sorted(os.listdir(current_path), key=lambda x: (not os.path.isdir(os.path.join(current_path, x)), x.lower()))
            for item in items:
                item_path = os.path.join(current_path, item)
                is_directory = os.path.isdir(item_path)
                emoji = self.emoji_assigner.get_emoji("folder" if is_directory else os.path.splitext(item)[1])
                display_text = f"{emoji} {item}"
                
                node = self.state.file_tree.add_node(
                    item, item_path, is_directory, parent_node_path, 
                    size=os.path.getsize(item_path) if not is_directory else 0,
                    extension=os.path.splitext(item)[1] if not is_directory else "",
                    emoji=emoji
                )
                
                tree_id = self.tree.insert(
                    parent_tree_id, "end", 
                    text=display_text, 
                    values=('',),
                    tags=(item_path,),
                    open=False
                )
                
                self.path_to_item_id[item_path] = tree_id
                
                if is_directory:
                    self._populate_tree(tree_id, item_path, item_path)
                        
        except PermissionError:
            pass
        except Exception as e:
            print(f"DEBUG: Error populating tree: {e}")