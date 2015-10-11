from __future__ import print_function
from composes.utils import io_utils

gastrovec = io_utils.load("gastrovec.ppmi.svd20.pkl")

gastrovec.export(file_prefix="fullexport", format="dm")
'''
with open("export3.csv","w") as f:
    # f.write("INGREDIENT " + " ".join(gastrovec.id2column) + "\n")
    with open("export.dm") as f_in:
        for line in f_in:
            f.write(line)
'''
