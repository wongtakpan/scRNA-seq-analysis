# scRNA-seq-analysis

> Code for analyzing the mRNA coexpression of adrenergic receptors with 7 different types of IN markers.
> 
>Also generates polar plots in svg format which can be further modified by CorelDRAW

This scRNA-seq analysis uses the Yao et al. data set from Allen Institute.  
For more information: https://doi.org/10.1038/s41586-023-06812-z



## Project Structure
scRNA-seq-analysis/
│  
├── analysis.py # Script 1: Generates coexpression counts and coexpression percentages  
├── plots.py # Script 2: Plots polar plots based on analysis output  
│  
├── data/ # Folder for input single-cell data  
│ └── [downloaded data files]  
│
├── metadata/ # Folder for metadata files  
│ └── [downloaded metadata files]  


- Required packages:
  - `pandas`
  - `numpy`
  - `matplotlib` / `seaborn` (for plotting)
