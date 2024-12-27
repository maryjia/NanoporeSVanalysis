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

Download the Nanopore_analysis_pipeline file above, which contains all of the python code necessary for analysis.

The next step is to activate your conda environment and run the alignment.py file to concatonate adn align your fastq.gz files to a supplied fasta reference file.

Below is how the code runs using the provided example data. Make sure you add your own pathing.

```rb
conda activate np_conda_env

python alignment.py \
  --input_dir "/Users/maryjia/fastq_pass/barcode02" \
  --sample_name MT2_repeat \
  --output_root "/Volumes/NP_DATA2/Raw_data/10kb" \
  --reference_fasta "/Users/maryjia/Downloads/sequence.fasta" \
  --threads 16 \
  --output_bam "/Volumes/NP_DATA2/Raw_data/10kb/MT2_repeat/custom_alignment.bam"

```

# Running the deepmod2 pipeline
