from pysam import VariantFile
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import sys

class VariantResults:
    def __init__(self,patient,model_name="v2-500m-multi-species",window_length="1500"):
        self.window_length = 2*int(window_length) - 2*int(window_length)%6 # should be a multiple of 6
        self.model_name = model_name
        self.patient = patient
        self.myvcf = VariantFile(f"{patient}/NT_inputs/{patient}_analysis-ready-variants-combined-sorted.vcf.gz")
        self.bed = pd.read_csv(f'{patient}/NT_inputs/{patient}_intervals.bed', sep="\t", header=None)
        self.bed.columns = ["chr","start","end"]

        self.bed = pd.read_csv(f'{patient}/NT_inputs/{patient}_intervals.bed', sep="\t", header=None)
    def generate_df(self):
        p = Path(f"{self.patient}/outputs/scores_per_chrom").glob("*")
        filelist = [str(path) for path in p]
        self.results_df = pd.DataFrame({"Chromosome":[],"Index_in_bed":[],"Begin_6mer":[],"Cosine_Similarity":[],"Dot_Product":[],"1-L1_Loss":[],"1-MSE_Loss":[]})
        for i in tqdm(range(len(filelist))):
            try:
                chr_df = pd.read_csv(filelist[i],sep="\t",header=None)
                chr_df.rename(columns={0:"Chromosome",1:"Index_in_bed",2:"Begin_6mer",3:"Cosine_Similarity",4:"Dot_Product",5:"1-L1_Loss",6:"1-MSE_Loss"},inplace=True)
                self.results_df = pd.concat((self.results_df,chr_df),ignore_index = True).astype({'Index_in_bed': 'int32',"Begin_6mer":"int32"})
            except:
                continue
        print("sorting...")
        self.results_df.sort_values(by=["Chromosome","Begin_6mer"],inplace=True)
    def lowest_scores(self,lowest_metric,n="100",plot="1",results_df = None):
        n = int(n)
        plot = bool(int(plot))
        if results_df is None:
            results_df = self.results_df
        self.lowest_scores_df = results_df.sort_values(by=lowest_metric).head(n)
        self.lowest_scores_df["Begin_Region"] = self.bed.iloc[self.lowest_scores_df["Index_in_bed"]]["start"].values
        self.lowest_scores_df["End_Region"] = self.bed.iloc[self.lowest_scores_df["Index_in_bed"]]["end"].values
        self.lowest_scores_df = self.lowest_scores_df[['Chromosome', 'Index_in_bed', 'Begin_Region', 'End_Region', 'Begin_6mer', 'Cosine_Similarity', 'Dot_Product', '1-L1_Loss', '1-MSE_Loss']]
        generated_index = []
        if plot:
            for index, row in tqdm(self.lowest_scores_df.iterrows(),total=n):
                if index in generated_index:
                    continue
                else:
                    generated_index.append(index)
                    self.metric_match_line_plot(row["Index_in_bed"],lowest_metric)
        self.lowest_scores_df.to_csv(f"{self.patient}/outputs/{self.patient}_{lowest_metric}_lowest_scores.bed", header=None,index=None, sep='\t', mode='w+')
        return self.lowest_scores_df
    def stream_variants(self,index):
        row = self.bed.iloc[index]
        print(f"The segment at {row["chr"]} from {row["start"]} to {row["end"]} contains the following variants:")
        print("CHROM","POS","REF","ALT","QUAL")
        for vcf_rec in self.myvcf.fetch(row["chr"],row["start"], row["end"]):
            print(vcf_rec.chrom,vcf_rec.pos,vcf_rec.ref,vcf_rec.alts[0],vcf_rec.qual)
    def histogram_plot(self, n_bins = 1000, global_results_df=None):
        if global_results_df is None:
            results_df = self.results_df
        n_bins = 1000
        dist1 = global_results_df["Cosine_Similarity"]
        dist2 = global_results_df["Dot_Product"]

        fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
        axs[0].set_ylim([0,5000000])
        axs[1].set_ylim([0,5000000])
        axs[0].set_xlabel("Cosine Similarity")
        axs[1].set_xlabel("Dot Product")
        title = f"Histograms ({n_bins} bins) showing the distribution of scores"
        plt.suptitle(title)
        axs[0].hist(dist1, bins=n_bins)
        axs[1].hist(dist2, bins=n_bins)
        plt.savefig(f"{self.patient}/outputs/histogram.png")
    def metric_match_line_plot(self,index_in_bed,metric):
        row = self.bed.iloc[index_in_bed]
        fig, ax = plt.subplots()
        plot_df = self.results_df[(self.results_df["Index_in_bed"]==index_in_bed)]
        scores = list(plot_df[metric])
        x = list(pd.concat([plot_df["Begin_6mer"],pd.Series([row["end"]])]))
        ax.stairs(edges=x,values=scores,color="black",label=metric)
        pos_snp = []
        pos_ins = []
        pos_del = []
        for vcf_rec in self.myvcf.fetch(row["chr"],row["start"], row["end"]):
            if len(vcf_rec.ref)==len(vcf_rec.alts[0]):
                pos_snp.append(vcf_rec.pos)
            elif len(vcf_rec.ref)>len(vcf_rec.alts[0]):
                pos_del.append(vcf_rec.pos)
            elif len(vcf_rec.ref)<len(vcf_rec.alts[0]):
                pos_ins.append(vcf_rec.pos)
        height_snp = []
        height_ins = []
        height_del = []
        for i in range(len(plot_df)):
            for snp in pos_snp:
                if x[i]<=snp and x[i+1]>snp:
                    height_snp.append(scores[i])
            for ins in pos_ins:
                if x[i]<=ins and x[i+1]>ins:
                    height_ins.append(scores[i])
            for dele in pos_del:
                if x[i]<=dele and x[i+1]>dele:
                    height_del.append(scores[i])
        try:
            ax.stem(pos_ins,height_ins,linefmt="green",label="Insertion in variant")
        except ValueError:
            pass
        try:
            ax.stem(pos_del,height_del,linefmt="blue",label="Deletion in variant")
        except ValueError:
            pass
        try:
            ax.stem(pos_snp,height_snp,linefmt="red",label="SNP")
        except ValueError:
            pass

        fig.set_size_inches(14*(row["end"]-row["start"])/50000, 6)
        fig.set_dpi(100)
        plt.title(f"Chromosome {row["chr"]}, Position {row["start"]}~{row["end"]}, Model {self.model_name}, Window length {self.window_length}, {metric}")
        plt.xlabel("Position on the reference genome")
        plt.xticks(rotation=45, ha="right")
        ax.ticklabel_format(useOffset=False, style='plain')
        ax.set_ylim([-1.1,1.1])
        ax.set_xlim([row["start"],row["end"]])
        plt.legend()
        plt.savefig(f"{self.patient}/outputs/low_score_plots/{index}_{metric}_{row["chr"]}_{row["start"]}-{row["end"]}_line_plot.png",bbox_inches='tight')
        plt.close()

metrics = ["Cosine_Similarity","Dot_Product","1-L1_Loss","1-MSE_Loss"]
results_class = VariantResults(sys.argv[1], window_length = sys.argv[2])
results_class.generate_df()
global_results_df = results_class.results_df
results_class.histogram_plot(global_results_df = global_results_df)
cos_lowest_scores_df = results_class.lowest_scores(metrics[0],n=sys.argv[3], plot=sys.argv[4],results_df = global_results_df)
dot_lowest_scores_df = results_class.lowest_scores(metrics[1],n=sys.argv[3], plot=sys.argv[4],results_df = global_results_df)
