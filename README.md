# TFIDF Search Improvement using Word Sets

## Introduction
This is a prototype implementation to show how to
add similarity search to a TFIDF (Term Frequency Inverse Document Frequency) search
as it is used in Elasticsearch/Lucene.

The idea is to use sets of similar words in addition to
exact word matches. The scoring formular is extended and a way is shown to
generate these sets of similar words using a language model. In this case, 
a language model from the NLP software library spaCy is used.

## Installation
Provide a virtual environment with

`python -m venv venv`

for example, activate it with

`source ./venv/bin/activate`

in case you are using venv and working with macOS or linux. Then install the necessary packages with

`pip install -r requirements.txt`

After spaCy is installed download the required language model using

`python -m spacy download en_core_web_lg`

The software was tested using a python 3.10.2 on macOS 13.5.2 

To run all tests use 

`python -m unittest discover -s test -p "*_tests.py"`

## Usage
The score computation can be found in the TextSearch class.
The automatic building of sets of similar word sets is implemented
in the WordSetBuilder class.


