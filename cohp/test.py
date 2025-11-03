from COHP_plot import * 
from COHP_run import *


# NbTaMoW-FLiBe COHP analysis
main_path = '/Users/agneskatai/cluster_data/Narval_test/NbTaMoW-FLiBe/dynamics/2_layer/salt'
times = [10, 20, 30, 40]
bonds = [Bond('Ta158', 'F45', 'blue'), Bond('Ta146', 'F88', 'red'), Bond('Nb138', 'F56', 'purple'), Bond('W160', 'F48', 'green')]

updated_bonds_list = COHP_plots(main_path, times, bonds, label=True, fig_name='NbTaMoW', fig_path='/Users/agneskatai/Desktop/Spring 2025/Figures/COHP/NbTaMoW/covalent_bonds')
plot_bond_lengths('/Users/agneskatai/Desktop/Spring 2025/Figures/COHP/NbTaMoW/covalent_bonds', times, updated_bonds_list, alloy_name='NbTaMoW')


# NbTaMoWV-FLiBe COHP analysis 
main_path = '/Users/agneskatai/cluster_data/Narval_test/NbTaMoWV-FLiBe/dynamics/2_layer/salt'
times = [10, 20, 30, 40]
bonds = [Bond('V117', 'F58', 'blue'), Bond('Ta166', 'F89', 'red'), Bond('V116', 'F45', 'purple'), Bond('Ta163', 'F66', 'green'), Bond('Mo149', 'F75', 'black'), Bond('Nb100', 'F84', 'magenta'), Bond('V129', 'F94', 'orange'), Bond('V119', 'F94', 'grey')]

updated_bonds_list = COHP_plots(main_path, times, bonds, label=True, fig_name='NbTaMoWV', fig_path='/Users/agneskatai/Desktop/Spring 2025/Figures/COHP/NbTaMoWV/covalent_bonds')
plot_bond_lengths('/Users/agneskatai/Desktop/Spring 2025/Figures/COHP/NbTaMoWV/covalent_bonds', times, updated_bonds_list, alloy_name='NbTaMoWV')



# # plot only specific covalent bonds < 2.0 Angstroms specified in bonds dictionary
# # H2O-NbTaMoW-FLiBe @ 40ps - 1 covalent bond forms 
main_path = '/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoW/100'
times = [10, 20, 30, 40]
bonds = [Bond('W165', 'O1', 'purple'), Bond('Ta149', 'F48', 'green')]

updated_bonds_list = COHP_plots(main_path, times, bonds, label=True, fig_name='NbTaMoW-H2O', fig_path='/Users/agneskatai/Desktop/Spring 2025/Figures/COHP/NbTaMoW-H2O/covalent_bonds')
plot_bond_lengths('/Users/agneskatai/Desktop/Spring 2025/Figures/COHP/NbTaMoW-H2O/covalent_bonds', times, updated_bonds_list, alloy_name='NbTaMoW-H2O')


# # plot only specific covalent bonds < 2.0 Angstroms specified in bonds dictionary
# # H2O-NbTaMoWV-FLiBe @ 30ps - 1 covalent bond forms 
main_path = '/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoWV/100'
times = [10, 20, 30, 40]
bonds = [Bond('V119', 'O1', 'purple'), Bond('V120', 'F92', 'green'), Bond('Nb103', 'O1', 'red'), Bond('V132', 'F48', 'black')]

updated_bonds_list = COHP_plots(main_path, times, bonds, label=True, fig_name='NbTaMoWV-H2O', fig_path='/Users/agneskatai/Desktop/Spring 2025/Figures/COHP/NbTaMoWV-H2O/covalent_bonds')
plot_bond_lengths('/Users/agneskatai/Desktop/Spring 2025/Figures/COHP/NbTaMoWV-H2O/covalent_bonds', times, updated_bonds_list, alloy_name='NbTaMoWV-H2O')


