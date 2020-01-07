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


input_dir=${1}
bam_file_name=${2}
output_dir=${3}
output_base_name=${4}

check_mkdir ${output_dir}

metrics=${output_dir}/${output_base_name}.metrics
tmp_file=${output_dir}/${output_base_name}.tmp
output_bam=${output_dir}/${output_base_name}.bam
input_bam_files=""

for input_file in $(find ${input_dir} -name ${bam_file_name}); do
    input_bam_files="${input_bam_files} I=${input_file}"
done



echo "input_dir: ${input_dir}"
echo "bam_file_name: ${bam_file_name}"
echo "output_dir: ${output_dir}"
echo "output_base_name: ${output_base_name}"

echo "metrics: ${metrics}"
echo "tmp_file: ${tmp_file}"
echo "output_bam: ${output_bam}"
echo "input_bam_files: ${input_bam_files}"


echo "${BIOBAMBAM}/bammarkduplicates \
M=${metrics} \
tmpfile=${tmp_file} \
markthreads=1 \
rewritebam=1 \
rewritebamlevel=1 \
index=1 \
md5=1 \
${input_bam_files} \
O=${output_bam}"
${BIOBAMBAM}/bammarkduplicates \
M=${metrics} \
tmpfile=${tmp_file} \
markthreads=1 \
rewritebam=1 \
rewritebamlevel=1 \
index=1 \
md5=1 \
${input_bam_files} \
O=${output_bam}
check_error $?


echo "${SAMTOOLS} index ${output_bam}"
${SAMTOOLS} index ${output_bam}
check_error $?


