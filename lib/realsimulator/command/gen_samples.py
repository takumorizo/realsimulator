#!/usr/bin/env python
# -*- coding: utf-8 -*-
from realsimulator.simulator.sim_samples import SampleSimulator
from realsimulator.command.gen_tree import read_tree

def gen_sample_in_proportion(n, alpha, simplex_path, input_vcf_path,
                             tumor_bam_path, normal_bam_path, output_bam_path,
                             min_vaf = 0.0, max_vaf = 1.0,
                             margin = 700, node_info_tag = 'NODE', seed = 0):
    simulator = SampleSimulator(seed)
    proportions = simulator.read_proportions(simplex_path)
    simulator.simulate_sample(proportions[n], input_vcf_path, tumor_bam_path, normal_bam_path,  output_bam_path,
                              min_vaf = min_vaf, max_vaf = max_vaf,
                              margin = margin, node_info_tag = node_info_tag)

def gen_sample(tree_vector_path, alpha, simplex_path, input_vcf_path,
               tumor_bam_path, normal_bam_path, output_bam_path,
               min_vaf = 0.0, max_vaf = 1.0,
               margin = 700, node_info_tag = 'NODE', seed = 0):
    tree = read_tree(tree_vector_path)
    simulator = SampleSimulator(seed)

    proportions = simulator.simulate_proportions(1, tree, alpha)
    simulator.output_proportions(proportions, simplex_path)

    simulator.simulate_sample(proportions[0], input_vcf_path, tumor_bam_path, normal_bam_path,  output_bam_path,
                              min_vaf = min_vaf, max_vaf = max_vaf,
                              margin = margin, node_info_tag = node_info_tag)

def gen_samples(N, tree_vector_path, alpha, simplex_path, input_vcf_path,
                tumor_bam_path, normal_bam_path, output_bam_path_base,
                min_vaf = 0.0, max_vaf = 1.0,
                margin = 700, node_info_tag = 'NODE', seed = 0):
    tree = read_tree(tree_vector_path)
    simulator = SampleSimulator(seed)

    proportions = simulator.simulate_proportions(N, tree, alpha)
    simulator.output_proportions(proportions, simplex_path)

    simulator.simulate_samples(proportions, input_vcf_path, tumor_bam_path, normal_bam_path,  output_bam_path_base,
                               min_vaf = min_vaf, max_vaf = max_vaf,
                               margin = margin, node_info_tag = node_info_tag)

def gen_error_sample(alpha, beta, input_error_vcf_path,
                     tumor_bam_path, normal_bam_path, output_bam_path_base,
                     margin = 700, seed = 0):
    simulator = SampleSimulator(seed)

    simulator.simulate_error_sample(alpha, beta, input_error_vcf_path, tumor_bam_path,
                                    normal_bam_path,  output_bam_path_base,
                                    margin = margin)

def gen_error_samples(N, alpha, beta, input_error_vcf_path,
                      tumor_bam_path, normal_bam_path, output_bam_path_base,
                      margin = 700, seed = 0):
    simulator = SampleSimulator(seed)

    simulator.simulate_error_samples(N, alpha, beta, input_error_vcf_path, tumor_bam_path,
                                     normal_bam_path,  output_bam_path_base,
                                     margin = margin)



