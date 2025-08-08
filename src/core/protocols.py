from typing import Protocol

class MarkdownContent(Protocol):
    def to_markdown(self) -> str:
        ...
