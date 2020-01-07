#!/usr/bin/env python
# -*- coding: utf-8 -*-
from realsimulator.simulator.sim_variants import VariantSimulator
from realsimulator.command.gen_tree import read_tree

def gen_variants(tree_vector_path, input_vcf, output_vcf, alpha = 0.2, seed = 0):
    tree = read_tree(tree_vector_path)
    simulator = VariantSimulator(seed = seed)
    simulator.add_node_tag_randomly(tree, input_vcf, output_vcf, alpha)

