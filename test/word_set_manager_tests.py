import unittest

from src.word_set_manager import WordSetManager


class WordSetManagerTestCase(unittest.TestCase):
    def test_create_word_set_manager(self):
        word_set_manager = WordSetManager()
        word_set_manager.add('noun', {'man', 'boy', 'garden'})
        word_set_manager.add('verb', {'go', 'went', 'is'})
        word_sets = word_set_manager.get_word_sets_for_element('man')
        self.assertEqual(len(word_sets), 1)


if __name__ == '__main__':
    unittest.main()
