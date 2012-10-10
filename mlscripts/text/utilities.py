#!/usr/local/bin/python
# coding: UTF-8

# released under bsd licence
# see LICENCE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Thomas Niederberger

import re
import numpy as np
import logging

from sklearn.feature_extraction.text import TfidfTransformer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from mlscripts.text.thes.openthesaurus import OpenThesaurus
from mlscripts.text.word_dict import *

logger = logging.getLogger(__name__)

replacements = {u'ä' : u'a', u'ö' : u'o', u'ü' : u'u', u'é' : u'e', u'à' : u'a', u'è' : u'e', u'ß' : u'ss', u'â' : u'a', u'û' : u'u', u'ê' : u'e', u'ô' : u'o'}
thes = OpenThesaurus(all_lowercase=False, remove_remarks=True)

def is_stopword(word, language='german'):
    return word in stopwords.words(language)

def to_lower(documents):
    """Transforms a list of strings to lowercase"""
    for i in range(len(documents)):
        documents[i] = documents[i].lower()
    return documents

def remove_urls(documents):
    """Removes URLs from a list of strings"""
    for i in range(len(documents)):
        #get rid of URLs
        documents[i] = re.sub('https://\S+', '', documents[i])
        documents[i] = re.sub('http://\S+', '', documents[i])
        documents[i] = re.sub('www\.\S+', '', documents[i])
    return documents

def remove_words(word_matrix, words):
    for i, w in enumerate(word_matrix):
        word_matrix[i] = [ elem for elem in w if elem.lower() not in words() ]
    return word_matrix

def remove_special_chars(document, repl=replacements):
    for key, value in repl.items():
        document = document.replace(key, value)
    return document

def remove_special_chars_list(documents, repl=replacements):
    """Removes special characters like ä, ö, ü, ß from a list of strings"""
    for i in range(len(documents)):
        documents[i] = remove_special_chars(documents[i], repl)
    return documents

def language_decider(document):
    """A very! simple approach to find out about the language of a string
    Currently only supports german, english and french. Based on counting special words.
    """
    counts = [0, 0, 0]
    counts[0] += document.count(" ein ")
    counts[0] += document.count(" der ")
    counts[0] += document.count(" die ")
    counts[0] += document.count(" das ")
    counts[1] += document.count(" the ")
    counts[2] += document.count(" les ")
    counts[2] += document.count(" la ")
    counts[2] += document.count(" le ")
    return np.argmax(counts)

def remove_stopwords(words, language='german'):
    i = 0
    for w in words:
        words[i] = [ elem for elem in w if elem.lower() not in stopwords.words(language) ]
        i += 1
    return words

"""def remove_stopwords_list(word_lists):
    for index in range(len(word_lists)):
        word_lists[index] = remove_stopwords(word_lists[index])
    return word_lists"""

def convert_to_n_gram_matrix(documents):
    """Split documents to 1 grams"""

    def repl(m):
        #inner_word = list(m.group(2))
        #random.shuffle(inner_word)
        return " " + m.group(3).lower()

    pattern = r'\b\w\w+\b' # pattern to define a word
    compiled = re.compile(pattern, re.UNICODE)
    matrix = []
    for d in documents:
        doc = unicode(d)
        doc = re.sub(r"(\.)(\W*)(.)", repl, doc)
        words = compiled.findall(doc)
        matrix.append(words)
    return matrix

def stem_word_matrix(word_matrix):
    """Stem a matrix of words with a german SnowballStemmer (porter stemmer). 
    during this process the word_matrix will be modified
    """
    stemmer = SnowballStemmer("german", ignore_stopwords=False)
    for i in range(len(word_matrix)):
        for j in range(len(word_matrix[i])):
            word_matrix[i][j] = stemmer.stem(word_matrix[i][j])
    return word_matrix

def clean_texts(texts, projectspecific_replacements={}):
    texts = to_lower(texts)
    texts = remove_urls(texts)
    texts = remove_special_chars_list(texts)
    if id in projectspecific_replacements:
        texts = remove_special_chars_list(texts,)
    word_matrix = convert_to_n_gram_matrix(texts)
    #word_matrix = thesaurus_extend_matrix(word_matrix)
    word_matrix = stem_word_matrix(word_matrix)
    word_matrix = remove_stopwords(word_matrix)
    return word_matrix

def get_word_matrix(text_list, dict):
    for word_list in text_list:
        dict.fit(word_list)
    mapping = dict.id_mapping_by_document_frequency()
    word_matrix = np.zeros((len(text_list), len(mapping)))
    doc_index = 0
    for word_list in text_list:
        index_list = dict.vectorize(word_list)
        #texts_index.append(index_list)
        for i in index_list:
            word_matrix[doc_index, mapping[i]] += 1
        doc_index += 1
    return word_matrix


def thesaurus_extend_matrix(word_matrix):
    """Extend word_matrix.
    Look up each word in a thesaurus and add synonyms to matrix.
    """
    for i in range(len(word_matrix)):
        for j in range(len(word_matrix[i])):
            synonyms = thes.find_word_stem(word_matrix[i][j])
            word_matrix[i].append(synonyms)

def texts_2_tfidf(texts):
    stemmed = clean_texts(texts)
    word_dict = WordDict()
    word_matrix = get_word_matrix(stemmed, word_dict)
    #calculate tag matrix from stemmed words (german stopwords will be removed too. but this should better be done in the beginning)
    #relevant_tags, tag_matrix = generate_tag_matrix(stemmed, 2*tag_weight)
    tf_matrix = tf_idf(word_matrix)
    logger.info('analyze word_matrix of size %s/%s' % tf_matrix.shape)
    logger.debug("first tf-idf row sum %s" % np.sum(tf_matrix[0, :]))
    logger.debug("first tf-idf row not null %s" % np.sum(tf_matrix[0, :] != 0))
    return tf_matrix, word_dict

def tf_idf(tag_matrix):
    #calculate TF-IDF
    tfidf = TfidfTransformer(None, use_idf=True)
    tfidf.fit(tag_matrix)
    tag_matrix = tfidf.transform(tag_matrix)
    dense_tag_matrix = tag_matrix.todense()
    return dense_tag_matrix
