#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pymatgen
from pymatgen.electronic_structure.core import OrbitalType
from pymatgen.electronic_structure.plotter import DosPlotter
from pymatgen.io.vasp.outputs import Vasprun
from pymatgen.electronic_structure.cohp import CompleteCohp
from pymatgen.electronic_structure.dos import CompleteDos
from pymatgen.electronic_structure.cohp import IcohpValue
from pymatgen.electronic_structure.cohp import IcohpCollection
from pymatgen.electronic_structure.cohp import Cohp
from pymatgen.electronic_structure.plotter import CohpPlotter
from pymatgen.electronic_structure.plotter import DosPlotter
from pymatgen.io.lobster import Cohpcar
from pymatgen.io.lobster import Icohplist

import pandas as pd
import re

from pymatgen.io.lobster import Cohpcar
import matplotlib.pyplot as plt
import numpy as np
from molecule import int_to_roman

class Bond:
    '''
    Fields:
        atom1 (Str) -> must be part of the periodic table
        atom2 (Str) -> must be part of the periodic table
        colour (Str) -> must be a valid matplotlib colour
    '''

    def __init__(self, metal, halide, colour='blue', bond_label=None):
        '''
        Constructor: Create a Bond object by calling Bond(atom1, atom2, colour, bond_label)

        Effect: Mutates self 

        __init__: Bond Str Str Str -> None
        '''
        self.metal = metal
        self.halide = halide
        self.colour = colour
        self.bond_label = bond_label



def find_atom(atom, poscar):

    '''
    Converts from COHP format Atom IDs which are numbered according to the total number of atoms in the system
    to VESTA Atom ID format which are numbered according to the total number of atoms for the given element type
    '''

    poscar = open(poscar)
    L = poscar.readlines()

    # Determine order of the atoms
    ordered_atoms = " ".join(L[5:7]).split()
    N = len(ordered_atoms)//2
    ordered_atoms = np.array(ordered_atoms).reshape(2, N)

    
    element = re.search(r'[a-zA-Z]+', atom).group()
    number = int(re.search(r'\d+', atom).group())

    index = np.where(ordered_atoms[0] == element)[0][0]
    

    for i in range(index):
        number -= int(ordered_atoms[1][i])
    s = element + str(number)
    return s



def find_atom_IDs(atom_numbers, poscar):
    poscar = open(poscar)
    L = poscar.readlines()

    # Determine order of the atoms
    ordered_atoms = " ".join(L[5:7]).split()
    N = len(ordered_atoms)//2
    ordered_atoms = np.array(ordered_atoms).reshape(2, N)

    d_ids = {}

    for atom_no in atom_numbers:
        element = re.search(r'[a-zA-Z]+', atom_no).group()
        number = int(re.search(r'\d+', atom_no).group())

        index = np.where(ordered_atoms[0] == element)[0][0]
        
        count_all_atoms = 0
        for i in range(index):
            count_all_atoms += int(ordered_atoms[1][i])
        count_all_atoms += number
        d_ids[f'{element}{count_all_atoms}'] = atom_no

    return d_ids

                

