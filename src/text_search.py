"""Implements the similarity search for texts using an extended BM25 score formular"""

from typing import List
import math
from dataclasses import dataclass
from src.text_index import TextIndex, Element


@dataclass
class TextIndexAndScore:
    """
        Container for the text index and score of the text to sort the
        text by score.
    """
    text_index: int
    score: float


class TextSearch:
    """
        Search for texts matching the given query keywords using a BM25 scoring
        with an extension to match the word categories as well.
    """
    def __init__(self, text_index: TextIndex):
        self.text_index = text_index

    def find_texts(self, keywords: List[str]) -> List[str]:
        """
            Using the given keywords the score for all texts is computed to find the best
            matching texts.
        :param keywords: List of words representing the user input
        :return: Provides the list of matching texts with the best matching text at the
        beginning of the list
        """
        keyword_elements = self.text_index.create_elements_for_words(keywords)
        text_indices_with_scores = self.__compute_scores(keyword_elements)
        sorted_text_indices = sorted(text_indices_with_scores, key=lambda x: x.score, reverse=True)
        return [self.text_index.texts[item.text_index] for item in sorted_text_indices]

    def __compute_scores(self, keywords: List[Element]) -> List[TextIndexAndScore]:
        result = []
        for idx in range(len(self.text_index.texts)):
            score_value = 0
            score_categories = 0
            number_of_category_keywords = 0
            score = 0
            for keyword in keywords:
                score += self.__compute_score_for_keyword(keyword, idx)
                if keyword.is_category:
                    score_categories += score
                    number_of_category_keywords += 1
                else:
                    score_value += score
            if number_of_category_keywords > 0:
                total_score = score_value + score_categories / number_of_category_keywords
            else:
                total_score = score_value
            result.append(TextIndexAndScore(idx, total_score))
        return result

    def __compute_score_for_keyword(self, keyword: Element, text_index: int) -> float:
        """
            About the BM25 score computation see https://en.wikipedia.org/wiki/Okapi_BM25
        :param keyword: Element for which the part of the score is computed
        :param text_index: Index of the text that is currently examined
        :return: Score for the given keyword (input)
        """
        b = 0.75
        k1 = 1.5
        frequency_in_text = self.text_index.get_element_frequency(keyword, text_index)
        total_number_of_texts = len(self.text_index.texts)
        average_length_of_texts = self.text_index.average_text_length
        length_of_text_in_words = self.text_index.get_word_length(text_index)
        number_of_texts_containing_word = len(self.text_index.get_texts_for_element(keyword))

        if keyword.is_category:
            number_of_elements_of_category = \
                self.text_index.get_number_of_category_elements(keyword.category_label)
            frequency_in_text = frequency_in_text / number_of_elements_of_category

        idf = math.log((total_number_of_texts - number_of_texts_containing_word + 0.5) / (
                    number_of_texts_containing_word + 0.5) + 1)
        tdf = (frequency_in_text * (k1 + 1)) / (
                    frequency_in_text + k1 * (1 - b + b * length_of_text_in_words / average_length_of_texts)
                )
        return idf * tdf
