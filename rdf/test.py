from PyVaspTools.structure import *
from RDF import * 

# # NbTaMoW
# path_0ps = '/Users/agneskatai/cluster_data/Narval_test/NbTaMoW-FLiBe/dynamics/2_layer/salt/0ps'
# path_40ps = '/Users/agneskatai/cluster_data/Narval_test/NbTaMoW-FLiBe/dynamics/2_layer/salt/40ps'

# NbTaMoW_0ps = Dataset(path_0ps, ls='-', label='0 ps')
# NbTaMoW_40ps = Dataset(path_40ps, ls='--', label='40 ps')
# rdf([NbTaMoW_0ps, NbTaMoW_40ps], Bond('F', 'F', 'blue'), Bond('Li', 'F', 'red'), Bond('Be', 'F', 'green'), fig_name='/Users/agneskatai/Desktop/Spring 2025/Figures/RDF/RDF')
# rdf([NbTaMoW_0ps, NbTaMoW_40ps], Bond('F', 'F', 'blue'), Bond('Li', 'F', 'red'), Bond('Be', 'F', 'green'), same_plot=False, fig_name='/Users/agneskatai/Desktop/Spring 2025/Figures/RDF/RDF_two_plots')

# # # NbTaMoWV 
# path_0ps = '/Users/agneskatai/cluster_data/Narval_test/NbTaMoW-FLiBe/dynamics/2_layer/salt/0ps'
# path_40ps = '/Users/agneskatai/cluster_data/Narval_test/NbTaMoWV-FLiBe/dynamics/2_layer/salt/40ps'

# NbTaMoWV_0ps = Dataset(path_0ps, ls='-', label='0 ps')
# NbTaMoWV_40ps = Dataset(path_40ps, ls='--', label='40 ps')
# # rdf([NbTaMoWV_0ps, NbTaMoWV_40ps], [Bond('F', 'F', 'blue'), Bond('Li', 'F', 'red'), Bond('Be', 'F', 'green')], fig_name='/Users/agneskatai/Desktop/Spring 2025/Figures/RDF/RDF_V')

# # #NbTaMoW-H2O
# path_0ps = '/Users/agneskatai/cluster_data/Narval_test/H2O/H2O-NbTaMoW/100/0ps'
# path_40ps = '/Users/agneskatai/cluster_data/Narval_test/H2O/H2O-NbTaMoW/100/40ps'

# NbTaMoW_0ps = Dataset(path_0ps, ls='-', label='0 ps')
# NbTaMoW_40ps = Dataset(path_40ps, ls='--', label='40 ps')
# # rdf([NbTaMoW_0ps, NbTaMoW_40ps], [Bond('F', 'F', 'blue'), Bond('Li', 'F', 'red'), Bond('Be', 'F', 'green')], fig_name='/Users/agneskatai/Desktop/Spring 2025/Figures/RDF/RDF_H2O')

# # #NbTaMoWV-H2O
# path_0ps = '/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoWV/100/0ps'
# path_40ps = '/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoWV/100/40ps'

# NbTaMoWV_0ps = Dataset(path_0ps, ls='-', label='0 ps')
# NbTaMoWV_40ps = Dataset(path_40ps, ls='--', label='40 ps')
# # rdf([NbTaMoWV_0ps, NbTaMoWV_40ps], [Bond('F', 'F', 'blue'), Bond('Li', 'F', 'red'), Bond('Be', 'F', 'green')], fig_name='/Users/agneskatai/Desktop/Spring 2025/Figures/RDF/RDF_H2O')


# # NbTaMoW
# path_NbTaMoW_0ps = '/Users/agneskatai/khartoum_data/tabgap/NbTaMoW/100/800K/Input_100'
# path_NbTaMoW_100ps = '/Users/agneskatai/utils/make_interface'

# NbTaMoW_0ps = Dataset(path_NbTaMoW_0ps, lc='blue', ls='-', label='0 ps')
# NbTaMoW_100ps = Dataset(path_NbTaMoW_100ps, lc='red', ls='-', label='100 ps')

