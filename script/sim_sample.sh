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

tumor_vcf=${1}
error_vcf=${2}
tumor_pure=${3}
normal_pure=${4}
output_dir=${5}/${SGE_TASK_ID}
tree_vector=${6}
param=${7}

source ${param}

check_mkdir ${output_dir}

: <<'#__CO__'
run simulator
#__CO__

echo "${PYTHON} ${DIR}/exec_error_simulator.py \
${error_vcf} \
${ALPHA_ERROR} \
${BETA_ERROR} \
${tumor_pure} \
${normal_pure} \
${output_dir}/sim_error_${SGE_TASK_ID}.tmp.bam \
${SGE_TASK_ID}"
${PYTHON} ${DIR}/exec_error_simulator.py \
${error_vcf} \
${ALPHA_ERROR} \
${BETA_ERROR} \
${tumor_pure} \
${normal_pure} \
${output_dir}/sim_error_${SGE_TASK_ID}.tmp.bam \
${SGE_TASK_ID}
check_error $?


echo "${PYTHON} ${DIR}/exec_tumor_simulator.py \
${tree_vector} \
${tumor_vcf}   \
${ALPHA_CLONE} \
${output_dir}/${SGE_TASK_ID}_tumor_proportions.txt \
${tumor_pure} \
${normal_pure} \
${output_dir}/sim_tumor_${SGE_TASK_ID}.tmp.bam \
${SGE_TASK_ID}"
${PYTHON} ${DIR}/exec_tumor_simulator.py \
${tree_vector} \
${tumor_vcf}   \
${ALPHA_CLONE} \
${output_dir}/${SGE_TASK_ID}_tumor_proportions.txt \
${tumor_pure} \
${normal_pure} \
${output_dir}/sim_tumor_${SGE_TASK_ID}.tmp.bam \
${SGE_TASK_ID}
check_error $?















