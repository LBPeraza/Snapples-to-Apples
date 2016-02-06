import jank_windows_fix
import random

from nltk.corpus import wordnet as wn

adjs = ""
for i in wn.all_synsets():
    if i.pos() in ['a', 's']:
        for j in i.lemmas():
            adjs += j.name() + "\n"

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)
writeFile('dict.txt', str(adjs))

print('done')