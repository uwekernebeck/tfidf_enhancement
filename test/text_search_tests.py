import unittest
import os
from pathlib import Path

from typing import List
from src.text_index import TextIndex
from src.text_search import TextSearch
from src.word_set_builder import WordSetBuilder
from src.word_tokenizer import WordTokenizer
from src.word_set_manager import WordSetManager


class TextSearchTestCase(unittest.TestCase):

    def test_find_text_without_exact_match(self):
        texts = [
            'the man is in the garden',
            'the women is in the kitchen'
        ]
        keywords = ["grandfather", "in"]
        text_index = self.__create_text_index(texts, self.__create_word_set_manager())

        text_search = TextSearch(text_index)
        results = text_search.find_texts(keywords)

        self.assertTrue(results[0].find("man") > -1)

    def test_find_text_with_exact_match(self):
        texts = [
            'the man is in the garden',
            'the boy is in the kitchen'
        ]
        keywords = ["man", "in"]
        text_index = self.__create_text_index(texts, self.__create_word_set_manager())

        text_search = TextSearch(text_index)
        results = text_search.find_texts(keywords)

        self.assertTrue(results[0].find("man") > -1)

    def test_find_text_with_automatically_created_word_categories(self):
        texts = [
            'the man is running in the garden',
            'the man is waiting in the kitchen'
        ]
        keywords = ["man", "moving"]
        text_index = self.__create_text_index(texts, self.__create_sts_file_word_set_manager())

        text_search = TextSearch(text_index)
        results = text_search.find_texts(keywords)

        self.assertTrue(results[0].find("running") > -1)

    def __create_text_index(self, texts: List[str], word_set_manager: WordSetManager) -> TextIndex:
        tokenizer = WordTokenizer()
        text_index = TextIndex(word_set_manager, tokenizer)
        for text in texts:
            text_index.add(text)
        return text_index

    def __create_word_set_manager(self) -> WordSetManager:
        word_set_manager = WordSetManager()
        word_set_manager.add('male_person', {'man', 'boy', 'grandfather'})
        word_set_manager.add('person_moving', {'go', 'went', 'run'})
        return word_set_manager

    def __create_sts_file_word_set_manager(self) -> WordSetManager:
        file_name = os.path.join(Path(__file__).parent, 'data/train.jsonl')
        tokenizer = WordTokenizer()
        word_set_builder = WordSetBuilder(tokenizer)
        word_sets = word_set_builder.create_sets_from_sts_file(file_name)
        word_set_manager = WordSetManager()
        word_set_manager.add_sets(word_sets)
        return word_set_manager

if __name__ == '__main__':
    unittest.main()
