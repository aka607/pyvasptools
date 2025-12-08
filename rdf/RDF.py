from pymatgen.core.structure import Structure 

from vasppy.rdf import RadialDistributionFunction
import matplotlib.pyplot as plt

from modify_xyz import modify_xyz
from PyVaspTools.structure import *


def rdf(datasets, bonds, same_plot=True, fig_name='RDF'):
    '''
    Plots the RDF as a function of interatomic distance between the centre atom and the distribution atom. The centre atom is atom1, the 
    distribution atom is atom2 in the Bond. The bond colour needs to also be defined in the Bond. 
    '''

    plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica'],
    'font.size': 14,
    'xtick.labelsize': 18,
    'ytick.labelsize': 18,
    'axes.labelsize': 14,
    'legend.fontsize': 12,      # use 67 for FLiBe and 61 for FLiBe + H2O      
})
    if not same_plot:
        fig, axes = plt.subplots(
        nrows=len(datasets),
        ncols=1,
        figsize=(6, 8),
        sharex=True,
    )
    
        print(axes)
        print(len(axes))
        

    for i in range(len(datasets)):
        dataset = datasets[i]
        structure = Structure.from_file(f'{dataset.path}/POSCAR')

        for bond in bonds:
            if bond.bond_label == None:
                bond.bond_label = bond.atom1 + '-' + bond.atom2

            rdf_ij = RadialDistributionFunction.from_species_strings(structures=[structure], 
                                        species_i=bond.atom1,
                                        species_j=bond.atom2)
            
            if not same_plot:
                print(dataset.ls)
                axes[i].plot(rdf_ij.r, rdf_ij.smeared_rdf(), color = bond.colour, linestyle=dataset.ls, label=f'{bond.bond_label} {dataset.label}')
                axes[i].set_ylim(ymin=0, ymax=40)
                axes[i].legend()
                plt.show()
            else:
                plt.plot(rdf_ij.r, rdf_ij.smeared_rdf(), color = bond.colour, linestyle=dataset.ls, label=f'{bond.bond_label} {dataset.label}')


    if same_plot:
        plt.xlabel('r (Å)')
        plt.ylabel('RDF')
        plt.legend()
        plt.savefig(f'{fig_name}.pdf', bbox_inches='tight')
        plt.show()
    else:
        fig.supylabel('RDF')
        axes[-1].set_xlabel("r (Å)")
        fig.savefig(fname=f'{fig_name}.pdf', format='pdf', dpi=300, bbox_inches='tight')
