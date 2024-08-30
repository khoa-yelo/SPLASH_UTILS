import common
import os
from os.path import join, basename
import subprocess
from blast_features import featurize_blast_out
from SeqUtils.seq_utils import read_fasta, split_fasta
import shutil

SLURM_ARRAY_TASK_COUNT = int(os.environ['SLURM_ARRAY_TASK_COUNT'])
SLURM_ARRAY_TASK_ID = int(os.environ['SLURM_ARRAY_TASK_ID'])
SPLIT_THRESH = 100
SPLIT_EACH = 50 

def run_blast(splitted_fasta, blast_folder, config):

    fmt="6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore sseqid sgi sacc slen staxids stitle"

    for i, f in enumerate(splitted_fasta):
        if i % SLURM_ARRAY_TASK_COUNT != SLURM_ARRAY_TASK_ID:
            continue
        blast_out = join(blast_folder, basename(f).split(".")[0] + ".blastout.tsv")
        cmd = f"blastn -outfmt '{fmt}' -query {f} -remote -db nt -out {blast_out} -evalue 0.1 -task blastn -dust no -word_size 24 -reward 1 -penalty -3 -max_target_seqs 4"
        subprocess.run(cmd, shell = True, check=True)
        print(f"Blast complete for {f}")

if __name__ == "__main__":
    args = common.parse_args()
    config, split_folder, lookup_folder, blast_folder, compactor_folder = common.preflight(args.config_path)

    if len(read_fasta(config["input_file"])) > SPLIT_THRESH:
        split_fasta(config["input_file"], split_folder, SPLIT_EACH)
    else:
        shutil.copy(config["input_file"], split_folder)
    splitted_fasta = [join(split_folder, f) for f in os.listdir(split_folder) if f.endswith(".fasta")]
    run_blast(splitted_fasta, blast_folder, config)