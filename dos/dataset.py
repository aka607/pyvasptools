import pandas as pd 
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import plotly.subplots as ps

from py4vasp import Calculation
import re
import string
import numpy as np
import diptest

from compound import * 


periodic_table = [
    "H",  "He", "Li", "Be", "B",  "C",  "N",  "O",  "F",  "Ne",
    "Na", "Mg", "Al", "Si", "P",  "S",  "Cl", "Ar", "K",  "Ca",
    "Sc", "Ti", "V",  "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
    "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y",  "Zr",
    "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
    "Sb", "Te", "I",  "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
    "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
    "Lu", "Hf", "Ta", "W",  "Re", "Os", "Ir", "Pt", "Au", "Hg",
    "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
    "Pa", "U",  "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm",
    "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
    "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"
]


class Dataset:
    '''
    Fields:
        path (str or pathlib.Path) 
        lc (str)
        ls (str)
        label (str)
        Requires:
            lc and ls must be valid linecolour and linestyle in matplotlib, respectively. 
    '''
    def __init__(self, path, lc=None, ls=None, label=None):
        '''
        Constructor: Creates a Dataset object by calling Dataset(path, lc, ls, label) where path is the path associated with the VASP 
        calculation (presumes that different subcalculations including DOS, workfunctions are located within this directory), lc is 
        the colour for the dataset, ls is the linestyle and label is what you want to label the dataset. 

        Effect: mutates self 
        '''
        valid_colors = list(mcolors.CSS4_COLORS.keys())
        linestyles_plt = ['solid', 'dotted', 'dashed', 'dashdot']
        linestyles_plotly = ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']

   
        self.path = path

        if (lc == None) or (lc in valid_colors) or re.fullmatch(r'#([A-Fa-f0-9]{6})', lc):
            self.lc = lc
        else:
            print(f'<lc> needs to be valid matlotlib colour')

        if (ls == None) or (ls in linestyles_plt) or (ls in linestyles_plotly):
            self.ls = ls 
        else:
            print(f'<ls> needs to be valid matlotlib linestyle')

        if isinstance(label, str) and len(label) <= 20:
            self.label = label 
        else:
            print(f'<label> needs to be a string datatype less than 20 characters long')


    def __repr__(self):
        '''
        Returns a string representation of self.

        __rep__: Dataset -> Str 
        '''
        s = "Dataset Name: {0.label}"
        return s.format(self)


    def total_DOS(self, select=False, spin='up', align_Fermi=False, to_csv=False):
        '''
        Returns a 1D array of energies (eV), 1D array of total density of states (1/eV), the Fermi level (eV) and the constituent elements in the system. 
        By default, the energies are not shifted wrt the Fermi level. By default, calculates DOS for spin up. The Fermi level is rounded to 3 decimal places. Note: it is presumed that your calculation was performed in 
        a "DOS" folder within your dataset path.

        Example:
        data = Dataset(".", lc="black", label="NbTaMoW 1ps")
        data.total_DOS() => energies, dos, E_fermi 
        '''
        # Initialize a py4vasp Calculation object 
        calc = Calculation.from_path(f'{self.path}/DOS')

        # Extract all the individual elements for which the partial DOS was calculated
        component_elements = [a for a in calc.projector.selections()['atom'] if a.isalpha()]      

        if select != False:
            # select a specific decomposed density of states
            _df = calc.dos.to_frame(selection=f'{select}')
            _dict = calc.dos.to_dict(selection=f'{select}')
        else:
            _df = calc.dos.to_frame()
            _dict = calc.dos.to_dict()
        
        E_fermi = _dict['fermi_energy']

        # Do not correct for Fermi level 
        if not align_Fermi:
            _dict['energies'] = _dict['energies'] + E_fermi

        if to_csv:
            _df.to_csv(f'{self.label}_Fermi_shifted.csv')
            pd.DataFrame(_dict).to_csv(f'{self.label}.csv')
  
        return _dict['energies'], _dict[f'{spin}'], E_fermi, component_elements
    

    def plot_total_DOS(self, fig, axes, select=False, spin='up', align_Fermi=False, to_csv=False, zoom_in=False, multiple=True):
        '''
        Plots the Dataset on the provided fig and axes which is useful for plotting multiple data sets on 1 graph.
        Note: even if you plot only 1 data set, your data will still be labelled accordingly.
        '''
        # Retrieve the relevant parameters from total_DOS
        energies, dos, E_fermi, component_elements = self.total_DOS()
        
        # Plot the data with desired plot parameters 
        axes.plot(energies, dos, linewidth=1.5, linestyle=self.ls, color=self.lc, label=self.label)
        axes.set_ylabel('DOS (1/eV)', fontsize=18, fontweight='bold')
        axes.set_xlabel('Energy (eV)', fontsize=18, fontweight='bold')
        axes.tick_params(axis='both', labelsize=16)  # Both x and y ticks
        axes.set_ylim(-5, 140)
        axes.set_xlim(-80, 10)
        
        # Other optional plot parameters and descriptors 
        if zoom_in:
            axes.set_xlim(-20, 10)

        if align_Fermi:
            if self.label == None:
                axes.axvline(x=0, color=self.lc, linewidth=1, linestyle='--', label=f'$E_F$')
            else:
                axes.axvline(x=0, color=self.lc, linewidth=1, linestyle='--', label=f'$E_F$ - {self.label}')
        else:
            if self.label == None:
                axes.axvline(x=E_fermi, color=self.lc, linewidth=1, linestyle='--', label=f'$E_F$={E_fermi:.3f} eV')
            else:
                axes.axvline(x=E_fermi, color=self.lc, linewidth=1, linestyle='--', label=f'$E_F$={E_fermi:.3f} eV - {self.label}')

        axes.legend(fontsize=16, loc='upper left')


    