def plot_specific_bonds_from_dataset(cp, data, cohp_path, custom_bonds, upgraded_bonds_list, cohp_atom_id_format=True):
    '''
    Plots the COHP for a specific set of bonds denoted by dictionary, bonds. The metals must be the keys and the halides (F) must be in the values. Note that AtomIDs in COHP format are numbered according
    to the total number of atoms in the system as opposed to the total number of atoms for the given element type. The default formatting
    of AtomIDs in the dictionary is the COHP format. 

    bonds is a (dictof (dictof Str Str) Str) where the key is the bond (key: metal, value: halide) and value is the matplotlib colour. 
    '''

    cohplist_path = cohp_path + "/ICOHPLIST.lobster"
    cohpcar_path = cohp_path + "/COHPCAR.lobster"
    poscar_path = cohp_path + "/POSCAR.lobster.vasp"

    completecohp = CompleteCohp.from_file(
    fmt="LOBSTER", filename=cohpcar_path, structure_file=poscar_path)

    # In this dictionary, the keys are the Atom ID#s and the values are the Atom Numbers. 

    if cohp_atom_id_format:
        d_bonds = {}
        for b in custom_bonds:
            d_bonds[b.metal] = b.halide

        metal_ID_list = list(d_bonds.keys())
        
    else:
        # convert from VESTA format (out of total N of each element type) to COHP format (out of total number of atoms in the system).
        # In dictionary returned, the keys are the COHP Atom ID#s and the values are the VESTA Atom Numbers. 
        d_ids = find_atom_IDs(list(d_bonds.keys()), poscar_path)
        metal_ID_list = list(d_ids.keys())
    

    cohplist = open(cohplist_path)
    lines = cohplist.readlines()


    for l in lines[2:len(lines)]:
        bond_data = l.split()
        cohp_no, atom1_id, atom2_id, bond_length, icohp_up, icohp_down = bond_data[0], bond_data[1], bond_data[2], bond_data[3], bond_data[7], bond_data[8]
    
        if atom2_id in metal_ID_list:
            
            if cohp_atom_id_format:
                bonded_atom = d_bonds[atom2_id]
            else:
                bonded_atom = list(find_atom_IDs(d_bonds[atom2_id], poscar_path).keys())[0]

            if atom1_id == bonded_atom:
                # Convert both metal atom and halide into the VESTA format (out of the total N for each element, not for the system)
                metal_atom_no = find_atom(atom2_id, poscar_path)
                bonded_atom_no = find_atom(atom1_id, poscar_path)


                
                plotlabel = (
                metal_atom_no
                + "-"
                + bonded_atom_no)

                    
                cp.add_cohp(plotlabel, completecohp.get_cohp_by_label(label=cohp_no))

                for b in custom_bonds:
                    if (b.metal == atom2_id) and (b.halide == atom1_id):
                        colour = b.colour
                        updated_bond = Bond(metal_atom_no, bonded_atom_no, colour=colour, bond_label=plotlabel)

                        if updated_bond not in upgraded_bonds_list:
                            upgraded_bonds_list.append(updated_bond)
                    
                print(
                    "This is a COHP between the following sites: "
                    + str(completecohp.bonds[cohp_no]["sites"][0])
                    + " and "
                    + str(completecohp.bonds[cohp_no]["sites"][1])
                )

                data['COHP#'].append(cohp_no)
                data['atom1'].append(bonded_atom_no)
                data['atom2'].append(metal_atom_no)
                data['bondlength'].append(f"{float(bond_length):.3f}")
                data['icohp_up'].append(f"{float(icohp_up):.3f}")
                data['icohp_down'].append(f"{float(icohp_down):.3f}")

    return cp, data, upgraded_bonds_list


def plot_specific_bonds(cohp_paths, alloy, custom_bonds, annotation='', plot_name='COHP_plot', cohp_atom_id_format=True):
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(6, 4), sharey=True)
    cp = CohpPlotter()
    data = {'COHP#': [], 'atom1': [], 'atom2': [], 'bondlength': [], 'icohp_up': [], 'icohp_down': []}


    for i in range(len(cohp_paths)):
        path = cohp_paths[i]
        if i == 0:
            upgraded_bonds_list = []
        cp, data, upgraded_bonds_list = plot_specific_bonds_from_dataset(cp, data, path, custom_bonds, upgraded_bonds_list, cohp_atom_id_format)
    
    if len(data['COHP#']) != 0:
        x = cp.get_plot(ylim = [-10, 6], integrated=False)
        lines = x.get_lines()
        
        i = 0 
        while i < len(lines):
            line = lines[i]
            label = line.get_label()
            print(f"Label: {line.get_label()} | Color: {line.get_color()} | ID: {id(line)}")
            
            if i < len(lines)-1:
                line2 = lines[i+1]
                if line.get_color() == line2.get_color():
                    print(True)

                    for b in upgraded_bonds_list:
                        if label == b.bond_label:
                            line.set_color(b.colour)
                            line2.set_color(b.colour)
                            i += 1 

            i += 1 
                
            
        x.legend(loc='upper right', fontsize=22)
        x.set_position([0.2, 0.2, 0.5, 0.5])  # Shrinks and centers the axes
        # If x is your Axes object
    
    
    # Save the COHP Plot 
    fig = x.figure  # get the figure from the Axes object
    fig.subplots_adjust(left=0.14, bottom=0.14, right=0.92, top=0.92)
    fig.text(0.82, 0.94, annotation, fontsize=35, color='black')
    fig.savefig(f"/Users/agneskatai/Desktop/Spring 2025/Figures/COHP/{alloy}/covalent_bonds/{plot_name}_COHP(e)", dpi=300, bbox_inches='tight')
    # plt.show()

    # Save the datasets as .csv file in the same folder 
    df = pd.DataFrame(data)
    df.to_csv(f'/Users/agneskatai/Desktop/Spring 2025/Figures/COHP/{alloy}/covalent_bonds/{plot_name}_COHP_data.csv')

    return upgraded_bonds_list




