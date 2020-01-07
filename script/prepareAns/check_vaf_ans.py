#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
import vcf

"""
python /home/moriyama/sftp_scripts/180202_SiMHaT/src/realSimulation/prepareAns/check_vaf_ans.py \
/home/moriyama/work/SiMHaT/simulation/TCGA_answer/output.HCC1143_ans.variant.vcf \
/home/moriyama/work/SiMHaT/simulation/TCGA_answer/output.HCC1143_ans.m30M70.variant.vcf \
ACT RCT 0.3 0.7

python /home/moriyama/sftp_scripts/180202_SiMHaT/src/realSimulation/prepareAns/check_vaf_ans.py \
/home/moriyama/work/SiMHaT/simulation/TCGA_answer/output.HCC1954_ans.variant.vcf \
/home/moriyama/work/SiMHaT/simulation/TCGA_answer/output.HCC1954_ans.m30M70.variant.vcf \
ACT RCT 0.3 0.7

"""

def main():
    argvs = sys.argv
    input_vcf_path  = argvs[1]
    output_vcf_path = argvs[2]
    act_tag         = argvs[3] # ACT
    rct_tag         = argvs[4] # RCT
    min_vaf         = float(argvs[5]) if len(argvs) > 5 else 0.0
    max_vaf         = float(argvs[6]) if len(argvs) > 6 else 1.0

    vcf_reader = vcf.Reader(open(input_vcf_path, 'r'))
    writer = vcf.Writer(open(output_vcf_path, 'w'), vcf_reader, lineterminator='\n')

    for record in vcf_reader:
        vaf = 0.0
        if len(record.samples) != 1:
            raise Exception("Unexpected number of samples.")

        vaf = 0.0
        sample = record.samples[0]
        rct = int(sample[rct_tag])
        act = int(sample[act_tag])
        depth = rct + act
        vaf = (1.0 * act)/(depth * 1.0)

        if min_vaf <= vaf <= max_vaf:
            writer.write_record(record)
    writer.close()


if __name__ == '__main__':
    main()