def plot_multiple_tdos(name, *args):
    '''
    Plots the total DOS for multiple datasets given as *args on the same figure. Creates both a full plot and a zoomed in plot.
    '''

    fig, axes = plt.subplots(1, 1, dpi=150, figsize=(14, 12))
    fig2, axes2 = plt.subplots(1, 1, dpi=150, figsize=(14, 12))

    for a in args:
        a.plot_total_DOS(fig, axes, align_Fermi=False)
        a.plot_total_DOS(fig2, axes2, align_Fermi=False, zoom_in=True)

    fig.savefig(f'{a.path}/{a.label}.png')
    fig2.savefig(f'{a.path}/{a.label}_zoomed.png')
    plt.show()



def pdos_orbital(axes, ith_d, energies, calc, d_orbitals, linecolor, dip_dataset, E_fermi=None, name=None):
    '''
    Plots the partial Density of States on axes for each constituent element in ith_d and each orbital in orbitals for a given Dataset. The
    py4vasp Calculation object calc contains the processed DOS data for the given Dataset. 
    '''
    orbitals = list(d_orbitals.keys())   

    for i in range(len(orbitals)):
        current_orbital = orbitals[i]
        s = ",".join(list(ith_d.keys()))
        _dict = calc.dos.to_dict(f"{current_orbital}({s})")

        for element in ith_d:
            if (current_orbital == 'd') and (periodic_table.index(element) < 20):
                continue
            
            element_spin_up = _dict[f'{element}_{current_orbital}_up']
            plot_no = ith_d[element]

            if current_orbital == 'd':
                dip, pval = diptest.diptest(element_spin_up)
                dip_dataset[0][plot_no-1] = element
                dip_dataset[1][plot_no-1] = dip
                dip_dataset[2][plot_no-1] = pval
            
            axes[plot_no].plot(energies, element_spin_up, color=linecolor, linewidth=18, linestyle=d_orbitals[current_orbital], label=f'{current_orbital} {name}')


            if i == len(orbitals)-1:
                axes[plot_no].axvline(x=E_fermi, color=linecolor, linewidth=18, linestyle='--')

                # Add text at a specific point (without an arrow)
                axes[plot_no].text(0.80, 0.75, f'{element}', transform=axes[plot_no].transAxes, fontfamily='sans-serif', fontname='Helvetica', fontsize=180, color='black') 
                axes[plot_no].tick_params(axis='x', which='major', direction='out', length=33, width=10)  # Show ticks
                axes[plot_no].tick_params(labelbottom=False)  # Hide x tick labels
                axes[plot_no].legend()

                    