def get_all_atoms_below_threshold(data, cohp_path, metals, bonded_atom, plot_name='plot', threshold=3.01, save=False):
    '''
    Returns a dictionary that includes atom identifiers, bond length, and ICOHP values. Plots the COHP for all metals that are bonded to bonded_atom. 
    You may provide a threshold - it will only take bonds that have a bond length below a certain threshold. All required COHP output data is extracted from cohp_path.
    Provide the plot with a plot_name. 
    '''
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(12, 5), sharey=True)

    # Identify all the COHP output files required 
    cohplist_path = cohp_path + "/ICOHPLIST.lobster"
    cohpcar_path = cohp_path + "/COHPCAR.lobster"
    poscar_path = cohp_path + "/POSCAR.lobster.vasp"

    completecohp = CompleteCohp.from_file(
    fmt="LOBSTER", filename=cohpcar_path, structure_file=poscar_path)
    cp = CohpPlotter()
    
    cohplist = open(cohplist_path)
    lines = cohplist.readlines()


    for l in lines[2:len(lines)]:
        bond_data = l.split()
        cohp_no, atom1_id, atom2_id, bond_length, icohp_up, icohp_down = bond_data[0], bond_data[1], bond_data[2], bond_data[3], bond_data[7], bond_data[8]
        element1 = ''.join(re.findall(r'[A-Za-z]+', atom1_id))
        element2 = ''.join(re.findall(r'[A-Za-z]+', atom2_id))
    
        if (element1 in metals) or (element2 in metals):
            if (element1 == bonded_atom) or (element2 == bonded_atom):
            
                if float(bond_length) < threshold:

                    fluorine_atom_no = find_atom(atom1_id, poscar_path)
                    metal_atom_no = find_atom(atom2_id, poscar_path)
                
                
                    plotlabel = (
                    metal_atom_no
                    + "-"
                    + fluorine_atom_no)


                    cp.add_cohp(plotlabel, completecohp.get_cohp_by_label(label=cohp_no))
                    
                    data['COHP#'].append(cohp_no)
                    data['atom1'].append(fluorine_atom_no)
                    data['atom2'].append(metal_atom_no)
                    data['bondlength'].append(bond_length)
                    data['icohp_up'].append(icohp_up)
                    data['icohp_down'].append(icohp_down)

    if len(data['COHP#']) != 0:
        x = cp.get_plot(ylim = [-10, 6], integrated=False)

    if save:
        # Step 3: Save the figure
        fig = x.figure  # get the figure from the Axes object
        fig.savefig(plot_name, dpi=300, bbox_inches='tight') 
        cp.show()

    return data



def calc_average_bond(data_file, filename):
    # Read the CSV string (you can load from a file too)
    data = pd.read_csv(data_file)  # Replace with your actual filename

    # Extract element symbol from atom2 (e.g., 'Nb18' -> 'Nb')
    data['metal'] = data['atom2'].str.extract(r'([A-Za-z]+)')

    # Group by metal type and calculate average bond length
    avg_bond_lengths = data.groupby('metal')['bondlength'].mean().reset_index()

    # Round to 3 decimal places
    avg_bond_lengths['bondlength'] = avg_bond_lengths['bondlength'].round(3)

    # Save the results to a CSV file
    avg_bond_lengths.to_csv(filename, index=False)









