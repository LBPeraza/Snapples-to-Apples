import random
from flask import (session, url_for, render_template, flash, redirect,
                   make_response)
from functools import wraps, update_wrapper
from datetime import datetime


def flashErrors(form):
    for field, errors in form.errors.items():
        for error in errors:
            e = 'Error in %s field -- %s' % (
                getattr(form, field).label.text,
                error
            )
            flash(e, 'danger')
            print(e)

### Decorators
def loginRequired(f):
    @wraps(f)
    def g(*args, **kwargs):
        if isLoggedIn():
            return f(*args, **kwargs)
        else:
            flash('You have to be logged in to do that.', 'warning')
            return redirect(url_for('snapples.index'))
    return g

def socketLoginRequired(f):
    @wraps(f)
    def g(*args, **kwargs):
        if isLoggedIn():
            return f(*args, **kwargs)
        else:
            emit('You have to be logged in to do that')
    return g

def nocache(view):
        @wraps(view)
        def no_cache(*args, **kwargs):
            response = make_response(view(*args, **kwargs))
            response.headers['Last-Modified'] = datetime.now()
            response.headers['Cache-Control'] = (
                'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0')
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '-1'
            return response
        return update_wrapper(no_cache, view)

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
    words = [adjs[random.randint(0, len(adjs))] for i in range(numWords)]
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
