import pandas as pd
from ast import literal_eval
import ast
import subprocess
import os
import numpy as np
from os.path import join, basename, dirname
import common


def clean_blast_features(blast_feature):
    cleaned_outs = []
    blast_feature = ast.literal_eval(blast_feature)
    for feat in blast_feature:
        if feat["gene"]:
            cleaned_outs.append(feat["gene"])
        if feat["product"]:
            cleaned_outs.append(feat["product"])
    return cleaned_outs

def main(path):
    blast_path = join(path, os.listdir(path)[0])
    lookup_path = join(path, os.listdir(path)[1])
    for file in os.listdir(lookup_path):
        if "microbes_trnx.cleaned.lookout.tsv" in file:
            lookup_tsv = join(lookup_path, file)
        elif "common_microbe_w_trnx.cleaned.lookout.tsv" in file:
            lookup_full_tsv = join(lookup_path, file)
    df_lookup = pd.read_csv(lookup_tsv, sep="\t")
    df_lookup_full = pd.read_csv(lookup_full_tsv, sep="\t")
    df_lookup["cleaned_matches"] = df_lookup.matches.apply(lambda x: " ".join(x.split(",")[1].split()[:-1])\
                                                            if x!= "{}" else None)
    df_feats = []
    df_blast_outs = []
    for blast_file in sorted(os.listdir(blast_path), key = lambda x: int(x.split(".")[0].split("_")[1])):
        full_path = join(blast_path, blast_file)
        if "feat" in blast_file:
            df_feat = pd.read_csv(full_path, sep = "\t")
            df_feats.append(df_feat)
        else:
            if os.path.getsize(full_path) == 0:
                continue
            df_blast_out = pd.read_csv(full_path, sep = "\t", header = None)
            df_blast_outs.append(df_blast_out)

    df_feats_concat = pd.concat(df_feats)
    df_blast_out_concat = pd.concat(df_blast_outs)
    dict = df_blast_out_concat.set_index(0).to_dict()[16]
    df_feats_concat["hit"] = df_feats_concat["query"].map(dict)

    df_feats_concat["has_features"] = df_feats_concat["features"].apply(lambda x: 1 if x != "[]" else 0)
    df_feats_concat_dedup = df_feats_concat.sort_values(by=['query', 'has_features'], ascending=[True, False])\
                .drop_duplicates(subset='query', keep='first')
    blast_dict = df_feats_concat_dedup.set_index("query").to_dict()
    df_lookup.columns = ["anchor", "slt_trnx_stats", "slt_trnx_matches", "slt_trnx_cleaned_matches"]
    df_lookup_full.columns = ["anchor", "slt_full_stats", "slt_full_matches"]
    df_annot = pd.merge(df_lookup, df_lookup_full)
    df_annot["blast_features"] = df_annot["anchor"].map(blast_dict["features"]).fillna("[]")
    df_annot["blast_features_5k_window"] = df_annot["anchor"].map(blast_dict["features_5000_window"]).fillna("[]")
    df_annot["blast_hit"] = df_lookup["anchor"].map(blast_dict["hit"])
    df_annot["blast_features_cleaned"] = df_annot["blast_features"].apply(lambda x: clean_blast_features(x))
    df_annot["blast_features_5k_window_cleaned"] = df_annot["blast_features_5k_window"].apply(lambda x: clean_blast_features(x))
    df_annot.to_csv(join(path, "annotations.tsv"), sep="\t", index = False)

if __name__ == "__main__":
    args = common.parse_args()
    config, split_folder, lookup_folder, blast_folder, compactor_folder = common.preflight(args.config_path)    
    path = config["output_folder"]
    main(path)
