
import unittest
from src.core.protocols import MarkdownContent

class ConcreteMarkdownContent(MarkdownContent):
    def to_markdown(self) -> str:
        return "I am markdown content"

class TestProtocols(unittest.TestCase):

    def test_markdown_content_protocol(self):
        content = ConcreteMarkdownContent()
        self.assertEqual(content.to_markdown(), "I am markdown content")

if __name__ == '__main__':
    unittest.main()
