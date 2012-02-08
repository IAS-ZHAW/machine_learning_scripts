# released under bsd licence
# see LICENSE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Timo Jeranko

import re
import time
import pickle
from classes import *
from functions import *

def read_file(name,named=False,clustered=False):
  f = open(name)
  file = f.read() 
  f.close
  file = re.split('\s*\n',file)
 
  words = file[0].split(";")

  if clustered:
     words = words[0:-1]
  
  data = file[1:-1]
  table = {}
  clusters = {}
  for i,line in enumerate(data):
    vector = re.split(';',line)

    if named:
      key = vector[0]
      key = re.sub('\"','',key)
      vector1 = to_float(vector[1:])
      table[key] = vector1
    else:
      key = "idea"+str(i)
      if clustered:
          table[key] = to_float(vector[0:-1])
          clusters[key] = vector[-1]
      else:
          vector = to_float(vector)
          table[key] = vector
  space = Space(table,words,named=named)

  if clustered:
      return space,clusters
  else:
      return space


def read_file2(name):
  f = open(name)
  file = f.read() 
  f.close
  file = re.split('\s*\n',file)

  words = file[0].split(" ")
  print len(words)
  
#  data = file[0:-1]
  data = file[0:-1]
  matrix = []
  for line in data:
      vector = re.split(' ',line)
    #  print len(vector)
      vector = to_float(vector)
      matrix.append( vector )

  return matrix

def save_map(mymap,filename=False):
    t = int(time.time())
    if filename:
        filename = "data/map-%s.pyc" % filename
    else:
        filename = "data/map-%s.pyc" % t
    f = open(filename,"w")
    pickle.dump(mymap,f)
    f.close()
    


def load_map(filename):
    filename = "data/map-%s.pyc" % filename
    f = open(filename)
    return pickle.load(f)
    f.close()





