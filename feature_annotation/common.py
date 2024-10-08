import argparse
import os
from os.path import join, basename
import json

#Example json
# EXAMPLE_JSON = {   
#     "lookup": true,
#     "blast": true,
#     "compactor_pfam": false,
#     "lookup_tables": ["/oak/stanford/groups/horence/khoa/scratch/data/lookup_table/tables/082924/common_microbe_lookup.slt", 
#         "/oak/stanford/groups/horence/khoa/scratch/data/lookup_table/tables/082924/microbes_trnx.slt",
#         "/oak/stanford/groups/horence/khoa/scratch/data/lookup_table/tables/082924/artifacts.slt",
#         "/oak/stanford/groups/horence/khoa/scratch/data/lookup_table/tables/082924/common_microbe_w_trnx.slt"],
#     "blast_window": 5000,
#     "input_file": "/oak/stanford/groups/horence/khoa/scratch/data/splash_outs/candida/filtered_22_21.glmnet.hits.fasta",
#     "output_folder": "/oak/stanford/groups/horence/khoa/scratch/data/splash_outs/candida/filtered_22_21_glmnet_hits_annotation",
#     "compactor_args":{
#         "fastq_files": null,
#         "anchor_list": null,
#         "output_file": null
#     }
# }

def parse_args():
    parser = argparse.ArgumentParser(description="Run Feature Annotation")
    parser.add_argument("config_path", help="Path to config file")
    return parser.parse_args()

def preflight(config_path):
    #Load config file
    with open(config_path) as f:
        config = json.load(f)
    #Check for required fields
    if config["lookup"]:
        assert any(config["lookup_tables"]), "No lookup tables specified in config file"
    if config["blast"]:
        assert config["blast_window"], "No blast window specified in config file"
    if config["compactor_pfam"]:
        assert config["compactor_args"]["fastq_files"], "No fastq files specified in config file"
        assert config["compactor_args"]["anchor_list"], "No anchor list specified in config file"
        assert config["compactor_args"]["output_file"], "No output file specified in config file"
    assert config["input_file"], "No input files specified in config file"
    assert config["output_folder"], "No output files specified in config file"
    #Create output folders
    lookup_folder = join(config["output_folder"], "lookup_outs")
    blast_folder = join(config["output_folder"], "blast_outs")
    compactor_folder = join(config["output_folder"], "compactor_outs")
    split_folder = join(config["output_folder"], "splits")
    os.makedirs(config["output_folder"], exist_ok=True)
    os.makedirs(split_folder, exist_ok=True)
    if config["lookup"]:
        os.makedirs(lookup_folder, exist_ok=True)
    if config["blast"]:
        os.makedirs(blast_folder, exist_ok=True)
    if config["compactor_pfam"]:
        os.makedirs(compactor_folder, exist_ok=True)
        
    return config, split_folder, lookup_folder, blast_folder, compactor_folder