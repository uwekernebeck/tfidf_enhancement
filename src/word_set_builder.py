"""Builds sets of words using the embeddings from the english spacy model."""

from typing import List, Dict, Set
import json
import hdbscan
import sklearn.cluster
from spacy.tokens import Token
import numpy as np
from numpy import dot
from numpy.linalg import norm


from src.word_tokenizer import WordTokenizer


class WordSetBuilder:
    """
        To create the word sets necessary for the improved TFIDF text scoring, this
        class uses the word embeddings of an english spacy language model to
        create the words sets automatically.
    """
    def __init__(self, tokenizer: WordTokenizer):
        if tokenizer is None:
            raise ValueError('tokenizer must be defined')
        self.tokenizer = tokenizer

    def create_sets_from_sts_file(self, file_name: str, number_of_lines: int = 100) -> List[Set[str]]:
        """
            Uses a file from the STS benchmark (Semantic Textual Similarity) to create a word list
        :param file_name: Name of the file from the STS benchmark
        :param number_of_lines: Number of lines that should be used for the set creation
        :return: Provides the found word sets
        """
        tokens = []
        with open(file_name, mode='r', encoding='utf-8') as f:
            for _ in range(number_of_lines):
                json_str = f.readline()
                data = json.loads(json_str)
                tokens.extend(self.tokenizer.tokenize(data['sentence1']))
                tokens.extend(self.tokenizer.tokenize(data['sentence2']))

        word_to_token_map = {token.text: token for token in tokens if not token.is_punct}
        filtered_tokens = {word_to_token_map[word] for word in word_to_token_map.keys()}
        return self.create_sets_from_token_list(filtered_tokens)

    def create_sets_from_word_list(self, word_list: List[str] | Set[str]) -> List[Set[str]]:
        tokens = [self.tokenizer.tokenize(word) for word in word_list]
        return self.create_sets_from_token_list(tokens)

    def create_sets_from_token_list(self, tokens: List[Token]) -> List[Set[str]]:
        word_sets = self.__create_word_sets(tokens)
        result = [word_sets[label] for label in word_sets.keys() if label != -1]
        uncategorized_set = word_sets[-1]
        self.__improve_result(result, uncategorized_set)
        return result

    def __improve_result(self, result: List[Set[str]], words: List[str]):
        if words is None or len(words) < 3:
            return
        tokens = [self.tokenizer.tokenize(word) for word in words]
        word_sets = self.__create_word_sets(tokens)
        for label in word_sets.keys():
            if label != -1:
                result.append(word_sets[label])
        if -1 in word_sets:
            uncategorized_set = word_sets[-1]
            if len(uncategorized_set) < len(words):
                self.__improve_result(result, uncategorized_set)
        return

    def __create_word_sets(self, words: List[Token]) -> Dict[str, Set[str]]:
        """
            Uses cluster algorithms to find a sets of words based on the word embedding
            similarity.
        :param words: List of tokens containing the embedding vectors
        :return: Provides a dictionary with category label as key and the set of words as value
        """
        # extract embeddings created during tokenization
        word_to_vector_map = {word.text: word.vector for word in words if word.has_vector}
        word_set = list(word_to_vector_map.keys())
        token_vectors = [word_to_vector_map[word] for word in word_set if word in word_to_vector_map.keys()]

        # create clusters even for small word sets
        optics = sklearn.cluster.OPTICS(min_samples=2)
        optics.fit(token_vectors)

        # create clusters
        distance_matrix = self.__compute_distance_matrix(token_vectors)
        hdb = hdbscan.HDBSCAN(metric='precomputed', algorithm='best', min_cluster_size=2)
        hdb.fit(distance_matrix)

        number_of_labels_optics = len(set(optics.labels_))
        number_of_labels_hdbscan = len(set(hdb.labels_))
        if number_of_labels_hdbscan > number_of_labels_optics:
            return self.__create_word_sets_from_clusters(hdb, word_set)
        return self.__create_word_sets_from_clusters(optics, word_set)

    def __create_word_sets_from_clusters(self, hdb, word_set) -> Dict[str, Set[str]]:
        sets = {}
        for idx in range(len(hdb.labels_)):
            label = hdb.labels_[idx]
            if label in sets.keys():
                s = sets[label]
            else:
                s = set()
                sets[label] = s
            s.add(word_set[idx])
        return sets

    def __compute_distance(self, x, y) -> float:
        similarity = dot(x, y) / (norm(x) * norm(y))
        return 1 - similarity

    def __compute_distance_matrix(self, words):
        result = []
        for _, x in enumerate(words):
            list = []
            result.append(list)
            for _, y in enumerate(words):
                dist = self.__compute_distance(x, y)
                list.append(dist)
        return np.array(result)
