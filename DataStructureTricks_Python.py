#!/usr/bin/env python3

import timeit
'''
1.All tricks use timeit to test timecost(s) followed by # annotation 
(benchmark:Microsoft Windows XP [release 5.1.2600],Python 3.4.4 (v3.4.4:737efcadf5a6, [MSC v.1600 32 bit (Intel)] on win32)
e.g:
    in:timeit.timeit('reduce(lambda x,y:x.update(y) or x,data)',setup="from functools import reduce;data=[{'a':2},{'c':5,'d':2},{'b':3},{'a':9,'e':8,'f':5}]")
    out:3.7995937120936185s(default exec statements 1000000 times)
2.Just as a coin has two sides,some solutions(performance and readability) are efficient but not very pythonic,especially "efficient" 
here means input little amount of parameters.What need to be explained is that ,as the size increased the "efficient" condition(timecost) 
will changed significantly.you can also contribute your own solutions to solve the more complex situations metioned above.
'''
#########################################################################tuple###############################################################################
'''Refer to the list part'''
####e.g.1    Flattening a tuple(one-level deep).
'''
[1]in:from functools import reduce
[3]in:import operator
[2]in:t = ((1,2,3),(4,5,6), (7,), (8,9))
[3]in:reduce(operator.concat, t)
[4]out:t = (1, 2, 3, 4, 5, 6, 7, 8, 9)
'''
t = ((1,2,3),(4,5,6), (7,), (8,9))

reduce(operator.concat, t) #1.48540176503775s


########################################################################list#################################################################################
'''Find many solutions to flatten a list on Google (there is no built-in flatten method in python). 
Here is one of them:http://www.daniel-lemire.com/blog/archives/2006/05/10/flattening-lists-in-python/
'''
####e.g.1    Flattening a shallow list(one-level deep).
'''
https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
[1]in:import itertools
[2]in:lol = [[1,2],[3],[5,89],[],[6],['a', 'b', 'c'],['xzy'],[1,2,3]]
[3]in:list(itertools.chain.from_iterable(lol))
[4]out:lol = [1, 2, 3, 5, 89, 6, 'a', 'b', 'c', 'xzy', 1, 2, 3]
'''
lol = [[1,2],[3],[5,89],[],[6],['a', 'b', 'c'],['xzy'],[1,2,3]]

list(itertools.chain.from_iterable(lol)) #3.5556429373536957s
sum(lol,[]) #4.1912247115396895s
functools.reduce(operator.concat,lol) #4.339995772854309s
functools.reduce(operator.add,lol) #4.411716270624311s
[item for sublist in lol for item in sublist] #5.026786384274601s
functools.reduce(lambda x,y: x.extend(y) or x, lol) #5.6559088408976095s
functools.reduce(lambda x,y: x+y,lol) #7.26806549054163s
[i[x] for i in lol for x in range(len(i))] #14.541105847165454s
numpy.concatenate(lol).ravel().tolist() #58.802661005422124s
numpy.concatenate(lol).tolist() #57.32027547058533s

#Especially,use some third-partition api.  
#eg:
#  1.http://matplotlib.org/api/cbook_api.html
#  2.https://github.com/metagriffin/morph#flattening


####e.g.2    Flatten a deep nested list(recursive).
'''
some solutions also adapt to one-level deep situations.
http://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html
https://stackoverflow.com/questions/10823877/what-is-the-fastest-way-to-flatten-arbitrarily-nested-lists-in-python?noredirect=1
[1]in:nests = [1, 2, [3, 4,[],[5],['hi']],'a',[6, [[[7, 'hello']]]]]
[2]in:
def flatten(l):
    for i in range(len(l)):
        if (isinstance(l[i], (list, tuple))):
            for a in l.pop(i):
                l.insert(i, a)
                i += 1
            return flatten(l)
    return l
[3]in:flatten(nests)
[4]out:nests = [1, 2, 3, 4, 5, 'hi', 'a', 6, 7, 'hello']
'''
nests = [1, 2, [3, 4,[],[5],['hi']],'a',[6, [[[7, 'hello']]]]]

'''
def flatten(l):
    for i in range(len(l)):
        if isinstance(l[i], (list, tuple)):
            for a in l.pop(i):
                l.insert(i, a)
                i += 1
            return flatten(l)
    return l '''
