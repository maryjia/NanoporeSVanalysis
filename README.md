# NanoporeSVanalysis
Structural variant and methylation pipeline for the Nelson lab

Welcome to the Nelson lab repository for nanopore analysis code! We have created multiple pipelines for variant calling and methylation detection.

Required dependencies:
```rb
conda create -n np_conda_env python=3.11
conda activate np_conda_env
conda install -c bioconda samtools minimap2 nanofilt minimap2 sniffles deepmod2
pip install biopython
pip install pandas 
```

# Running the structural variant pipeline

# Running the deepmod2 pipeline
