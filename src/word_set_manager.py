"""Provides an index to associate a list of word set to each element."""

from typing import Set, Dict, List
import json
import uuid


class WordSet:
    """
        Represents a set of strings and a label to identify the set.
        It is used as a helper for the word set manager.
    """
    def __init__(self, label: str, elements: Set[str]):
        self.label = label
        self.elements = elements

    def get_label(self):
        return self.label

    def get_elements(self):
        return self.elements


class WordSetManager:
    """
        Provides access to the word sets that are associated with an element (string)
    """
    def __init__(self):
        self.category_to_sets_map: Dict[str, WordSet] = {}
        self.element_to_word_sets_map: Dict[str, Set[WordSet]] = {}

    def get_word_sets_for_element(self, word: str) -> Set[WordSet]:
        if word not in self.element_to_word_sets_map:
            return set()
        return self.element_to_word_sets_map.get(word)

    def add_sets(self, word_sets: List[Set[str]]):
        for word_set in word_sets:
            label = str(uuid.uuid4())
            self.add(label, word_set)

    def add(self, category: str, elements: Set[str]):
        element_set = set(elements)
        new_word_set = WordSet(category, element_set)
        if category in self.category_to_sets_map:
            for element in elements:
                self.category_to_sets_map.get(category).elements.update(element)
        else:
            self.category_to_sets_map[category] = new_word_set

        for element in elements:
            if element in self.element_to_word_sets_map:
                self.element_to_word_sets_map.get(element).add(new_word_set)
            else:
                self.element_to_word_sets_map[element] = set()
                self.element_to_word_sets_map[element].add(new_word_set)

    def save(self, file_name: str):
        with open(file_name, mode='w', encoding='utf-8') as file:
            json.dump(self, file)

    def load(self, file_name: str):
        with open(file_name, mode='r', encoding='utf-8') as file:
            word_set_manager = json.load(file)
            self.element_to_word_sets_map = word_set_manager.element_to_word_sets_map
            self.category_to_sets_map = word_set_manager.category_to_sets_map
