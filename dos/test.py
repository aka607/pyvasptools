from dataset import *

# Test 1
d = {'Nb': 1, 'Ta': 2, 'Mo': 3, 'W': 4, 'F': 5}
times = [10, 20, 30, 40]
path = "/Users/agneskatai/cluster_data/Narval_test/NbTaMoW-FLiBe/dynamics/2_layer"

def calc_DOS(times, path, d, alloy):
    '''
    Calculate the projected density of states for all times using the data in path. structures contains all
    the chemical components in your system. 
    '''
    elements = Compound(alloy).get_component_elements()
    N_alloy = len(elements)
    N_total = N_alloy + 1
    for t in times:
        no_salt = Dataset(path=f'{path}/no_salt/{t}ps', lc="blue", ls="solid", label=f'{alloy}')
        salt = Dataset(path=f'{path}/salt/{t}ps', lc="red", ls="solid", label=f'{alloy}-FLiBe')

        plot_pdos_modified(d, {'d': 'solid', 'p': 'dashed', 's': 'dotted'}, f'/Users/agneskatai/Desktop/Spring 2025/Figures/DOS/{alloy}', no_salt, salt, x_lim=(-10, 10), y_lim=(((-5, 100),) + ((-1, 20),) * N_alloy + ((-5, 50),)), labels=("", "- FLiBe"), plot_name=f'pure_{alloy}_{t}ps')
        
calc_DOS(times, path, d, "NbTaMoW")


# Test 2
d = {'Nb': 1, 'Ta': 2, 'Mo': 3, 'W': 4}
NbTaMoW = Dataset(path=f'{path}/no_salt/40ps', lc="blue", ls="solid", label=f'NbTaMoW')

plot_pdos_modified(d, {'d': 'solid', 'p': 'dashed', 's': 'dotted'}, f'/Users/agneskatai/Desktop/Spring 2025/Figures/DOS/test', NbTaMoW, x_lim=(-10, 10), y_lim=(((-5, 100),) + ((-1, 20),) * 4), labels=("",), plot_name='NbTaMoW_40ps')
