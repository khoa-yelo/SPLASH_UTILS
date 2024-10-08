#!/bin/bash
CONFIG_FILE="$1"
NUM_ARRAY=50
export IMAGE="/oak/stanford/groups/horence/khoa/scratch/repos/SPLASH_UTILS/envs/python-sequtils-blast-splash-pfam_latest.sif"
export REPO="/oak/stanford/groups/horence/khoa/scratch/repos/SPLASH_UTILS"
export ENV="singularity run -B $REPO,$OAK $IMAGE"
export LOG_DIR="logs"
### Run lookup table
JOB_ID0=$(sbatch --parsable \
                 --partition=horence,owners \
                 --time=2:00:00 \
                 --mem=20GB \
                 --job-name=lookup \
                 --output=$LOG_DIR/lookup_%j.out \
                 --error=$LOG_DIR/lookup_%j.err \
                 --wrap="$ENV python run_lookup.py $CONFIG_FILE")
echo "Submitted lookup job with ID: $JOB_ID0"
### Clean lookup table
JOB_ID1=$(sbatch --parsable \
                 --dependency=afterok:$JOB_ID0 \
                 --partition=horence,owners \
                 --time=2:00:00 \
                 --mem=20GB \
                 --job-name=c_lookup \
                 --output=$LOG_DIR/c_lookup_%j.out \
                 --error=$LOG_DIR/c_lookup_%j.err \
                 --wrap="$ENV python clean_lookup.py $CONFIG_FILE")
echo "Submitted clean lookup job with ID: $JOB_ID1"
# Run blast
JOB_ID2=$(sbatch --parsable \
                 --partition=horence,owners \
                 --time=10:00:00 \
                 --mem=10GB \
                 --job-name=blast \
                 --output=$LOG_DIR/blast_%A_%a.out \
                 --error=$LOG_DIR/blast_%A_%a.err \
                 --array=0-$NUM_ARRAY \
                 --wrap="$ENV python run_blast.py $CONFIG_FILE")
echo "Submitted blast job with ID: $JOB_ID2"
### Run blast features
JOB_ID3=$(sbatch --parsable \
                 --partition=horence,owners \
                 --dependency=afterok:$JOB_ID2 \
                 --time=2:00:00 \
                 --mem=10GB \
                 --job-name=blast_feat \
                 --output=$LOG_DIR/blast_feat_%A_%a.out \
                 --error=$LOG_DIR/blast_feat_%A_%a.err \
                 --array=0-$NUM_ARRAY \
                 --wrap="$ENV python blast_features.py $CONFIG_FILE")
echo "Submitted blast feature job with ID: $JOB_ID3"
Run compactors
JOB_ID4=$(sbatch --parsable \
                 --partition=horence,owners \
                 --time=40:00:00 \
                 --mem=128GB \
                 --cpus-per-task=20 \
                 --job-name=compactors \
                 --output=$LOG_DIR/compactors_%A_%a.out \
                 --error=$LOG_DIR/compactors_%A_%a.err \
                 --wrap="$ENV python run_compactors.py $CONFIG_FILE")
echo "Submitted compactors job with ID: $JOB_ID4"
## Run pfam

JOB_ID5=$(sbatch --parsable \
                 --partition=horence,owners \
                 --dependency=afterok:$JOB_ID4 \
                 --time=10:00:00 \
                 --mem=32GB \
                 --cpus-per-task=4 \
                 --job-name=pfam \
                 --output=$LOG_DIR/pfam_%A_%a.out \
                 --error=$LOG_DIR/pfam_%A_%a.err \
                 --wrap="$ENV python run_pfam.py $CONFIG_FILE")
echo "Submitted pfam job with ID: $JOB_ID5"