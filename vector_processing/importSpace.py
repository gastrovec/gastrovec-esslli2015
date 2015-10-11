from __future__ import print_function
import sys
from composes.semantic_space.space import Space
from composes.semantic_space.peripheral_space import PeripheralSpace
from composes.transformation.scaling.ppmi_weighting import PpmiWeighting
from composes.transformation.dim_reduction.svd import Svd
from composes.utils import io_utils

print("Loading ingredient space...",end="",file=sys.stderr)
sys.stderr.flush()
gastrovec = Space.build(data = "../corpus_collection/corpus.sm",
                        rows = "../corpus_collection/corpus.rows",
                        cols = "../corpus_collection/corpus.cols",
                        format = "sm")
print("done.", file=sys.stderr)

io_utils.save(gastrovec, "gastrovec.pkl")

print("Applying PPMI... ",end="", file=sys.stderr)
sys.stderr.flush()
gastrovec = gastrovec.apply(PpmiWeighting())
print("Applying SVD (20)... ",end="",file=sys.stderr)
sys.stderr.flush()
gastrovec = gastrovec.apply(Svd(20))
print("done.", file=sys.stderr)

io_utils.save(gastrovec, "gastrovec.ppmi.svd20.pkl")

print("Loading recipe peripheral space...",end="",file=sys.stderr)
sys.stderr.flush()
recipes = PeripheralSpace.build(gastrovec,
                                  data = "../corpus_collection/recipes.sm",
                                  rows = "../corpus_collection/recipes.rows",
                                  cols = "../corpus_collection/recipes.cols",
                                  format = "sm")
print("done.", file=sys.stderr)

io_utils.save(recipes, "recipes.ppmi.svd20.pkl")

