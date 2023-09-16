# TFIDF Search Improvement using Word Sets

## Introduction
This is a prototype implementation to show how to
add similarity search to a TFIDF (Term Frequency Inverse Document Frequency) search
as it is used in Elastic Search / Lucene.

The idea is to use sets of similar words instead of an
exact match. The scoring formular is extended and a way is shown to
generate these sets of similar words using a language model. In this case, 
one of spacy's language models is used.

## Installation
Provide a virtual environment with

`python -m venv venv`

for example and install the necessary packages with

`pip install -r requirements.txt`

The software was tested using a python 3.10.2 on macOS 13.5.2 

To run all tests use 

`python -m unittest discover -s test -p "*_tests.py"`

## Usage
The score computation can be found in the TextSearch class.
The automatic building of sets of similar word sets is implemented
in the WordSetBuilder class.


