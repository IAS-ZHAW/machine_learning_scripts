#!/usr/local/bin/python
# coding: UTF-8

# released under bsd licence
# see LICENCE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Thomas Niederberger

import re
import numpy as np

from scikits.learn.feature_extraction.text import WordNGramAnalyzer
from nltk.corpus import stopwords

replacements = {'ä' : 'a', 'ö' : 'o', 'ü' : 'u', 'é' : 'e', 'à' : 'a', 'è' : 'e', 'ß' : 'ss', "buddel" : '', "willi" : '', "kunst" : '', "kunstler" : '', " künstler" : '', " werk" : '', " art" : '', " museum" : '', " bad" : ''}

def to_lower(documents):
    """Transforms a list of strings to lowercase"""
    for i in range(len(documents)):
        documents[i] = documents[i].lower()
        lang = language_decider(documents[i])
        if lang > 0:
            print str(lang) + ": " + documents[i]
    return documents

def remove_urls(documents):
    """Removes URLs from a list of strings"""
    for i in range(len(documents)):
        #get rid of URLs
        documents[i] = re.sub('https://\S+', '', documents[i])
        documents[i] = re.sub('http://\S+', '', documents[i])
        documents[i] = re.sub('www\.\S+', '', documents[i])
    return documents


def remove_special_chars(documents):
    """Removes special characters like ä, ö, ü, é from a list of strings"""
    for i in range(len(documents)):        
        for key, value in replacements.items():
            documents[i] = documents[i].replace(key, value)    
    return documents

def language_decider(document):
    """A very simple approach to find out about the language of a string
    only supports german, english, french. Based on counting special words."""
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
    analyzer = WordNGramAnalyzer()
    i = 0
    for doc in words:
        words[i] = [ elem for elem in doc if elem not in stopwords.words(language) ]
        i = i + 1
    return words