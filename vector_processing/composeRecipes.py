from __future__ import print_function
import sys
from random import randint
from itertools import count
from composes.utils import io_utils
from composes.composition.weighted_additive import WeightedAdditive
from composes.semantic_space.space import Space


stacked_space = io_utils.load("gastrovec.ppmi.svd20.pkl")

WA = WeightedAdditive(alpha = 1, beta = 1)

recipes = {}
max_size = 0
with open("../corpus_collection/composition_counts.txt") as f:
    for line in f:
        words = line.split()
        recipes[words[0]] = words[1:]
        if len(words)-1 > max_size:
            max_size = len(words)-1

WA = WeightedAdditive(alpha = 1, beta = 1)
last_space = None
number = count()
for size in xrange(max_size,1,-1):
    relevant = (rec for rec in recipes if len(recipes[rec]) == size)
    print(size)
    composition = []
    for recipe in relevant:
        old = recipes[recipe]
        if size == 2:
            name = recipe
        else:
            name = "comp_" + str(next(number))
        if old[-2] in stacked_space.id2row:
            composition.append((old[-1],old[-2],name))
            recipes[recipe].pop(-1)
            recipes[recipe].pop(-1)
            recipes[recipe].append(name)
        else:
            recipes[recipe].pop(-2)
    if composition:
        last_space = WA.compose(composition, stacked_space)
        if size != 2:
            stacked_space = Space.vstack(stacked_space, last_space)

io_utils.save(last_space, "recicomp.pkl")
