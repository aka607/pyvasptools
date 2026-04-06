from pyvasptools.dataset import * 
from pyvasptools.critic2.critic2 import * 

# NbTaMoW-FLiBe interface 
# path = "/Users/agneskatai/cluster_data/Narval_test/NbTaMoW-FLiBe/dynamics/2_layer/salt"
# plot_critic_over_timesteps(path, [1, 10, 20, 30, 40], 'Ta20', 'F3', 'Ta8', 'F46', 'W2', 'F6', 'Nb20', 'F14', plot_name="NbTaMoW")


# NbTaMoWV-FLiBe interface 
# path = "/Users/agneskatai/cluster_data/Narval_test/NbTaMoWV-FLiBe/dynamics/2_layer/salt"

# Plot 1) V atoms
# plot_critic_over_timesteps(path, [1, 10, 20, 30, 40], 'V3', 'F16', 'V2', 'F3', 'V15', 'F52', plot_name="NbTaMoWV_V_atoms")
# Plot 2) other element types 
# plot_critic_over_timesteps(path, [1, 10, 20, 30, 40], 'Ta4', 'F47', 'Ta1', 'F24', 'Nb2', 'F42', 'Mo3', 'F33', plot_name="NbTaMoWV_other_elements")


output_dir = Path(__file__).parent

# NbTaMoW-H2O-FLiBe interface 
path = "/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoW/100"
plot_critic_over_timesteps(path, [1, 10, 20, 30, 40], 'W4', 'O1', 'Ta8', 'F3', output_dir=output_dir, plot_name="NbTaMoW-H2O")


# NbTaMoWV-H2O-FLiBe interface 
path = "/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoWV/100"
plot_critic_over_timesteps(path, [1, 10, 20, 30, 40], 'V2', 'O1', 'V15', 'F3', 'V3', 'F47', 'Nb2', output_dir=output_dir, plot_name="NbTaMoWV-H2O")

