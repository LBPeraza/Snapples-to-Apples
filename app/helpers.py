import random
from flask import session, url_for, render_template, flash, redirect
from functools import wraps

### Decorators
def loginRequired(f):
    @wraps(f)
    def g(*args, **kwargs):
        if isLoggedIn():
            f(*args, **kwargs)
        else:
            flash('You have to be logged in to do that.')
            return redirect(url_for('snapples.index'))
    return g

### Game helpers
def isLoggedIn():
    info = session.get('user-info')
    return (info is not None)

### Dictionary helpers
def initializeAdjDict():
    d = open('dict.txt')
    adjs = d.readlines()
    adjs = [word.strip() for word in adjs]
    return adjs

def getWord(adjs, numWords):
    words = random.sample(adjs, numWords)
    return words

def loadAdjs(filename):

    from nltk.corpus import wordnet as wn

    adjs = ""
    for i in wn.all_synsets():
        if i.pos() in ['a', 's']:
            for j in i.lemmas():
                adjs += j.name() + "\n"

    def writeFile(path, contents):
        with open(path, "wt") as f:
            f.write(contents)
    writeFile(filename, str(adjs))
