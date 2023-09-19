from typing import Set, List
import os
import unittest
from pathlib import Path
from src.word_set_builder import WordSetBuilder
from src.word_tokenizer import WordTokenizer


class WordSetBuilderTestCase(unittest.TestCase):
    def test_create_word_sets_from_file(self):
        file_name = os.path.join(Path(__file__).parent, 'data', 'train.jsonl')
        tokenizer = WordTokenizer()
        word_set_builder = WordSetBuilder(tokenizer)
        word_sets = word_set_builder.create_sets_from_sts_file(file_name)
        self.assertTrue(self.__contains_set(word_sets, {"moving", "running"}))

    def __contains_set(self, word_sets: List[Set[str]], required_word_set: Set[str]) -> bool:
        for word_set in word_sets:
            set_found = True
            for word in required_word_set:
                if not word in word_set:
                    set_found = False
                    break
            if set_found:
                print(word_set)
                return True
        return False

if __name__ == '__main__':
    unittest.main()
