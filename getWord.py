import random

def initializeAdjDict():
    d = open('dict.txt')
    adjs = d.readlines()
    adjs = [word.strip() for word in adjs]
    return adjs

def getWord(adjs, numWords):
    words = [adjs[random.randint(0, len(adjs)) for i in range(numWords)]