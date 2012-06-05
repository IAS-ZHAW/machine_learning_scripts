
def decay_learning_rate(a=1.0, b=1000.0, alpha=1.0):
    """ decaying learning rate in the form a/(b + alpha*i) where i is the increasing number of iterations.""" 
    i = 0
    while True:
        yield a / (b + alpha * i)
        i += 1

def const_learning_rate(rate):
    while True:
        yield rate

