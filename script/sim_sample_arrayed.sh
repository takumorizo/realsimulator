#! /bin/sh
#$ -S /bin/sh
#$ -cwd
if [ -z "${DIR}" ]; then
	readonly DIR=`dirname ${0}`
fi
if [ -z "${CONFIG}" ]; then
	CONFIG=${DIR}/config.sh
fi
if [ -z "${UTIL}" ]; then
	UTIL=${DIR}/utility.sh
fi
source ${CONFIG}
source ${UTIL}

# echo SGE_TASK_ID : $SGE_TASK_ID
# echo SGE_TASK_FIRST : $SGE_TASK_FIRST
# echo SGE_TASK_LAST : $SGE_TASK_LAST
# echo SGE_TASK_STEPSIZE : $SGE_TASK_STEPSIZE

seed=${1}
sample_idx=${2}

tumor_vcf=${3}
error_vcf=${4}
tumor_pure=${5}
normal_pure=${6}
output_dir=${7}/${SGE_TASK_ID}
tree_vector=${8}
proportion_path=${9}
param=${10}
chr_all=${11}

echo "seed: ${1}"
echo "sample_idx: ${2}"
echo "tumor_vcf: ${3}"
echo "error_vcf: ${4}"
echo "tumor_pure: ${5}"
echo "normal_pure: ${6}"
echo "output_dir: ${7}/${SGE_TASK_ID}"
echo "tree_vector: ${8}"
echo "proportion_path: ${9}"
echo "param=: ${10}"
echo "chr_all=: ${11}"

source ${param}
check_mkdir ${output_dir}

chr_concern=$(sed -n ${SGE_TASK_ID}P ${chr_all})

echo "chr_concern: ${chr_concern}"
tumor_tmp_vcf=${output_dir}/tumor.${chr_concern}.vcf
error_tmp_vcf=${output_dir}/error.${chr_concern}.vcf

echo "${VCFTOOLS} --vcf ${tumor_vcf} --stdout --chr ${chr_concern} --recode --recode-INFO-all > ${output_dir}/tumor.${chr_concern}.vcf"
${VCFTOOLS} --vcf ${tumor_vcf} --stdout --chr ${chr_concern} --recode --recode-INFO-all > ${output_dir}/tumor.${chr_concern}.vcf
check_error $?

echo "${VCFTOOLS} --vcf ${error_vcf} --stdout --chr ${chr_concern} --recode --recode-INFO-all > ${output_dir}/error.${chr_concern}.vcf"
${VCFTOOLS} --vcf ${error_vcf} --stdout --chr ${chr_concern} --recode --recode-INFO-all > ${output_dir}/error.${chr_concern}.vcf
check_error $?

: <<'#__CO__'
run simulator
#__CO__

error_tmp_bam=${output_dir}/sim_error_${sample_idx}.tmp.bam
tumor_tmp_bam=${output_dir}/sim_tumor_${sample_idx}.tmp.bam

sample_at=$((${sample_idx}-1))

echo "${PYTHON} ${DIR}/exec_tumor_simulator.py \
${tumor_tmp_vcf}   \
${ALPHA_CLONE} \
${proportion_path} \
${sample_at} \
${tumor_pure} \
${normal_pure} \
${tumor_tmp_bam} ${MIN_VAF} ${MAX_VAF}"
${PYTHON} ${DIR}/exec_tumor_simulator.py \
${tumor_tmp_vcf}   \
${ALPHA_CLONE} \
${proportion_path} \
${sample_at} \
${tumor_pure} \
${normal_pure} \
${tumor_tmp_bam} ${MIN_VAF} ${MAX_VAF}
check_error $?


echo "${PYTHON} ${DIR}/exec_error_simulator.py \
${error_tmp_vcf} \
${ALPHA_ERROR} \
${BETA_ERROR} \
${tumor_pure} \
${normal_pure} \
${error_tmp_bam} \
${seed}"
${PYTHON} ${DIR}/exec_error_simulator.py \
${error_tmp_vcf} \
${ALPHA_ERROR} \
${BETA_ERROR} \
${tumor_pure} \
${normal_pure} \
${error_tmp_bam} \
${seed}
check_error $?

error_fq_base=${output_dir}/sim_error
tumor_fq_base=${output_dir}/sim_tumor
all_fq_base=${output_dir}/sim_both

echo "${SAMTOOLS} bam2fq ${error_tmp_bam} -1 ${error_fq_base}_1.fastq -2 ${error_fq_base}_2.fastq"
${SAMTOOLS} bam2fq ${error_tmp_bam} -1 ${error_fq_base}_1.fastq -2 ${error_fq_base}_2.fastq
check_error $?

echo "${SAMTOOLS} bam2fq ${tumor_tmp_bam} -1 ${tumor_fq_base}_1.fastq -2 ${tumor_fq_base}_2.fastq"
${SAMTOOLS} bam2fq ${tumor_tmp_bam} -1 ${tumor_fq_base}_1.fastq -2 ${tumor_fq_base}_2.fastq
check_error $?

echo "cat ${error_fq_base}_1.fastq >  ${all_fq_base}_1.fastq"
cat ${error_fq_base}_1.fastq >  ${all_fq_base}_1.fastq
check_error $?

echo "cat ${error_fq_base}_2.fastq >  ${all_fq_base}_2.fastq"
cat ${error_fq_base}_2.fastq >  ${all_fq_base}_2.fastq
check_error $?

echo "cat ${tumor_fq_base}_1.fastq >> ${all_fq_base}_1.fastq"
cat ${tumor_fq_base}_1.fastq >> ${all_fq_base}_1.fastq
check_error $?

echo "cat ${tumor_fq_base}_2.fastq >> ${all_fq_base}_2.fastq"
cat ${tumor_fq_base}_2.fastq >> ${all_fq_base}_2.fastq
check_error $?


echo "${BWA} mem ${REF} ${all_fq_base}_1.fastq ${all_fq_base}_2.fastq > ${output_dir}/all.tmp.bam"
${BWA} mem ${REF} ${all_fq_base}_1.fastq ${all_fq_base}_2.fastq > ${output_dir}/all.tmp.bam
check_error $?


echo "${SAMTOOLS} sort -O bam -o ${output_dir}/all.sort.bam ${output_dir}/all.tmp.bam"
${SAMTOOLS} sort -O bam -o ${output_dir}/all.sort.bam ${output_dir}/all.tmp.bam
check_error $?

echo "${SAMTOOLS} index ${output_dir}/all.sort.bam"
${SAMTOOLS} index ${output_dir}/all.sort.bam
check_error $?


echo "rm ${error_tmp_bam}"
rm ${error_tmp_bam}

echo "rm ${tumor_tmp_bam}"
rm ${tumor_tmp_bam}

echo "rm ${output_dir}/all.tmp.bam"
rm ${output_dir}/all.tmp.bam



