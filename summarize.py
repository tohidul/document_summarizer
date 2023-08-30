import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest

npl = spacy.load('en')

document = ""

doc = nlp(document)
