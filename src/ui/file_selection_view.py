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

        # Path selection frame
        path_frame = ttk.Frame(self.frame)
        path_frame.pack(fill=tk.X, padx=5, pady=5)

        self.path_input = ttk.Entry(path_frame)
        self.path_input.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=(0, 5))

        browse_button = ttk.Button(path_frame, text="Browse...", command=self.open_folder_dialog)
        browse_button.pack(side=tk.LEFT)

        # Tree configuration with proper hierarchy display
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0,5))

        self.tree = ttk.Treeview(tree_frame, show='tree headings', columns=('selected',))
        self.tree.heading('#0', text='Name')
        self.tree.heading('selected', text='Selected')
        self.tree.column('#0', width=400, anchor='w')
        self.tree.column('selected', width=80, anchor='center')

        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        v_scrollbar.pack(side="right", fill="y")
        
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        h_scrollbar.pack(side="bottom", fill="x")
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)

        parent.add(self.frame, text="Select Files")

        # Bind click events
        self.tree.bind("<Button-1>", self.on_tree_click)
        
        # Initialize with current directory
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
            
            if item and column == "#2":  # Selected column
                self.toggle_item_selection(item)

    def toggle_item_selection(self, item_id):
        """Toggle the selection state of an item"""
        try:
            # Get the file path from the item's tags
            tags = self.tree.item(item_id, 'tags')
            if not tags:
                return
                
            file_path = tags[0]
            file_node = self.state.file_tree.get_node_by_path(file_path)
            
            if file_node:
                # Toggle the selection state
                file_node.is_selected = not file_node.is_selected
                
                print(f"DEBUG: Toggled selection for {file_path} -> {file_node.is_selected}")
                
                # Load content if it's a file and now selected
                if file_node.is_selected and not file_node.is_directory:
                    file_node.load_content()
                    print(f"DEBUG: Content loaded for {file_path}, size: {len(file_node.content or '') if file_node.content else 0} chars")
                
                # Update the visual state
                self.update_tree_item_selection(item_id, file_node.is_selected)
                
                # If it's a directory, select/deselect all children
                if file_node.is_directory:
                    self._toggle_children_selection(item_id, file_node, file_node.is_selected)
        except Exception as e:
            print(f"DEBUG: Error in toggle_item_selection: {e}")

    def _toggle_children_selection(self, parent_id, parent_node, selected):
        """Recursively toggle selection of all children in the tree and data structure"""
        # Toggle in tree view
        for child_id in self.tree.get_children(parent_id):
            try:
                tags = self.tree.item(child_id, 'tags')
                if not tags:
                    continue
                    
                file_path = tags[0]
                file_node = self.state.file_tree.get_node_by_path(file_path)
                
                if file_node:
                    file_node.is_selected = selected
                    
                    if selected and not file_node.is_directory:
                        file_node.load_content()
                    
                    self.update_tree_item_selection(child_id, selected)
                    
                    if file_node.is_directory:
                        self._toggle_children_selection(child_id, file_node, selected)
            except Exception as e:
                print(f"DEBUG: Error toggling child: {e}")

    def update_tree_item_selection(self, item_id, is_selected):
        """Update the visual representation of a tree item's selection state"""
        self.tree.set(item_id, 'selected', '✓' if is_selected else '')

    def populate_tree(self, path):
        """Populate the tree with files and directories"""
        self.path_input.delete(0, tk.END)
        self.path_input.insert(0, path)
        self.tree.delete(*self.tree.get_children())
        self.emoji_assigner = EmojiAssigner()
        
        # Reset the file tree in app state
        self.state.file_tree = FileTree()
        
        print(f"DEBUG: Populating tree for path: {path}")
        self._populate_tree("", path, None)

    def _populate_tree(self, parent_tree_id, current_path, parent_node_path, indent_level=0):
        """Populate the tree with files and directories with proper indentation"""
        try:
            items = []
            # Get all items and sort them (directories first, then files)
            for item in os.listdir(current_path):
                item_path = os.path.join(current_path, item)
                is_directory = os.path.isdir(item_path)
                items.append((item, item_path, is_directory))
            
            # Sort: directories first, then alphabetically
            items.sort(key=lambda x: (not x[2], x[0].lower()))
            
            for item, item_path, is_directory in items:
                # Create indentation for visual hierarchy
                indent = "    " * indent_level  # 4 spaces per level
                
                if is_directory:
                    emoji = self.emoji_assigner.get_emoji("folder")
                    # Add node to file tree
                    node = self.state.file_tree.add_node(
                        item, item_path, True, parent_node_path, emoji=emoji
                    )
                    
                    # Add to tree view with indentation
                    display_name = f"{indent}{emoji} {item}"
                    tree_id = self.tree.insert(
                        parent_tree_id, "end", 
                        text=display_name,
                        values=('',),
                        tags=(item_path,),
                        open=False
                    )
                    
                    print(f"DEBUG: Added directory: {item_path}")
                    
                    # Recursively populate the directory
                    self._populate_tree(tree_id, item_path, item_path, indent_level + 1)
                else:
                    _, extension = os.path.splitext(item)
                    emoji = self.emoji_assigner.get_emoji(extension)
                    size = os.path.getsize(item_path)
                    
                    # Add node to file tree
                    node = self.state.file_tree.add_node(
                        item, item_path, False, parent_node_path, 
                        size=size, extension=extension, emoji=emoji
                    )
                    
                    # Add to tree view with indentation
                    display_name = f"{indent}{emoji} {item}"
                    tree_id = self.tree.insert(
                        parent_tree_id, "end", 
                        text=display_name,
                        values=('',),
                        tags=(item_path,)
                    )
                    
                    print(f"DEBUG: Added file: {item_path} (extension: {extension})")
                    
        except PermissionError as e:
            print(f"DEBUG: Permission denied for {current_path}: {e}")
        except Exception as e:
            print(f"DEBUG: Error populating tree: {e}")