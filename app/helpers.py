import random

### Dictionary helpers
def initializeAdjDict():
    d = open('dict.txt')
    adjs = d.readlines()
    adjs = [word.strip() for word in adjs]
    return adjs

def getWord(adjs, numWords):
    words = [adjs[random.randint(0, len(adjs)) for i in range(numWords)]

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