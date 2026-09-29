from pyvasptools.cohp.COHP_plot import *
from pyvasptools.cohp.COHP_run import * 
from pyvasptools.dataset import *


current_dir = Path(__file__).parent
root_dir = current_dir.parents[1]

# NbTaMoW-FLiBe COHP analysis
main_path = root_dir / 'sample_data/NbTaMoW-FLiBe'
times = [10, 20]
bonds = [Bond('Ta158', 'F45', 'blue'), Bond('Ta146', 'F88', 'red'), Bond('Nb138', 'F56', 'purple'), Bond('W160', 'F48', 'green')]

updated_bonds_list = COHP_plots(main_path, times, bonds, label=True, fig_path=current_dir / "NbTaMoW-FLiBe")
plot_bond_lengths(current_dir / "NbTaMoW-FLiBe", times, updated_bonds_list, file_name=current_dir / 'NbTaMoW-FLiBe')



