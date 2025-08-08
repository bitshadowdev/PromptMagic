import unittest
from src.core.emoji_assigner import EmojiAssigner


class TestEmojiAssigner(unittest.TestCase):
    def test_get_emoji(self):
        assigner = EmojiAssigner()
        self.assertEqual(assigner.get_emoji(".py"), "🐍")
        self.assertEqual(assigner.get_emoji(".js"), "📜")
        self.assertEqual(assigner.get_emoji(".ts"), "📜")
        self.assertEqual(assigner.get_emoji(".java"), "☕")
        self.assertEqual(assigner.get_emoji(".c"), "🇨")
        self.assertEqual(assigner.get_emoji(".cpp"), "🇨")
        self.assertEqual(assigner.get_emoji(".cs"), "🇨#")
        self.assertEqual(assigner.get_emoji(".go"), "🐹")
        self.assertEqual(assigner.get_emoji(".rb"), "💎")
        self.assertEqual(assigner.get_emoji(".php"), "🐘")
        self.assertEqual(assigner.get_emoji(".html"), "🌐")
        self.assertEqual(assigner.get_emoji(".css"), "🎨")
        self.assertEqual(assigner.get_emoji(".json"), "📦")
        self.assertEqual(assigner.get_emoji(".xml"), "📄")
        self.assertEqual(assigner.get_emoji(".md"), "📝")
        self.assertEqual(assigner.get_emoji(".txt"), "📄")
        self.assertEqual(assigner.get_emoji(".gitignore"), "🙈")
        self.assertEqual(assigner.get_emoji(".pdf"), "📄")
        self.assertEqual(assigner.get_emoji(".png"), "🖼️")
        self.assertEqual(assigner.get_emoji(".jpg"), "🖼️")
        self.assertEqual(assigner.get_emoji(".jpeg"), "🖼️")
        self.assertEqual(assigner.get_emoji(".gif"), "🖼️")
        self.assertEqual(assigner.get_emoji(".svg"), "🖼️")
        self.assertEqual(assigner.get_emoji("unknown_extension"), "📄")
        self.assertEqual(assigner.get_emoji("folder"), "📁")


if __name__ == "__main__":
    unittest.main()
