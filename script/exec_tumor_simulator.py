#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from realsimulator.command.gen_tree import gen_tree
from realsimulator.command.gen_variants import gen_variants
from realsimulator.command.gen_samples import gen_sample_in_proportion
from realsimulator.simulator.sim_samples import SampleSimulator


def main():
    argvs = sys.argv

    # tree_vector_path     = argvs[1]
    input_vcf            = argvs[1]
    alpha_clone          = float(argvs[2]) if len(argvs) > 2  else 0.2
    simplex_path         = argvs[3]        if len(argvs) > 3  else None
    sample_at            = int(argvs[4])   if len(argvs) > 4  else None
    tumor_bam_path       = argvs[5]        if len(argvs) > 5  else None
    normal_bam_path      = argvs[6]        if len(argvs) > 6  else None
    output_bam_path      = argvs[7]        if len(argvs) > 7  else None
    min_vaf              = float(argvs[8]) if len(argvs) > 8  else 0.0
    max_vaf              = float(argvs[9]) if len(argvs) > 9  else 1.0
    # seed                 = int(argvs[9])   if len(argvs) > 9  else None

    gen_sample_in_proportion(sample_at, alpha_clone, simplex_path, input_vcf,
                             tumor_bam_path, normal_bam_path, output_bam_path,
                             min_vaf = min_vaf, max_vaf = max_vaf,
                             margin = 700, node_info_tag = 'NODE', seed = 0)

    # gen_sample(tree_vector_path, alpha_clone, simplex_path, input_vcf,
                # tumor_bam_path, normal_bam_path, output_bam_path,
                # margin = 700, node_info_tag = 'NODE', seed = seed)



if __name__ == '__main__':
    main()
