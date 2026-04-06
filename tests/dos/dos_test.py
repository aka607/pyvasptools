from pyvasptools.dataset import *
from pyvasptools.dos.dos import *  
from pyvasptools.compound import * 

NbTaMoW = Dataset(path='/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoW/pure_metal/10ps/DOS', lc='black', label='NbTaMoW')
NbTaMoWV = Dataset(path='/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoWV/pure_metal/10ps/DOS', lc='purple', label='NbTaMoWV')

# Save figure to directory of this test script 
output_dir = Path(__file__).parent
NbTaMoW.plot_total_DOS(output_dir=output_dir, output_name=NbTaMoW)
plot_multi_overlaid_dos(NbTaMoW, NbTaMoWV, zoom_in=True, output_dir=output_dir, output_name='NbTaMoW_vs_NbTaMoWV')

# Test 1
elements = ['Nb', 'Ta', 'Mo', 'W', 'F', 'O']

NbTaMoW = Dataset(path="/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoW/100_v2/30ps/DOS", lc="blue", ls="solid", label=f'')
NbTaMoWV = Dataset(path="/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoWV/100_v2/30ps/DOS", lc="purple", ls="solid", label=f'V')

plot_pdos_modified(elements, {'d': 'solid', 'p': 'dashed', 's': 'dotted'}, NbTaMoW, NbTaMoWV, x_lim=(-10, 10), y_lim=(((-5, 100),) + ((-1, 20),) * 4 + ((-5, 50),) + ((-1, 3),)), labels=("", "V"), plot_name='NbTaMoW_vs_NbTaMoWV')
        

def calc_DOS_H2O(times, salt_path, pure_metal_path, elements, alloy):
    alloy_elements = Compound(alloy).elements
    for t in times:
        no_salt = Dataset(path=f'{pure_metal_path}/{t}ps/DOS', lc="blue", ls="solid", label=f'{alloy}')
        water = Dataset(path=f'{salt_path}/{t}ps/DOS', lc="black", ls="solid", label=f'{alloy}-H2O')
        plot_pdos_modified(elements, {'d': 'solid', 'p': 'dashed', 's': 'dotted'}, no_salt, water, x_lim=(-10, 10), y_lim=(((-5, 100),) + ((-1, 20),) * len(alloy_elements) + ((-5, 50),) + ((-0.1, 2),)), labels=("", "- FLiBe"), path_to_fig=f'/Users/agneskatai/Desktop/Spring 2025/Figures/DOS/H2O-{alloy}-v2', plot_name=f'H2O_{alloy}_{t}ps')


# Test 2 - BCC NbTaMoW + FLiBe + H2O 
# only elements that you wish to appear in the DOS 
elements = ['Nb', 'Ta', 'Mo', 'W', 'F', 'O']
times = [10, 30, 40] 
pure_metal_path = "/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoW/pure_metal"
salt_path = "/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoW/100_v2"

calc_DOS_H2O(times, salt_path, pure_metal_path, elements, "NbTaMoW")


# Test 2 - BCC NbTaMoWV + FLiBe + H2O 
# only elements that you wish to appear in the DOS 
elements = ['Nb', 'Ta', 'Mo', 'W', 'V', 'F', 'O']
times = [10, 30, 40] 
pure_metal_path = "/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoWV/pure_metal"
salt_path = "/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoWV/100_v2"

calc_DOS_H2O(times, salt_path, pure_metal_path, elements, "NbTaMoWV")
