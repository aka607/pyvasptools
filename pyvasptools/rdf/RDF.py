from pymatgen.core.structure import Structure 

from vasppy.rdf import RadialDistributionFunction
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def rdf(datasets, *args, same_plot=True, total_RDF=False, **kwargs):
    '''
    Plots the RDF as a function of interatomic distance between the centre atom and the distribution atom. *args must be a Bond object. The centre atom is atom1, the 
    distribution atom is atom2 in the Bond. The bond colour needs to also be defined in the Bond. 

    datasets : list[Dataset]
        One or more Dataset objects containing vasp output files 
    args : Bonds, optional
        Bonds for which to plot the RDF 
    same_plot : bool, optional
        If True, all datasets are plotted on the same plot. If False, datasets are plotted on separate plots 
    total_RDF : bool, optional
        If True, plots the total_RDF. If False, plots the RDF only for specific bonds. 
    fig_name: str, optional
        figure name
    elements_to_plot: list[str]
        If plotting total_RDF, only elements_to_plot are included in the total_RDF calculation. elements in elements_to_plot must be valid elements from the periodic table. 
    '''
    fig_name = kwargs.get("fig_name", "RDF")
    elements_to_plot = kwargs.get("elements_to_plot", [])

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
    
        
    for i in range(len(datasets)):
        dataset = datasets[i]
        structure = Structure.from_file(f'{dataset.path}/POSCAR')           # get structure -- either POSCAR or XDATCAR from VASP output files

        if total_RDF:
            if len(elements_to_plot) > 0:
                L_indices = []
                L_species = structure.species

                for ii in range(len(structure)):
                    if L_species[ii].symbol in elements_to_plot:
                        L_indices.append(ii)

                rdf = RadialDistributionFunction(structures=[structure], indices_i=L_indices, indices_j=L_indices)
            else:
                rdf = RadialDistributionFunction(structures=[structure], indices_i=list(range(len(structure))), indices_j=list(range(len(structure))))

            if not same_plot:
                axes[i].xaxis.set_major_locator(ticker.MultipleLocator(1))  # major ticks every 1 unit
                axes[i].plot(rdf.r, rdf.smeared_rdf(), color=dataset.lc, linestyle=dataset.ls, label=f'total - {dataset.label}')
                axes[i].legend()
            else:
                plt.plot(rdf.r, rdf.smeared_rdf(), color=dataset.lc, linestyle=dataset.ls, label=f'total - {dataset.label}')

        for bond in args:
            rdf_ij = RadialDistributionFunction.from_species_strings(structures=[structure], 
                                        species_i=bond.atom1,
                                        species_j=bond.atom2)
            
            if not same_plot:
                axes[i].xaxis.set_major_locator(ticker.MultipleLocator(1))  # major ticks every 1 unit
                axes[i].plot(rdf_ij.r, rdf_ij.smeared_rdf(), color = bond.colour, linestyle=dataset.ls, label=f'{bond.bond_label} - {dataset.label}')
                axes[i].legend()
            else:
                plt.plot(rdf_ij.r, rdf_ij.smeared_rdf(), color = bond.colour, linestyle=dataset.ls, label=f'{bond.bond_label} - {dataset.label}')


    if same_plot:
        plt.xticks(range(0, 11))   # integer tick positions from min to max
        plt.xlabel('r (Å)')
        plt.ylabel('RDF')
        plt.legend()
        plt.savefig(f'{fig_name}.pdf', bbox_inches='tight')
        plt.show()
    else:
        fig.supylabel('RDF')
        axes[-1].set_xlabel("r (Å)")
        fig.savefig(fname=f'{fig_name}.pdf', format='pdf', dpi=300, bbox_inches='tight')
