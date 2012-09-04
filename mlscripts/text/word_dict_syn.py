#!/usr/local/bin/python
# coding: UTF-8

# released under bsd licence
# see LICENCE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Thomas Niederberger

from mlscripts.text.utilities import *
from mlscripts.text.word_desc import WordDesc
from numpy import argsort
from nltk.stem.snowball import SnowballStemmer

class WordDictSyn:
    def __init__(self):
        self.__words = {}
        self.__stemmer = SnowballStemmer("german", ignore_stopwords=False)
        self.__id_mapping = {} 
        self.__current_mapping_id = 0
    
    def analyze(self, word_list):
        cleaned_list = []
        
        for word in word_list:
            #word to lower
            word = word.lower()
            #word replace special chars
            word = remove_special_chars(word)
            #word stem
            word = self.__stemmer.stem(word)
            cleaned_list.append(word)
        sorted_indices = argsort(cleaned_list)
        #cleaned_list.sort()
        previous_word = None
        for i in sorted_indices:
            stem = cleaned_list[i]
            if stem in self.__words:
                item = self.__words[stem]
                item.add_variant(word_list[i])
                if stem != previous_word:
                    item.document_count += 1
            else:
                item = WordDesc(stem)
                item.add_variant(word_list[i])
                self.__words[stem] = item
                
    def get_word_ids(self, word):
        word = word.lower()
        #word replace special chars
        word = remove_special_chars(word)
        #word stem
        word = self.__stemmer.stem(word)
        entry = self.__words[word]
        if entry == None:
            return None
        #no id means this word has synonyms
        if entry.id == None:
            return [self.__id_mapping[key] for key in entry.syngroups]
        else: #no synonyms -> return word id
            return [entry.id]            
    
    @property
    def size(self):
        return self.__current_mapping_id
                
    def print_variants(self):
        for stem, desc in self.__words.iteritems():
            if len(desc.variants) > 1:
                print '%s (%s): %s' % (stem, desc.is_noun(), desc.variants)
                
    def print_synonyms(self):
        for stem, desc in self.__words.iteritems():
            if len(desc.syngroups) > 1:
                strings = [ thes.get_syngroup(id) for id in desc.syngroups] # if self.get_word_ids(s) != None]
                print '%s: %s' % (stem, strings)                
                
    def fit_synonyms(self, thes):
        for key, entry in self.__words.iteritems():
            entry.syngroups = thes.find(key)
            if len(entry.syngroups) > 0:
                for id in entry.syngroups:
                    if id not in self.__id_mapping:
                        self.__id_mapping[id] = self.__current_mapping_id
                        self.__current_mapping_id += 1
            #word has no synonyms, but increase counter by one to leave some space in the matrix for this word
            else:
                entry.id = self.__current_mapping_id
                self.__current_mapping_id += 1

    def get_by_id(self, id):
        for key, entry in self.__words.iteritems():
            if entry.id == id:
                return key
        for key, temp_id in self.__id_mapping.iteritems():
            if temp_id == id:
                return thes.get_syngroup(key)
