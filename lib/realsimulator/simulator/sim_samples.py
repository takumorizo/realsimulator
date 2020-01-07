#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pysam
import re
import numpy as np
import vcf
from realsimulator.simulator.bam_reader import BamReader
from realsimulator.simulator.read_collector import ReadCollector

class SampleSimulator(object):
    """docstring for SampleSimulator"""
    def __init__(self, seed = 0):
        super(SampleSimulator, self).__init__()
        np.random.seed(seed=seed)

    def simulate_proportions(self, N, tree, alpha):
        alpha_vector = [ alpha for i in range(tree.size()) ]
        return [ list(np.random.dirichlet(alpha_vector, 1).flat) for i in range(N) ]

    def output_proportions(self, simplex_vectors, output_path):
        if len(simplex_vectors) > 0:
            with open(output_path, 'w') as output_file:
                output_list = ['sample/node']
                for i in range(len(simplex_vectors[0])):
                    output_list.append(i)
                output_string = '\t'.join(map(str, output_list)) + '\n'
                output_file.writelines(output_string)

                for i in range(len(simplex_vectors)):
                    output_list = [i]
                    for p in simplex_vectors[i]:
                        output_list.append(p)
                    output_string = '\t'.join(map(str, output_list)) + '\n'
                    output_file.writelines(output_string)

    def read_proportions(self, simplex_path):
        ans = []
        is_header = True
        with open(simplex_path, 'r') as simplex_file:
            for line in simplex_file:
                if is_header:
                    is_header = False
                    continue

                line = line.replace('\n','')
                line = line.replace('\r','')
                line_cols = re.split('\t',line)
                line_cols = line_cols[1:len(line_cols)]
                line_cols = map(float, line_cols)
                ans.append(line_cols)

        return ans

    def simulate_error_samples(self, N, alpha, beta, error_vcf_path, tumor_bam_path, normal_bam_path, output_bam_path_base,
                               margin = 700):
        for n in range(N):
            print("============= sample: " + str(n) + " =============" ) # debug
            self.simulate_sample(alpha, beta, error_vcf_path, tumor_bam_path, normal_bam_path, output_bam_path_base + "_" + str(n) + ".bam",
                                 margin = margin)

    def simulate_error_sample(self, alpha, beta, error_vcf_path, tumor_bam_path, normal_bam_path, output_bam_path,
                              margin = 700):
        print("============= simulate_error_sample =============" ) # debug
        vcf_reader = vcf.Reader(open(error_vcf_path, 'r'))
        tumor_reader  = BamReader()
        normal_reader = BamReader()

        tumor_reads  = ReadCollector()
        normal_reads = ReadCollector()
        num_output_pair = 0

        with tumor_reader.prepare(tumor_bam_path), normal_reader.prepare(normal_bam_path):
            output_bam = pysam.AlignmentFile(output_bam_path, 'w', header = tumor_reader.bam.header)
            for record in vcf_reader:
                Chr = record.CHROM
                pos = record.POS

                p = list(np.random.dirichlet([alpha, beta], 1).flat)
                tumor_proportoin_here  = p[0]
                normal_proportion_here = p[1]

                rct, rcn, act, acn = 0, 0, 0, 0 # debug
                for sample in record.samples:   # debug
                    rct += sample["RCT"]        # debug
                    rcn += sample["RCN"]        # debug
                    act += sample["ACT"]        # debug
                    acn += sample["ACN"]        # debug
                    break                       # debug

                ref_prediction = int(rct * tumor_proportoin_here + rcn * normal_proportion_here )                   # debug
                alt_prediction = int(act * tumor_proportoin_here + acn * normal_proportion_here )                   # debug
                print( str(record.CHROM) + ":" + str(record.POS) + ", (tumor proportion, normal proportion): " + \
                       str((tumor_proportoin_here, normal_proportion_here)) + ", (ref, alt) predicted: " + \
                       str((ref_prediction, alt_prediction)) )                                                      # debug

                tumor_reads.clear()
                normal_reads.clear()
                for read in tumor_reader.search(Chr, pos - margin, pos + margin, f_flag = 0, F_flag = 2816):
                    tumor_reads.push(read)

                for read in normal_reader.search(Chr, pos - margin, pos + margin, f_flag = 0, F_flag = 2816):
                    normal_reads.push(read)

                for ID, read_group in tumor_reads:
                    reads = read_group[1]
                    if len(reads) >= 2 and tumor_proportoin_here >= np.random.rand():
                        for read in reads:
                            read.query_name = 'error_'+str(num_output_pair)+'_'+read.query_name
                            output_bam.write(read)
                        num_output_pair +=1

                for ID, read_group in normal_reads:
                    reads = read_group[1]
                    if len(reads) >= 2 and normal_proportion_here >= np.random.rand():
                        for read in reads:
                            read.query_name = 'error_'+str(num_output_pair)+'_'+read.query_name
                            output_bam.write(read)
                        num_output_pair +=1

        output_bam.close()


    def simulate_samples(self, proportions, vcf_path, tumor_bam_path, normal_bam_path,  output_bam_path_base,
                         min_vaf = 0.0, max_vaf = 1.0,
                         margin = 700, node_info_tag = 'NODE'):
        for n in range(len(proportions)):
            print("============= sample: " + str(n) + " =============" ) # debug
            self.simulate_sample(proportions[n], vcf_path, tumor_bam_path, normal_bam_path, output_bam_path_base + "_" + str(n) + ".bam",
                                 min_vaf = 0.0, max_vaf = 1.0, margin = margin, node_info_tag = node_info_tag)

    def simulate_sample(self, proportion, vcf_path, tumor_bam_path, normal_bam_path, output_bam_path,
                        min_vaf = 0.0, max_vaf = 1.0, margin = 700, node_info_tag = 'NODE'):
        sys.stderr.writelines("min_vaf: " + str(min_vaf) + ", max_vaf: " + str(max_vaf) + "\n")
        vcf_reader = vcf.Reader(open(vcf_path, 'r'))
        tumor_reader  = BamReader()
        normal_reader = BamReader()

        tumor_reads  = ReadCollector()
        normal_reads = ReadCollector()
        num_output_pair = 0

        with tumor_reader.prepare(tumor_bam_path), normal_reader.prepare(normal_bam_path):
            output_bam = pysam.AlignmentFile(output_bam_path, 'w', header = tumor_reader.bam.header)
            for record in vcf_reader:
                Chr = record.CHROM
                pos = record.POS
                nodes = re.split('/', record.INFO[node_info_tag])
                nodes = map(int, nodes)

                tumor_proportoin_here  = 0.0
                normal_proportion_here = 1.0
                for node in nodes:
                    tumor_proportoin_here  += proportion[node]
                    normal_proportion_here -= proportion[node]

                # rct, rcn, act, acn = 0, 0, 0, 0 # debug
                # for sample in record.samples:   # debug
                #     rct += sample["RCT"]        # debug
                #     rcn += sample["RCN"]        # debug
                #     act += sample["ACT"]        # debug
                #     acn += sample["ACN"]        # debug
                #     break                       # debug

                # ref_prediction = int(rct * tumor_proportoin_here + rcn * normal_proportion_here )                   # debug
                # alt_prediction = int(act * tumor_proportoin_here + acn * normal_proportion_here )                   # debug
                # print( str(record.CHROM) + ":" + str(record.POS) + ", (tumor proportion, normal proportion): " + \
                #        str((tumor_proportoin_here, normal_proportion_here)) + ", (ref, alt) predicted: " + \
                #        str((ref_prediction, alt_prediction)) )                                                      # debug

                vaf = 0.0
                if len(record.samples) != 1:
                    raise Exception("Unexpected number of samples in answer vcf.")

                sample = record.samples[0]
                rct = int(sample["RCT"])
                act = int(sample["ACT"])
                depth = rct + act
                vaf = (1.0 * act)/(depth * 1.0)
                if not(min_vaf <= vaf <= max_vaf):
                    rcn = int(sample["RCN"])    # debug
                    acn = int(sample["ACN"])    # debug

                    ref_prediction = int(rct * tumor_proportoin_here + rcn * normal_proportion_here )                   # debug
                    alt_prediction = int(act * tumor_proportoin_here + acn * normal_proportion_here )                   # debug
                    sys.stderr.writelines("filtered: " + str(record.CHROM) + ":" + str(record.POS) +                      # debug
                                          ", (tumor proportion, normal proportion): " +                                 # debug
                                          str((tumor_proportoin_here, normal_proportion_here)) +                        # debug
                                          ", (ref, alt) predicted: " + str((ref_prediction, alt_prediction)) + "\n")    # debug
                    continue
                else:
                    rcn = int(sample["RCN"])    # debug
                    acn = int(sample["ACN"])    # debug

                    ref_prediction = int(rct * tumor_proportoin_here + rcn * normal_proportion_here )                   # debug
                    alt_prediction = int(act * tumor_proportoin_here + acn * normal_proportion_here )                   # debug
                    sys.stderr.writelines("passed: " + str(record.CHROM) + ":" + str(record.POS) +                      # debug
                                          ", (tumor proportion, normal proportion): " +                                 # debug
                                          str((tumor_proportoin_here, normal_proportion_here)) +                        # debug
                                          ", (ref, alt) predicted: " + str((ref_prediction, alt_prediction)) + "\n")    # debug


                tumor_reads.clear()
                normal_reads.clear()
                for read in tumor_reader.search(Chr, pos - margin, pos + margin, f_flag = 0, F_flag = 2816):
                    tumor_reads.push(read)

                for read in normal_reader.search(Chr, pos - margin, pos + margin, f_flag = 0, F_flag = 2816):
                    normal_reads.push(read)

                for ID, read_group in tumor_reads:
                    reads = read_group[1]
                    if len(reads) >= 2 and tumor_proportoin_here >= np.random.rand():
                        for read in reads:
                            read.query_name = 'tumor_'+str(num_output_pair)+'_'+read.query_name
                            output_bam.write(read)
                        num_output_pair +=1


                for ID, read_group in normal_reads:
                    reads = read_group[1]
                    if len(reads) >= 2 and normal_proportion_here >= np.random.rand():
                        for read in reads:
                            read.query_name = 'tumor_'+str(num_output_pair)+'_'+read.query_name
                            output_bam.write(read)
                        num_output_pair +=1

        output_bam.close()


