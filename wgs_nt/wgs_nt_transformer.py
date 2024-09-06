print("Importing libraries...")
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

class Data:
    def __init__(self, patient):
        self.bed = pd.read_csv(f'{patient}/NT_inputs/{patient}_intervals.bed', sep="\t", header=None)
        self.bed.columns = ["chr","start","end"]
        self.hg38 = SeqIO.to_dict(SeqIO.parse('supporting_files/hg38/hg38.fa','fasta'))
        self.patient = patient
        self.vcf = VariantFile(f"{patient}/NT_inputs/{patient}_analysis-ready-variants-combined-sorted.vcf.gz")

class VariantAnalyzer:
    def __init__(self, Data, model_name="v2-500m-multi-species", window_length="1500"):
        self.window_length = 2*int(window_length)-2*int(window_length) % 6
        self.model_name = model_name
        self.model = AutoModelForMaskedLM.from_pretrained("InstaDeepAI/nucleotide-transformer-" + self.model_name, trust_remote_code=True).to(device="cuda")
        self.tokenizer = AutoTokenizer.from_pretrained("InstaDeepAI/nucleotide-transformer-" + self.model_name, trust_remote_code=True)
        
        self.patient = Data.patient
        self.hg38 = Data.hg38
        self.bed = Data.bed
        self.vcf = Data.vcf
    def generate_results(self): 
        chr_filelist = [str(path).split("/")[-1][:-4] for path in Path(f"{self.patient}/outputs/scores_per_chrom").glob("*")]
        all_chrs = self.bed["chr"].unique()
        chrs_to_use = [chrom for chrom in all_chrs if chrom not in chr_filelist]
        if len(chrs_to_use) == 0:
            print("No chromosomes to analyze.")
            return None
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
                    #if self.mem_max > 2:
                    #    self.mem_max -= 2
                else:
                    mem_min = mem
            except torch.cuda.OutOfMemoryError:
                mem_max = mem
                gc.collect()
                torch.cuda.empty_cache() 
        print(f"GPUs: {torch.cuda.device_count()}, maximum batch size: {self.mem_max}")
        
        for chrom in chrs_to_use:
            print(f"Currently at chromosome {chrom}...")
            temp_indices = list(self.bed[self.bed["chr"]==chrom].index)
            unused_indices = []
            used_indices = []
            ref_seqs = []
            var_seqs = []
            for index in tqdm(temp_indices):
                try:
                    row = self.bed.iloc[index]
                    var_seq = ""
                    current = max(0,row["start"]-1)
                    var_lag = 0
                    for vcf_rec in self.vcf.fetch(row["chr"],row["start"], row["end"]):
                        if "*" in vcf_rec.ref or "*" in vcf_rec.alts[0]:
                            continue
                        var_seq = var_seq + str(self.hg38[row["chr"]][current:vcf_rec.pos-1].seq).upper() + vcf_rec.alts[0]
                        current = vcf_rec.pos+len(vcf_rec.ref)-1
                        var_lag = var_lag+len(vcf_rec.ref)-len(vcf_rec.alts[0]) 
                    ref_seq = str(self.hg38[row["chr"]][max(0,row["start"]-1):min(row["end"]-1,len(self.hg38[row["chr"]])-1)].seq).upper()
                    var_seq = var_seq + str(self.hg38[row["chr"]][current:min(row["end"]-1+var_lag,len(self.hg38[row["chr"]])-1+var_lag)].seq).upper()
                    if len(ref_seq) != len(var_seq) or ref_seq == "" or var_seq == "" or ref_seq.count("N") > 0 or var_seq.count("N") > 0:
                        raise ValueError
                    else:
                        row = self.bed.iloc[index]
                        used_indices.append(index)
                        ref_seqs.append(ref_seq)
                        var_seqs.append(var_seq)
                except ValueError as e:
                    unused_indices.append(index) #The segment leads to strings of different sizes, which indicates overlapping variants and is therefore skipped
            print(f"In {chrom}, {len(used_indices)} are processed and {len(unused_indices)} regions are skipped due to overlapping indels or N nucleotides being included.")
            t_start = time.time()
            results_region = [self.generate_results_region(used_indices[i],ref_seqs[i],var_seqs[i]) for i in tqdm(range(len(used_indices)))]
            print("Time needed: {:.3f}s".format(time.time() - t_start))
            try: 
                results_df_this_chrom = pd.concat(results_region)
                results_df_this_chrom.to_csv(f"{self.patient}/outputs/scores_per_chrom/{chrom}.bed", header=None, index=None, sep='\t', mode='w+')
            except:
                print("No applicable regions.")
                open(f"{self.patient}/outputs/scores_per_chrom/{chrom}.bed","w+").close()
    def generate_results_region(self, index, ref_seq, var_seq):
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
        cos, dot, l1, mse = self.generate_scores(ref_embeddings,var_embeddings)
        for i in range(k, len(ref_seq_split),self.mem_max):
            ref_embeddings = torch.Tensor(self.generate_embeddings(ref_seq_split[i:i+self.mem_max]))
            var_embeddings = torch.Tensor(self.generate_embeddings(var_seq_split[i:i+self.mem_max]))
            this_cos, this_dot,this_l1, this_mse = self.generate_scores(ref_embeddings,var_embeddings)
            cos = torch.cat((cos, this_cos))
            l1 = torch.cat((l1, this_l1))
            mse = torch.cat((mse, this_mse))
            dot = torch.cat((dot,this_dot)) 
            
        pos_6mer = np.arange(self.bed.iloc[index]["start"],self.bed.iloc[index]["start"]+len(ref_seq),6,dtype=np.int64)
        index_of_6mer = np.full(fill_value=index,shape=len(pos_6mer))
        chr_6mer = np.full(fill_value=self.bed.iloc[index]["chr"],shape=len(pos_6mer))
        cos = cos[:len(pos_6mer)]
        l1 = l1[:len(pos_6mer)]
        mse = mse[:len(pos_6mer)] 
        dot = dot[:len(pos_6mer)]
        this_df =  pd.DataFrame({"Chromosome":chr_6mer,"Index_in_bed":index_of_6mer,"Begin_6mer":pos_6mer,"Cosine_Similarity":cos,"Dot_Product":dot,"1-L1_Loss":l1,"1-MSE_Loss":mse})
        return this_df
    def generate_embeddings(self, split):     
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
        cos_metric = nn.CosineSimilarity(dim=-1)
        l1_metric = nn.L1Loss()
        mse_metric = nn.MSELoss() 
        
        ref_embeddings = torch.cat(tuple(ref_embeddings[i,:,:] for i in range(ref_embeddings.shape[0])),axis=0)
        var_embeddings = torch.cat(tuple(var_embeddings[i,:,:] for i in range(var_embeddings.shape[0])),axis=0)
        
        cos = cos_metric(ref_embeddings,var_embeddings)
        l1 = torch.tensor([1-l1_metric(ref_embeddings[i,:],var_embeddings[i,:]).item() for i in range(ref_embeddings.shape[0])])
        mse = torch.tensor([1-mse_metric(ref_embeddings[i,:],var_embeddings[i,:]).item() for i in range(ref_embeddings.shape[0])])
        dot = torch.tensor([torch.dot(ref_embeddings[i,:],var_embeddings[i,:]).item() for i in range(ref_embeddings.shape[0])])
        return (cos,dot,l1,mse)

print("Loading Data...")
data_class = Data(sys.argv[1])
nt_class = VariantAnalyzer(data_class,window_length = sys.argv[2])
nt_class.generate_results()
