#!/usr/local/bin/python
# coding: UTF-8

# released under bsd licence
# see LICENCE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Thomas Niederberger

class WordDesc:
    def __init__(self, stem):
        self.__id = None
        self.__stem = stem
        self.__title_word = False
        self.__tag_word = False
        self.__syngroups = []
        self.__n_doc = 0
        self.__n_upper = 0
        self.__n_lower = 0
        self.__variants = set([])
        
    def is_noun(self):
        return self.__n_upper >= 1#/ (self.__n_upper + self.__n_lower) >= 0.5
    
    def add_variant(self, variant):
        if variant.istitle():
            self.__n_upper += 1
        else:
            self.__n_lower += 1
        self.__variants.add(variant)
    
    @property
    def stem(self):
        return self.__stem
    
    @property
    def total_count(self):
        return (self.__n_upper + self.__n_lower)
     
    @property
    def document_count(self):
        return self.__n_doc
     
    @document_count.setter
    def document_count(self, new_count):
        self.__n_doc = new_count

    @property
    def variants(self):
        return self.__variants
    
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id
        
    @property
    def syngroups(self):
        return self.__syngroups
    
    @syngroups.setter
    def syngroups(self, syngroups):
        self.__syngroups = syngroups