#!/usr/local/bin/python
# coding: UTF-8

# released under bsd licence
# see LICENCE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Thomas Niederberger

import re
import os

"""
  - deal with double s
  - deal with ä, ö, ü
  - remove special classes (vulgäre, derb)
"""
class OpenThesaurus:
    def __init__(self, path=os.path.join(os.path.dirname(__file__), 'openthesaurus.txt'), all_lowercase = False, remove_remarks = True):
        self.__all_lowercase = all_lowercase
        self.__entries = []
        self.__separator = ';'
        
        f = open(path, 'r')
        for line in f:
            if line[0] ==  '#': #ignore comments
                continue
            line = line.strip() # get rid of newline
            if remove_remarks: 
                reg = re.compile(r"(?P<start>;?)\s*\(.*?\)\s*(?P<end>;?)") # remove everything inside brackets
                line = reg.sub(r"\g<start>\g<end>", line)
                
            if self.__all_lowercase:
                line = line.lower()
            self.__entries.append(line)
  
    def find(self, word):
        if self.__all_lowercase:
            word = word.lower()
        return self.find_regex("(^|%s)%s(;|$)" % (self.__separator, word))

    def find_part(self, word):
        if self.__all_lowercase:
            word = word.lower()
        return self.find_regex(".*%s.*" % word)
    
    def find_beginning(self, word):
        if self.__all_lowercase:
            word = word.lower()
        return self.find_regex("(^|%s)%s.*" % (self.__separator, word))
    
    def find_word_stem(self, word):
        if self.__all_lowercase:
            word = word.lower()
        return self.find_regex("(^|%s)%s\w{0,2}(%s|$)" % (self.__separator, word, self.__separator))

    def find_regex(self, regex_pattern):
        l = set([])
        reg = re.compile(regex_pattern)
        for syngroup, line in enumerate(self.__entries):
            if reg.search(line):
                l.add(syngroup)
                #l.update(line.rsplit(self.__separator))
        return l

    def get_syngroup(self, id):
        return self.__entries[id]

if __name__ == "__main__":
    thes = OpenThesaurus(all_lowercase = True)
    words = thes.find('schlafen')
    print words
    words = thes.find('Tisch')
    print words
    words = thes.find('tisch')
    print words
    words = thes.find_part('tisch')
    print words
    words = thes.find_beginning('schlaf')
    print words
    words = thes.find_word_stem('schlaf')
    print words
