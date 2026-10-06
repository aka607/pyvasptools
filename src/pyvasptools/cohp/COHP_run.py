import os


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


from pyvasptools.cohp.COHP_plot import plot_custom_bonds
from pyvasptools.dataset import int_to_roman


def COHP_plots(main_path, times, custom_bonds, label=False, fig_path='./'):
    '''
    Generates COHP(e) plots for a specific set of Bond in custom_bonds that are listed at least once in any ICOHPLIST.lobster file as having a length of < 2 Angstroms. The main_path directory contains all data from electronic analyses 
    conducted at each time in times, i.e., f'{main_path}/{t}ps/COHP-1-2' and f'{main_path}/{t}ps/COHP-2-3'. By default, the plots are not sequentially labelled with the designated timepoints 
    and the current working directory contains the necessary output data.
    
    Returns upgraded_bonds_list in which the atoms are formatted in VESTA format - out of the total number of each element type. 

    COHP_plots(str, (listof Nat), (listof Bond), Bool, Str) -> (listof Bond)
    Requires:
        - For each t in times, main_path must contain a subfolder named '{t}ps' (e.g. '150ps').
    '''
    for i in range(len(times)):
        t = times[i]
        path_1_2 = f'{main_path}/{t}ps/COHP-1-2'            # Path to access 1-2 Angstroms COHP data  
        path_2_3 = f'{main_path}/{t}ps/COHP-2-3'            # Path to access 2-3 Angstroms COHP data 

        if label:
            annotation = f'{int_to_roman(i + 1)}) {times[i]}ps'
        else:
            annotation = ''
        
        upgraded_bonds_list = plot_custom_bonds(custom_bonds, path_1_2, path_2_3, annotation=annotation, fig_path=f'{fig_path}_{t}ps')

    return upgraded_bonds_list



def plot_bond_lengths(read_csv_path, times, bonds, spin_up=True, file_name=''):
    '''
    Plots the bond length and ICOHP evolution with times for the specific bonds provided. It is recommended to plot in VESTA format and be consistent with the AtomID formatting.

    plot_bond_lengths(Str, (listof Nat), (listof Bond), Bool, Str) -> None
    '''
    plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica'],
    'font.size': 18,
    'xtick.labelsize': 18,
    'ytick.labelsize': 18,
    'axes.labelsize': 18,
    'legend.fontsize': 14,      # use 67 for FLiBe and 61 for FLiBe + H2O      
})
    
    
    fig, axes = plt.subplots(
        nrows=1,
        ncols=2,
        figsize=(12.4, 6.8),
        sharey=False,
    )

    if spin_up:
        icohp_index = 5
    else:
        icohp_index = 6 

    d_bond_length = {}
    d_cohp = {}

    for t in times:

        dataset = pd.read_csv(f'{read_csv_path}_{t}ps_COHP_data.csv')
        halide_arr = dataset.iloc[:, 2].values   # atom1 column (halide/oxygen)
        metal_arr = dataset.iloc[:, 3].values    # atom2 column (metal)

        for bond in bonds:
            # Match on both atoms so a metal bonded to several halides maps to the right row.
            matches = np.nonzero((metal_arr == bond.atom1) & (halide_arr == bond.atom2))[0]

            if len(matches):
                ind = matches[0]
                bond_length = dataset.iloc[ind, 4]
                icohp = dataset.iloc[ind, icohp_index]
            else:
                bond_length = np.nan
                icohp = np.nan


            if bond in d_bond_length:
                d_bond_length[bond].append(bond_length)
                d_cohp[bond].append(icohp)
            else:
                d_bond_length[bond] = [bond_length]
                d_cohp[bond] = [icohp]


    print(d_bond_length)

    for bond in d_bond_length:
        X = times
        Y1 = d_bond_length[bond]
        axes[0].plot(X, Y1, marker='o', markersize=8, linewidth=2.5, label=f'{bond.atom1}-{bond.atom2}', color=bond.colour)
    
    fig.legend(loc='outside upper right')


    for bond in d_cohp:
        X = times
        Y2 = d_cohp[bond]
        axes[1].plot(X, Y2, marker='o', markersize=8, linewidth=2.5, label=f'{bond.atom1}-{bond.atom2}', color=bond.colour)  

    axes[0].set_ylim(ymin=1.50, ymax=2.50)
    axes[0].set_xlabel("Time (ps)")
    axes[0].set_ylabel('Bond Length (Å)')
    axes[1].set_ylim(ymin=-2.50, ymax=0.10)
    axes[1].set_xlabel("Time (ps)")
    axes[1].set_ylabel('ICOHP (eV)')

    fig.subplots_adjust(left=0.07, right=0.85, wspace=0.25)  # default left ~0.125

    fig.savefig(f'{file_name}_COHP_plot_all_times')
    plt.show()
