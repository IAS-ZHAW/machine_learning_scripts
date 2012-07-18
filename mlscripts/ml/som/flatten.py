# released under bsd licence
# see LICENSE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Timo Jeranko

def flatten(array):
    out =[]
    return flat(array,out)

def flat(array,out):
    if getattr(array,'__iter__',False):
        for i in array:
            flat(i,out)
    else:
        out.append(array)
    return out

def flatten2(array):
    out =[]
    return flat2(array,out)
   
def flat2(array,out):
    if getattr(array[0],'__iter__',False):
        for i in array:
            flat2(i,out)
    else:
        out.append(array)
    return out

def deep_function(array,function):
    out = []
    if getattr(array,'__iter__',False):
        for i in array:
            out.append( deep_function(i,function) )
    else:
        out = function(array)
    return out


