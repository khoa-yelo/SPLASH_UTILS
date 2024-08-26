"""
Module to run lookup table on input sequences 
and output the results in cleaned format
Khoa Hoang
08/23/24
"""

import pandas as pd
import subprocess
import re
from collections import Counter
import common
import os
from os.path import join, basename

    
def run_lookup(input_file, output_file, lookup_table, lookup_binary):
    command = f"{lookup_binary} query --truncate_paths --stats_fmt with_stats {input_file} {lookup_table} {output_file}"
    subprocess.run(command.split(), capture_output=False, check=True)
    return output_file

if __name__ == "__main__":
    args = common.parse_args()
    config, split_folder, lookup_folder, blast_folder, compactor_folder = common.preflight(args.config_path)
    lookup_binary = join(config["splash_bin"], "lookup_table")
    for table in config["lookup_tables"]:
        output_file = join(lookup_folder, basename(config["input_file"]).split(".")[0] \
                                + "_" + basename(table).split(".")[0] + ".lookout.tsv")
        cleaned_output_file = join(lookup_folder, basename(config["input_file"]).split(".")[0] \
                                + "_" + basename(table).split(".")[0] + ".cleaned.lookout.tsv")
        run_lookup(config["input_file"], output_file, table, lookup_binary)
        print(f"Lookup table {table} complete. Output file: {output_file}")
   