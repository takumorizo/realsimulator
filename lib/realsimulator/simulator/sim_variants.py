#!/usr/bin/env python
# -*- coding: utf-8 -*-
import vcf
import sys
import numpy as np
from realsimulator.simulator.tree import Tree
from vcf.parser import _Info as VcfInfo

class VariantSimulator(object):
    """docstring for VariantSimulator"""
    def __init__(self, seed = 0):
        super(VariantSimulator, self).__init__()
        np.random.seed(seed=seed)

    def add_node_tag_randomly(self, tree, input_vcf, output_vcf, alpha,
                              add_info_tag  = 'NODE',
                              add_info_num  = 1,
                              add_info_type = 'String',
                              add_info_description = 'Nodes in a tree.',
                              add_info_source  = None,
                              add_info_version = None):
        weights = self.__sample_node_proportion(tree, alpha)
        original_reader = vcf.Reader(open(input_vcf, 'r'))
        original_reader.infos[add_info_tag] = VcfInfo(add_info_tag,
                                                      add_info_num,
                                                      add_info_type,
                                                      add_info_description,
                                                      add_info_source,
                                                      add_info_version)

        writer = vcf.Writer(open(output_vcf, 'w'), original_reader, lineterminator='\n')
        for record in original_reader:
            node  = self.__sample_node(tree, weights)
            nodes = tree.sub_tree_nodes(at = node)
            nodes_string = '/'.join(map(str, nodes))
            record.add_info(add_info_tag, nodes_string)
            writer.write_record(record)
        writer.close()

    def __sample_node_proportion(self, tree, alpha):
        alpha_vector = [ alpha for i in range(tree.size())]
        return list(np.random.dirichlet(alpha_vector, 1).flat)

    def __sample_node(self, tree, weights):
        if not len(weights) == tree.size():
            sys.stderr.writelines(str(weights) + ': len: ' + str(len(weights)) + '\n')
            sys.stderr.writelines(str(tree.vector) + ': len: ' + str(tree.size()) + '\n')
            raise Exception("Sampling weights len invalid.")

        if not(abs(sum(weights) - 1.0) < 1e-8):
            sys.stderr.writelines(str(weights) + '\n')
            sys.stderr.writelines(str(tree.vector) + '\n')
            raise Exception("Sampling weights invalid.")

        return np.random.randint(0, tree.size())