flatten(nests) #16.412650750018656s

'''
def flatten(items):
    for i, x in enumerate(items):
        while (i < len(items)):
            if isinstance(items[i],(list,tuple)):
                items[i:i+1] = items[i]
            else :break
    return items '''
flatten(nests) #19.205846394528635s

'''
def rewritten_flatten(l):
    ltype = type(l)
    l = list(l)
    i = 0
    try: 
        while i < len(l):
            while isinstance(l[i],(list, tuple)):
                if not l[i]: ##if l[i] is empty
                    l.pop(i) ##discard l[i]
                else:
                    l[i:i + 1] = l[i] ##insert list into self - increasing len(l)
            i += 1
    except IndexError:
        pass
    return ltype(l) '''
rewritten_flatten(nests) #34.895477816725816s

'''
def flatten(container):
    for i in container:
        if isinstance(i, (list,tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i'''
list(flatten(nests)) #35.65887954333448s

'''
def fletchers_flatten(l):
    ltype = type(l)
    l = list(l)
    i = 0
    while i < len(l):
        while isinstance(l[i],(list, tuple)):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1
    return ltype(l)'''
fletchers_flatten(nests) #35.70534790997044s

'''
def flat_list(list_to_flat):
    if not isinstance(list_to_flat,(list,tuple)):
        yield list_to_flat
    else:
        for item in list_to_flat:
            yield from flat_list(item) #yield from syntax available from python3.3 
'''
list(flat_list(nests)) #38.07334185666501s

'''
def iter_flatten(iterable):
    it = iter(iterable)
    for e in it:
        if isinstance(e, (list, tuple)):
            for f in iter_flatten(e):
                yield f
        else:
            yield e'''
list(iter_flatten(nests)) #38.38234978629043s

'''
def flattenlist(d):
    thelist = []
    for x in d:
        if not isinstance(x,(list,tuple)):
            thelist +=[x]
        else:
            thelist +=flattenlist(x)
    return thelist '''
flattenlist(nests) #38.38784174804459s

'''
def flatten(l):
    if isinstance(l,list):
        return sum(map(flatten,l),[])
    else:
        return [l] '''
flatten(nests) #42.70681502521256s

'''
def flatten(input):
    output,stack = [],[]
    stack.extend(reversed(input))
    while stack:
        top = stack.pop()
        if isinstance(top, (list, tuple)):
            stack.extend(reversed(top))
        else:
            output.append(top)
    return output '''
flatten(nests) #46.554564924128954s

'''
def flatten(nestedList):
    result = []
    if not nestedList:
        return result
    stack = [list(nestedList)]
    while stack:
        current = stack.pop()
        next = current.pop()
        if current:
            stack.append(current)
        if isinstance(next, list):
            if next:
                stack.append(list(next))
        else:
            result.append(next)
    result.reverse()
    return result '''
flatten(nests) #51.36927718148581s

'''
def flatten(iterable):
    iterator, sentinel, stack = iter(iterable), object(), []
    while True:
        value = next(iterator, sentinel)
        if value is sentinel:
            if not stack:
                break
            iterator = stack.pop()
        elif isinstance(value, str):
            yield value
        else:
            try:
                new_iterator = iter(value)
            except TypeError:
                yield value
            else:
                stack.append(iterator)
                iterator = new_iterator '''
list(flatten(nests)) #67.29974737600423s

'''
from functools import reduce
def flatten(l):
    return reduce(lambda a,b: a + (flatten(b) if hasattr(b,'__iter__') and not isinstance(b, (str, bytes)) else [b]), l, []) '''
flatten(nests) #78.00092893566398s

'''
import collections
def flatten(iterable):
    iterator = iter(iterable)
    array, stack = collections.deque(), collections.deque()
    while True:
        try:
            value = next(iterator)
        except StopIteration:
            if not stack:
                return tuple(array)
            iterator = stack.pop()
        else:
            if not isinstance(value, str) \
               and isinstance(value, collections.Iterable):
                stack.append(iterator)
                iterator = iter(value)
            else:
                array.append(value) '''
flatten(nests) #141.30945284153754s

