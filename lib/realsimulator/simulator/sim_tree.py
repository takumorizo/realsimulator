#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from realsimulator.simulator.tree import Tree
from vcf.parser import _Info as VcfInfo

class TreeSimulator(object):
    """docstring for TreeSimulator"""
    def __init__(self, seed = 0):
        super(TreeSimulator, self).__init__()
        np.random.seed(seed=seed)

    def sim_tree_uniform(self, K, zero_weight = 0.1):
        vector = [0 for i in range(K)]
        for i in range(2, K):
            if zero_weight >= np.random.rand():
                continue
            else:
                vector[i] = np.random.randint(1, i)
        return Tree(vector)
