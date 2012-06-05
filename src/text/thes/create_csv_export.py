#!/usr/local/bin/python
# coding: UTF-8

# released under bsd licence
# see LICENCE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Thomas Niederberger

import MySQLdb
from ias.clustering.data_handling import *

"""
a script to fetch all synonyms and create an csv-export from OpenThesaurus database
Procedure:

written by Thomas Niederberger
internal use only
"""
 
mysql_opts = { 
    'host': "localhost", 
    'user': "root", 
    'pass': "abc1234", 
    'db':   "atizo" 
    } 
mysql = MySQLdb.connect(mysql_opts['host'], mysql_opts['user'], mysql_opts['pass'], mysql_opts['db'])

project_cursor = mysql.cursor() 
project_query = "select id from ideaproject"
idea_query = """select id, REPLACE(title, '"', ' '), REPLACE(plain_tags, '"', ' '), REPLACE(REPLACE(REPLACE(description, '"', ' '), '\n', ' '), '\r', ' '), author, rate_up, rate_down, created from idea where project = %s order by id asc"""

project_cursor.execute(project_query) 
projects = project_cursor.fetchall()
for p in projects:
    print p[0]
    
    idea_cursor = mysql.cursor()
    idea_cursor.execute(idea_query, p[0]) 
    ideas = idea_cursor.fetchall()
    f = open(raw_path(p[0]), 'w')
    f.write("id,title, tags, description,author,rate_up,rate_down,created\n")
    for i in ideas:
        for index in range(len(i)):
            if type(i[index]).__name__ == "str":
                f.write("\"")
                f.write(i[index])
                f.write("\"")
            else: 
                f.write(str(i[index]))
            f.write(",")
        f.write("\n")
    f.close()