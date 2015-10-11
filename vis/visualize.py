from __future__ import print_function
from composes.utils import io_utils
import os
import sys
import csv
import copy
import random
import itertools
from operator import itemgetter
from collections import defaultdict

# Make sure you've got Numpy and Scipy installed:
import numpy as np
import scipy
import scipy.spatial.distance
from numpy.linalg import svd

# For visualization:
from tsne import tsne # See http://lvdmaaten.github.io/tsne/#implementations
import matplotlib.pyplot as plt

# For clustering in the 'Word-sense ambiguities' section:
from sklearn.cluster import AffinityPropagation

gastrovec = io_utils.load("../vector_processing/gastrovec.ppmi.svd20.pkl")

def build(space):
    mat = []
    for row in range(len(space.id2row)-5000):
        mat.append(np.array([space.cooccurrence_matrix[row,i] for i in range(20)]))
    return (np.array(mat), list(map(lambda x: x.decode("utf8"),space.id2row[:-5000])), space.id2column)

gastro = build(gastrovec)

def tsne_viz(
        mat=None,
        rownames=None,
        indices=None,
        colors=None,
        output_filename=None,
        figheight=40,
        figwidth=50,
        display_progress=False):
    """2d plot of mat using tsne, with the points labeled by rownames, 
    aligned with colors (defaults to all black).
    If indices is a list of indices into mat and rownames, 
    then it determines a subspace of mat and rownames to display.
    Give output_filename a string argument to save the image to disk.
    figheight and figwidth set the figure dimensions.
    display_progress=True shows the information that the tsne method prints out."""
    if not colors:
        colors = ['black' for i in range(len(rownames))]
    temp = sys.stdout
    if not display_progress:
        # Redirect stdout so that tsne doesn't fill the screen with its iteration info:
        f = open(os.devnull, 'w')
        sys.stdout = f
    tsnemat = tsne(mat)
    sys.stdout = temp
    # Plot coordinates:
    if not indices:
        indices = range(len(rownames))
    vocab = np.array(rownames)[indices]
    xvals = tsnemat[indices, 0]
    yvals = tsnemat[indices, 1]
    # Plotting:
    fig, ax = plt.subplots(nrows=1, ncols=1)
    fig.set_figheight(40)
    fig.set_figwidth(50)
    ax.plot(xvals, yvals, marker='', linestyle='')
    # Text labels:
    for word, x, y, color in zip(vocab, xvals, yvals, colors):
        ax.annotate(word, (x, y), fontsize=8, color=color)
    # Output:
    if output_filename:
        plt.savefig(output_filename, bbox_inches='tight')
    else:
        plt.show()

tsne_viz(mat=gastro[0],rownames=gastro[1], display_progress=True)
