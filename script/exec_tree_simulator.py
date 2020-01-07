#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from realsimulator.command.gen_tree import gen_tree, read_tree
from realsimulator.command.gen_variants import gen_variants
from realsimulator.simulator.sim_samples import SampleSimulator


def main():
    argvs = sys.argv
    output_tree_path_base = argvs[1]
    node_size             = int(argvs[2])
    seed                  = int(argvs[3]) if len(argvs) > 3 else 0
    zero_weight           = float(argvs[4]) if len(argvs) > 4 else 0.1

    tree_vector_path = output_tree_path_base + '.txt'
    input_vcf        = argvs[5] if len(argvs) > 5 else None
    output_vcf       = argvs[6] if len(argvs) > 6 else None
    alpha            = float(argvs[7]) if len(argvs) > 7 else 0.2

    simplex_path = argvs[8] if len(argvs) > 8 else None
    alpha_clone  = float(argvs[9]) if len(argvs) > 9 else None
    sample_size  = int(argvs[10])   if len(argvs) > 10 else None

    gen_tree(output_tree_path_base, node_size, seed = seed, zero_weight = zero_weight)
    gen_variants(tree_vector_path, input_vcf, output_vcf, alpha = alpha, seed = seed)

    tree = read_tree(tree_vector_path)
    simulator = SampleSimulator(seed)
    proportions = simulator.simulate_proportions(sample_size, tree, alpha_clone)
    simulator.output_proportions(proportions, simplex_path)



if __name__ == '__main__':
    main()




