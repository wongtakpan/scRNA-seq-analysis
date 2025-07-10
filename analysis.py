# Import packages
import pandas as pd
import os
import scanpy as sc

# Associating the ensemble gene numbers with the gene symbols
d = {
    'genenum' : ['ENSMUSG00000005716', 'ENSMUSG00000004366', 'ENSMUSG00000032532', 'ENSMUSG00000019772', 'ENSMUSG00000028222',
                 'ENSMUSG00000003657', 'ENSMUSG00000029819', 'ENSMUSG00000035283', 'ENSMUSG00000045730', 'ENSMUSG00000031489',
                 'ENSMUSG00000045875', 'ENSMUSG00000050541', 'ENSMUSG00000027335', 'ENSMUSG00000033717', 'ENSMUSG00000058620', 'ENSMUSG00000045318'],
    'genesym' : ['Pvalb', 'Sst', 'Cck', 'Vip', 'Calb1', 'Calb2', 'NPY',
                 'Adrb1', 'Adrb2', 'Adrb3', 'Adra1a', 'Adra1b', 'Adra1d', 'Adra2a', 'Adra2b', 'Adra2c'],
}
genes = pd.DataFrame(data=d)

# Generate a file list containing the directory of all the anndata files
project_dir = os.getcwd()
data_dir = project_dir +  "\\data"

file_list = [
    os.path.join(data_dir, f)
    for f in os.listdir(data_dir)
    if f.endswith(".h5ad")
]

# Filter all anndata files for the genes of interest
lst = []
for f in file_list:
    adatas = sc.read_h5ad(f, backed='r')
    adfiletemp =sc.get.obs_df(adatas, keys=list(genes.genenum))
    lst.append(adfiletemp)

adfilegenes = pd.concat(lst)
adfilegenes = adfilegenes.reset_index()

# Import metadata
metadata_file = project_dir + "\\metadata\\cell_metadata_with_cluster_annotation.csv"
metadata = pd.read_csv(metadata_file, low_memory=False)
metadata= metadata[['cell_label', 'region_of_interest_acronym', 'neurotransmitter']]

# Add region_of_interest_acronym and neurotransmitter columns from metadata to adfilegenes
adfile_merged = adfilegenes.merge(metadata, on='cell_label', how='right')

# Filter for GABA cells
adfile_merged = adfile_merged[adfile_merged['neurotransmitter'] == 'GABA']

# Rename columns
col_names = ['cell_label'] + genes.genesym.tolist() + ['region_of_interest_acronym'] + ['neurotransmitter']
adfile_merged.columns = col_names

## Coexpression counts and coexpression percentages analysis. Checks for number of GABA cells coexpressing AR- and
## IN-specific gene (gene expression>0) by region
IN_acronym = genes.genesym[:7].to_list()
AR_acronym = genes.genesym[7:].to_list()
result_coexp_counts = {}
result_coexp = {}

for IN_cols in IN_acronym:
    coexp_counts = {}

    # Build coexpression lambda function
    for AR_cols in AR_acronym:
        coexp_counts[f'{IN_cols}&{AR_cols}_coexpression'] = (
        lambda x, ref=IN_cols, c = AR_cols :(
                (pd.to_numeric(x[ref], errors='coerce') > 0) &
                (pd.to_numeric(x[c], errors='coerce') > 0)
            ).sum()
            )

    # Apply region-wise
    results = []
    coexp_results = []
    for region, group in adfile_merged.groupby('region_of_interest_acronym'):
        region_result = {'region_of_interest_acronym': region}
        region_coexp_result = {'region_of_interest_acronym': region}
        region_result[f'{IN_cols}_count'] = (pd.to_numeric(group[f'{IN_cols}'], errors='coerce')>0).sum()
        for key, func in coexp_counts.items():
            region_result[key] = func(group)
            region_coexp_result[key] = region_result[key]/ region_result[f'{IN_cols}_count']
        results.append(region_result)
        coexp_results.append(region_coexp_result)
    result_coexp_counts[f'{IN_cols}'] = pd.DataFrame(results)
    result_coexp[f'{IN_cols}'] = pd.DataFrame(coexp_results)

# Export to Excel(.xlsx) file
with pd.ExcelWriter('coexpression_counts.xlsx', engine='xlsxwriter') as writer:
    for key, df in result_coexp_counts.items():
        df.to_excel(writer, sheet_name=key, index=False)

with pd.ExcelWriter('coexpression.xlsx', engine='xlsxwriter') as writer:
    for key, df in result_coexp.items():
        df.to_excel(writer, sheet_name=key, index=False)
