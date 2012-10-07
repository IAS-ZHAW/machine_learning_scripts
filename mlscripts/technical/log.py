#!/usr/local/bin/python
# coding: UTF-8

# released under bsd licence
# see LICENCE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Thomas Niederberger

class LogLevel:
    VERBOSE = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
   
class Environment:
    LOCAL = 1
    SERVER = 2
   
log_level = LogLevel.VERBOSE
env = Environment.LOCAL

def log(message, level):
    if level >= log_level:
        print message