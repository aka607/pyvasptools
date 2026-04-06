import numpy as np 
import re 


def get_vesta_atom_id(atom, poscar):

    '''
    Converts from COHP format Atom IDs which are numbered according to the total number of atoms in the system
    to VESTA Atom ID format which are numbered according to the total number of atoms for a given element type.

    For example, in a H2O-FLiBe-NbTaMoW chemical system with a total of 181 atoms out of which 20 are Nb atoms and 56 are F atoms, 
    Nb140 -> Nb19 and F46 -> F1 

    find_atom(Str, Str) -> Str
    Requires:
        - poscar is a valid POSCAR file 
    '''

    poscar = open(poscar)
    L = poscar.readlines()

    # Determine order of the atoms in which they appear in POSCAR 
    ordered_atoms = " ".join(L[5:7]).split()
    N = len(ordered_atoms)//2
    ordered_atoms = np.array(ordered_atoms).reshape(2, N)

    
    element = re.search(r'[a-zA-Z]+', atom).group()
    number = int(re.search(r'\d+', atom).group())

    index = np.where(ordered_atoms[0] == element)[0][0]
    

    for i in range(index):
        number -= int(ordered_atoms[1][i])
    s = element + str(number)
    return s


def get_cohp_atom_ids(poscar, *atom_ids):
    '''
    Convert the atom_ids from VESTA format (out of total N of each element type) to COHP format (out of total number of atoms in the chemical system).
    Returns a dictionary in which the keys are the COHP Atom ID#s and the values are the VESTA Atom Numbers. 

    For example, in a H2O-FLiBe-NbTaMoW chemical system with a total of 181 atoms out of which 20 are Nb atoms and 56 are F atoms,
    Nb19 -> Nb140 and F1 -> F46

    find_atom_IDs(Str Str) -> (dictof Str Str)
    '''
    poscar = open(poscar)
    L = poscar.readlines()

    # Determine order of the atoms
    ordered_atoms = " ".join(L[5:7]).split()
    N = len(ordered_atoms)//2
    ordered_atoms = np.array(ordered_atoms).reshape(2, N)

    d_ids = {}

    for atom_no in atom_ids:
        element = re.search(r'[a-zA-Z]+', atom_no).group()
        number = int(re.search(r'\d+', atom_no).group())

        index = np.where(ordered_atoms[0] == element)[0][0]
        
        count_all_atoms = 0
        for i in range(index):
            count_all_atoms += int(ordered_atoms[1][i])
        count_all_atoms += number
        d_ids[f'{element}{count_all_atoms}'] = atom_no

    return d_ids
