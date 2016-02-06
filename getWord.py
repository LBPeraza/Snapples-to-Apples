import random

d = open('dict.txt')
adjs = d.readlines()

adjs = [word.strip() for word in adjs]

for i in range(10):
    print(adjs[random.randint(0, len(adjs))])