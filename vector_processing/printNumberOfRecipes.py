import sys
from composes.utils import io_utils

if len(sys.argv) < 2:
    name = "recipes.ppmi.svd200.pkl"
else:
    name = sys.argv[1]
print len(io_utils.load(name).id2row)
