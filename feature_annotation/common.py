import argparse
import os
from os.path import join, basename
import json


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