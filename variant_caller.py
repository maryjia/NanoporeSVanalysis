#!/usr/bin/env python3.11
# conda activate np_conda_env
#
# Nelson lab structural variant pipeline
# Calling variants from aligned bam files using cuteSV and sniffles
# Updated:     26.12.2024
# Author:      Mary Jia
# Maintainer:  Mary Jia
# Contact:     mary.jia@duke.edu
#

import subprocess
import os
import argparse

class VariantCallingProcessor:
    def __init__(self, sample_name, output_dir, genome_reference):
        self.sample_name = sample_name
        self.output_dir = output_dir
        self.genome_reference = genome_reference
        self.output_dir2_cutesv = os.path.join(output_dir, 'cuteSV_output')
        self.output_dir2_sniffles = os.path.join(output_dir, 'sniffles_output')

    def run_command(self, cmd):
        """Helper function to run commands."""
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            raise

    def run_cutesv(self):
        """Run cuteSV pipeline."""
        os.makedirs(self.output_dir2_cutesv, exist_ok=True)
        cmd = [
            "cuteSV", "--min_size", "30", "--max_size", "100000", "--diff_ratio_merging_DEL", "0.3", "--max_cluster_bias_DEL", "100", "--write_old_sigs",
            "--diff_ratio_merging_INS", "0.3","--max_cluster_bias_INS","100","-S", self.sample_name, "--retain_work_dir", "--report_readid", 
            "--genotype", f"{self.output_dir}/custom_alignment.bam",
            self.genome_reference, f"{self.output_dir2_cutesv}/cuteSV_output.vcf", self.output_dir2_cutesv
        ]
        self.run_command(cmd)

    def run_sniffles(self):
        """Run Sniffles pipeline."""
        os.makedirs(self.output_dir2_sniffles, exist_ok=True)
        cmd = [
            "sniffles", "-i", f"{self.output_dir}/custom_alignment.bam", "--reference", self.genome_reference,
            "-v", f"{self.output_dir2_sniffles}/output.vcf", "-t", "6", "--minsupport", "0", "--mosaic", "--allow-overwrite",
            "--mosaic-af-min", "0", "--qc-output-all", "--output-rnames"
        ]
        self.run_command(cmd)

    def process_variant_calling(self):
        """Run both cuteSV and Sniffles."""
        print("Running cuteSV pipeline...")
        self.run_cutesv()

        print("Running Sniffles pipeline...")
        self.run_sniffles()

def main():
    parser = argparse.ArgumentParser(description="Run cuteSV and Sniffles for variant calling.")
    parser.add_argument("sample_name", type=str, help="Sample name")
    parser.add_argument("output_dir", type=str, help="Output directory")
    parser.add_argument("genome_reference", type=str, help="Path to genome reference file")

    args = parser.parse_args()

    # Initialize processor and run pipelines
    processor = VariantCallingProcessor(args.sample_name, args.output_dir, args.genome_reference)
    processor.process_variant_calling()

if __name__ == "__main__":
    main()
