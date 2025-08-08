import unittest
from src.core.app_state import AppState
from src.core.file_tree import FileTree

class TestAppState(unittest.TestCase):

    def setUp(self):
        AppState._instance = None

    def test_singleton_instance(self):
        instance1 = AppState()
        instance2 = AppState()
        self.assertIs(instance1, instance2)

    def test_initial_state(self):
        state = AppState()
        self.assertIsInstance(state.file_tree, FileTree)
        self.assertIsNone(state.file_tree.root)
        self.assertEqual(state.prompt_template, "")

    def test_state_persistence(self):
        state1 = AppState()
        state1.prompt_template = "test template"
        state1.file_tree.insert("test.txt", "/path/to/test.txt", 100, ".txt", "📄")

        state2 = AppState()
        self.assertEqual(state2.prompt_template, "test template")
        self.assertIsNotNone(state2.file_tree.root)
        self.assertEqual(state2.file_tree.root.name, "test.txt")

if __name__ == '__main__':
    unittest.main()
