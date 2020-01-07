LOGDIR=/home/moriyama/sftp_scripts/180202_SiMHaT/log
REF=/home/moriyama/tools/ref/fasta/GRCh37.fa

SAMTOOLS=/home/moriyama/tools/bin/samtools-1.8/samtools
BEDTOOLS=/home/moriyama/tools/bin/bedtools-2.17.0/bin/bedtools
BWA=/home/moriyama/tools/bin/bwa-0.7.10/bwa
BIOBAMBAM=/home/moriyama/tools/bin/biobambam-0.0.191/bin

BCFTOOLS=/home/moriyama/tools/bin/bcftools-1.8/bcftools
VCFTOOLS=/home/moriyama/tools/bin/vcftools/bin/vcftools
VCFANNOTATE=/home/moriyama/tools/bin/vcftools/bin/vcf-annotate
VCFCONCAT=/home/moriyama/tools/bin/vcftools/bin/vcf-concat
VCFMERGE=/home/moriyama/tools/bin/vcftools/bin/vcf-merge
VCFSORT=/home/moriyama/tools/bin/vcftools/bin/vcf-sort

BGZIP=/home/moriyama/tools/bin/htslib-1.8/bgzip
TABIX=/home/moriyama/tools/bin/htslib-1.8/tabix

DBSNP=/home/moriyama/tools/ref/db/GRCh37_snp138.sorted.bed.gz
LOWMAP=/home/moriyama/work/OHVarfinDer/db/SNP/GRCh37_snp138.sort.bed

OHVARDIR=/home/moriyama/sftp_scripts/github/OHVarfinDer/
OHVARFINDER=${OHVARDIR}/bin/ohvarfinder

# PYTHON=/usr/local/package/python/current2.7/bin/python
PYTHON=/usr/local/package/python/2.7.15/bin/python

export PERL5LIB=~/myperl/lib:~/myperl/lib/perl5:~/myperl/lib/perl5/version/x86_64-linux-thread-multi:~/myperl/lib/perl5/site_perl/version:/home/moriyama/tools/packages/vcftools/src/perl
export PATH=/home/moriyama/tools/bin/htslib-1.8:$PATH
export PYTHONPATH=~/local/lib/python2.7/site-packages:${PYTHONPATH}

