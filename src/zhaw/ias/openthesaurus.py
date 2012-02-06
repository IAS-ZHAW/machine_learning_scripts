#!/usr/local/bin/python
# coding: UTF-8

"""
  - deal with double s
  - deal with ä, ö, ü
  - beginning of word
  - remove remarks
"""
class OpenThesaurus:
    def __init__(self, path="openthesaurus.txt", all_lowercase = False, remove_remarks = True):
        self.all_lowercase = all_lowercase
        self.entries = []
        
        f = open(path, 'r')
        for line in f:
            if line[0] ==  '#': #ignore comments
                continue
            line = line.strip() # get rid of newline
            if all_lowercase:
                line = line.lower()
            self.entries.append(line.rsplit(';'))
  
    def find(self, word):
        l = []
        if self.all_lowercase:
            word = word.lower()
        for word_list in self.entries:
            if word in word_list:
                l.extend(word_list)
        return l

if __name__ == "__main__":
    thes = OpenThesaurus(all_lowercase = True)
    words = thes.find('schlafen')
    print words
    words = thes.find('Tisch')
    print words
    words = thes.find('tisch')
    print words