""" The text index is inverted index for given set of texts."""

from dataclasses import dataclass

from typing import List, Dict, Set
from src.word_tokenizer import WordTokenizer
from src.word_set_manager import WordSetManager, WordSet


@dataclass(frozen=True)
class Element:
    value: str
    category_label: str | None
    is_category: bool


class TextIndex:
    """
        Represents an inverted index from element to text.
        However, not only the words of the text but also the categories
        for the word are stored.
        In addition, for the BM25 scoring the element frequency and
        average text length is stored.
    """
    def __init__(self, word_set_manager: WordSetManager, tokenizer: WordTokenizer):
        if word_set_manager is None or tokenizer is None:
            raise ValueError('word set manager and tokenizer must be defined')
        self.word_set_manager = word_set_manager
        self.tokenizer = tokenizer
        self.element_to_text_map: Dict[Element, Set[int]] = {}
        self.texts: List[str] = []
        self.text_index_to_word_length_map: Dict[int, int] = {}
        self.average_text_length = 0
        self.element_to_text_index_to_frequency_map: Dict[Element, Dict[int, int]] = {}

    def add(self, text: str):
        if text is None:
            return

        self.texts.append(text)

        elements = self.create_elements_for_text(text)

        words = filter(lambda e: not e.is_category, elements)
        word_length = len(list(words))
        text_index = len(self.texts) - 1
        self.text_index_to_word_length_map[text_index] = word_length
        self.average_text_length = (self.average_text_length * (len(self.texts) - 1) + word_length) / \
                                   len(self.texts)

        for element in elements:
            if element in self.element_to_text_index_to_frequency_map:
                text_index_to_frequency_map = self.element_to_text_index_to_frequency_map.get(element)
                if text_index in text_index_to_frequency_map:
                    frequency = text_index_to_frequency_map[text_index]
                    self.element_to_text_index_to_frequency_map[element][text_index] = frequency + 1
                else:
                    self.element_to_text_index_to_frequency_map[element][text_index] = 1
            else:
                self.element_to_text_index_to_frequency_map[element] = {}
                self.element_to_text_index_to_frequency_map[element][text_index] = 1

            if element in self.element_to_text_map:
                self.element_to_text_map.get(element).add(text_index)
            else:
                text_index_set = {text_index}
                self.element_to_text_map[element] = text_index_set

    def create_elements_for_text(self, text: str) -> List[Element]:
        if text is None or text.isspace():
            return []
        words = [word.text for word in self.tokenizer.tokenize(text)]
        return self.create_elements_for_words(words)

    def create_elements_for_words(self, words: List[str]) -> List[Element]:
        result = []
        for word in words:
            element = Element(word, None, False)
            result.append(element)
            categories = self.word_set_manager.get_word_sets_for_element(word)
            for category in categories:
                category_element = self.create_category_element(category)
                result.append(category_element)
        return result

    def create_category_element(self, category: WordSet) -> Element:
        return Element(value='<<' + category.get_label() + '>>', category_label=category.label, is_category=True)

    def get_texts_for_element(self, element: Element) -> List[str]:
        if element not in self.element_to_text_map:
            return []
        return [self.texts[idx] for idx in self.element_to_text_map.get(element)]

    def get_element_frequency(self, element: Element, text_index: int) -> int:
        if element not in self.element_to_text_index_to_frequency_map:
            return 0
        text_index_to_frequency_map = self.element_to_text_index_to_frequency_map.get(element)
        if text_index in text_index_to_frequency_map:
            return text_index_to_frequency_map[text_index]
        return 0

    def get_word_length(self, text_index: int) -> int:
        if text_index in self.text_index_to_word_length_map:
            return self.text_index_to_word_length_map.get(text_index)
        return 0

    def get_number_of_category_elements(self, category: str) -> int:
        if category in self.word_set_manager.category_to_sets_map:
            return len(self.word_set_manager.category_to_sets_map.get(category).elements)

    def get_average_text_length(self):
        return self.average_text_length
