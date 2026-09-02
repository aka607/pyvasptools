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


def get_component_elements(chemical_formula):
        '''
        Returns a list[str] of elements contained in chemical_formula. 

        get_component_elements: str -> list[str]
        
        Examples: 
            get_component_elements("H") => ['H']
            
            get_component_elements("LiCoO4") => ['Li', 'Co', 'O']
            
            get_component_elements("C6H6-H2O") => ['C', 'H', 'O']
        '''
        s = chemical_formula
        
        i = 0 
        L = []
        curr_element = ""

        while i < len(s):

            if (s[i] == '-') or (s[i].isdigit()):
                i += 1 

            elif s[i].isupper():
                if (i == len(s) - 1) or s[i+1].isupper() or (s[i+1] == '-') or (s[i+1].isdigit()):
                    curr_element += s[i]
                    i += 1 
                else:
                    curr_element += s[i:i+2]
                    i += 2 
                if curr_element in periodic_table:
                    if not curr_element in L:
                        L.append(curr_element)
                    curr_element = ""
                else:
                    raise Exception(f"{curr_element} is not a valid element in the periodic table of elements")

        return L

    

class Compound:
    def __init__(self, chemical_formula):
        '''
        Constructor: Create a Compound object by calling Compound(chemical_formula)

        Effects: Mutates self

        __init__: Compound Str -> None 
        Requires:
            - chemical_formula must correspond to a valid molecular formula. 
            - different molecules/alloys in chemical_formula can be separated by '-', i.e., NbTaMoW-FLiBe or NbTaMoW-FLiBe-H2O
        '''
        elements = get_component_elements(chemical_formula)

        self.chemical_formula = chemical_formula
        self.elements = elements 

    def __repr__(self):
        '''
        Returns a string representation of self.

        __rep__: Compound -> Str 
        '''
        s = f"Compound Name: {self.chemical_formula}\nElements: {','.join(self.elements)}"
        return s

    
    



