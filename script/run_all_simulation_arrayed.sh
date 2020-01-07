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


all_data=${1}
seed=${2:-0}
job_id=${3:-default}
sample_seed_stride=${4:-100}

CURLOGDIR=${LOGDIR}/realSimulation/${job_id}
check_mkdir ${CURLOGDIR}
LOGSTR=-e\ ${CURLOGDIR}\ -o\ ${CURLOGDIR}


cat ${all_data} | while read called_vcf ans_vcf normal_pure tumor_pure num_sample output_dir tag param; do
	job_name=${tag}

	check_mkdir ${output_dir}/tree
	tree_vector_base=${output_dir}/tree/tree_${tag}
	tree_vector=${output_dir}/tree/tree_${tag}.txt

	echo "qsub -l os7 -q mjobs.q,ljobs.q -v DIR=${DIR} -v CONFIG=${CONFIG} \
	-l s_vmem=4G,mem_req=4G -N sim_tree.${job_name} ${LOGSTR} ${DIR}/sim_tree.sh \
	${called_vcf} \
	${ans_vcf} \
	${output_dir}/tree \
	${tree_vector_base} \
	${output_dir}/tree/tumor.vcf \
	${output_dir}/tree/error.vcf \
	${output_dir}/tree/tumor_proportions.txt \
	${num_sample} \
	${param} \
	${seed}"
	qsub -l os7 -q mjobs.q,ljobs.q -v DIR=${DIR} -v CONFIG=${CONFIG} \
	-l s_vmem=4G,mem_req=4G -N sim_tree.${job_name} ${LOGSTR} ${DIR}/sim_tree.sh \
	${called_vcf} \
	${ans_vcf} \
	${output_dir}/tree \
	${tree_vector_base} \
	${output_dir}/tree/tumor.vcf \
	${output_dir}/tree/error.vcf \
	${output_dir}/tree/tumor_proportions.txt \
	${num_sample} \
	${param} \
	${seed}

	tumor_vcf=${output_dir}/tree/tumor.vcf
	error_vcf=${output_dir}/tree/error.vcf

	chr_all=${output_dir}/tree/chr_all.txt
	echo "${PYTHON} ${DIR}/print_chromosomes.py ${called_vcf} ${ans_vcf} > ${chr_all}"
	${PYTHON} ${DIR}/print_chromosomes.py ${called_vcf} ${ans_vcf} > ${chr_all}
	chr_size=$(cat ${chr_all} | wc -l)

	for (( n = 1; n <= ${num_sample}; n++ )); do
		sample_seed=$((${seed}*${sample_seed_stride}+${n}))
		echo "qsub -l os7 -q mjobs.q,ljobs.q -v DIR=${DIR} -v CONFIG=${CONFIG} -t 1-${chr_size}:1 -tc 5 \
		-l s_vmem=8G,mem_req=8G -hold_jid \"sim_tree.${job_name}\" -N sim_sample.${job_name}.${n} ${LOGSTR} ${DIR}/sim_sample_arrayed.sh \
		${sample_seed} \
		${n}		   \
		${tumor_vcf}   \
		${error_vcf}   \
		${tumor_pure}  \
		${normal_pure} \
		${output_dir}/${n}/tmp/ \
		${tree_vector} \
		${output_dir}/tree/tumor_proportions.txt \
		${param} \
		${chr_all}"
		qsub -l os7 -q mjobs.q,ljobs.q -v DIR=${DIR} -v CONFIG=${CONFIG} -t 1-${chr_size}:1 -tc 5 \
		-l s_vmem=8G,mem_req=8G -hold_jid "sim_tree.${job_name}" -N sim_sample.${job_name}.${n} ${LOGSTR} ${DIR}/sim_sample_arrayed.sh \
		${sample_seed} \
		${n}		   \
		${tumor_vcf}   \
		${error_vcf}   \
		${tumor_pure}  \
		${normal_pure} \
		${output_dir}/${n}/tmp/ \
		${tree_vector} \
		${output_dir}/tree/tumor_proportions.txt \
		${param} \
		${chr_all}

		echo "qsub -l os7 -q mjobs.q,ljobs.q -pe def_slot 2 -v DIR=${DIR} -v CONFIG=${CONFIG} \
		-l s_vmem=10.6G,mem_req=10.6G -hold_jid \"sim_sample.${job_name}.${n}\" -N markdup.${job_name}.${n} ${LOGSTR} ${DIR}/markdup_bams.sh \
		${output_dir}/${n}/tmp all.sort.bam ${output_dir}/${n}/all/ simulated"
		qsub -l os7 -q mjobs.q,ljobs.q -pe def_slot 2 -v DIR=${DIR} -v CONFIG=${CONFIG} \
		-l s_vmem=10.6G,mem_req=10.6G -hold_jid "sim_sample.${job_name}.${n}" -N markdup.${job_name}.${n} ${LOGSTR} ${DIR}/markdup_bams.sh \
		${output_dir}/${n}/tmp all.sort.bam ${output_dir}/${n}/all/ simulated
	done

done





