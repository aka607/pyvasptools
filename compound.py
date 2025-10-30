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



