# scRNA-seq-analysis

> Code for analyzing the mRNA coexpression of adrenergic receptors with 7 different types of IN markers.
> 
>Also generates polar plots in svg format which can be further modified by CorelDRAW

This scRNA-seq analysis uses the Yao et al. data set from Allen Institute.  
For more information: https://doi.org/10.1038/s41586-023-06812-z

## How to run

your_project/
│
├── analysis_script.py # Script 1: Computes coexpression counts and percentages
├── plotting_script.py # Script 2: Plots graphs based on analysis output
│
├── data/ # Folder for input single-cell data
│ └── [downloaded data files]
│
├── metadata/ # Folder for metadata files
│ └── [downloaded metadata files]
│
├── output/ # (Optional) Folder where xlsx and plots can be saved
│
└── README.md
