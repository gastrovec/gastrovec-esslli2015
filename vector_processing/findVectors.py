from __future__ import print_function
import sys
from composes.utils import io_utils
from composes.similarity.cos import CosSimilarity

if len(sys.argv) > 1:
    gastrovec = io_utils.load(sys.argv[1])
else:
    gastrovec = io_utils.load("gastrovec.ppmi.svd20.pkl")

while True:
    inp = raw_input("> ")
    if not inp:
        break
    inp = inp.replace(" ","_")
    for ing in gastrovec.id2row:
        if inp in ing:
            print(ing)
