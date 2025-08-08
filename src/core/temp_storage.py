import os
import tempfile
import json
from typing import Dict, Any

class TempStorage:
    """Handles temporary storage of selected files content during the workflow"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="prompt_magic_")
        self.content_file = os.path.join(self.temp_dir, "selected_content.json")
        self.markdown_file = os.path.join(self.temp_dir, "content.md")
        
    def save_selected_files(self, file_tree):
        """Save selected files and their markdown content to temporary storage"""
        selected_files = file_tree.get_selected_files()
        content_data = []
        markdown_parts = []
        
        print(f"DEBUG: Saving {len(selected_files)} selected files to temp storage")
        
        for file_node in selected_files:
            # Ensure content is loaded
            if file_node.content is None:
                file_node.load_content()
            
            # Save file data
            file_data = {
                'name': file_node.name,
                'path': file_node.path,
                'extension': file_node.extension,
                'emoji': file_node.emoji,
                'content': file_node.content or "",
                'size': file_node.size
            }
            content_data.append(file_data)
            
            # Generate markdown
            markdown = file_node.to_markdown()
            markdown_parts.append(markdown)
            
            print(f"DEBUG: Saved file {file_node.path} with content size: {len(file_node.content or '')}")
        
        # Save structured data to JSON
        with open(self.content_file, 'w', encoding='utf-8') as f:
            json.dump(content_data, f, indent=2, ensure_ascii=False)
        
        # Save combined markdown
        combined_markdown = "\n\n".join(markdown_parts)
        with open(self.markdown_file, 'w', encoding='utf-8') as f:
            f.write(combined_markdown)
            
        print(f"DEBUG: Saved content to {self.content_file}")
        print(f"DEBUG: Saved markdown to {self.markdown_file}")
        
        return combined_markdown
    
    def load_markdown_content(self) -> str:
        """Load the combined markdown content from temporary storage"""
        try:
            with open(self.markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"DEBUG: Loaded markdown content, size: {len(content)} characters")
                return content
        except FileNotFoundError:
            print("DEBUG: No markdown content found in temp storage")
            return ""
        except Exception as e:
            print(f"DEBUG: Error loading markdown content: {e}")
            return ""
    
    def load_content_data(self) -> list:
        """Load the structured content data from temporary storage"""
        try:
            with open(self.content_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"DEBUG: Loaded {len(data)} files from temp storage")
                return data
        except FileNotFoundError:
            print("DEBUG: No content data found in temp storage")
            return []
        except Exception as e:
            print(f"DEBUG: Error loading content data: {e}")
            return []
    
    def cleanup(self):
        """Clean up temporary files"""
        try:
            if os.path.exists(self.content_file):
                os.remove(self.content_file)
            if os.path.exists(self.markdown_file):
                os.remove(self.markdown_file)
            os.rmdir(self.temp_dir)
            print(f"DEBUG: Cleaned up temp directory: {self.temp_dir}")
        except Exception as e:
            print(f"DEBUG: Error cleaning up temp files: {e}")
    
    def get_temp_dir(self) -> str:
        """Get the temporary directory path"""
        return self.temp_dir