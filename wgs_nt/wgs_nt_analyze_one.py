print("Importing libraries...")
import itertools
from Bio import SeqIO
from pysam import VariantFile
import gc
import numpy as np

import torch
from torch import nn
from torch.utils.data import Dataset,DataLoader

from tqdm import tqdm
import sys
import time
import os
from pathlib import Path
import pandas as pd
from transformers import AutoTokenizer, AutoModelForMaskedLM

import matplotlib.pyplot as plt

class Data:
    def __init__(self, patient):
        self.bed = pd.read_csv(f'{patient}/NT_inputs/{patient}_intervals.bed', sep="\t", header=None)
        self.bed.columns = ["chr","start","end"]
        self.hg38 = SeqIO.to_dict(SeqIO.parse('supporting_files/hg38/hg38.fa','fasta'))
        self.patient = patient
        self.vcf = VariantFile(f"{patient}/NT_inputs/{patient}_analysis-ready-variants-combined-sorted.vcf.gz")


class AnalyzeOneRegion:
    def __init__(self, Data,index,roi_pos, model_name="v2-500m-multi-species", window_length="1500"):
        """
        Parameters:
            self.window_length: The amount of bases to the left and right of each variant that is analyzed. This is also the size of the input sequences for the Nucleotide Transformer.
            self.model_name: The name of the Nucleotide Transformer model used.
            self.model: The downloaded Nucleotide Transformer.
            self.tokenizer: The downloaded tokenizer that transforms the sequences into numeric tokens.
        """
        
        self.window_length = 2*int(window_length)-2*int(window_length) % 6
        self.model_name = model_name
        
        self.model = AutoModelForMaskedLM.from_pretrained("InstaDeepAI/nucleotide-transformer-" + self.model_name, trust_remote_code=True).to(device="cuda")
        self.tokenizer = AutoTokenizer.from_pretrained("InstaDeepAI/nucleotide-transformer-" + self.model_name, trust_remote_code=True)
        
        self.patient = Data.patient
        self.hg38 = Data.hg38
        self.bed = Data.bed
        self.vcf = Data.vcf
        
        self.index = int(index)
        self.roi_pos = int(roi_pos)
    
    def get_variants(self,chrom=None,start=None,end=None):
        """
        All variants in a certain region are printed.
        If the chromosome, the start position, and the end position are given as arguments, this region is searched.
        If an index is given, then the region at that index in the .bed file is searched.
        """
        if start is None:
            row = self.bed.iloc[self.index]
            print(f"The segment at {row["chr"]} from {row["start"]} to {row["end"]} contains the following variants:")
            print("CHROM","POS","REF","ALT","QUAL")
            for vcf_rec in self.vcf.fetch(row["chr"],row["start"], row["end"]):
                print(vcf_rec.chrom,vcf_rec.pos,vcf_rec.ref,vcf_rec.alts[0])
        else:
            print(f"The segment at {chrom} from {start} to {end} contains the following variants:")
            print("CHROM","POS","REF","ALT")
            for vcf_rec in self.vcf.fetch(chrom,start,end):
                print(vcf_rec.chrom,vcf_rec.pos,vcf_rec.ref,vcf_rec.alts[0])        

    def generate_results(self):
        """
        Using binary search, the maximal batch size (the number of window_length long parts of each region that can be run through the
        Nucleotide Transformer at once without causing out of memory errors) is determined.
        """
        mem_test_split = np.full((128), ["A"*self.window_length])
        too_large = True
        mem_max = 128
        mem_min = 0
        while too_large:
            mem = int((mem_max+mem_min)/2)
            if mem == 0:
                raise torch.cuda.OutOfMemoryError
            try:
                test_embeddings = self.generate_embeddings(mem_test_split[:mem])
                if mem_max-mem == 1:
                    too_large = False
                    self.mem_max = mem
                    if self.mem_max > 2:
                        self.mem_max -= 2
                else:
                    mem_min = mem
            except torch.cuda.OutOfMemoryError:
                mem_max = mem
                gc.collect()
                torch.cuda.empty_cache() 

        print(f"GPUs: {torch.cuda.device_count()}, maximum batch size: {self.mem_max}")
        """
        In the interval, find the 8 closest variants to analyze all 2^10 combinations.
        """
        row = self.bed.iloc[self.index]
        vcf_pos = np.empty(0,dtype=np.int64)
        vcf_ref = np.empty(0)
        vcf_alt = np.empty(0)
        for vcf_rec in self.vcf.fetch(row["chr"],row["start"],row["end"]):
            if "*" in vcf_rec.ref or "*" in vcf_rec.alts[0]:
                continue  
            else:
                vcf_pos = np.append(vcf_pos, vcf_rec.pos)
                vcf_ref = np.append(vcf_ref, vcf_rec.ref)
                vcf_alt = np.append(vcf_alt, vcf_rec.alts[0])
        arg_closest_pos = np.sort(np.argsort([abs(vcf_pos[i]-self.roi_pos) for i in range(len(vcf_pos))])[:8])
        self.vcf_pos = vcf_pos[arg_closest_pos]
        self.vcf_ref = vcf_ref[arg_closest_pos]
        self.vcf_alt = vcf_alt[arg_closest_pos]

        full_results_df = []
        min_results_df = []
        for iter in tqdm(itertools.product([True,False],repeat=len(self.vcf_pos)),total=2**len(self.vcf_pos)):
            current_pos = self.vcf_pos[np.array(iter)]
            current_ref = self.vcf_ref[np.array(iter)]
            current_alt = self.vcf_alt[np.array(iter)]
            ref_seqs = []
            var_seqs = []
            var_seq = ""
            current = max(0,row["start"]-1)
            var_lag = 0
            for i in range(len(current_pos)):
                var_seq = var_seq + str(self.hg38[row["chr"]][current:current_pos[i]-1].seq).upper() + current_alt[i]
                current = current_pos[i]+len(current_ref[i])-1
                var_lag = var_lag+len(current_ref[i])-len(current_alt[i]) 
            ref_seq = str(self.hg38[row["chr"]][max(0,row["start"]-1):row["end"]-1].seq).upper()
            var_seq = var_seq + str(self.hg38[row["chr"]][current:row["end"]-1+var_lag].seq).upper()
            split_window = np.append(np.arange(0,len(ref_seq),self.window_length),len(ref_seq))
            ref_seq_split = np.array([ref_seq[split_window[i]:split_window[i+1]] for i in range(len(split_window)-1)])
            var_seq_split = np.array([var_seq[split_window[i]:split_window[i+1]] for i in range(len(split_window)-1)])
            if len(ref_seq_split)%self.mem_max == 1:
                ref_embeddings = torch.Tensor(self.generate_embeddings([ref_seq_split[0]]))
                var_embeddings = torch.Tensor(self.generate_embeddings([var_seq_split[0]]))
                k = 1
            else:
                ref_embeddings = torch.Tensor(self.generate_embeddings(ref_seq_split[0:self.mem_max]))
                var_embeddings = torch.Tensor(self.generate_embeddings(var_seq_split[0:self.mem_max]))
                k = self.mem_max        
            cos = self.generate_scores(ref_embeddings,var_embeddings)
            for i in range(k, len(ref_seq_split),self.mem_max):
                ref_embeddings = torch.Tensor(self.generate_embeddings(ref_seq_split[i:i+self.mem_max]))
                var_embeddings = torch.Tensor(self.generate_embeddings(var_seq_split[i:i+self.mem_max]))
                this_cos = self.generate_scores(ref_embeddings,var_embeddings)
                cos = torch.cat((cos, this_cos))
            """
            The dataframe containing information about the current region is created and returned.
            """
            pos_6mer = np.arange(row["start"],row["start"]+len(ref_seq),6,dtype=np.int64)
            cos = cos[:len(pos_6mer)]
            variants = np.full(fill_value="".join(np.array(iter).astype(int).astype(str)),shape=len(pos_6mer))
            this_df = pd.DataFrame({"Variant_Combination":variants,"Begin_6mer":pos_6mer,"Cosine_Similarity":cos})
            full_results_df.append(this_df)
            min_results_df.append(this_df.sort_values(by="Cosine_Similarity").head(1))
            
        self.full_results_df = pd.concat(full_results_df)
        self.min_results_df = pd.concat(min_results_df)
        self.min_results_df = self.min_results_df[self.min_results_df["Cosine_Similarity"] == self.min_results_df["Cosine_Similarity"].min()]
        print(self.min_results_df)
    def generate_embeddings(self, split):     
        """
        The embeddings of the current batch/split are calculated. Then, occupied memory is freed.
        """
        gc.collect()
        torch.cuda.empty_cache()
        
        tokens_ids = self.tokenizer.batch_encode_plus(split, return_tensors="pt",padding="longest")["input_ids"].to(device="cuda")
        attention_mask = tokens_ids != self.tokenizer.pad_token_id
        attention_mask.to("cuda")
        
        torch_outs = self.model(
            tokens_ids,
            attention_mask=attention_mask,
            encoder_attention_mask=attention_mask,
            output_hidden_states=True
        )
        
        embeddings = torch_outs['hidden_states'][-1].detach()
        attention_mask = torch.unsqueeze(attention_mask, dim=-1)
        embeddings = (attention_mask * embeddings)[:,1:,:]
        embeddings = embeddings.cpu()
        gc.collect()
        torch.cuda.empty_cache()
        return embeddings
    def generate_scores(self, ref_embeddings, var_embeddings):
        """
        The cosine similarity, dot product, manhattan distance and euclidian distance are calculated
        between the embeddings of the variant and reference of the same region.
        """
        cos_metric = nn.CosineSimilarity(dim=-1)
        
        ref_embeddings = torch.cat(tuple(ref_embeddings[i,:,:] for i in range(ref_embeddings.shape[0])),axis=0)
        var_embeddings = torch.cat(tuple(var_embeddings[i,:,:] for i in range(var_embeddings.shape[0])),axis=0)
        cos = cos_metric(ref_embeddings,var_embeddings)
        return cos
    def metric_match_line_plot(self,combination):
        row = self.bed.iloc[self.index]
        fig, ax = plt.subplots()
        plot_df = self.full_results_df[(self.full_results_df["Variant_Combination"]==combination)]
        scores = list(plot_df["Cosine_Similarity"])
        x = list(pd.concat([plot_df["Begin_6mer"],pd.Series([row["end"]])]))
        ax.stairs(edges=x,values=scores,color="black",label="Cosine_Similarity")
        pos_snp = []
        pos_ins = []
        pos_del = []
        iter = np.array([x for x in combination]).astype(int).astype(np.bool)
        current_pos = self.vcf_pos[np.array(iter)]
        current_ref = self.vcf_ref[np.array(iter)]
        current_alt = self.vcf_alt[np.array(iter)]
        for i in range(len(current_pos)):
            if len(current_ref[i])==len(current_alt[i]):
                pos_snp.append(current_pos[i])
            elif len(current_ref[i])>len(current_alt[i]):
                pos_del.append(current_pos[i])
            elif len(current_ref[i])<len(current_alt[i]):
                pos_ins.append(current_pos[i])
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
        plt.title(f"{combination}, Chromosome {row["chr"]}, Position {row["start"]}~{row["end"]}, Cosine_Similarity of {plot_df["Cosine_Similarity"].min()}")
        plt.xlabel("Position on the reference genome")
        plt.xticks(rotation=45, ha="right")
        ax.ticklabel_format(useOffset=False, style='plain')
        ax.set_ylim([-1.1,1.1])
        ax.set_xlim([row["start"],row["end"]])
        plt.legend()
        plt.savefig(f"ROI/{row["chr"]}_{self.roi_pos}/low_score_plots/{self.patient}_{combination}_line_plot.png",bbox_inches='tight')
        plt.close()

"""
This code is similar to wgs_nt_transformer, but is used to analyze a single region by examining all 2^n combinations of the n variants closest to the low score site. The n bit long number indicates which variants are turned on or off in a certain run (e.g. if the number if 101000, then (from left to right) only the 1st and 3rd of the 6 mutations in the region are used to generate the variant sequence).
"""

print("Loading Data...")
data_class = Data(sys.argv[1])
nt_class = AnalyzeOneRegion(data_class,index=sys.argv[3],roi_pos=sys.argv[4],window_length = sys.argv[2])
nt_class.get_variants()
nt_class.generate_results()
nt_class.metric_match_line_plot("11111111")
#nt_class.metric_match_line_plot("1111000")
nt_class.metric_match_line_plot("01000000")