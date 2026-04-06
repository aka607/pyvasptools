import pandas as pd 
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt 

from py4vasp import Calculation
import re
from compound import * 

from pathlib import Path


def get_letters_only(s):
    return ''.join(c for c in s if c.isalpha())


def int_to_roman(n):
        '''
        Converts an integer n into a roman numeral (str). 

        int_to_roman: Nat -> Str
        Requires:
            n > 0 
        '''
        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4, 1
        ]
        syms = [
            'M', 'CM', 'D', 'CD',
            'C', 'XC', 'L', 'XL',
            'X', 'IX', 'V', 'IV', 'I'
        ]
        roman = ''
        for i in range(len(val)):
            while n >= val[i]:
                roman += syms[i]
                n -= val[i]
        return roman.lower()


class Bond:
    '''
    Fields:
        atom1 (Str) -> must be part of the periodic table
        atom2 (Str) -> must be part of the periodic table
        colour (Str) -> must be a valid matplotlib colour
    '''

    def __init__(self, atom1, atom2, colour='blue', bond_label=None):
        '''
        Constructor: Create a Bond object by calling Bond(atom1, atom2, colour, bond_label)

        Effect: Mutates self 

        __init__: Bond Str Str Str -> None
        Requires:
            - atom1 and atom2 must be valid elements from the periodic table
            - colour must be a valid matplotlib colour. 
            - bond_label needs to be less than 20 characters long
        '''
        valid_colors = set(mcolors.CSS4_COLORS.keys())

        # Validate atoms
        if get_letters_only(atom1) not in periodic_table:
            raise ValueError(f"{atom1} is not a valid element in the periodic table")

        if get_letters_only(atom2) not in periodic_table:
            raise ValueError(f"{atom2} is not a valid element in the periodic table")

        # Validate color
        if colour not in valid_colors:
            raise ValueError(f"{colour} is not a valid matplotlib color")

        # Validate bond_label
        if bond_label is not None and not isinstance(bond_label, str) and not len(bond_label) <= 20:
            raise TypeError("bond_label must be a string less than 20 characters long")

        # Default label
        if bond_label is None:
            bond_label = f"{atom1}-{atom2}"

        # Assign attributes
        self.atom1 = atom1
        self.atom2 = atom2
        self.colour = colour
        self.bond_label = bond_label

    def __repr__(self):
        '''
        Returns a string representation of self.

        __rep__: Dataset -> Str 
        '''
        s = "Bond: {0.bond_label}\nColour: {0.colour}"
        return s.format(self)



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
        Constructor: Creates a Dataset object by calling Dataset(path, lc, ls, label) 

        Effect: mutates self 

        __init__: str or pathlib.Path str str str -> None 
        Requires:
            - path contains VASP output calculations, particularly vaspout.h5.
            - lc and ls must be a valid matplotlib colour and linestyle, respectively 
            - label needs to be a string datatype less than 20 characters long
        '''
        valid_colors = list(mcolors.CSS4_COLORS.keys())
        linestyles_plt = ['-', '--', 'solid', 'dotted', 'dashed', 'dashdot']

        self.path = path

        if lc is None or (lc in valid_colors) or re.fullmatch(r'#([A-Fa-f0-9]{6})', lc):
            self.lc = lc
        else:
            raise ValueError(f"{lc} is not a valid matplotlib color")

        if ls is None or (ls in linestyles_plt):
            self.ls = ls 
        else:
            raise ValueError(f"{ls} is not a valid matplotlib linestyle")

        if label is None or (isinstance(label, str) and len(label) <= 20):
            self.label = label 
        else:
            print(f'label needs to be a string datatype less than 20 characters long')


    def __repr__(self):
        '''
        Returns a string representation of self.

        __rep__: Dataset -> Str 
        '''
        s = "Dataset Name: {0.label}"
        return s.format(self)
    

    def get_elements_partial_dos(self):
        '''
        Returns a list of elements for which the DOS was calculation. 
        
        :param self: Description
        '''
        # Initialize a py4vasp Calculation object 
        calc = Calculation.from_path(self.path)

        # Extract all the individual elements for which the partial DOS was calculated
        component_elements = [a for a in calc.projector.selections()['atom'] if a.isalpha()]     

        return component_elements


    def total_DOS(self, spin='up', align_Fermi=False, to_csv=False):
        '''
        Returns a 1D array of energies in eV, 1D array of total density of states (1/eV) and the Fermi level (eV). 
        By default, the energies are not shifted wrt the Fermi level. By default, calculates DOS for spin up. The Fermi level is rounded to 3 decimal places. Note: it is presumed that your calculation was performed in 
        a "DOS" folder within your dataset path.

        Example:
        data = Dataset(".", lc="black", label="NbTaMoW 1ps")
        data.total_DOS() => energies, dos, E_fermi 
        '''
        # Initialize a py4vasp Calculation object 
        calc = Calculation.from_path(self.path)

        _df = calc.dos.to_frame()
        _dict = calc.dos.to_dict()
        
        E_fermi = _dict['fermi_energy']

        # Do not correct for Fermi level 
        if not align_Fermi:
            _dict['energies'] = _dict['energies'] + E_fermi
            if to_csv:
                pd.DataFrame(_dict).to_csv(f'{self.label}.csv')

        else:
            if to_csv:
                _df.to_csv(f'{self.path}/{self.label}.csv')
  
        return _dict['energies'], _dict[f'{spin}'], E_fermi
    

    def plot_total_DOS(self, spin='up', align_Fermi=False, zoom_in=False, ylim=None, xlim=None, output_dir=None, output_name=None):
        '''
        Plots the Dataset on the provided fig and axes which is useful for plotting multiple data sets on 1 graph.
        Note: even if you plot only 1 data set, your data will still be labelled accordingly.

        plot_total_DOS: Dataset Str Bool Bool Tuple Tuple Str -> None 
        Requires:
            - spin must be either 'up' or 'down' 
            - xlim and ylim must be a tuple of size 2
            - dir is the directory where you want the figure saved 

        Examples:
            NbTaMoWV = Dataset(path='/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoWV/pure_metal/10ps/DOS', lc='red', label='NbTaMoWV')

            NbTaMoWV.plot_total_DOS() => None
        '''
        fig, axes = plt.subplots(1, 1, dpi=150, figsize=(14, 12))

        # Retrieve the relevant parameters from total_DOS
        energies, dos, E_fermi = self.total_DOS(spin=spin, align_Fermi=align_Fermi)
        
        # Plot the data with desired plot parameters 
        axes.plot(energies, dos, linewidth=1.5, linestyle=self.ls, color=self.lc)
        axes.set_ylabel('DOS (1/eV)', fontsize=18, fontweight='bold')
        axes.set_xlabel('Energy (eV)', fontsize=18, fontweight='bold')
        axes.tick_params(axis='both', labelsize=16)  # Both x and y ticks

        # Other optional plot parameters and descriptors 
        if ylim is not None:
            axes.set_ylim(ylim[0], ylim[1])
        if xlim is not None:
            axes.set_xlim(xlim[0], xlim[1])
        
        if zoom_in:
            axes.set_xlim(-20, 10)

        if align_Fermi:
            axes.axvline(x=0, color=self.lc, linewidth=1.5, linestyle='--', label=f'$E_F$')
        else:
            axes.axvline(x=E_fermi, color=self.lc, linewidth=1.5, linestyle='--', label=f'$E_F$={E_fermi:.3f} eV')

        axes.legend(fontsize=16, loc='upper left')

        if output_dir is None:
            output_dir = self.path

        if output_name is None:
            output_name = self.label

        output_path = Path(output_dir) / f"{output_name}.png"
        fig.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.show()
