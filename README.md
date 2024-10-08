# SPLASH_UTILS

## Overview


## Feature Annotation

#### Setup Environment

```
singularity pull docker://scr.svc.stanford.edu/khoang99/containers/python-sequtils-blast 
```


Example config.json

```
{   
    "lookup": false,
    "blast": false,
    "compactor_pfam": true,
    "lookup_tables": ["/oak/stanford/groups/horence/khoa/scratch/data/lookup_table/tables/082924/common_microbe_lookup.slt", 
        "/oak/stanford/groups/horence/khoa/scratch/data/lookup_table/tables/082924/microbes_trnx.slt",
        "/oak/stanford/groups/horence/khoa/scratch/data/lookup_table/tables/082924/artifacts.slt",
        "/oak/stanford/groups/horence/khoa/scratch/data/lookup_table/tables/082924/common_microbe_w_trnx.slt"],
    "blast_window": 5000,
    "input_file": "/oak/stanford/groups/horence/khoa/scratch/data/splash_outs/candida/cluster_extenders.fasta",
    "input_meta": null,
    "output_folder": "/oak/stanford/groups/horence/khoa/scratch/data/splash_outs/candida/cluster_extenders_annotations",
    "compactor_args":{
        "fastq_files": "/oak/stanford/groups/horence/khoa/scratch/data/splash_outs/candida/fastqs.txt",
        "anchor_list": "/oak/stanford/groups/horence/khoa/scratch/data/splash_outs/candida/cluster_anchors.anchorlist",
        "output_file": "/oak/stanford/groups/horence/khoa/scratch/data/splash_outs/candida/cluster_anchors.compactors.out.fasta"
    }
}
```


Run annotate.sh

```
./annotate.sh confg.json
```

