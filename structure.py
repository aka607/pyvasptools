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


def int_to_roman(n):
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


class Compound:
    def __init__(self, chemical_formula):
        '''
        Constructor: Creates a Molecule object by calling Molecule(molecular_formula) where molecular_formula is a str associated with a
        molecular formula. 
        '''
        self.chemical_formula = chemical_formula

    def __repr__(self):
        '''
        Returns a string representation of self.

        __rep__: Compound -> Str 
        '''
        s = "Compound Name: {0.chemical_formula}"
        return s.format(self)

    def get_component_elements(self):
        '''
        Returns a list of atomic elements that constitute the chemical Compound. 
            
        NbTaMoW -> ['Nb', 'Ta', 'Mo', 'W']
        H2O -> ['H', 'O']
        FLiBe -> ['F', 'Li', Be']
            
        '''
        s = self.chemical_formula
        
        i = 0 
        L = []

        while i < len(s)-1:       
            if s[i+1].isupper():
                L.append(s[i])
                if i+1 == len(s)-1:
                    L.append(s[i+1])
                i += 1 
            else:
                L.append(s[i:i+2])
                if i+2 == len(s)-1:
                    L.append(s[i+2])
                i += 2 
        return L
    

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
        '''
        self.atom1 = atom1
        self.atom2 = atom2
        self.colour = colour
        self.bond_label = bond_label



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
        linestyles_plt = ['-', '--', 'solid', 'dotted', 'dashed', 'dashdot']

   
        self.path = path

        if (lc == None) or (lc in valid_colors) or re.fullmatch(r'#([A-Fa-f0-9]{6})', lc):
            self.lc = lc
        else:
            print(f'<lc> needs to be valid matlotlib colour')

        if (ls == None) or (ls in linestyles_plt):
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



