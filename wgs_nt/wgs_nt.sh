#!/bin/bash

echo "Download reference genome"

if [ ! -f supporting_files/hg38/hg38.fa ]; then
	mkdir supporting_files supporting_files/hg38

	wget -P supporting_files/hg38/ https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz
	gunzip supporting_files/hg38/hg38.fa.gz

	index ref - .fai file before running haplotype caller
	samtools faidx supporting_files/hg38/hg38.fa


	ref dict - .dict file before running haplotype caller
	gatk CreateSequenceDictionary R=supporting_files/hg38/hg38.fa O=supporting_files/hg38/hg38.dict

	wget -P supporting_files/hg38/ https://storage.googleapis.com/genomics-public-data/resources/broad/hg38/v0/Homo_sapiens_assembly38.dbsnp138.vcf
	wget -P supporting_files/hg38/ https://storage.googleapis.com/genomics-public-data/resources/broad/hg38/v0/Homo_sapiens_assembly38.dbsnp138.vcf.idx
	bwa index ${ref}
else
	echo "Already done."
fi

ref="../supporting_files/hg38/hg38.fa"
if [ ! -f $1/reads/$1_R1.fastq.gz ]; then
	echo "Reads could not be found. Please place them into the reads folder."
	mkdir $1 $1/reads
	exit
fi

cd $1/
mkdir aligned_reads metrics metrics/bam_metrics metrics/fastqc NT_inputs outputs outputs/low_score_plots outputs/scores_per_chrom  variants
echo "1/11: FastQC"
if [ ! -f metrics/fastqc/$1_R1_fastqc.html ]; then
	fastqc reads/$1_R1.fastq.gz -o metrics/fastqc
	fastqc reads/$1_R2.fastq.gz -o metrics/fastqc
	read -p "Is trimming needed (y/n)" check_trim
	if [ $check_trim == y ]; then
		trimmomatic SE -threads 4 reads/$1_R1.fastq.gz reads/$1_R1_trimmed.fastq.gz TRAILING:10 -phred33
		trimmomatic SE -threads 4 reads/$1_R2.fastq.gz reads/$1_R2_trimmed.fastq.gz TRAILING:10 -phred33
		fastqc reads/$1_R1_trimmed.fastq.gz -o metrics/fastqc
		fastqc reads/$1_R2_trimmed.fastq.gz -o metrics/fastqc
	fi
else
	echo "Already done."
fi

echo "2/11: Map reads to hg38"
if [ ! -f aligned_reads/$1.paired.sam ]; then
	if [ $check_trim == y ]; then
		bwa mem -t 4 -R "@RG\tID:$1\tPL:ILLUMINA\tSM:$1" ${ref} reads/$1_R1_trimmed.fastq.gz reads/$1_R2_trimmed.fastq.gz > aligned_reads/$1.paired.sam
	else
		bwa mem -t 4 -R "@RG\tID:$1\tPL:ILLUMINA\tSM:$1" ${ref} reads/$1_R1.fastq.gz reads/$1_R2.fastq.gz > aligned_reads/$1.paired.sam
	fi
else
	echo "Already done."
fi

echo "3/11: Mark duplicates"
if [ ! -f aligned_reads/$1_sorted_dedup_reads.bam ]; then
	mkdir tmp
	picard SortSam -I aligned_reads/$1.paired.sam -O aligned_reads/$1_sorted.bam -SORT_ORDER coordinate --TMP_DIR tmp
	rmdir -rf tmp

	mkdir tmp
	picard MarkDuplicates -I aligned_reads/$1_sorted.bam -O aligned_reads/$1_sorted_dedup_reads.bam -M aligned_reads/$1_marked_dup_metrics.txt --TMP_DIR tmp
	rmdir -rf tmp
else
	echo "Already done."
fi

echo "4/11: Base Quality Score Recalibration"
if [ ! -f aligned_reads/$1_sorted_dedup_bqsr_reads.bam ]; then
	gatk BaseRecalibrator -I aligned_reads/$1_sorted_dedup_reads.bam -R ${ref} --known-sites ../supporting_files/hg38/Homo_sapiens_assembly38.dbsnp138.vcf -O aligned_reads/recal_data.table

	gatk ApplyBQSR -I aligned_reads/$1_sorted_dedup_reads.bam -R ${ref} --bqsr-recal-file aligned_reads/recal_data.table -O aligned_reads/$1_sorted_dedup_bqsr_reads.bam 
else
	echo "Already done."
fi

echo "5/11: MultiQC"
#Originally contained multiqc reports, is now skipped.
echo "Skipped."

echo "6/11: Variant Calling"