'''
def _flatten(l, fn, val=[]):
    if type(l) != list:
        return fn(l)
    if len(l) == 0:
        return fn(val)
    return [lambda x: _flatten(l[0], lambda y: _flatten(l[1:],fn,y), x), val]
def flattened(l):
    result = _flatten(l, lambda x: x)
    while type(result) == list and len(result) and callable(result[0]):
        if result[1] != []:
            yield result[1]
        result = result[0]([])
    yield result'''
list(flattened(nests)) #147.43469733037637s



##############################################################################dict###########################################################################
'''          '''
####e.g 1    Lookup the key to the max value in a dict.
'''
[1]in:data={'a':1,'b':3,'c':9,'e':2,'an':4}
[2]in:max(data,key = data.get)
[3]out:'c'
'''
data = {'a':1,'b':3,'c':9,'e':2,'an':4}

max (data,key = data.get) #3.4447730144992477s
max (zip(data.values(), data.keys()))[1] #3.9161372415683218s


#########################################################################compounds###########################################################################
'''tuple nested list,list nested tuple,list nested dict............'''

####e.g 1 Pairs in tuples nested in list. Sort list by one element of pairs.
'''
https://docs.python.org/dev/tutorial/controlflow.html#lambda-expressions
[1]in:pairs = [(1, 'f'), (2, 'd'), (3, 'a'), (4, 'c'),(5,'dc')]
[2]in:pairs.sort(key=lambda pair: pair[1])
[3]out:pairs = [(3, 'a'), (4, 'c'), (2, 'd'), (5, 'dc'), (1, 'f')]
[4]in:pairs.sort(key=lambda pair: pair[0])
[5]out:pairs = [(1, 'f'), (2, 'd'), (3, 'a'), (4, 'c'),(5,'dc')]
'''
pairs = [(1, 'f'), (2, 'd'), (3, 'a'), (4, 'c'),(5,'dc')]

pairs.sort(key=lambda pair: pair[1]) #5.185777903273774s


####e.g 2 Create a dictionary with list comprehension.
'''
https://stackoverflow.com/questions/1747817/create-a-dictionary-with-list-comprehension-in-python
[1]in:lc = [('f',1), ('d',2), ('a',3), ('c',4),('dc',5)]
[2]in:{key: value for (key, value) in lc}
In Python 2.6 and earlier syntax in:dict((key, value) for (key, value) in lc)
[3]out:lc = {'a': 3, 'c': 4, 'd': 2, 'dc': 5, 'f': 1}
'''
lc = [('f',1), ('d',2), ('a',3), ('c',4),('dc',5)]

{key: value for (key, value) in lc} #2.0591526246680587s


####e.g 3 dicts(no duplicate K-V pairs)nested in list. Merge dicts into a dict with single expression.
'''
https://stackoverflow.com/questions/38987/how-to-merge-two-python-dictionaries-in-a-single-expression/26853961#26853961
[1]in:from functools import reduce
[2]in:data=[{'a':2},{'c':5,'d':2},{'b':3},{'ar':9,'e':8,'f':5}]
[3]in:reduce(lambda x,y:x.update(y) or x,data)
[4]out:data={'d': 2, 'ar': 9, 'e': 8, 'c': 5, 'b': 3, 'a': 2, 'f': 5}
'''
data=[{'a':2},{'c':5,'d':2},{'b':3},{'ar':9,'e':8,'f':5}]

reduce(lambda x,y:x.update(y) or x,data) #3.883738605947201
reduce(lambda x,y:(x.update(y),x)[1],data) #4.44267423819656s
{k:v for i in data for k,v in i.items()} #6.143100802988556s
dict(itertools.chain.from_iterable(dct.items() for dct in data)) #10.944527065365207s


###e.g 3 Recursive flatten tuples and lists mixed.
'''
https://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists
[1]in:import collections
[2]in:c = [0, 1, (2, 3), [[4, 5, (6, 7,['a', ['b', ('c', 'd')]], (8,), [9,([])]), 10]], (11,)]
[3]in:
def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el
[4]in:list(flatten(c))
[5]out:c = [0, 1, 2, 3, 4, 5, 6, 7, 'a', 'b', 'c', 'd', 8, 9, 10, 11]
'''
c = [0, 1, (2, 3), [[4, 5, (6, 7,['a', ['b', ('c', 'd')]], (8,), [9,([])]), 10]], (11,)]

'''
def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el '''
list(flatten(c)) #217.46189735244297s