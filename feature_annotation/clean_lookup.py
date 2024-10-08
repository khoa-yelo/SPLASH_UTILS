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
from SeqUtils.seq_utils import read_fasta

def remove_special_chars(string, accepted_chars=[",", ".", " ", "-", "_"]):
    """Remove special characters from string"""
    return "".join([c for c in string if c.isalnum() or c in accepted_chars])

def parse_to_dict(data_str):
    """Parse lookup table stats to dictionary"""
    data_dict = {k: int(v) for k, v in (item.split(': ') for item in data_str.split(', '))}
    return data_dict


def clean_lookup_out(raw_lookup_out, output_file):
    df_lookup_out = pd.read_csv(raw_lookup_out, sep="\t", header=None)
    df_lookup_out[0] = df_lookup_out[0].apply(count_lookup_string_occurences)
    df_lookup_out[1] = df_lookup_out[1].apply(lambda x: dict(sorted(parse_to_dict(x).items(), key=lambda item: item[1], reverse=True)))
    # remove any key with 0 value
    df_lookup_out[1] = df_lookup_out[1].apply(lambda x: {k: v for k, v in x.items() if v > 0})
    df_lookup_out[0] = df_lookup_out[0].apply(lambda x: {k: v for k, v in x.items() if any(v)})
    # name column matches, stats 
    df_lookup_out.columns = ["matches", "stats", "sample"]
    df_lookup_out = df_lookup_out[["sample", "stats", "matches"]]
    # add column 
    df_lookup_out.to_csv(output_file, sep="\t", index=False)
    return output_file


def count_lookup_string_occurences(lookup_out):
    """Clean lookup of kmers to count occurrences of each category"""

    # Step 1: Clean and split the strings
    splitted_strings = lookup_out.split(", ")
    filtered_strings = [s for s in splitted_strings if not re.match(r'[UNP]', s)]

    # Step 2: Combine strings that should be grouped together
    new_strings = []
    for i, s in enumerate(filtered_strings):
        if i == 0 or re.match(r'[1234]:', s):
            new_strings.append(s)
        else:
            new_strings[-1] += "," + s

    # Step 3: Group by categories
    cat_1, cat_2, cat_3, cat_4 = [], [], [], []

    for s in new_strings:
        if s.startswith('1:'):
            cat_1.append(remove_special_chars(s.strip('1:')))
        elif s.startswith('2:'):
            cat_2.append(remove_special_chars(s.strip('2:')))
        elif s.startswith('3:'):
            cat_3.append(remove_special_chars(s.strip('3:')))
        elif s.startswith('4:'):
            cat_4.append(remove_special_chars(s.strip('4:')))

    # Split and count occurrences
    cat_3_split = [item for sublist in cat_3 for item in sublist.split(", ")]
    # Count occurrences
    cat_1_count = Counter(cat_1).most_common(1)
    cat_2_count = Counter(cat_2).most_common(1)
    cat_3_count = Counter(cat_3_split).most_common(1)
    cat_4_count = Counter(cat_4).most_common(1)
    # Prepare the report dictionary
    report_dict = {1: cat_1_count, 2: cat_2_count, 3: cat_3_count, 4: cat_4_count}

    return report_dict


if __name__ == "__main__":
    args = common.parse_args()
    config, split_folder, lookup_folder, blast_folder, compactor_folder = common.preflight(args.config_path)
    input_file = config["input_file"]
    input_file_header_id = list(read_fasta(input_file).keys())
    for table in config["lookup_tables"]:
        output_file = join(lookup_folder, basename(config["input_file"]).split(".")[0] \
                                + "_" + basename(table).split(".")[0] + ".lookout.tsv")
        assert os.path.isfile(output_file), f"{output_file} does not exist"
        cleaned_output_file = join(lookup_folder, basename(config["input_file"]).split(".")[0] \
                                + "_" + basename(table).split(".")[0] + ".cleaned.lookout.tsv")
        # add a third column to the output file
        output_df = pd.read_csv(output_file, sep="\t", header=None)
        output_df[2] = input_file_header_id
        output_df.to_csv(output_file, sep="\t", index=False, header=False)
        # clean the lookup table
        cleaned_output_file = clean_lookup_out(output_file, cleaned_output_file)
        # bring sample id to the first column
        output_df.columns = ["matches", "sample", "stats"]
        output_df = output_df[["sample", "stats", "matches"]]
        output_df.to_csv(output_file, sep="\t", index=False)
        print(f"Lookup table {table} cleaned. Output file: {cleaned_output_file}")