# rdf([NbTaMoW_0ps, NbTaMoW_100ps], total_RDF=True, same_plot=False, fig_name='/Users/agneskatai/Desktop/Spring 2025/Figures/RDF/total_RDF_NbTaMoW')


# # NbTaMoWV
# path_NbTaMoWV_0ps = '/Users/agneskatai/khartoum_data/tabgap/NbTaMoWV/100/0K'
# path_NbTaMoWV_100ps = '/Users/agneskatai/khartoum_data/tabgap/NbTaMoWV/100/800K'

# NbTaMoWV_0ps = Dataset(path_NbTaMoWV_0ps, lc='blue', ls='-', label='0 ps')
# NbTaMoWV_100ps = Dataset(path_NbTaMoWV_100ps, lc='red', ls='-', label='100 ps')

# rdf([NbTaMoWV_0ps, NbTaMoWV_100ps], total_RDF=True, same_plot=False, fig_name='/Users/agneskatai/Desktop/Spring 2025/Figures/RDF/total_RDF_NbTaMoWV')


# NbTaMoW - pure metal after 10 ps
path_NbTaMoW_FLiBe_0ps = '/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoW/100_v2/0ps'
path_NbTaMoW_FLiBe_10ps = '/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoW/100_v2/10ps/kpts-6'

# metal only
NbTaMoW_FLiBe_0ps = Dataset(path_NbTaMoW_FLiBe_0ps, lc='blue', ls='-', label='0 ps')
NbTaMoW_FLiBe_10ps = Dataset(path_NbTaMoW_FLiBe_10ps, lc='red', ls='-', label='10 ps')
rdf([NbTaMoW_FLiBe_0ps, NbTaMoW_FLiBe_10ps], total_RDF=True, fig_name='/Users/agneskatai/Desktop/Spring 2025/Figures/RDF/RDF_NbTaMoW_FLiBe_v2_metal', elements_to_plot=['Nb', 'Ta', 'Mo', 'W'])

# salt only
NbTaMoW_FLiBe_10ps = Dataset(path_NbTaMoW_FLiBe_10ps, lc='red', ls='--', label='10 ps')
rdf([NbTaMoW_FLiBe_0ps, NbTaMoW_FLiBe_10ps], Bond('F', 'F', 'blue'), Bond('Li', 'F', 'red'), Bond('Be', 'F', 'green'), fig_name='/Users/agneskatai/Desktop/Spring 2025/Figures/RDF/RDF_NbTaMoW_FLiBe_v2_salt')



# NbTaMoWV - pure metal after 10 ps
path_NbTaMoWV_FLiBe_0ps = '/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoWV/100_v2/0ps'
path_NbTaMoWV_FLiBe_10ps = '/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoWV/100_v2/10ps/kpts-6'

# metal only
NbTaMoWV_FLiBe_0ps = Dataset(path_NbTaMoWV_FLiBe_0ps, lc='blue', ls='-', label='0 ps')
NbTaMoWV_FLiBe_10ps = Dataset(path_NbTaMoWV_FLiBe_10ps, lc='red', ls='-', label='10 ps')
rdf([NbTaMoWV_FLiBe_0ps, NbTaMoWV_FLiBe_10ps], total_RDF=True, fig_name='/Users/agneskatai/Desktop/Spring 2025/Figures/RDF/RDF_NbTaMoWV_FLiBe_v2_metal', elements_to_plot=['Nb', 'Ta', 'Mo', 'W', 'V'])

# salt only
NbTaMoWV_FLiBe_10ps = Dataset(path_NbTaMoWV_FLiBe_10ps, lc='red', ls='--', label='10 ps')
rdf([NbTaMoWV_FLiBe_0ps, NbTaMoWV_FLiBe_10ps], Bond('F', 'F', 'blue'), Bond('Li', 'F', 'red'), Bond('Be', 'F', 'green'), fig_name='/Users/agneskatai/Desktop/Spring 2025/Figures/RDF/RDF_NbTaMoWV_FLiBe_v2_salt')







