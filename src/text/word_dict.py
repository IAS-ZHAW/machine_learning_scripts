#!/usr/local/bin/python
# coding: UTF-8

# released under bsd licence
# see LICENCE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Thomas Niederberger

from text.utilities import *
from text.word_desc import WordDesc
from numpy import argsort

class WordDict:
    def __init__(self):
        self.__current_id = 0
        self.__words = {}
    
    def vectorize(self, word_list):
        """Word_list must be in a sorted order"""
        #cleaned_list.sort()
        id_list = []
        for stem in word_list:
            if stem in self.__words:
                item = self.__words[stem]
                if item.document_count >= 2:
                    id_list.append(item.id)
            else:
                raise NameError('unknown word %s' % stem)
        return id_list
    
    def fit(self, word_list):
        """Word_list must be in a sorted order"""
        #cleaned_list.sort()
        previous_word = None
        for stem in word_list:
            if stem in self.__words:
                item = self.__words[stem]
                if stem != previous_word:
                    item.document_count += 1
            else:
                item = WordDesc(self.__current_id, stem)
                self.__words[stem] = item
                self.__current_id += 1

    @property
    def size(self):
        return self.__current_id
    
    def id_mapping_by_document_frequency(self, frequency=2):
        c = 0
        mapping = {}
        for key, word in self.__words.items():
            if word.document_count >= frequency:
                mapping[word.id] = c
                c += 1
        return mapping
    
    def get_by_id(self, id): 
        for key, entry in self.__words.iteritems(): 
            if entry.id == id: 
                return key 
