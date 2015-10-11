"""
Created on Oct 2, 2012

@author: Jonathan Oberlaender

Adapted from cos.py from Nghia & Georgiana
"""
import numpy as np

from composes.similarity.similarity import Similarity
from scipy.spatial.distance import jaccard


class JaccardSimilarity(Similarity):
    """
    Computes the jaccard similarity of two vectors.
    """

    def _sim(self, v1, v2):
        if v1.norm() == 0 or v2.norm() == 0:
            return 0.0
        return jaccard(v1, v2)

    def _sims_to_matrix(self, vector, matrix_):
        raise NotImplementedError("whatevs")
