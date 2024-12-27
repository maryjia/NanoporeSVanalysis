#!/usr/bin/env python3.11
# conda activate np_conda_env
#
# Nelson lab structural variant pipeline
# Filtering, sorting, and aligning fastq.gz nanopore files to a fasta reference
# Updated:     26.12.2024
# Author:      Mary Jia
# Maintainer:  Mary Jia
# Contact:     mary.jia@duke.edu
#
"""
Variant calling and alignment
"""
import subprocess
from pathlib import Path
import glob
import shutil
import argparse


class FastqProcessor:
    def __init__(self, input_dir, sample_name, output_root, additional_dir=None):
        self.input_dir = Path(input_dir)
        self.sample_name = sample_name
        self.output_dir = Path(output_root) / sample_name
        self.additional_dir = Path(additional_dir) if additional_dir else None
        self.all_fastq = self.output_dir / "all_guppy.fastq.gz"

    def create_directory(self, directory_path):
        Path(directory_path).mkdir(parents=True, exist_ok=True)

    def concatenate_files(self, input_pattern, output_file):
        with open(output_file, "wb") as outfile:
            for file_path in glob.glob(input_pattern):
                with open(file_path, "rb") as infile:
                    shutil.copyfileobj(infile, outfile)
        print(f"Files from {input_pattern} concatenated into {output_file}")

    def process_fastq(self):
        self.create_directory(self.output_dir)
        self.concatenate_files(str(self.input_dir / "*.fastq.gz"), self.all_fastq)

        if self.additional_dir:
            self.concatenate_files(str(self.additional_dir / "*.fastq.gz"), Path("all_guppy.fastq.gz"))

        return self.all_fastq


class AlignmentProcessor:
    def __init__(self, input_fastq, reference_fasta, output_bam, threads=24):
        self.input_fastq = Path(input_fastq)
        self.reference_fasta = Path(reference_fasta)
        self.output_bam = Path(output_bam)
        self.threads = threads

    def run_command(self, command):
        try:
            print(f"Running: {' '.join(command)}")
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: Command failed with error: {e}")
            raise

    def process_alignment(self):
        temp_bam = self.output_bam.with_suffix(".unsorted.bam")

        gunzip_cmd = ["gunzip", "-c", str(self.input_fastq)]
        nanofilt_cmd = ["NanoFilt", "-q", "10", "--headcrop", "50", "-l", "1000"]
        minimap2_cmd = ["minimap2", "--MD", "-ax", "map-ont", str(self.reference_fasta), "-"]
        samtools_sort_cmd = ["samtools", "sort", "-O", "BAM", f"-@{self.threads}", "-o", str(temp_bam), "-"]

        try:
            print("Starting alignment pipeline...")
            with subprocess.Popen(gunzip_cmd, stdout=subprocess.PIPE) as gunzip_proc, \
                 subprocess.Popen(nanofilt_cmd, stdin=gunzip_proc.stdout, stdout=subprocess.PIPE) as nanofilt_proc, \
                 subprocess.Popen(minimap2_cmd, stdin=nanofilt_proc.stdout, stdout=subprocess.PIPE) as minimap2_proc, \
                 subprocess.Popen(samtools_sort_cmd, stdin=minimap2_proc.stdout):
                gunzip_proc.stdout.close()
                nanofilt_proc.stdout.close()
                minimap2_proc.stdout.close()

            print(f"Alignment pipeline completed. Output saved to {temp_bam}.")
        except Exception as e:
            print(f"Error during alignment pipeline: {e}")
            raise

        temp_bam.rename(self.output_bam)
        print(f"Renamed sorted BAM to final output: {self.output_bam}")

        self.run_command(["samtools", "index", f"--threads={self.threads}", str(self.output_bam)])
        print(f"BAM file indexed: {self.output_bam}")

    def run(self):
        self.process_alignment()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process FASTQ files and align sequences.")
    parser.add_argument("--input_dir", required=True, help="Input directory containing FASTQ files.")
    parser.add_argument("--sample_name", required=True, help="Sample name for output organization.")
    parser.add_argument("--output_root", required=True, help="Root directory for output files.")
    parser.add_argument("--reference_fasta", required=True, help="Path to reference FASTA file.")
    parser.add_argument("--additional_dir", default=None, help="Optional additional directory for FASTQ files.")
    parser.add_argument("--threads", type=int, default=24, help="Number of threads to use for alignment.")
    parser.add_argument("--output_bam", default="alignment.bam", help="Path for the final BAM file.")

    args = parser.parse_args()

    # Process FASTQ files
    fastq_processor = FastqProcessor(
        input_dir=args.input_dir,
        sample_name=args.sample_name,
        output_root=args.output_root,
        additional_dir=args.additional_dir
    )
    concatenated_fastq = fastq_processor.process_fastq()

    # Align and process BAM file
    alignment_processor = AlignmentProcessor(
        input_fastq=concatenated_fastq,
        reference_fasta=args.reference_fasta,
        output_bam=args.output_bam,
        threads=args.threads
    )
    alignment_processor.run()
