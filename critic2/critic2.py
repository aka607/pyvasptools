import re
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import numpy as np

def plot_critic(criticout, *args, current_element = 'Li'):
    '''
    Returns a dictionary with rho values calculated via critic2 for all Atom IDs listed as *args at a given timestep. criticout_path is the directory that contains
    the critic2 output files at a given timestep. 
    
    plot_critic(Str, Str, Str) -> (dictof Str Float)
    Requires:
        - criticout is the path to the Critic2 output file for a given timestep. 
        - *args must contain valid Atom IDs in VESTA format (out of the total number of each element type)
        - current_element must be the first element listed in the critic2 output file 
    '''
    criticout = open(criticout)
    L = criticout.readlines()

    for i in range(len(L)):
        if "Pop" in L[i]:
            start = i + 1
    
    d = {}
    current_atom = current_element
    element_no = 0

    for ii in range(start, len(L)):
        l = L[ii].split()

        if len(l) == 10:
            id = l[0]
            atom = l[3]

            if atom == current_atom:
                element_no += 1 
            else:
                current_atom = atom 
                element_no = 1

            if atom + str(element_no) in args:
                rho = float(l[9])
                d[atom + str(element_no)] = rho
            ii += 1
        else:
            break
    
    criticout.close()
    return d
   


def plot_critic_over_timesteps(path, timesteps, *args, normalize=True, plot_name='critic2', current_element = 'Li'):
    '''
    Plots the valence electrons on a given atom listed in atom_numbers at each time in timesteps. The default is to normalize the valence electrons 
    at a given time to the intitial number of valence electrons at time 0 ps. 

    args is a list of Atom IDs expresed in the same format. 

    plot_critic_over_timesteps(Str, (listof Nat), Str, Bool, Str) -> None 
    Requires:
        - current_element is the first element type that appears in the critic2 output file 
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
        t_rho = plot_critic(criticout_path, *args)

        if t == 1:
            t = 0
        data[t] = t_rho

    times = list(data.keys())
    atom_numbers = list(data[times[0]].keys())
    marker_count = 0

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



