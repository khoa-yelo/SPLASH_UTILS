# SPLASH_UTILS

## Overview


## Feature Annotation

#### Setup Environment

```
singularity pull docker://scr.svc.stanford.edu/khoang99/containers/python-sequtils-blast 
```


config.json

```
{   
    "lookup": true,
    "blast": true,
    "compactor_pfam": false,
    "lookup_tables": ["/oak/stanford/groups/horence/khoa/scratch/data/lookup_table/microbe_lookup_with_microbe_trnx.slt", 
        "/oak/stanford/groups/horence/khoa/scratch/data/lookup_table/microbial_transcriptomes.slt"],
    "blast_window": 5000,
    "splash_bin": "/oak/stanford/groups/horence/khoa/scratch/build/splash2.6.1",
    "input_file": "/oak/stanford/groups/horence/khoa/scratch/play/selected_anchors_top10perc_dedup_list_with_id.fasta",
    "output_folder": "/oak/stanford/groups/horence/khoa/scratch/data/lookup_table/35kouts_3"
}
```


Run annotate.sh

