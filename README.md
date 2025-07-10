# scRNA-seq-analysis

> Code for analyzing the mRNA coexpression of adrenergic receptors with 7 different types of IN markers.
> 
>Also generates polar plots in svg format which can be further modified by CorelDRAW

This scRNA-seq analysis uses the Yao et al. data set from Allen Institute.  
For more information: https://doi.org/10.1038/s41586-023-06812-z



###  Project Structure
```
scRNA-seq-analysis/
│  
├── analysis.py             # Script 1: Generates coexpression counts and coexpression percentages  
├── plots.py                # Script 2: Plots polar plots based on analysis output  
│  
├── data/                   # Folder containing all anndata files  
│ └── [downloaded data files]  
│
├── metadata/               # Folder containing metadata files  
│ └── [downloaded metadata files]  

```

- Required packages:
  - `pandas`
  - `numpy`
  - `scanpy`
  - `os`
  - `matplotlib`

## Setup Instructions
1. Create a new project folder and place both Python scripts (`analysis.py`, `plots.py`) inside it.
2.  Download the data:
  
    - Data files: This project uses the log normalized version of the expression matrices. The log2 anndata files of WMB-10Xv3, WMB-  10Xv2 and WMB-10XMulti which were used for the analysis can be downloaded from the `expression_matrices` folder in the given database: https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html

    - Metadata files: `cell_metadata.csv` can be found in `metadata/WMB-10X/`. For the analysis the version dated `20241115` was used. 

3. Create directories: In your project folder, create two new folders: `data` and `metadata`. Place all data files inside the `data/` folder and the inside the `metadata/` folder.

