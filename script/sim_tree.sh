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

: <<'#__CO__'
CURLOGDIR=${LOGDIR}
check_mkdir ${CURLOGDIR}
LOGSTR=-e\ ${CURLOGDIR}\ -o\ ${CURLOGDIR}
#__CO__

called_vcf=${1}
ans_vcf=${2}
output_dir=${3}
tree_vector_base=${4}
tumor_vcf=${5}
error_vcf=${6}
proportion_path=${7}
num_sample=${8}
param=${9}
seed=${10}


source ${param}

echo called_vcf ${called_vcf}
echo ans_vcf ${ans_vcf}
echo output_dir ${output_dir}
echo tree_vector_base ${tree_vector_base}
echo tumor_vcf ${tumor_vcf}
echo error_vcf ${error_vcf}
echo proportion_path ${proportion_path}
echo num_sample ${num_sample}
echo param ${param}
echo seed ${seed}


check_mkdir ${output_dir}

: <<'#__CO__'
Extract true mutations and error positions in vcf format.
#__CO__

echo "${VCFSORT} ${called_vcf} > ${output_dir}/called.tmp.sort.vcf"
${VCFSORT} ${called_vcf} > ${output_dir}/called.tmp.sort.vcf
check_error $?

echo "${VCFSORT} ${ans_vcf} > ${output_dir}/ans.tmp.sort.vcf"
${VCFSORT} ${ans_vcf} > ${output_dir}/ans.tmp.sort.vcf
check_error $?

echo "${BEDTOOLS} intersect -header -v -a ${output_dir}/called.tmp.sort.vcf -b ${output_dir}/ans.tmp.sort.vcf -sorted > ${error_vcf}"
${BEDTOOLS} intersect -header -v -a ${output_dir}/called.tmp.sort.vcf -b ${output_dir}/ans.tmp.sort.vcf -sorted > ${error_vcf}
check_error $?

echo "${PYTHON} ${DIR}/exec_tree_simulator.py \
${tree_vector_base} \
${NODE_SIZE} \
${seed} \
${ZERO_WEIGHT} \
${ans_vcf} \
${tumor_vcf} \
${ALPHA_VARIANT} \
${proportion_path} \
${ALPHA_CLONE} \
${num_sample}"
${PYTHON} ${DIR}/exec_tree_simulator.py \
${tree_vector_base} \
${NODE_SIZE} \
${seed} \
${ZERO_WEIGHT} \
${ans_vcf} \
${tumor_vcf} \
${ALPHA_VARIANT} \
${proportion_path} \
${ALPHA_CLONE} \
${num_sample}

check_error $?











