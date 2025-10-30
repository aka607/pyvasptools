import re
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import numpy as np

def plot_critic(criticout, atom_numbers):
    '''
    criticout is the path of the criticout file. atom_list is the list of atoms for which to calculate parameters 'pop' and 'rho'. If
    average = True, the average rho and pop for the surface atoms in taken, presuming the atoms are of the same type (Mo, Ta, Nb, etc.)
    '''
    criticout = open(criticout)
    L = criticout.readlines()

    for i in range(len(L)):
        if "Pop" in L[i]:
            start = i + 1
    
    d = {}
    current_atom = 'Li'
    element_no = 0

    for ii in range(start, len(L)):
        l = L[ii].split()

        if len(l) == 10:
            id = l[0]
            atom = l[3]

            if atom == current_atom:
                element_no += 1 
            else:
                print(atom)
                current_atom = atom 
                element_no = 1

            if atom + str(element_no) in atom_numbers:
                print(True)
                print(id)
                rho = float(l[9])
                print(rho)
                d[atom + str(element_no)] = rho
            ii += 1
        else:
            break

    return d
   


def plot_critic_over_timesteps(plot_name, path, timesteps, atom_numbers, normalize=True):
    '''
    args is a list of atom IDs of the same type that will be grouped in 1 list based on type

    '''
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Helvetica'],
        'font.size': 32,
        'axes.titlesize': 32,
        'axes.labelsize': 32,
        'xtick.labelsize': 32,
        'ytick.labelsize': 32,
        'legend.fontsize': 20,
    })
    
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(12, 10), sharey=False, layout='constrained')

    data = {}
    for t in timesteps:
        criticout_path = f'{path}/{t}ps/DOS/criticout'
        t_rho = plot_critic(criticout_path, atom_numbers)

        if t == 1:
            t = 0
        data[t] = t_rho

    times = list(data.keys())
    atom_numbers = list(data[times[0]].keys())
    marker_count = 0
    print(data)
    for a_n in atom_numbers:
        print(f' Current atom is {a_n}')
        atom_rho_values = {}
        rho_t1 = data[times[0]][a_n]

        for i in range(len(times)):
            t = times[i]
            rho_value = data[t][a_n]
            atom_rho_values[t] = rho_value - rho_t1
        
        time = list(atom_rho_values.keys())
        rho = list(atom_rho_values.values())

    
        if marker_count == 0:
            marker = "^"
        elif marker_count % 4 == 0:
            marker = "<"
        elif marker_count % 2 == 0:
            marker = "v"
        else:
            marker = "s"
        
        axes.plot(time, rho, marker=marker, markersize=8, linewidth=2.5, label=a_n)
        
        marker_count += 1
    
    axes.set_ylim(ymin=-1, ymax=1)
    axes.set_ylabel("Valence electrons wrt. initial state")
    axes.set_xlabel("Time (ps)")
    fig.legend(loc='outside right upper')  # Center of the plot
    axes.set_yticks(np.arange(-1, 1, 0.2))  # from 0 to 30 in steps of 5
    plt.show()
    fig.savefig(f'{plot_name}_critic.png')




# Nb = ['Nb17', 'F12', 'Nb20', 'F14', 'Nb18', 'F2', 'Nb1', 'F39']
# other_elements = ['Ta2', 'F19', 'Ta20', 'F15', 'Ta8', 'F36', 'Mo1', 'F54']
path = "/Users/agneskatai/cluster_data/Narval_test/NbTaMoW-FLiBe/dynamics/2_layer/salt"

atom_numbers = ['Ta20', 'F3', 'Ta8', 'F46', 'W2', 'F6', 'Nb20', 'F14']
plot_critic_over_timesteps("NbTaMoW", path, [1, 10, 20, 30, 40], atom_numbers, normalize=True)


path = "/Users/agneskatai/cluster_data/Narval_test/NbTaMoWV-FLiBe/dynamics/2_layer/salt"

atom_numbers = ['V3', 'F16', 'V2', 'F3', 'V15', 'F52']
plot_critic_over_timesteps("NbTaMoWV_V_atoms", path, [1, 10, 20, 30, 40], atom_numbers, normalize=True)

atom_numbers = ['Ta4', 'F47', 'Ta1', 'F24', 'Nb2', 'F42', 'Mo3', 'F33']
plot_critic_over_timesteps("NbTaMoWV", path, [1, 10, 20, 30, 40], atom_numbers, normalize=True)


path = "/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoW/100"
atom_numbers = ['W4', 'O1', 'Ta8', 'F3']
plot_critic_over_timesteps("NbTaMoW-H2O", path, [1, 10, 20, 30, 40], atom_numbers, normalize=True)

path = "/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoWV/100"
atom_numbers = ['V2', 'O1', 'V15', 'F3', 'V3', 'F47', 'Nb2']
plot_critic_over_timesteps("NbTaMoWV-H2O", path, [1, 10, 20, 30, 40], atom_numbers, normalize=True)

