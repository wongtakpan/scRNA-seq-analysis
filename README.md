# scRNA-seq-analysis

> Code for analyzing the mRNA coexpression of adrenergic receptors with 7 different types of IN markers.
> 
>Also generates polar plots in svg format which can be further modified by ***CorelDRAW***

This scRNA-seq analysis uses the Yao et al. data set from Allen Institute.  
For more information: https://doi.org/10.1038/s41586-023-06812-z



###  Project Structure
```
scRNA-seq-analysis/
│  
├── analysis.py                       # Generates coexpression counts and coexpression percentages  
├── plots.py                          # Plots polar plots based on analysis output
├── polarplots_region_names.xlsx      # Acronyms and full names for region used for plotting.
│  
├── data/                             # Folder containing downloaded anndata files   
│
├── metadata/                         # Folder containing downloaded metadata file  
│

```

- Dependencies:
  - `pandas`
  - `numpy`
  - `scanpy`
  - `os`
  - `matplotlib`

## How to Run
1. Create a new project folder and place both Python scripts (`analysis.py`, `plots.py`) and `polarplots_region_names.xlsx` file inside it.
2.  Download the data:
    - Latest files can be downloaded from: https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html
    - Data files: This project uses the log normalized version of the expression matrices. The log2 anndata files of WMB-10Xv3, WMB-  10Xv2 and WMB-10XMulti which were used for the analysis can be downloaded from the `expression_matrices` folder in the database.
    - Metadata files: `cell_metadata_with_cluster_annotation.csv` can be found in `metadata/WMB-10X/20241115/views` in the database.

4. Create directories: In your project folder, create two new folders: `data` and `metadata`. Place all data files inside the `data/` folder and the inside the `metadata/` folder.
5. Run `analysis.py`. The script produces two Excel (.xlsx) files:
    - `coexpression_counts.xlsx`: Number of coexpressing cells.
    - `coexpression.xlsx`: Percentages of coexpression
6. Run `plots.py`: Generates polar plots in `.svg` format and saves them in the `svg/` folder.

## Region Filtering Note
**Note:** Some similar brain regions were combined due to anatomical similarity and their coexpression values were averaged. They were then renamed in the final figure. These include:

- *Anterior cingulate area* and *Prelimbic/infralimbic/orbital areas* used as *Prefrontal Cortex*
- *Striatum-like amygdalar nuclei* and *Cortical subplate* used as *Amygdala*

This repository includes a file named `regions_to_plot.xlsx`, which specifies the brain regions used for generating plots. This file includes the combined region names. The original file containing all the region acronyms and full names can be found in the online database as `metadata/WMB-10X/20241115/region_of_interest_metadata.csv` 

##  Output
`plots.py` stores polar plots in `.svg` vector graphics format. These files were then edited and finalized in ***CorelDRAW*** for the final figure used in the paper.
