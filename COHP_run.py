from COHP_plot import Bond, get_all_atoms_below_threshold, calc_average_bond, plot_specific_bonds, find_atom
import pandas as pd
from molecule import int_to_roman
import matplotlib.pyplot as plt
import numpy as np

def average_bond_lengths(alloy, times):
    metals = alloy.split()

    for t in times:
        plotname = f'{alloy}-{t}ps'
        data = {'COHP#': [], 'atom1': [], 'atom2': [], 'bondlength': [], 'icohp_up': [], 'icohp_down': []}
            

        # get the average bond length for all metal fluorides - NbF, MoF, WF, TaF, etc. First, extract all data from 1-2 Angstroms,
        # then extract data from 2-3 Angstroms 
        path = f'/Users/agneskatai/cluster_data/Narval_test/{alloy}-FLiBe/dynamics/2_layer/salt/{t}ps/COHP-1-2'
        data = get_all_atoms_below_threshold(data, path, metals, "F", plotname)

        path = f'/Users/agneskatai/cluster_data/Narval_test/{alloy}-FLiBe/dynamics/2_layer/salt/{t}ps/COHP-2-3'
        data = get_all_atoms_below_threshold(data, path, metals, "F", plotname)

        df = pd.DataFrame(data)
        csv_file_path = f'/Users/agneskatai/Desktop/Spring 2025/Figures/COHP/{alloy}/avg_bonds/{plotname}_COHP_below_threshold.csv'
        df.to_csv(csv_file_path)
        calc_average_bond(csv_file_path, filename=f"/Users/agneskatai/Desktop/Spring 2025/Figures/COHP/{alloy}/avg_bonds/{plotname}_average_bondlengths.csv")


def COHP_plots(main_path, alloy, times, custom_bonds, label=False):
    for i in range(len(times)):
        t = times[i]
        path_1_2 = f'{main_path}/{t}ps/COHP-1-2'            # Path to access 1-2 Angstroms COHP data  
        path_2_3 = f'{main_path}/{t}ps/COHP-2-3'            # Path to access 2-3 Angstroms COHP data 
        cohp_paths = [path_1_2, path_2_3]

        if label:
            annotation = f'{int_to_roman(i + 1)}) {times[i]}ps'
        else:
            annotation = ''

        upgraded_bonds_list = plot_specific_bonds(cohp_paths, alloy, custom_bonds, annotation=annotation, plot_name=f'{alloy}_{t}ps')

    return upgraded_bonds_list



