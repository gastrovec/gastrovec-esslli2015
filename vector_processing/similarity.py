from __future__ import print_function
import sys
from composes.utils import io_utils
from composes.similarity.cos import CosSimilarity
from jaccard import JaccardSimilarity

if len(sys.argv) > 2:
    gastrovec = io_utils.load(sys.argv[2])
else:
    gastrovec = io_utils.load("gastrovec.ppmi.svd20.pkl")

if len(sys.argv) > 1:
    num = int(sys.argv[1])
else:
    num = 1

while True:
    inp = raw_input("1> ")
    if not inp:
        break
    inp2 = raw_input("2> ")
    if not inp2:
        break
    inp = inp.replace(" ","_")
    if inp not in gastrovec.id2row:
        continue
    inp2 = inp2.replace(" ","_")
    if inp2 not in gastrovec.id2row:
        continue
    top = []
    sim = gastrovec.get_sim(inp, inp2, CosSimilarity())
    print("Similarity: {}".format(sim))