if [ ! -f variants/$1_raw_indels.vcf ]; then
	gatk HaplotypeCaller -R ${ref} -I aligned_reads/$1_sorted_dedup_bqsr_reads.bam -O variants/$1_raw_variants.vcf
	gatk SelectVariants -R ${ref} -V variants/$1_raw_variants.vcf --select-type SNP -O variants/$1_raw_snps.vcf
	gatk SelectVariants -R ${ref} -V variants/$1_raw_variants.vcf --select-type INDEL -O variants/$1_raw_indels.vcf
else
	echo "Already done."
fi

echo "7/11: Variant Filtering"

if [ ! -f variants/$1_analysis-ready-indels-filteredGT.vcf ]; then
	gatk VariantFiltration -R ${ref} -V variants/$1_raw_snps.vcf -O variants/$1_filtered_snps.vcf -filter "QD < 2.0" --filter-name "QD2" -filter "QUAL < 30.0" --filter-name "QUAL30" -filter "SOR > 3.0" --filter-name "SOR3" -filter "FS > 60.0" --filter-name "FS60" -filter "MQ < 40.0" --filter-name "MQ40" -genotype-filter-expression "DP < 10" -genotype-filter-name "DP10" -genotype-filter-expression "GQ < 10" -genotype-filter-name "GQ10"
	gatk VariantFiltration -R ${ref} -V variants/$1_raw_indels.vcf -O variants/$1_filtered_indels.vcf -filter "QD < 2.0" --filter-name "QD2" -filter "QUAL < 30.0" --filter-name "QUAL30" -filter "FS > 200.0" --filter-name "FS200" -genotype-filter-expression "DP < 10" -genotype-filter-name "DP10" -genotype-filter-expression "GQ < 10" -genotype-filter-name "GQ10"
	
	gatk SelectVariants --exclude-filtered -V variants/$1_filtered_snps.vcf -O variants/$1_analysis-ready-snps.vcf
	gatk SelectVariants --exclude-filtered -V variants/$1_filtered_indels.vcf -O variants/$1_analysis-ready-indels.vcf
	cat variants/$1_analysis-ready-snps.vcf|grep -v -E "DP10|GQ10" > variants/$1_analysis-ready-snps-filteredGT.vcf
	cat variants/$1_analysis-ready-indels.vcf| grep -v -E "DP10|GQ10" > variants/$1_analysis-ready-indels-filteredGT.vcf
else
	echo "Already done."
fi

echo "8/11: Sort and index variants"
if [ ! -f NT_inputs/$1_analysis-ready-variants-combined-sorted.vcf ]; then
	bgzip -k variants/$1_analysis-ready-indels-filteredGT.vcf
	bgzip -k variants/$1_analysis-ready-snps-filteredGT.vcf
	bcftools index -t variants/$1_analysis-ready-snps-filteredGT.vcf.gz
	bcftools index -t variants/$1_analysis-ready-indels-filteredGT.vcf.gz
	bcftools concat -a variants/$1_analysis-ready-indels-filteredGT.vcf.gz variants/$1_analysis-ready-snps-filteredGT.vcf.gz -o variants/$1_analysis-ready-variants-combined.vcf.gz
	bcftools sort variants/$1_analysis-ready-variants-combined.vcf.gz -o NT_inputs/$1_analysis-ready-variants-combined-sorted.vcf.gz
	bcftools index -t NT_inputs/$1_analysis-ready-variants-combined-sorted.vcf.gz
	gunzip -c NT_inputs/$1_analysis-ready-variants-combined-sorted.vcf.gz > NT_inputs/$1_analysis-ready-variants-combined-sorted.vcf
else
	echo "Already done."
fi

echo "9/11: Merge regions"
if [ ! -f NT_inputs/$1_intervals.bed ]; then
	cat NT_inputs/$1_analysis-ready-variants-combined-sorted.vcf | grep -v "#" | awk -v FS='\t' -v OFS='\t' -vwindow=${2:-1500} '{print $1,(($2-window>0 ? $2-window : 0)),$2+window}' > NT_inputs/$1_intervals_non_merged.bed
	bedtools merge -i NT_inputs/$1_intervals_non_merged.bed > NT_inputs/$1_intervals_merged.bed
	cat NT_inputs/$1_intervals_merged.bed | awk -v FS='\t' -v OFS='\t' '{print $1, $2, $3-($3-$2)%6}' > NT_inputs/$1_intervals.bed
else
	echo "Already done."
fi

cd ..
echo "10/11 Use the Nucleotide Transformer"
python3 wgs_nt_transformer.py $1 ${2:-1500}

echo "11/11: Find the lowest scores"
#Broken, use the notebook instead.
if [ ! -f $1/outputs/$1_Dot_Product_lowest_scores.bed ]; then
	python3 wgs_nt_results.py $1 ${2:-1500} ${3:-1000} ${4:-1}
else
	echo "Already done."
fi
