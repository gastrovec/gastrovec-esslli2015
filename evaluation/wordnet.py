from __future__ import print_function
import sys
from composes.utils import io_utils, scoring_utils
from composes.similarity.cos import CosSimilarity
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk.corpus import wordnet_ic
from itertools import combinations
print("Loading brown IC")
brown_ic = wn.ic(brown, False, 0.0)
print("done")

def getss(word):
    return wn.synsets(word,'n')[0]
def wn_sim(ss1,ss2):
    print("comparing",ss1,"with",ss2)
    return wn.path_similarity(ss1,ss2)
def jcn_sim(ss1,ss2):
    return ss1.jcn_similarity(ss2, brown_ic)
def lin_sim(ss1,ss2):
    return ss1.lin_similarity(ss2, brown_ic)
def res_sim(ss1,ss2):
    return ss1.res_similarity(ss2, brown_ic)
def wup_sim(ss1,ss2):
    return ss1.wup_similarity(ss2, brown_ic)
def lch_sim(ss1,ss2):
    return ss1.lch_similarity(ss2, brown_ic)
def mean(seq):
    print(sum(seq) / len(seq))
    return sum(seq) / len(seq)
def is_better(ingredients, result, other):
    return mean(map(lambda x: sim(x,result),ingredients)) > mean(map(lambda x: sim(x,other),ingredients))
def vs_sim(word1,word2,space):
    return space.get_sim(word1,word2,CosSimilarity())
def limit(iterator,num):
    for _ in range(num):
        yield next(iterator)
    raise StopIteration

gastrovec = io_utils.load("../vector_processing/gastrovec.ppmi.svd20.pkl")

wn_scores, vs_scores = [], []
jcn_scores, res_scores, lin_scores, lch_scores, wup_scores = [], [], [], [], []

ingredients = []

with open("../vector_processing/ingredients_in_wordnet") as f:
    for line in limit(f,int(sys.argv[1])):
        l = line.strip()
        ingredients.append(l)

for (a,b) in combinations(ingredients,2):
    a_,b_=getss(a), getss(b)
    wn_scores.append(wn_sim(a_,b_))
    res_scores.append(res_sim(a_,b_))
    jcn_scores.append(jcn_sim(a_,b_))
    lin_scores.append(lin_sim(a_,b_))
    wup_scores.append(wup_sim(a_,b_))
    lch_scores.append(lch_sim(a_,b_))
    vs_scores.append(vs_sim(a,b,gastrovec))

print("Path distance:")
print(scoring_utils.score(wn_scores,vs_scores,"spearman"))
print("JCN distance:")
print(scoring_utils.score(jcn_scores,vs_scores,"spearman"))
print("LIN distance:")
print(scoring_utils.score(jcn_scores,vs_scores,"spearman"))
print("RES distance:")
print(scoring_utils.score(res_scores,vs_scores,"spearman"))
print("WUP distance:")
print(scoring_utils.score(wup_scores,vs_scores,"spearman"))
print("LCH distance:")
print(scoring_utils.score(lch_scores,vs_scores,"spearman"))
