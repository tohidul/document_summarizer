import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest

nlp = spacy.load('en_core_web_sm')


def filter_tokens(document):
    keywords = []
    stopwords = list(STOP_WORDS)
    pos_tag = ["PROPN", "ADJ", "NOUN", "VERB"]

    for token in document:
        if token.text in stopwords or token.text in punctuation:
            continue
        if token.pos_ in pos_tag:
            keywords.append(token.text)

    return keywords


def count_word_frquency(keywords):
    word_frequency = Counter(keywords)
    maximum_frequency = Counter(keywords).most_common(1)[0][1]
    for word in word_frequency.keys():
        word_frequency[word] = (word_frequency[word]/maximum_frequency)
    return word_frequency


def weighing_sentences(document, keyword_frequencies):
    sentence_strength = {}

    for sentence in document.sents:
        for word in sentence:
            if word.text in  keyword_frequencies.keys():
                if sentence in sentence_strength.keys():
                    sentence_strength[sentence] += keyword_frequencies[word.text]
                else:
                    sentence_strength[sentence] = keyword_frequencies[word.text]

    return sentence_strength


def get_summarized_text(sentence_strength, number_of_sentence):
    if len(sentence_strength.keys()) < number_of_sentence:
        number_of_sentence = len(sentence_strength.keys())
    summarized_sentences = nlargest(number_of_sentence, sentence_strength, key=sentence_strength.get)
    final_sentences = [w.text for w in summarized_sentences]
    summary = ' '.join(final_sentences)
    return summary

