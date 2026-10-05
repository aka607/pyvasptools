#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pymatgen.electronic_structure.cohp import CompleteCohp
from pymatgen.electronic_structure.plotter import CohpPlotter
import pandas as pd 


from pyvasptools.dataset import Bond
from pyvasptools.convert_atom_ids import get_vesta_atom_id


def plot_custom_bonds_from_path(cp, data, cohp_path, custom_bonds, upgraded_bonds_list):
    '''
    Plots COHP(e) for a custom set of Bond (custom_bonds) onto cp, a CohpPlotter(),
    reading the LOBSTER output (ICOHPLIST/COHPCAR/POSCAR) found in cohp_path.

    Appends the matched bonds' tabulated COHP values (bond length and ICOHP) to data,
    and appends their upgraded Bonds — re-expressed in VESTA format instead of COHP
    format — to upgraded_bonds_list. Returns the updated (cp, data, upgraded_bonds_list).

    Note: COHP file format: atoms numbered out of the total number of atoms in the system,
          not the number of atoms of each type (i.e., Nb, Ta, Mo, etc.).
          VESTA file format: atoms numbered out of the total number of each atom type.

    plot_custom_bonds_from_path(CohpPlotter(), (dictof Str (listof Str)), Str, (listof Bond), (listof Bond))
        -> CohpPlotter(), (dictof Str (listof Str)), (listof Bond)
    Requires:
        - Bonds must contain the metal as atom1 and the halide or oxygen atom as atom2
    '''

    cohplist_path = cohp_path + "/ICOHPLIST.lobster"
    cohpcar_path = cohp_path + "/COHPCAR.lobster"
    poscar_path = cohp_path + "/POSCAR.lobster.vasp"

    completecohp = CompleteCohp.from_file(
    fmt="LOBSTER", filename=cohpcar_path, structure_file=poscar_path)

    # Set of (metal, halide) pairs. In Bond, atom1 is the metal and atom2 the halide.
    bond_pairs = {(b.atom1, b.atom2) for b in custom_bonds}
    
    with open(cohplist_path) as cohplist:
        lines = cohplist.readlines()


    for l in lines[2:len(lines)]:
        bond_data = l.split()
        if len(bond_data) < 9:   # skip blank/short lines (e.g. trailing newline)
            continue
        cohp_no, atom1_id, atom2_id, bond_length, icohp_up, icohp_down = bond_data[0], bond_data[1], bond_data[2], bond_data[3], bond_data[7], bond_data[8]
    
        # In the ICOHPLIST columns, atom2_id is the metal and atom1_id the halide.
        if (atom2_id, atom1_id) in bond_pairs:
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


def plot_custom_bonds(custom_bonds, *args, annotation='', fig_path='./'):
    '''
    Generates COHP(e) plots for a custom set of Bond (custom_bonds), reading the LOBSTER
    output found in each cohp_path given in *args, and saves the figure together with a
    .csv of the tabulated COHP values (bond length and ICOHP) under fig_path.

    By default the plots are not labelled with a timepoint (annotation=''). The atoms in
    custom_bonds are given in COHP file format. Returns upgraded_bonds_list, the matched
    bonds re-expressed in VESTA format for plotting.

    Note: COHP file format: atoms numbered out of the total number of atoms in the system,
          not the number of atoms of each type (i.e., Nb, Ta, Mo, etc.).
          VESTA file format: atoms numbered out of the total number of each atom type.
  
    plot_custom_bonds(listof Bond, Str, Str, Str) -> (dictof Bond)
    '''
    cp = CohpPlotter()
    data = {'COHP#': [], 'atom1': [], 'atom2': [], 'bondlength': [], 'icohp_up': [], 'icohp_down': []}


    upgraded_bonds_list = []
    for i in range(len(args)):
        path = args[i]
        
        cp, data, upgraded_bonds_list = plot_custom_bonds_from_path(cp, data, path, custom_bonds, upgraded_bonds_list)
    
    if len(data['COHP#']) == 0:
        print(f"No matching bonds found for {fig_path}; skipping plot.")
        return upgraded_bonds_list

    x = cp.get_plot(ylim = [-10, 6], integrated=False)
    if True:
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
    fig.savefig(f'{fig_path}_COHP(e)', dpi=300, bbox_inches='tight')

    # Save the datasets as .csv file in the same folder 
    df = pd.DataFrame(data)
    df.to_csv(f'{fig_path}_COHP_data.csv')

    return upgraded_bonds_list
