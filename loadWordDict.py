import jank_windows_fix

from nltk.corpus import wordnet as wn

def loadAdjs(filename):
    adjs = ""
    for i in wn.all_synsets():
        if i.pos() in ['a', 's']:
            for j in i.lemmas():
                adjs += j.name() + "\n"

    def writeFile(path, contents):
        with open(path, "wt") as f:
            f.write(contents)
    writeFile(filename, str(adjs))