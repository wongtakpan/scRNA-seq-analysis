# Importing packages
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np


in_genesym = ['Pvalb', 'Sst', 'Cck', 'Vip', 'Calb1', 'Calb2', 'NPY']
in_types = ['PV', 'SST', 'CCK', 'VIP', 'CB', 'CR', 'NPY']
ar_subtypes = ['β1', 'β2', 'β3', '⍺1A', '⍺1B', '⍺1D', '⍺2A', '⍺2B', '⍺2C']

# Load outuput of analysis.py
sheets = pd.read_excel('coexpression.xlsx', sheet_name=None)

# Rename INs, ARs and use region as index
new_keys = dict(zip(in_genesym, in_types))
sheets = {new_keys.get(k,k): v for k,v in sheets.items()}
for in_type in sheets:
    df = sheets[in_type]
    df.columns = ['Region'] + ar_subtypes
    df.set_index('Region', inplace=True)
    sheets[in_type] = df

# Restructure dictionary for plotting
region_dict = {}

for in_type, df in sheets.items():
    for region in df.index:
        if region not in region_dict:
           region_dict[region] = pd.DataFrame(index=in_types, columns=ar_subtypes)
        region_dict[region].loc[in_type] = df.loc[region].values

# Combine some regions in the dictionary and add them
region_dict['ACA-PL-ILA-ORB'] = pd.concat([region_dict['ACA'], region_dict['PL-ILA-ORB']]).groupby(level=0).mean().reindex(in_types)
region_dict['MO-FRP-MOp'] = pd.concat([region_dict['MO-FRP'], region_dict['MOp']]).groupby(level=0).mean().reindex(in_types)
region_dict['sAMY-CTXsp'] = pd.concat([region_dict['sAMY'], region_dict['CTXsp']]).groupby(level=0).mean().reindex(in_types)

polarplots_regions = pd.read_excel('arcplots_region_names.xlsx')

polarplots_input = {key: region_dict[key] for key in polarplots_regions['acronym']}

# Generate a new dictionary with full region name
polarplots_fullname = dict(zip(polarplots_regions['acronym'], polarplots_regions['full_name']))
polarplots_input_full={}

for short_name, df in polarplots_input.items():
    full_name = polarplots_fullname.get(short_name, short_name)  # fallback to original if not found
    polarplots_input_full[full_name] = df

## Final Arcplots as SVG
receptors = ['⍺2B', '⍺2A', '⍺1D', '⍺1B', '⍺1A', 'β1', 'β2', 'β3', '⍺2C']
receptor_families = ['⍺2', '⍺2', '⍺1', '⍺1', '⍺1', 'β', 'β', 'β', '⍺2']

# Angles and arc width
num_receptors = len(receptors)
angle_per_receptor = 360 / num_receptors
angles = np.deg2rad(np.arange(0, 360, angle_per_receptor)) + np.deg2rad(10)
width = np.deg2rad(angle_per_receptor)

receptor_color_map = {
    '⍺1A': '#de2d26',
    '⍺1B': '#fc9272',
    '⍺1D': '#fee0d2',
    '⍺2A': '#31a354',
    '⍺2B': '#a1d99b',
    '⍺2C': '#e5f5e0',
    'β1': '#cc99ff',
    'β2': '#cc33ff',
    'β3': '#993d99',
}


folder = "svg"
os.makedirs(folder, exist_ok=True)

# Plotting
for region, df in polarplots_input_full.items():
    for in_type in df.index:
        coexpression_values = df.loc[in_type, receptors]
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})

        # Draw arcs
        for angle, radius, receptor in zip(angles, coexpression_values, receptors):
            color = receptor_color_map[receptor]
            ax.bar(angle, radius, width=width, bottom=0.0, align='edge',
                   edgecolor='black', color=color, linewidth=1.2)

        # Receptor labels
        label_radius = 0.97
        for angle, label in zip(angles, receptors):
            # color = receptor_color_map[label]
            ax.text(angle + width / 2, label_radius, label,
                    ha='center', va='center',
                    fontsize=11, fontweight='medium', color='black', alpha=1.0,
                    rotation=0)

        # Manually plot guide circles
        ring_levels = [0.25, 0.5, 0.75]
        ring_colors = ['#f2f2f2', '#e6e6e6', '#d9d9d9', '#cccccc']
        for i in range(len(ring_levels) - 1, 0, -1):
            inner = ring_levels[i - 1]
            outer = ring_levels[i]
            ax.bar(x=0, height=outer - inner, width=2 * np.pi, bottom=inner,
                   color=ring_colors[i], edgecolor=None, linewidth=0, alpha=0.3, zorder=0)

        # Radial boundary lines
        boundary_angles = np.deg2rad([90, 210, 330])
        for angle in angles:
            ax.plot([boundary_angles, boundary_angles], [0, 0.75], linestyle='solid', color='gray', linewidth=0.7,
                    zorder=0)

        # Percentage markers
        for r in [0.25, 0.5, 0.75]:
            ax.text(np.pi / 2, r, f'{int(r * 100)}%', ha='right', va='bottom',
                    fontsize=11, color='black', alpha=1)

        ax.set_yticklabels([])
        ax.set_xticks([])
        ax.set_ylim(0, 1.0)
        ax.grid(False)
        ax.set_frame_on(False)
        plt.subplots_adjust(top=0.8)
        fig.suptitle(f"ARs Coexpression with {in_type} IN in\nRegion : {region}",
                     fontsize=14, fontweight='bold', va='bottom', y=0.9)
        plt.tight_layout()

        # Save as SVG
        filename = f"{region}_{in_type}.svg".replace(" ", "_").replace("/", "_")
        full_path = os.path.join(folder, filename)
        plt.savefig(full_path, format="svg")
        plt.close(fig)
