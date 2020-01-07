#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
import copy
import pysam

"""
cp ~/sftp_scripts/160521_ohvarfinder/result/findAnsFromPure/AnsPure.txt ~/tempSimulation/AnsPure.txt

grep HCC1143_n40t60 ~/tempSimulation/AnsPure.txt > ~/tempSimulation/AnsPure.HCC1143.txt
grep HCC1954_n40t60 ~/tempSimulation/AnsPure.txt > ~/tempSimulation/AnsPure.HCC1954.txt

python /home/moriyama/sftp_scripts/180202_SiMHaT/src/realSimulation/ans_to_vcf.py \
/home/moriyama/tools/ref/fasta/GRCh37.fa \
/home/moriyama/tempSimulation/AnsPure.HCC1143.txt \
/home/moriyama/tempSimulation/AnsPure.HCC1143.vcf \
HCC1143

python /home/moriyama/sftp_scripts/180202_SiMHaT/src/realSimulation/ans_to_vcf.py \
/home/moriyama/tools/ref/fasta/GRCh37.fa \
/home/moriyama/tempSimulation/AnsPure.HCC1954.txt \
/home/moriyama/tempSimulation/AnsPure.HCC1954.vcf \
HCC1954

"""

def prepare_vcf_header(ref_path, sample):
    fasta_obj     =  pysam.FastaFile(ref_path)
    header = ""
    header += "##fileformat=VCFv4.2\n"
    header += "##FILTER=<ID=PASS,Description=\"All filters passed\">\n"
    header += '##reference=file://' + ref_path + '\n'
    for i in range(len(fasta_obj.lengths)):
        header += '##<ID=' + str(fasta_obj.references[i]) + ',length=' + str(fasta_obj.lengths[i]) + '>\n'
    header += '##ALT=<ID=*,Description=\"Represents allele(s) other than observed.\">\n'
    header += '##FORMAT=<ID=RCT,Number=1,Type=Integer,Description=\"Ref Count Tumor\">\n'
    header += '##FORMAT=<ID=ACT,Number=1,Type=Integer,Description=\"Alt Count Tumor\">\n'
    header += '##FORMAT=<ID=RCN,Number=1,Type=Integer,Description=\"Ref Count Normal\">\n'
    header += '##FORMAT=<ID=ACN,Number=1,Type=Integer,Description=\"Alt Count Normal\">\n'
    header += '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t' + str(sample) +  '\n'
    fasta_obj.close()
    return header

def convert_to_vcf_variant(Type, Chr, pos, ref, obs):
    if Type == 'M':
        vcf_ref = ref
        vcf_obs = obs
    elif Type == 'D':
        vcf_ref = ref + obs
        vcf_obs = ref
    elif Type == 'I':
        vcf_ref = ref
        vcf_obs = ref + obs
    else:
        raise Exception("unexpected mutation type")
    return [Chr, pos, '.', vcf_ref, vcf_obs]

def main():
    argvs = sys.argv
    ref_path        = argvs[1]
    ans_path        = argvs[2]
    output_vcf_path = argvs[3]
    sample_name     = argvs[4]

    with open(ans_path, 'r') as ans_file, open(output_vcf_path, 'w') as output_vcf:
        header = prepare_vcf_header(ref_path, sample_name)
        output_vcf.writelines(header)
        for line in ans_file:
            output_list = []
            line = line.replace('\n','')
            line = line.replace('\r','')
            cols = re.split('\t',line)

            Type, Chr, pos, ref, obs = cols[0], cols[1], cols[2], cols[3], cols[4]
            ref_T, obs_T, ref_N, obs_N = -1, -1, -1, -1

            output_list.extend(convert_to_vcf_variant(Type, Chr, pos, ref, obs))
            output_list.extend(['.', \
                                '.', \
                                '.', \
                                'RCT:ACT:RCN:ACN', \
                                str(ref_T)+':'+str(obs_T)+':'+str(ref_N)+':'+str(obs_N)])
            outputString = '\t'.join(map(str, output_list))
            outputString = outputString.replace('\n', '')
            outputString = outputString + '\n'
            output_vcf.writelines(outputString)

if __name__ == '__main__':
    main()
