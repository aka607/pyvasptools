from pymatgen.core.structure import Structure 

from vasppy.rdf import RadialDistributionFunction
import matplotlib.pyplot as plt

from modify_xyz import modify_xyz
from PyVaspTools.structure import *


def rdf(datasets, linestyles, *args, fig_name='RDF'):
    '''
    Plots the RDF as a function of interatomic distance between the centre atom and the distribution atom. The centre atom is atom1, the 
    distribution atom is atom2 in the Bond. The bond colour needs to also be defined in the Bond. 
    '''

    plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica'],
    'font.size': 14,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'axes.labelsize': 14,
    'legend.fontsize': 12,      # use 67 for FLiBe and 61 for FLiBe + H2O      
})
    
    for i in range(len(datasets.keys())):
        dataset = list(datasets.keys())[i]
        path = datasets[dataset]
        structure = Structure.from_file(f'{path}/POSCAR')

        for bond in args:
            if bond.bond_label == None:
                bond.bond_label = bond.atom1 + '-' + bond.atom2

            rdf_ij = RadialDistributionFunction.from_species_strings(structures=[structure], 
                                        species_i=bond.atom1,
                                        species_j=bond.atom2)
            plt.plot(rdf_ij.r, rdf_ij.smeared_rdf(), color = bond.colour, linestyle=linestyles[i], label=f'{bond.bond_label} {dataset}')

    plt.xlabel('r (Å)')
    plt.ylabel('RDF')
    plt.legend()
    plt.savefig(f'{fig_name}.pdf', bbox_inches='tight')
    plt.show()
