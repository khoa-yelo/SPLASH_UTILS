import common   
import os
from os.path import join, basename
import json
import subprocess
import shutil
import sys

PFAM_HMM = os.getenv("PFAM_HMM")
def run_pfam(seq_file):
    cmd = f"seqkit translate -F --clean -f 6 {seq_file} > {seq_file}.prot"
    subprocess.run(cmd, shell=True, check=True)
    cmd = f"hmmsearch --notextw -o PFAM.stdout --tblout {seq_file}.prot.pfam --cpu 4 {PFAM_HMM} {seq_file}.prot" 
    subprocess.run(cmd, shell=True, check=True)

if __name__ == "__main__":
    args = common.parse_args()
    config, split_folder, lookup_folder, blast_folder, compactor_folder = common.preflight(args.config_path)
    if not os.path.exists(compactor_folder):
        print("Not running pfam as the compactor folder does not exist, Compactor = ", config["compactor_pfam"])
        sys.exit(0)
    run_pfam(config["compactor_args"]["output_file"] + ".fasta")
    # copy the pfam output to the compactor folder
    shutil.copy(config["compactor_args"]["output_file"]+ ".fasta.prot.pfam", compactor_folder)
    shutil.copy(config["compactor_args"]["output_file"]+ ".fasta.prot", compactor_folder)
    

