WHOLE GENOME SEQUENCING NUCLEOTIDE TRANSFORMER, written by Georg Christian Sommerer, 2024, Metzger Lab, Max Delbrueck Center Berlin


The Whole Genome Sequencing Nucleotide Transformer (WGS-NT) is a program that takes WGS paired end reads, calls the variants on them, and then calculates the cosine similarities of the output embeddings of the Nucleotide Transformer (https://www.biorxiv.org/content/10.1101/2023.01.11.523679v3) on them.

====================================================================
INSTALLATION
====================================================================
1. Create a conda environment (recommended).
2. Install PyTorch within the environment. Since this program only works with GPUs and not with CPUs, it is necessary to make sure that PyTorch is installed while GPUs are enabled and that the installed PyTorch version works for the GPU version.
3. Download the following programs within the environment: samtools, bcftools, bedtools, bwa, gatk, picard, fastqc, multiqc
4. Install the following python packages within the environment: biopython, pysam, time, pathlib, numpy, pandas, matplotlib, transformers, gc, tqdm

====================================================================
FILE STRUCTURE
====================================================================
In wgs_nt:
	wgs_nt.sh: Runs the pipeline (working).
	wgs_nt_transformer.py: Generates the chr*.bed files using the Nucleotide Transformer (working).
	wgs_nt_transformer.ipynb: Jupyter Notebook with the same content as the .py file (possibly broken).
	wgs_nt_results.py: Used to generate plots, histograms, lowest scores, etc. (broken).
	wgs_nt_results.ipynb: Jupyter Notebook with the same content as the .py file (working).
	wgs_nt_ROI.ipynb: Downstream analysis for CHG034730 and CHG034731: Used to generate a dataframe with the common lowest scores (working).
	wgs_nt_analyze_one.py: Downstream analysis: analyzes the effects of combinations of variants in a region to determine which has the strongest effect on the score (working).
	(raw data not in this repository) CHG034730: WGS of patient 1 with an undiagnosed neurodevelopmental disease.
	(raw data not in this repository) CHG034731: WGS of patient 1 (sister of patient 1) with an undiagnosed neurodevelopmental disease.
	ROI: Regions of interest of both patient 1 and 2.
	test: Small subset of the reads of patient 1 to quickly run the pipeline for testing purposes.
	(raw data not in this repository, but can be downloaded from https://trace.ncbi.nlm.nih.gov/Traces/index.html?view=run_browser&acc=SRR11567769&display=download) SRR11567769: WES of a patient with Leigh syndrome used for validation of the Nucleotide Transformers ability to link cosine similarity and disease severity.
	(not in this repository, but is downloaded automatically in wgs_nt.sh) supporting_files: Files such as the reference genome or common variants that are downloaded in step 0 of the pipeline.
In patient_name:
	reads: Contains the raw reads and must be created before running the pipeline.
	aligned_reads: Contains .bam/.sam files created in the alignment and base quality recalibration steps.
	variants: Contains .vcf files from the variant calling and filtering steps.
	NT_inputs: Contains the analysis ready .vcf file as well as the .bed files with the variant containing regions.
	outputs: Contains the outputs of the Nucleotide Transformer (chr*.bed files, histogram, lowest scores, plots of lowest scores).
	metrics: Contains information about the quality of the reads (fastqc), the quality of the alignment (multiqc), etc.

====================================================================
USAGE
====================================================================
1. Create a folder with the patient name in the wgs_nt folder and a folder called "reads" within this folder. Then, place the .fastq.gz reads in this folder.
2. In the wgs_nt folder, write ./wgs_nt.sh patient_name window_length n plot
	patient_name must match the name of the folder in the wgs_nt folder. This argument is mandatory.
	window_length is the number of bases to the left and right of each variant. Therefore, the region [variant_pos - window_length, variant_pos + window_length] is analyzed. The standard value is 1500.
	n is the number of lowest scores that is output. The standard value is 1000, meaning that (in case of cosine similarity) the positions of the 1000 6-mers with the lowest cosine similarities is saved.
	plot determines whether or not plots of the regions with the n lowest scores should be created (0=No, 1=Yes). The standard value is 0.
    Note 1: The results from CHG034730, CHG034731, and SRR11567769 were generated with the standard values.
    Note 2: Since the only step that requires n and plot is broken (and should probably be done in the jupyter notebook anyways), the only arguments really needed are patient_name and maybe window_length.
3. It is also possible to open the last steps in a Jupyter Notebook, where it is possible to change more values than via the command line (e.g. the number of bins of the histogram, etc.). Also, wgs_nt_results.py seems to be broken, therefore it is recommended to perform step 11 via wgs_nt_results.ipynb.
4. In this specific use case, the notebook wgs_nt_ROI.ipynb was used to combine the lowest scores from the two siblings in CHG034730 and CHG034731.
5. python3 wgs_nt_analyze_one.py patient_name window_size index_in_bed lowest_score_position can be run for further analysis of the mutations in a region of interest. The index_in_bed can be found in the lowest_scores.bed files of each sibling (for easier access to these values, it might be useful to also write them in the roi_metric.bed file).

====================================================================
OUTPUTS
====================================================================
in .patient_name/outputs:
	histogram.png: A histogram with the distribution of cosine similarities and dot products.
	lowest_scores.bed: Files containing the chromosome name, the index in the patient_name_intervals.bed file used as the input, the start of the analyzed region, the end of the analyzed region, the position of the 6-mer in the chromosome, as well as various scores. It contains n entries which correspond to the 6-mers that have the lowest values in the score that is equal to the file name (e.g. patient_name_Cosine_Similarity_lowest_scores.bed contains the n 6-mers with the lowest cosine similarities).
	scores_per_chr/*: Contains the raw 6-mers for each chromosome with the same column structures as lowest_scores.bed.
	low_score_plots/*: Contains the plots of the regions with entries in lowest_scores.bed. The name structure is Begin6mer_Metric_Chromosome_StartPosition_EndPosition_line_plot.png (currently, the name does not indicate the position in lowest_scores.bed; instead, the plots of regions with the lowest scores are created first. It might be wise to include this information (as well as Index_in_bed) in the file name).
in ROI:
	chr_lowest_score_pos/lowest_score_plots: Contains plots of the cosine similarity of the same region with a certain subset of mutations.
	roi_score.bed: Contains the common lowest scores (cosine similarity, dot product) between patient 1 and 2. Since the top 50 entries of both files are approximately equal (or at least appear in both files), it probably makes little difference which score to use.

====================================================================
NEXT STEPS
====================================================================
There are four main steps that can be taken from here on:
    1. Verify the severity of the found mutations (see S:\Metzger Lab Common\Presentations\georg_sommerer_wgs_nt_presentation.pptx) by inducing them in vitro in organoids
    2. Verify the efficacy of the WGS-NT pipeline. This can be done by running the entire pipeline on WGS or WES of patients where both the disease and the genetic cause is known, or by taking single mutations (e.g. from ClinVar) that are known to cause diseases and creating a var_seq with only this mutation induced. This has been tried on WES from a patient with Leigh Syndrome (SRR11567769), where the relevant mutation was 8993T>G in chrM (MT-ATP6); if the single N in the mitochondrial chromosome of hg38 is replaced by any nucleotide (so that chrM is not skipped), then the lowest Cosine Similarity is only 0.076, which is way too high to stand out. Therefore, it is possible that the WGS-NT does not recognize significant SNPs, but only significant Indels (which has to be tested with another dataset).
    3. If the WGS-NT pipline has been found to recognize severe mutations, then run it on other patients (e.g. the other pairs of siblings).
    4. Modify the code to address shortcomings:
        4.1. Regions that contain an N are ignored. This is because if due to an indel the number of N between var_seq and ref_seq are different, the number of scores generated would become different and can not be compared.
        4.2. It is relatively common (in 2% of entries in the .vcf file) that two different variants (on for each chromosome) exists. In this case, the var_seq is created by only inserting the first of these variants; the second one is currently completely ignored.
        4.3. Currently, a score is generated for each 6-mer and the lowest 6-mers are collected. Meanwhile, it might be better to instead (as the original paper suggests) average the cosine similarities for each region and then compare these averages. In this case, the average of cosine similarities other than 1 (or close to 1) should probably be calculated. The reason is that most scores before the first indel are mostly 1 (see the low_score_plots), meaning that generally, the later the first indel comes or the smaller the region is, the larger the proportion of cosine similarities close to 1 becomes, which is caused simply by the design of the regions and not due to any biological reason.