def plot_pdos_modified(d_elements, d_orbitals, path_to_fig, *args, **kwargs):
    '''
    Plots the total and partial DOS for multiple Datasets on the same figure. The Datasets to be plotted are provided in *args. It is recommended to have a maximum of 2 Datasets (*args) to prevent plot overload. 
    In addition to the total DOS plotted in the first row, the pDOS is plotted separately for each of the elements in d_elements (keys) which has its own subplot numbered according to the corresponding values. 

    plot_pdos_modified((dictof Str Nat) 

    - d_elements has element names (from the periodic table) as keys and the corresponding subplot number as values
    - d_orbitals has orbital names as keys and the corresponding matplotlib linestyles as values

    Example:
    These are the elements to be plot in pDOS numbered accordingly: 
    d_elements = {'Nb': 1, 'Ta': 2, 'Mo': 3, 'W': 4}
    
    These are the orbitals to plot in pDOS corresponding to each element: 
    orbitals: {'d': solid, 'p': longdash, 's': 'dot' }
    x_lim = ((-80, 10), (-15, 10))

    ''' 
    y_lim = kwargs.get("y_lim")         # tuple of tuples 
    x_lim = kwargs.get("x_lim")         # tuple of tuples 
    labels = kwargs.get("labels", tuple(list(str(i) for i in range(1, len(args)+1))))       # tuple of dataset names 
    plot_name = kwargs.get("plot_name")   


    plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica'],
    'font.size': 64,
    'xtick.labelsize': 92,
    'ytick.labelsize': 92,
    'axes.labelsize': 64,
    'legend.fontsize': 61,      # use 67 for FLiBe and 61 for FLiBe + H2O      
    'legend.loc': 'upper left'
})

    elements_to_plot = list(d_elements.keys())
    num_elements = len(elements_to_plot)
    num_plots = num_elements + 1

    fig, axes = plt.subplots(
        nrows=num_plots,
        ncols=1,
        figsize=(48, 80),
        sharex=True,
    )
    fig.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.05, hspace=0.08)

    dip_results = np.empty((len(args), 3, num_elements), dtype=object)

    for i in range(len(args)):      # each argument in *args is a dataset object for which a DOS calculation can be performed 
        dataset = args[i]
        dip_dataset = np.empty((3, num_elements), dtype=object)

        energies, total_dos, E_fermi, component_elements = dataset.total_DOS()
        elements_list = list(set(component_elements) & set(elements_to_plot))
        print(f'The elements that are available to plot for {dataset.label} is {elements_list}')

        if elements_list == []:
            continue

        else:
            ith_d = {k: d_elements[k] for k in elements_list}

            system_name = labels[i]

            axes[0].plot(energies, total_dos, color=dataset.lc, linewidth=18, linestyle=dataset.ls, label=f"Total {system_name}")
            axes[0].axvline(x=E_fermi, color=dataset.lc, linewidth=18, linestyle='--', label=f'$E_F$={E_fermi:.3f} eV')
            axes[0].text(0.80, 0.75, f'Total', transform=axes[0].transAxes, fontfamily='sans-serif', fontname='Helvetica', fontsize=180, color='black')
            axes[0].tick_params(axis='x', which='major', direction='out', length=33, width=10)  # Show ticks
            axes[0].tick_params(labelbottom=False)  # Hide x tick labels
            axes[0].legend()

            calc = Calculation.from_path(f'{dataset.path}/DOS')
            pdos_orbital(axes, ith_d, energies, calc, d_orbitals, dataset.lc, dip_dataset, E_fermi=E_fermi, name=system_name)
            dip_results[i] = dip_dataset


    [ax.set_autoscale_on(False) for ax in axes]

    if y_lim != None:
        for i in range(len(y_lim)):
            if x_lim != None:
                axes[i].set_xlim(x_lim)
            axes[i].set_ylim(y_lim[i])

    axes[-1].set_xlabel("Energy (eV)", fontsize=122)
    axes[-1].tick_params(axis='x', which='major', direction='out', length=33, width=10)  # Show ticks
    axes[-1].tick_params(labelbottom=True)
    fig.supylabel("Density of States (1/eV)", fontsize=122)

    fig.savefig(fname=f'{path_to_fig}/{plot_name}_pDOS.pdf', format='pdf', dpi=300, bbox_inches='tight')

    return dip_results



