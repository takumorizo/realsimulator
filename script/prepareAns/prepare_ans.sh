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

bash /home/moriyama/sftp_scripts/180202_SiMHaT/src/realSimulation/prepareAns/prepare_ans.sh \
/home/moriyama/work/OHVarfinDer/realWhole/outputMutationCall/HCC1143_Pure/OHVarfinDer.tmp.calls.noheader.txt \
/home/moriyama/work/SiMHaT/simulation/TCGA_answer \
HCC1143_ans

bash /home/moriyama/sftp_scripts/180202_SiMHaT/src/realSimulation/prepareAns/prepare_ans.sh \
/home/moriyama/work/OHVarfinDer/realWhole/outputMutationCall/HCC1954_Pure/OHVarfinDer.tmp.calls.noheader.txt \
/home/moriyama/work/SiMHaT/simulation/TCGA_answer \
HCC1954_ans

#__CO__

ohvar_no_header=${1}
output_dir=${2}
tag=${3}

check_mkdir ${output_dir}

echo "source ${DIR}/params/filter_list.sh"
source ${DIR}/params/filter_list.sh
echo "source ${DIR}/params/params.sh"
source ${DIR}/params/params.sh

echo "cat ${ohvar_no_header} | grep -E -v ${filterExpression} | ${PYTHON} ${DIR}/rm_snp.py > ${output_dir}/output.${tag}.variant"
cat ${ohvar_no_header} | grep -E -v ${filterExpression} | ${PYTHON} ${DIR}/rm_snp.py > ${output_dir}/output.${tag}.variant
check_error $?

echo "${PYTHON} ${DIR}/ohvar_ans_to_vcf.py ${REF} ${output_dir}/output.${tag}.variant ${output_dir}/output.${tag}.variant.vcf ${tag} -1000"
${PYTHON} ${DIR}/ohvar_ans_to_vcf.py ${REF} ${output_dir}/output.${tag}.variant ${output_dir}/output.${tag}.variant.vcf ${tag} -1000
check_error $?