def plot_bond_lengths(read_csv_path, times, alloy, bonds, cohp_atom_id_format=True, spin_up=True):
    '''
    path: path to bond lengths/tabulated COHP data 
    bond_lengths: dictof Bond (listof float)
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

        dataset = pd.read_csv(f'{read_csv_path}/{alloy}_{t}ps_COHP_data.csv')
        metal_arr = dataset.iloc[:, 3].values

        for bond in bonds:
            metal = bond.metal

            if metal in list(metal_arr):
                ind = list(metal_arr).index(metal)
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
        axes[0].plot(X, Y1, marker='o', markersize=8, linewidth=2.5, label=f'{bond.metal}-{bond.halide}', color=bond.colour)
    
    fig.legend(loc='outside upper right')


    for bond in d_cohp:
        X = times
        Y2 = d_cohp[bond]
        axes[1].plot(X, Y2, marker='o', markersize=8, linewidth=2.5, label=f'{bond.metal}-{bond.halide}', color=bond.colour)  

    axes[0].set_ylim(ymin=1.50, ymax=2.50)
    axes[0].set_xlabel("Time (ps)")
    axes[0].set_ylabel('Bond Length (Å)')
    axes[1].set_ylim(ymin=-2.50, ymax=0.10)
    axes[1].set_xlabel("Time (ps)")
    axes[1].set_ylabel('ICOHP (eV)')

    fig.savefig(f'{alloy}_COHP_plot_all_times')

    fig.subplots_adjust(left=0.07, right=0.85, wspace=0.25)  # default left ~0.125
    plt.show()


# NbTaMoW-FLiBe COHP analysis
# main_path = '/Users/agneskatai/cluster_data/Narval_test/NbTaMoW-FLiBe/dynamics/2_layer/salt'
# times = [10, 20, 30, 40]
# bonds = [Bond('Ta158', 'F45', 'blue'), Bond('Ta146', 'F88', 'red'), Bond('Nb138', 'F56', 'purple'), Bond('W160', 'F48', 'green')]

# COHP_plots(main_path, 'NbTaMoW', times, bonds)



# NbTaMoWV-FLiBe COHP analysis 
# main_path = '/Users/agneskatai/cluster_data/Narval_test/NbTaMoWV-FLiBe/dynamics/2_layer/salt'
# times = [10, 20, 30, 40]
# bonds = [Bond('V117', 'F58', 'blue'), Bond('Ta166', 'F89', 'red'), Bond('V116', 'F45', 'purple'), Bond('Ta163', 'F66', 'green'), Bond('Mo149', 'F75', 'black'), Bond('Nb100', 'F84', 'magenta'), Bond('V129', 'F94', 'orange'), Bond('V119', 'F94', 'grey')]

# COHP_plots(main_path, 'NbTaMoWV', times, bonds)


# times = [10, 20, 30, 40]
# path = '/Users/agneskatai/Desktop/Spring 2025/Figures/COHP/NbTaMoW/covalent_bonds'
# bonds = [Bond('Ta20', 'F3', 'blue'), Bond('Ta8', 'F46', 'red'), Bond('Nb20', 'F14', 'purple'), Bond('W2', 'F6', 'green')]

# plot_bond_lengths(path, times, 'NbTaMoW', bonds)


# times = [10, 20, 30, 40]
# path = '/Users/agneskatai/Desktop/Spring 2025/Figures/COHP/NbTaMoWV/covalent_bonds'
# bonds = [Bond('V2', 'F3', 'blue'), Bond('V3', 'F16', 'red'), Bond('V15', 'F52', 'purple'), Bond('Ta1', 'F24', 'green'), Bond('Mo3', 'F33', 'black'), Bond('Nb2', 'F42', 'magenta'), Bond('Ta4', 'F47', 'orange')]

# plot_bond_lengths(path, times, 'NbTaMoWV', bonds)


# # plot only specific covalent bonds < 2.0 Angstroms specified in bonds dictionary
# # H2O-NbTaMoW-FLiBe @ 40ps - 1 covalent bond forms 
main_path = '/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoW/100'
times = [10, 20, 30, 40]
bonds = [Bond('W165', 'O1', 'purple'), Bond('Ta149', 'F48', 'green')]

updated_bonds_list = COHP_plots(main_path, 'NbTaMoW-H2O', times, bonds, label=True)
plot_bond_lengths('/Users/agneskatai/Desktop/Spring 2025/Figures/COHP/NbTaMoW-H2O/covalent_bonds', times, 'NbTaMoW-H2O', updated_bonds_list)



# # plot only specific covalent bonds < 2.0 Angstroms specified in bonds dictionary
# # H2O-NbTaMoWV-FLiBe @ 30ps - 1 covalent bond forms 
main_path = '/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoWV/100'
times = [10, 20, 30, 40]
bonds = [Bond('V119', 'O1', 'purple'), Bond('V120', 'F92', 'green'), Bond('Nb103', 'O1', 'red'), Bond('V132', 'F48', 'black')]

updated_bonds_list = COHP_plots(main_path, 'NbTaMoWV-H2O', times, bonds, label=True)
plot_bond_lengths('/Users/agneskatai/Desktop/Spring 2025/Figures/COHP/NbTaMoWV-H2O/covalent_bonds', times, 'NbTaMoWV-H2O', updated_bonds_list)


