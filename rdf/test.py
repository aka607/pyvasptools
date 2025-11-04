from PyVaspTools.structure import * 
from RDF import * 

# NbTaMoW
path_0ps = '/Users/agneskatai/cluster_data/Narval_test/NbTaMoW-FLiBe/dynamics/2_layer/salt/0ps'
path_40ps = '/Users/agneskatai/cluster_data/Narval_test/NbTaMoW-FLiBe/dynamics/2_layer/salt/40ps'

datasets = {'0 ps': path_0ps, '40 ps': path_40ps}

rdf(datasets, ['-', '--'], Bond('F', 'F', 'blue'), Bond('Li', 'F', 'red'), Bond('Be', 'F', 'green'), fig_name='/Users/agneskatai/Desktop/Spring 2025/Figures/RDF/RDF')

# NbTaMoWV 
path_0ps = '/Users/agneskatai/cluster_data/Narval_test/NbTaMoW-FLiBe/dynamics/2_layer/salt/0ps'
path_40ps = '/Users/agneskatai/cluster_data/Narval_test/NbTaMoWV-FLiBe/dynamics/2_layer/salt/40ps'

rdf(datasets, ['-', '--'], Bond('F', 'F', 'blue'), Bond('Li', 'F', 'red'), Bond('Be', 'F', 'green'), fig_name='/Users/agneskatai/Desktop/Spring 2025/Figures/RDF/RDF_V')


#NbTaMoW-H2O
path_0ps = '/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoW/100/0ps'
path_40ps = '/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoW/100/40ps'

rdf(datasets, ['-', '--'], Bond('F', 'F', 'blue'), Bond('Li', 'F', 'red'), Bond('Be', 'F', 'green'), fig_name='/Users/agneskatai/Desktop/Spring 2025/Figures/RDF/RDF_H2O')


#NbTaMoWV-H2O
path_0ps = '/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoWV/100/0ps'
path_40ps = '/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoWV/100/40ps'

rdf(datasets, ['-', '--'], Bond('F', 'F', 'blue'), Bond('Li', 'F', 'red'), Bond('Be', 'F', 'green'), fig_name='/Users/agneskatai/Desktop/Spring 2025/Figures/RDF/RDF_H2O_V')