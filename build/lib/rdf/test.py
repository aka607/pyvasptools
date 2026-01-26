from PyVaspTools.structure import *
from RDF import * 

# NbTaMoW
path_0ps = '/Users/agneskatai/cluster_data/Narval_test/NbTaMoW-FLiBe/dynamics/2_layer/salt/0ps'
path_40ps = '/Users/agneskatai/cluster_data/Narval_test/NbTaMoW-FLiBe/dynamics/2_layer/salt/40ps'

NbTaMoW_0ps = Dataset(path_0ps, ls='-', label='0 ps')
NbTaMoW_40ps = Dataset(path_40ps, ls='--', label='40 ps')
rdf([NbTaMoW_0ps, NbTaMoW_40ps], [Bond('F', 'F', 'blue'), Bond('Li', 'F', 'red'), Bond('Be', 'F', 'green')], fig_name='/Users/agneskatai/Desktop/Spring 2025/Figures/RDF/RDF')
rdf([NbTaMoW_0ps, NbTaMoW_40ps], [Bond('F', 'F', 'blue'), Bond('Li', 'F', 'red'), Bond('Be', 'F', 'green')], same_plot=False, fig_name='/Users/agneskatai/Desktop/Spring 2025/Figures/RDF/RDF_two_plots')

# # NbTaMoWV 
path_0ps = '/Users/agneskatai/cluster_data/Narval_test/NbTaMoW-FLiBe/dynamics/2_layer/salt/0ps'
path_40ps = '/Users/agneskatai/cluster_data/Narval_test/NbTaMoWV-FLiBe/dynamics/2_layer/salt/40ps'

NbTaMoWV_0ps = Dataset(path_0ps, ls='-', label='0 ps')
NbTaMoWV_40ps = Dataset(path_40ps, ls='--', label='40 ps')
rdf([NbTaMoWV_0ps, NbTaMoWV_40ps], [Bond('F', 'F', 'blue'), Bond('Li', 'F', 'red'), Bond('Be', 'F', 'green')], fig_name='/Users/agneskatai/Desktop/Spring 2025/Figures/RDF/RDF_V')

# #NbTaMoW-H2O
path_0ps = '/Users/agneskatai/cluster_data/Narval_test/H2O/H2O-NbTaMoW/100/0ps'
path_40ps = '/Users/agneskatai/cluster_data/Narval_test/H2O/H2O-NbTaMoW/100/40ps'

NbTaMoW_0ps = Dataset(path_0ps, ls='-', label='0 ps')
NbTaMoW_40ps = Dataset(path_40ps, ls='--', label='40 ps')
rdf([NbTaMoW_0ps, NbTaMoW_40ps], [Bond('F', 'F', 'blue'), Bond('Li', 'F', 'red'), Bond('Be', 'F', 'green')], fig_name='/Users/agneskatai/Desktop/Spring 2025/Figures/RDF/RDF_H2O')

# #NbTaMoWV-H2O
path_0ps = '/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoWV/100/0ps'
path_40ps = '/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoWV/100/40ps'

NbTaMoWV_0ps = Dataset(path_0ps, ls='-', label='0 ps')
NbTaMoWV_40ps = Dataset(path_40ps, ls='--', label='40 ps')
rdf([NbTaMoWV_0ps, NbTaMoWV_40ps], [Bond('F', 'F', 'blue'), Bond('Li', 'F', 'red'), Bond('Be', 'F', 'green')], fig_name='/Users/agneskatai/Desktop/Spring 2025/Figures/RDF/RDF_H2O')
