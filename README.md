# pyvasptools

Provides Python scripts for analyzing the:

- **Radial distribution function (RDF)** — calculated directly from VASP structure files (`POSCAR`)
- **Density of states (DOS)** — calculated directly from VASP output files (`vaspout.h5`)
- **Crystal orbital Hamilton population analysis** — analyzed beforehand with LOBSTER
- **Electron localization function partitioning** — analyzed beforehand with critic2

## Installation

Requires Python ≥ 3.10.14.

1. Create a Python environment to isolate the package dependencies:

   ```bash
   python3 -m venv ~/envs/pyvasp_tools
   ```

2. Activate the Python environment:

   ```bash
   source ~/envs/pyvasp_tools/bin/activate
   ```

3. Install the package from PyPI:

   ```bash
   pip install pyvasptools
   ```

   Or install from a local clone (for development):

   ```bash
   cd /path/to/pyvasptools/
   pip install .
   ```

## Sample data

The example VASP outputs used by the tests and demos are too large for git and
are hosted on Zenodo: https://doi.org/10.5281/zenodo.22182966

Download the archive and unzip its contents into the repository root so that a
`sample_data/` folder sits next to this README:

```bash
cd /path/to/pyvasptools/
# download sample_data.zip from the Zenodo record above, then:
unzip sample_data.zip
```
