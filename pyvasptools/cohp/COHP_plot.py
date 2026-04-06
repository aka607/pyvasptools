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

import re
import pandas as pd 

from pymatgen.io.lobster import Cohpcar
import matplotlib.pyplot as plt
import numpy as np
from pyvasptools.compound import *
from pyvasptools.dataset import *

from pyvasptools.convert_atom_ids import * 


                

def plot_specific_bonds_from_dataset(cp, data, cohp_path, custom_bonds, upgraded_bonds_list):
    '''
    Plots the COHP(e) for a specific set of bonds specified in custom_bonds using cp - CohpPlotter(). Note that AtomIDs expressed COHP format are numbered according
    to the total number of atoms in the system as opposed to the total number of atoms of a given element type. 
    Returns a CohpPlotter(), tabulated COHP values including the bond length and ICOHP, and a list of upgraded Bonds expressed in VESTA format instead of COHP format -
    that is out of the total number of atoms with a certain element type. 

    plot_specific_bonds_from_dataset(CohpPlotter(), (dictof Str (listof Str or Float)), (listof Bond), (listof Bond)) -> CohpPlotter(), (dictof Str (listof Float)), (listof Bond)
    Requires:
        - Bonds must contain the metal as atom1 and the halide or oxygen atom as atom2 
    '''

    cohplist_path = cohp_path + "/ICOHPLIST.lobster"
    cohpcar_path = cohp_path + "/COHPCAR.lobster"
    poscar_path = cohp_path + "/POSCAR.lobster.vasp"

    completecohp = CompleteCohp.from_file(
    fmt="LOBSTER", filename=cohpcar_path, structure_file=poscar_path)

    # In this dictionary, the keys are the metal and the values are the halide. 
    d_bonds = {}
    for b in custom_bonds:
        d_bonds[b.atom1] = b.atom2
    
    cohplist = open(cohplist_path)
    lines = cohplist.readlines()


    for l in lines[2:len(lines)]:
        bond_data = l.split()
        cohp_no, atom1_id, atom2_id, bond_length, icohp_up, icohp_down = bond_data[0], bond_data[1], bond_data[2], bond_data[3], bond_data[7], bond_data[8]
    
        if atom2_id in list(d_bonds.keys()):
            
            
            bonded_atom = d_bonds[atom2_id]

            if atom1_id == bonded_atom:
                # Convert both metal atom and halide into the VESTA format (out of the total N for each element, not for the system)
                metal_atom_no = get_vesta_atom_id(atom2_id, poscar_path)
                bonded_atom_no = get_vesta_atom_id(atom1_id, poscar_path)


                
                plotlabel = (
                metal_atom_no
                + "-"
                + bonded_atom_no)

                cp.add_cohp(plotlabel, completecohp.get_cohp_by_label(label=cohp_no))

                for b in custom_bonds:
                    if (b.atom1 == atom2_id) and (b.atom2 == atom1_id):
                        updated_bond = Bond(metal_atom_no, bonded_atom_no, colour=b.colour, bond_label=plotlabel)

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


def plot_specific_bonds(custom_bonds, *args, annotation='', plot_name='COHP_plot'):
    '''
    Generates COHP(e) plots for a specific set of bonds in custom_bonds that are listed in the ICOHPLIST.lobster file contained in the paths provided in *args. 
    By default, the plots are not sequentially labelled with the designated timepoints and the plot name is COHP_plot. By default, the atoms in Bond 
    are formatted in the COHP file format, that is out of the total number of atoms in the system. 
    
    Returns upgraded_bonds_list in which the atoms are formatted in VESTA format - out of the total number of each element type. 
    
    plot_specific_bonds(dictof Bond, Str, Str, Str, Str) -> (dictof Bond)
    '''
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(6, 4), sharey=True)
    cp = CohpPlotter()
    data = {'COHP#': [], 'atom1': [], 'atom2': [], 'bondlength': [], 'icohp_up': [], 'icohp_down': []}


    upgraded_bonds_list = []
    for i in range(len(args)):
        path = args[i]
        
        cp, data, upgraded_bonds_list = plot_specific_bonds_from_dataset(cp, data, path, custom_bonds, upgraded_bonds_list)
    
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
    fig.savefig(f'{plot_name}_COHP(e)', dpi=300, bbox_inches='tight')

    # Save the datasets as .csv file in the same folder 
    df = pd.DataFrame(data)
    df.to_csv(f'{plot_name}_COHP_data.csv')

    return upgraded_bonds_list
