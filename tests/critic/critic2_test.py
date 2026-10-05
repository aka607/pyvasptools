from pathlib import Path


from pyvasptools.critic2.critic2 import plot_critic_over_timesteps


current_dir = Path(__file__).parent
root_dir = current_dir.parents[1]

# NbTaMoW-H2O-FLiBe interface 
path = root_dir / 'sample_data/NbTaMoW-FLiBe'
plot_critic_over_timesteps(path, [10, 20], 'Ta20', 'F3', 'Ta8', 'F46', 'W2', 'F6', 'Nb20', 'F14', plot_path=current_dir / "NbTaMoW-FLiBe")

