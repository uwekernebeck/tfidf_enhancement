import unittest

from src.text_index import TextIndex
from src.word_tokenizer import WordTokenizer
from src.word_set_manager import WordSetManager


class TextIndexTestCase(unittest.TestCase):
    def test_TextIndex_without_word_sets(self):
        text1 = 'the man is in the garden'
        text2 = 'the boy gets angry'
        word_sets_manager = WordSetManager()
        tokenizer = WordTokenizer()

        text_index = TextIndex(word_sets_manager, tokenizer)
        text_index.add(text1)
        text_index.add(text2)

        average_text_length = text_index.average_text_length
        self.assertTrue(average_text_length > 0)

    def test_CreateTextIndex_with_word_sets(self):
        text1 = 'the man is in the garden'
        text2 = 'the boy gets angry'
        word_sets_manager = WordSetManager()
        word_sets_manager.add('noun', {'man', 'boy', 'garden'})
        word_sets_manager.add('verb', {'go', 'went', 'is'})
        tokenizer = WordTokenizer()

        text_index = TextIndex(word_sets_manager, tokenizer)
        text_index.add(text1)
        text_index.add(text2)

        number_of_category_elements = text_index.get_number_of_category_elements('noun')
        self.assertTrue(number_of_category_elements > 0)


if __name__ == '__main__':
    unittest.main()
