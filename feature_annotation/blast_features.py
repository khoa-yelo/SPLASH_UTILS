from Bio import Entrez, SeqIO
import pandas as pd
import time
import common
import sys
import os
from os.path import join, basename

Entrez.email = "khoang99@stanford.edu"
MAX_RETRIES = 100
SLURM_ARRAY_TASK_COUNT = int(os.environ['SLURM_ARRAY_TASK_COUNT'])
SLURM_ARRAY_TASK_ID = int(os.environ['SLURM_ARRAY_TASK_ID'])

def fetch_sequence(seq_id):
    print(f"Fetching sequence {seq_id}")
    # retry until success, sleep for 5 seconds between each retry, max retries = MAX_RETRIES
    for i in range(MAX_RETRIES):
        try:
            handle = Entrez.efetch(db="nucleotide", id=seq_id, rettype="gb", retmode="text")
            record = SeqIO.read(handle, "genbank")
            handle.close()
            break
        except:
            time.sleep(5)
    return record

def find_overlapping_features(record, window_start, window_end):
    overlapping_features = []
    for feature in record.features:
        if feature.type == "source":
            continue
        feature_start = feature.location.start
        feature_end = feature.location.end

        # Check if the feature overlaps with the specified window
        overlap = (feature_start <= window_end) and (feature_end >= window_start)

        if overlap:
            overlapping_features.append({
                "type": feature.type,
                "start": str(feature_start),
                "end": str(feature_end),
                "gene": feature.qualifiers.get("gene"),
                "product": feature.qualifiers.get("product")
            })

    return overlapping_features

def featurize_blast_out(blast_out, window=10000):
    df = pd.read_csv(blast_out, sep="\t", header=None)
    df.columns = ["query", "subject", "identity", "alignment_length", "mismatches", "gap_opens",\
                     "q_start", "q_end", "s_start", "s_end", "evalue", "bit_score", "sgi", \
                        "sacc", "slen", "staxids", "stitle"]
    df["features"] = None
    df[f"features_{window}_window"] = None
    sacc_records = {}
    for sacc in df["sacc"].unique():
        sacc_records[sacc] = fetch_sequence(sacc)

    for index, row in df.iterrows():
        record = sacc_records[row["sacc"]]
        features = find_overlapping_features(record, row["s_start"], row["s_end"])
        df.at[index, "features"] = features
        # get the window
        window_start = max(row["s_start"] - window, 0)
        window_end = row["s_end"] + window
        features = find_overlapping_features(record, window_start, window_end)
        df.at[index, f"features_{window}_window"] = features
    
    return df[["query", "identity", "features", f"features_{window}_window"]]


if __name__ == "__main__":
    args = common.parse_args()
    config, split_folder, lookup_folder, blast_folder, compactor_folder = common.preflight(args.config_path)
    if not os.path.exists(blast_folder):
        print(f"Blast folder {blast_folder} does not exist. Exiting. Blast option = {config['blast']}")
        sys.exit(0)

    blast_outs = [join(blast_folder, f) for f in os.listdir(blast_folder) if f.endswith(".blastout.tsv")]
    blast_feat_outs = [join(blast_folder, basename(f).split(".")[0] + ".blastfeatout.tsv") for f in blast_outs]
    print(f"Total blast output files: {len(blast_outs)}")
    i = -1 
    for blast_out, blast_feat_out in zip(blast_outs, blast_feat_outs):
        i+=1
        if i % SLURM_ARRAY_TASK_COUNT != SLURM_ARRAY_TASK_ID:
            continue
        df_features = featurize_blast_out(blast_out, config["blast_window"])
        df_features.to_csv(blast_feat_out, index = None, sep = "\t")
        print(f"Featurize blast output complete for {blast_out}. Output file: {blast_feat_out}")
