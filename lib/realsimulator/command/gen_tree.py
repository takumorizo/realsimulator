#!/usr/bin/env python
# -*- coding: utf-8 -*-
from realsimulator.simulator.sim_tree import TreeSimulator
from realsimulator.simulator.tree import Tree
import re

def gen_tree(output_tree_path_base, node_size, zero_weight = 0.1, seed = 0):
    simulator = TreeSimulator(seed = seed)
    tree = simulator.sim_tree_uniform(node_size, zero_weight = zero_weight)
    tree.output_tree(output_tree_path_base)

def read_tree(output_tree_vector_path):
    vector = None
    with open(output_tree_vector_path, "r") as tree_vector_file:
        for line in tree_vector_file:
            line = line.replace('\n','')
            line = line.replace('\r','')
            vector = map(int, re.split('\t',line))
    return Tree(vector)



