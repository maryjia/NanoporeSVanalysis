# NanoporeSVanalysis
Structural variant and methylation pipeline for the Nelson lab

Welcome to the Nelson lab repository for nanopore analysis code! We have created multiple pipelines for variant calling and methylation detection.

Before you run the pipelines, ensure that you have all required packages downloaded (credited below) to facilitate the analysis. 
Required dependencies:
```rb
conda create -n np_conda_env python=3.11
conda activate np_conda_env
conda install -c bioconda samtools minimap2 nanofilt minimap2 sniffles deepmod2
pip install biopython
pip install pandas 
```

# Running the structural variant pipeline

Download the alignment.py and variant_caller.py files above, which contains all of the python code necessary for analysis. 

Go to the terminal and change directories to enter the directory where you have saved these .py files.

The next step is to activate your conda environment and run the alignment.py file to concatonate adn align your fastq.gz files to a supplied fasta reference file.

Below is how the code runs using the provided example data. Make sure you add your own pathing.

```rb
conda activate np_conda_env

python alignment.py \
  --input_dir "/Your/input/directory" \
  --sample_name YOUR_SAMPLE \
  --output_root "/Volumes/NP_DATA2/Raw_data/10kb" \
  --reference_fasta "/Users/maryjia/Downloads/sequence.fasta" \
  --threads 16 \
  --output_bam "/Volumes/NP_DATA2/Raw_data/10kb/MT2_repeat/custom_alignment.bam"

```
This will result in a consolidated single fastq.gz and alignment files needed to call the variant calling script.

Below is an example of how you would use the output.bam file to call variants using cuteSV and sniffles in parallel.

Note that, here, /Your/path/to/bam/files will be the same as where you generated your output files, i.e. /Your/desired/output/path/here from above.

```rb
conda activate np_conda_env

python variant_caller.py sample_name /Your/path/to/bam/files /Your/path/to/YOUR_REFERENCE.fasta

```

# Running the methylation pipeline

Using the same conda environment as generated above, you can use bam files that have been aligned and basecalled using modified base calling software to detect for methylated sites.

Below is an example of how this code would be run.

```rb
conda activate np_conda_env

python methylation.py \
  --sample_name YOUR_SAMPLE \
  --reference_genome /Your/path/to/YOUR_REFERENCE.fasta \
  --bam_file /Your/path/to/bam/file \
  --region YOUR_REFERENCE
```
