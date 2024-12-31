#!/usr/bin/env python3.11
# conda activate np_conda_env
#
# Nelson lab nanopore analysis pipeline
# Analyzing methylation data
# Updated:     26.12.2024
# Author:      Mary Jia
# Maintainer:  Mary Jia
# Contact:     mary.jia@duke.edu
#
import os
import subprocess
import argparse

def main(args):
    # Define variables from command-line arguments
    sample_name = args.sample_name
    reference_genome = args.reference_genome
    bam_file = args.bam_file
    sample_dir = f"{sample_name}"
    output_dir = os.path.join(sample_dir, "methylation")

    # Create directories
    os.makedirs(output_dir, exist_ok=True)

    # Sort the BAM file
    sorted_bam = os.path.join(sample_dir, "sorted.bam")
    print("Sorting BAM file...")
    sort_command = f"samtools sort {bam_file} -o {sorted_bam}"
    subprocess.run(sort_command, shell=True, executable="/bin/zsh")

    # Check if sorted BAM file is indexed
    bam_index = f"{sorted_bam}.bai"
    if not os.path.exists(bam_index):
        print("Indexing sorted BAM file...")
        index_command = f"samtools index {sorted_bam}"
        subprocess.run(index_command, shell=True, executable="/bin/zsh")

    # Run modbam2bed for methylation analysis
    output_bed = os.path.join(output_dir, "output.cpg.bed")
    modbam2bed_command = (
        f"modbam2bed --aggregate -e -m 5mC --cpg -t 4 "
        f"-r {args.region} {reference_genome} {sorted_bam} > {output_bed}"
    )

    print("Running modbam2bed...")
    subprocess.run(modbam2bed_command, shell=True, executable="/bin/zsh")  # Ensure zsh compatibility

    print(f"Methylation analysis completed. Results are in {output_bed}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze methylation using modbam2bed without alignment.")

    # Define command-line arguments
    parser.add_argument("--sample_name", required=True, help="Sample name (e.g., MT2_ncats_AAV)")
    parser.add_argument("--reference_genome", required=True, help="Path to the reference genome file")
    parser.add_argument("--bam_file", required=True, help="Path to the unsorted BAM file")
    parser.add_argument("--region", required=True, help="Region name for modbam2bed (e.g., ncats_AAV_insert)")

    args = parser.parse_args()

    main(args)
