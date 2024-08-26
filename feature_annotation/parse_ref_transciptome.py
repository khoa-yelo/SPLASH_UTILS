"""
Parse the reference transcriptome to get gene, protein, and product names
compatile with lookup table transcriptomes input

Khoa Hoang
08/23/24
"""
import pandas as pd 
import numpy as np
import Bio
from Bio import SeqIO
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Parse the reference transcriptome')
    parser.add_argument('transcriptome', type=str, help='Path to the reference transcriptome')
    parser.add_argument('output', type=str, help='Path to the output file')
    return parser.parse_args()

def get_gene_name(header):
    gene_name = header.split("gene=")[1].split("]")[0]
    gene_name = f"([Gene]: {gene_name})"
    return gene_name

def get_protein_name(header):
    protein_name = header.split("protein=")[1].split("]")[0]
    protein_name = f"([Protein]: {protein_name})"
    return protein_name

def get_product_name(header):
    product_name = header.split("product=")[1].split("]")[0]
    product_name = f"([Product]: {product_name})"
    return product_name

def main():
    args = parse_args()
    transcriptome = args.transcriptome
    output = args.output

    # generate fasta with new headers
    fasta_sequences = SeqIO.parse(open(transcriptome),'fasta')
    new_fasta = []
    for fasta in fasta_sequences:
        header, sequence = fasta.description, str(fasta.seq)
        if "gene=" in header:
            gene_name = get_gene_name(header)
            new_fasta.append(">"+gene_name+"\n"+sequence)
        elif "protein=" in header:
            protein_name = get_protein_name(header)
            new_fasta.append(">"+protein_name+"\n"+sequence)
        elif "product=" in header:
            product_name = get_product_name(header)
            new_fasta.append(">"+product_name+"\n"+sequence)
        else:
            assert False, "No gene name found in header"

    # write new fasta

    with open(output, "w") as f:
        for line in new_fasta:
            f.write(line+"\n")
    print("Write to", output)
    
if __name__ == "__main__":
    print("Parsing reference transcriptome")
    main()


