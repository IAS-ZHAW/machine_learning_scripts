#!/usr/local/bin/python
# coding: UTF-8

# released under bsd licence
# see LICENCE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Thomas Niederberger

import re
import numpy as np

from scikits.learn.feature_extraction.text import WordNGramAnalyzer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from text.thes.openthesaurus import OpenThesaurus

replacements = {u'ä' : u'a', u'ö' : u'o', u'ü' : u'u', u'é' : u'e', u'à' : u'a', u'è' : u'e', u'ß' : u'ss'}
thes = OpenThesaurus(all_lowercase = False, remove_remarks = True)

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

def remove_special_chars(document, repl = replacements):
    for key, value in repl.items():
        document = document.replace(key, value)
    return document

def remove_special_chars_list(documents, repl = replacements):
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

def thesaurus_extend_matrix(word_matrix):
    """Extend word_matrix.
    Look up each word in a thesaurus and add synonyms to matrix.
    """ 
    for i in range(len(word_matrix)):
        for j in range(len(word_matrix[i])):
            synonyms = thes.find_word_stem(word_matrix[i][j])
            word_matrix[i].append(synonyms)