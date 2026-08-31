from pyvasptools.dataset import *
from pyvasptools.dos.dos import *  
from pyvasptools.compound import * 

current_dir = Path(__file__).parent
root_dir = current_dir.parents[1]

# 1. Sample data set 1: Compare the density of states of two (100)-NbTaMoW and (100)-NbTaMoWV slabs 
NbTaMoW = Dataset(path=root_dir / 'sample_data/NbTaMoW/10ps/DOS', lc='black', label='NbTaMoW')
NbTaMoWV = Dataset(path=root_dir / 'sample_data/NbTaMoWV/10ps/DOS', lc='purple', label='NbTaMoWV')


# Save figure to directory of this test script 
# 1. Plot the density of states of a single (100)-NbTaMoW alloy 
NbTaMoW.plot_total_DOS(output_dir=current_dir, output_name='DOS_NbTaMoW')
# 2. Zoom in near the Fermi level.
NbTaMoW.plot_total_DOS(output_dir=current_dir, zoom_in=True, output_name='DOS_NbTaMoW_Fermi')


# 2. Compare the density of states of two (100)-NbTaMoW and (100)-NbTaMoWV slabs. zoom_in=True zooms in close to the Fermi level. 
plot_multi_overlaid_dos(NbTaMoW, NbTaMoWV, zoom_in=True, output_dir=current_dir, output_name='DOS_NbTaMoW_vs_NbTaMoWV')



# 3. Now compare the partial density of states of a NbTaMoW-H2O-FLiBe and NbTaMoWV-H2O-FLiBe interface. 
elements = ['Nb', 'Ta', 'Mo', 'W', 'F']

NbTaMoW = Dataset(path=root_dir / 'sample_data/NbTaMoW-FLiBe/10ps/DOS', lc="blue", ls="solid", label=f'')
NbTaMoWV = Dataset(path=root_dir / 'sample_data/NbTaMoWV-FLiBe/10ps/DOS', lc="purple", ls="solid", label=f'V')

plot_pdos_modified(elements, {'d': 'solid', 'p': 'dashed', 's': 'dotted'}, NbTaMoW, NbTaMoWV, x_lim=(-10, 10), y_lim=(((-5, 100),) + ((-1, 20),) * 4 + ((-5, 50),)), labels=("", "V"), path_to_fig=current_dir / 'pDOS_NbTaMoW_vs_NbTaMoWV')
        