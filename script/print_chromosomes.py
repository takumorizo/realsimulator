#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
import vcf

def main():
    argvs = sys.argv
    vcf_path_list = argvs[1:len(argvs)]
    chr_set = set([])
    for vcf_path in vcf_path_list:
        vcf_reader = vcf.Reader(open(vcf_path, 'r'))
        for record in vcf_reader:
            chr_set.add(str(record.CHROM))

    chr_list = [ Chr for Chr in chr_set ]
    chr_list.sort()

    for Chr in chr_list:
        print(Chr)


if __name__ == '__main__':
    main()
