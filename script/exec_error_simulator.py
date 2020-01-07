#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
# import re
from realsimulator.command.gen_samples import gen_error_sample

def main():
    argvs = sys.argv

    error_vcf_path       = argvs[1]
    alpha                = float(argvs[2])
    beta                 = float(argvs[3])

    tumor_bam_path       = argvs[4]
    normal_bam_path      = argvs[5]
    output_bam_path_base = argvs[6]

    seed                 = int(argvs[7]) if len(argvs) > 7 else 0

    gen_error_sample(alpha, beta, error_vcf_path,
                     tumor_bam_path, normal_bam_path, output_bam_path_base,
                     margin = 700, seed = seed)


if __name__ == '__main__':
    main()
