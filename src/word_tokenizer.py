"""Split a text into tokens that also contain embeddings"""

from typing import List
import re
import spacy
from spacy.tokenizer import Tokenizer
from spacy.tokens import Token


class WordTokenizer:
    """
        Convert strings into a list of tokens. It is used in several places so
        this class can be used to configure the tokenizer consistently.
    """
    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')
        infix_re = re.compile(r'''[.\,\?\:\;\...\‘\’\`\“\”\"\'~]''')
        self.tokenizer = Tokenizer(self.nlp.vocab, infix_finditer=infix_re.finditer)

    def tokenize(self, text: str) -> List[Token]:
        return self.tokenizer(text)
