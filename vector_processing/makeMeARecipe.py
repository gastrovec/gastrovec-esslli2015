from __future__ import print_function
import sys
from composes.utils import io_utils
from composes.composition.weighted_additive import WeightedAdditive
from composes.semantic_space.space import Space
from composes.similarity.cos import CosSimilarity
from itertools import count

if len(sys.argv) > 1:
    num = int(sys.argv[1])
else:
    num = 1
if len(sys.argv) > 2:
    recipe_space = sys.argv[2]
else:
    recipe_space = "recicomp.pkl"

def ins(lst, el):
    if len(lst) < num:
        lst.append(el)
        lst.sort(reverse=True)
        return
    else:
        if el[0] > lst[-1][0]:
            lst.pop(-1)
            lst.append(el)
            lst.sort(reverse=True)

stacked = io_utils.load("gastrovec.ppmi.svd20.pkl")
recicomp = io_utils.load(recipe_space)

WA = WeightedAdditive(alpha = 1, beta = 1)
number = count()

ingredients = []
print("Enter ingredients, enter when done")
while True:
    ingredient = raw_input("> ").replace(" ","_")
    if ingredient == "":
        break
    if ingredient not in stacked.id2row:
        print("(not found, skipping)")
        continue
    ingredients.append(ingredient)

name = ""
while True:
    (a,b) = ingredients.pop(-1),ingredients.pop(-1)
    name = "comp_" + str(next(number))
    ingredients.append(name)
    new_space = WA.compose([(a,b,name)], stacked)
    if len(ingredients) > 1:
        stacked = Space.vstack(stacked, new_space)
    else:
        break

stacked = Space.vstack(recicomp, new_space)
top = []
for recipe in stacked.id2row:
    if recipe == name:
        continue
    sim = stacked.get_sim(recipe, name, CosSimilarity())
    ins(top, (sim,recipe))
print("Nearest neighbors:",", ".join([x[1].replace("_"," ") + " (" + str(x[0]) + ")" for x in top]))
