from typing import Dict

class EmojiAssigner:
    def __init__(self):
        self.emoji_map: Dict[str, str] = {
            ".py": "🐍",
            ".js": "📜",
            ".ts": "📜",
            ".java": "☕",
            ".c": "🇨",
            ".cpp": "🇨",
            ".cs": "🇨#",
            ".go": "🐹",
            ".rb": "💎",
            ".php": "🐘",
            ".html": "🌐",
            ".css": "🎨",
            ".json": "📦",
            ".xml": "📄",
            ".md": "📝",
            ".txt": "📄",
            ".gitignore": "🙈",
            ".pdf": "📄",
            ".png": "🖼️",
            ".jpg": "🖼️",
            ".jpeg": "🖼️",
            ".gif": "🖼️",
            ".svg": "🖼️",
            "default": "📄",
            "folder": "📁"
        }

    def get_emoji(self, extension: str) -> str:
        """
        Assigns an emoji to a file extension.
        This acts as a simple finite state machine.
        """
        return self.emoji_map.get(extension, self.emoji_map["default"])
