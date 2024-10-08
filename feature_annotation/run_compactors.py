import common
import os
from os.path import join, basename
import json
import subprocess
import sys

def run_compactors(fastq_files, anchor_list, output_file):
    # make parent directory of output_file if it does not exist
    parent_dir = os.path.dirname(output_file)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    # run compactors
    cmd = f"compactors --beta 0.5 --epsilon 0.001 --num_threads 20 --all_anchors {fastq_files} {anchor_list} {output_file}"
    print(cmd)
    subprocess.run(cmd, shell=True, check=True)


if __name__ == "__main__":
    args = common.parse_args()
    config, split_folder, lookup_folder, blast_folder, compactor_folder = common.preflight(args.config_path)
    if not os.path.exists(compactor_folder):
        print("Not running compactor as the compactor folder does not exist, Compactor = ", config["compactor_pfam"])
        sys.exit(0)
    run_compactors(config["compactor_args"]["fastq_files"], config["compactor_args"]["anchor_list"], config["compactor_args"]["output_file"])