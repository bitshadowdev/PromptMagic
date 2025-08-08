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

        path_frame = ttk.Frame(self.frame)
        path_frame.pack(fill=tk.X, padx=5, pady=5)

        self.path_input = ttk.Entry(path_frame)
        self.path_input.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=(0, 5))

        browse_button = ttk.Button(path_frame, text="Browse...", command=self.open_folder_dialog)
        browse_button.pack(side=tk.LEFT)

        # Configure the tree with a checkbox column
        self.tree = ttk.Treeview(self.frame, columns=('selected', 'name'), show='tree')
        self.tree.heading('#0', text='')
        self.tree.column('#0', width=0, stretch=tk.NO)  # Hide the first column
        self.tree.heading('selected', text='')
        self.tree.column('selected', width=30, anchor='center')
        self.tree.heading('name', text='Name')
        self.tree.column('name', width=400, anchor='w')
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0,5))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        parent.add(self.frame, text="Select Files")

        # Bind single click to toggle selection
        self.tree.bind("<Button-1>", self.on_tree_click)
        
        # Store item IDs for quick lookup
        self.item_ids = {}
        
        self.populate_tree(os.path.abspath('.'))

    def open_folder_dialog(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.populate_tree(folder_path)

    def on_tree_click(self, event):
        """Handle click events on the treeview"""
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            item = self.tree.identify_row(event.y)
            column = self.tree.identify_column(event.x)
            
            if column == "#1":  # Checkbox column
                self.toggle_item_selection(item)

    def toggle_item_selection(self, item_id):
        """Toggle the selection state of an item"""
        # Get the file path from the item's tags
        file_path = self.tree.item(item_id, 'tags')[0]
        file_node = self.state.file_tree.get_node_by_path(file_path)
        
        if file_node:
            # Toggle the selection state
            file_node.is_selected = not file_node.is_selected
            
            # Update the visual state
            self.update_tree_item_selection(item_id, file_node.is_selected)
            
            # If it's a directory, select/deselect all children
            if file_node.is_directory:
                self._toggle_children_selection(item_id, file_node.is_selected)

    def _toggle_children_selection(self, parent_id, selected):
        """Recursively toggle selection of all children in the tree"""
        for child_id in self.tree.get_children(parent_id):
            file_path = self.tree.item(child_id, 'tags')[0]
            file_node = self.state.file_tree.get_node_by_path(file_path)
            if file_node:
                file_node.is_selected = selected
                self.update_tree_item_selection(child_id, selected)
                if file_node.is_directory:
                    self._toggle_children_selection(child_id, selected)

    def update_tree_item_selection(self, item_id, is_selected):
        """Update the visual representation of a tree item's selection state"""
        self.tree.set(item_id, 'selected', '✓' if is_selected else '')
        
        # Also update the visual style if needed
        if is_selected:
            self.tree.item(item_id, tags=('selected',))
        else:
            self.tree.item(item_id, tags=())

    def populate_tree(self, path):
        self.path_input.delete(0, tk.END)
        self.path_input.insert(0, path)
        self.tree.delete(*self.tree.get_children())
        self.emoji_assigner = EmojiAssigner()
        # We will rebuild the tree in the app state
        self.state.file_tree = FileTree()
        self._populate_tree("", path, "", self.state.file_tree.root)

    def _populate_tree(self, parent_tree_id, current_path, parent_node_path, file_tree_root):
        """Populate the tree with files and directories"""
        try:
            for item in sorted(os.listdir(current_path), key=lambda x: (not os.path.isdir(os.path.join(current_path, x)), x.lower())):
                item_path = os.path.join(current_path, item)
                is_directory = os.path.isdir(item_path)
                
                if is_directory:
                    emoji = self.emoji_assigner.get_emoji("folder")
                    node = self.state.file_tree.add_node(item, item_path, True, parent_node_path, emoji=emoji)
                    tree_id = self.tree.insert(
                        parent_tree_id, "end", 
                        text=f"{emoji} {item}", 
                        values=('', f"{emoji} {item}"),
                        tags=(item_path,),
                        open=False
                    )
                    # Store the mapping from path to tree ID
                    self.item_ids[item_path] = tree_id
                    
                    # Recursively populate the directory
                    self._populate_tree(tree_id, item_path, item_path, file_tree_root)
                else:
                    _, extension = os.path.splitext(item)
                    emoji = self.emoji_assigner.get_emoji(extension)
                    size = os.path.getsize(item_path)
                    node = self.state.file_tree.add_node(
                        item, item_path, False, parent_node_path, 
                        size=size, extension=extension, emoji=emoji
                    )
                    tree_id = self.tree.insert(
                        parent_tree_id, "end", 
                        text=item,
                        values=('', f"{emoji} {item}"),
                        tags=(item_path,)
                    )
                    # Store the mapping from path to tree ID
                    self.item_ids[item_path] = tree_id
                    
                    # Update selection state if needed
                    if node.is_selected:
                        self.update_tree_item_selection(tree_id, True)
                        
        except PermissionError:
            # Skip directories we don't have permission to access
            pass