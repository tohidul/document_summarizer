import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest

nlp = spacy.load('en_core_web_sm')

document = "Machine learning (ML) is the scientific study of algorithms and statistical models that computer systems use to progressively improve their performance on a specific task. Machine learning algorithms build a mathematical model of sample data, known as “training data”, in order to make predictions or decisions without being explicitly programmed to perform the task. Machine learning algorithms are used in the applications of email filtering, detection of network intruders, and computer vision, where it is infeasible to develop an algorithm of specific instructions for performing the task. Machine learning is closely related to computational statistics, which focuses on making predictions using computers. The study of mathematical optimization delivers methods, theory and application domains to the field of machine learning. Data mining is a field of study within machine learning and focuses on exploratory data analysis through unsupervised learning. In its application across business problems, machine learning is also referred to as predictive analytics."


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

doc = nlp(document)
keywords = filter_tokens(doc)
word_freq = count_word_frquency(keywords)
sentence_strength = weighing_sentences(doc, word_freq)
print(get_summarized_text(sentence_strength, 3))

# print(word_freq)
# n = len(list(doc.sents))
# print(n)