# Feature Annotation

## Setup Environment

```
singularity pull docker://scr.svc.stanford.edu/khoang99/containers/python-sequtils-blast-splash-pfam
```

Modify the IMAGE and REPO env variable in `annotate.sh` file with path to the downloaded singularity container and the cloned git repo.

## Usage

Step 1: construct a `config.json` file

Example config.json

```
{   
    "lookup": false, # whether to run lookup table
    "blast": false,  # whether to run lookup table
    "compactor_pfam": true, # whether to run compactor and pfam annotation
    "lookup_tables": ["/oak/stanford/groups/horence/khoa/scratch/data/lookup_table/tables/082924/common_microbe_lookup.slt", 
        "/oak/stanford/groups/horence/khoa/scratch/data/lookup_table/tables/082924/microbes_trnx.slt",
        "/oak/stanford/groups/horence/khoa/scratch/data/lookup_table/tables/082924/artifacts.slt",
        "/oak/stanford/groups/horence/khoa/scratch/data/lookup_table/tables/082924/common_microbe_w_trnx.slt"], # a list of lookup tables to query from
    "blast_window": 5000, # window size to look for blast features
    "input_file": "/oak/stanford/groups/horence/khoa/scratch/data/splash_outs/candida/cluster_extenders.fasta", # input fasta to annotate
    "input_meta": null, # extra metadata of input sequences
    "output_folder": "/oak/stanford/groups/horence/khoa/scratch/data/splash_outs/candida/cluster_extenders_annotations", # output folder
    "compactor_args":{
        "fastq_files": "/oak/stanford/groups/horence/khoa/scratch/data/splash_outs/candida/fastqs.txt",
        "anchor_list": "/oak/stanford/groups/horence/khoa/scratch/data/splash_outs/candida/cluster_anchors.anchorlist",
        "output_file": "/oak/stanford/groups/horence/khoa/scratch/data/splash_outs/candida/cluster_anchors.compactors.out.fasta"
    } # arguments to compactors
}
```

Step 2: Run annotate.sh

```
./annotate.sh config.json
```

### Outputs

`annotations.tsv`: summarized annotation of each sequence in the fasta input
- anchor: sequence in input fasta
- slt_trnx_stats: lookup table result for transcriptome lookup table
- slt_trnx_matches: lookup table output 
- slt_trnx_cleaned_matches: look up table output - only show highest frequency match for each category
- slt_full_stats: lookup table result for all microbes sequence lookup table
- slt_full_matches: lookup table matches for all microbes sequence lookup tale
- blast_features: corresponding features that query sequence matched to, usually a gene/CDS/protein
- blast_features_5k_window: corresponding features within 5k windows query sequence matched to (window size can be changed in config file)
- blast_hit: subject sequence name
- blast_features_cleaned: cleaned version of blast features (e.g. only gene names are kept instead of locations, etc...)
- blast_features_5k_window_cleaned: cleaned version of blast features within 5k window

`blast_outs`: blast result for each sequence and corresponding features

`compactor_outs`: compactor and pfam for compactor

`lookup_outs`: lookup table outputs containing raw query output and cleaned versions

`splits`: input_file splitted in multiple fastas