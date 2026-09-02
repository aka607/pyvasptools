from src.pyvasptools.dataset import * 
from src.pyvasptools.rdf.RDF import * 


current_dir = Path(__file__).parent
root_dir = current_dir.parents[1]


# 1. Sample data set 1: Compare the radial distribution function of NbTaMoW versus NbTaMoWV
NbTaMoW_interface = Dataset(path=root_dir / 'sample_data/NbTaMoW-FLiBe/10ps/DOS', ls='-', label='NbTaMoW')
NbTaMoWV_interface = Dataset(path=root_dir / 'sample_data/NbTaMoWV-FLiBe/10ps/DOS', ls='--', label='NbTaMoWV')

rdf([NbTaMoW_interface, NbTaMoWV_interface], Bond('F', 'F', 'blue'), Bond('Li', 'F', 'red'), Bond('Be', 'F', 'green'), fig_name=current_dir / 'RDF')
rdf([NbTaMoW_interface, NbTaMoWV_interface], Bond('F', 'F', 'blue'), Bond('Li', 'F', 'red'), Bond('Be', 'F', 'green'), same_plot=False, fig_name=current_dir / 'RDF_separate_plots')


# # metal only
NbTaMoW = Dataset(path=root_dir / 'sample_data/NbTaMoW/10ps/DOS', ls='-', label='NbTaMoW')
NbTaMoWV = Dataset(path=root_dir / 'sample_data/NbTaMoWV/10ps/DOS', ls='--', label='NbTaMoWV')
rdf([NbTaMoW, NbTaMoWV], total_RDF=True, fig_name=current_dir / 'metal_surfaces_RDF', elements_to_plot=['Nb', 'Ta', 'Mo', 'W'])