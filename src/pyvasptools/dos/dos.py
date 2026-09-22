import matplotlib.pyplot as plt

from py4vasp import Calculation
import numpy as np
import diptest

from src.pyvasptools.dataset import * 
from src.pyvasptools.compound import * 

from pathlib import Path



def plot_multi_overlaid_dos(*dos_datasets, spin='up', zoom_in=False, ylim=None, xlim=None, output_dir='.', output_name='DOS'):
    """
    Plot the total density of states (DOS) for multiple datasets on a single figure.

    This function overlays the DOS curves from multiple datasets for comparison.
    Optionally, a zoomed-in view of the DOS can also be generated.

    *dos_datasets : Dataset
        One or more Dataset objects containing DOS data to be plotted.
    spin : str, optional
        Spin channel to plot. Typically 'up' or 'down'. Default is 'up'.
    zoom_in : bool, optional
        If True, generates an additional zoomed-in plot. Default is False.
    ylim : tuple of float, optional
        Limits for the y-axis as (ymin, ymax). If None, limits are determined automatically.
    xlim : tuple of float, optional
        Limits for the x-axis as (xmin, xmax). If None, limits are determined automatically.
    output_dir : str or pathlib.Path, optional
        Directory where the plot(s) will be saved. Default is current directory ('.').
    output_name : str, optional
        Base filename for the saved plot(s). Default is 'DOS'.

    plot_multi_overlaid_dos: Dataset str bool (tupleof float) (tupleof float) (str or pathlib.Path) str -> None 

    Requires:
        - `ylim` and `xlim`, if provided, must be tuples of length 2.

    Examples:
        NbTaMoW = Dataset(
            path='/path/to/NbTaMoW/DOS',
            lc='black',
            label='NbTaMoW'
        )
        NbTaMoWV = Dataset(
            path='/path/to/NbTaMoWV/DOS',
            lc='purple',
            label='NbTaMoWV'
        )
        plot_multi_overlaid_dos(
            NbTaMoW,
            NbTaMoWV,
            spin='up',
            zoom_in=True,
            output_dir='.',
            output_name='DOS'
        )
    """

    fig, axes = plt.subplots(1, 1, dpi=150, figsize=(14, 12))

    for d in dos_datasets:
        energies, dos, E_fermi = d.total_DOS(spin=spin)

        # Plot the data with desired plot parameters 
        axes.plot(energies, dos, linewidth=1.5, linestyle=d.ls, color=d.lc, label=d.label)

        if d.label is None:
            axes.axvline(x=E_fermi, color=d.lc, linewidth=1.5, linestyle='--', label=f'$E_F$={E_fermi:.3f} eV')
        else:
            axes.axvline(x=E_fermi, color=d.lc, linewidth=1.5, linestyle='--', label=f'$E_F$={E_fermi:.3f} eV')

    axes.set_ylabel('DOS (1/eV)', fontsize=18, fontweight='bold')
    axes.set_xlabel('Energy (eV)', fontsize=18, fontweight='bold')
    axes.tick_params(axis='both', labelsize=16)  # Both x and y ticks

    # Other optional plot parameters and descriptors 
    if ylim is not None:
        axes.set_ylim(ylim[0], ylim[1])
    if xlim is not None:
        axes.set_xlim(xlim[0], xlim[1])
    
    if zoom_in:
        axes.set_xlim(-20, 10)

    axes.legend(fontsize=16, loc='upper left')

    output_path = Path(output_dir) / f"{output_name}.png"
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.show()



def pdos_orbital(axes, elements_to_plot, energies, calc, d_orbitals, linecolor, dip_dataset, E_fermi=None, label=None):
    """
    Plot the partial density of states (PDOS) for selected elements and orbitals.

    This function plots orbital-resolved PDOS curves on the provided axes for each
    element in `elements_to_plot` and each orbital specified in `d_orbitals`.

    Parameters
    ----------
    axes : matplotlib.axes.Axes
        Matplotlib axes object on which the PDOS will be plotted.
    elements_to_plot : list of str
        List of element symbols for which the PDOS will be computed and plotted.
    energies : array-like
        Energy values in eV (typically obtained from py4vasp).
    calc : object
        DOS calculation object (e.g., from py4vasp) used to extract PDOS data.
    d_orbitals : dict of {str : str}
        Dictionary mapping orbital names (e.g., 'd_xy', 'd_z2') to matplotlib
        linestyles (e.g., '-', '--') for plotting.
    linecolor : str
        Color used for plotting the PDOS curves for a given element.
    dip_dataset : array-like
        Array of shape (3, n_elements) containing orbital-projected DOS data
        corresponding to the selected elements.
    E_fermi : float, optional
        Fermi level in eV. If provided, energies may be shifted relative to it.
        Default is None.
    label : str, optional
        Label for the plotted data (used in legends). Default is None.

    Returns
    -------
    None

    Notes
    -----
    - Each element–orbital combination is plotted with a distinct linestyle
      as defined in `d_orbitals`.
    - All curves are plotted on the same axes for comparison.
    """
    orbitals = list(d_orbitals.keys())   

    for i in range(len(orbitals)):
        current_orbital = orbitals[i]
        s = ",".join(elements_to_plot)
        _dict = calc.dos.to_dict(f"{current_orbital}({s})")

        for ii in range(len(elements_to_plot)):
            element = elements_to_plot[ii]
            plot_no = ii + 1 

            if (current_orbital == 'd') and (periodic_table.index(element) < 20):
                continue

            element_spin_up = _dict[f'{element}_{current_orbital}_up']

            if current_orbital == 'd':
                dip, pval = diptest.diptest(element_spin_up)
                dip_dataset[0][ii] = element
                dip_dataset[1][ii] = dip
                dip_dataset[2][ii] = pval
            
            axes[plot_no].plot(energies, element_spin_up, color=linecolor, linewidth=18, linestyle=d_orbitals[current_orbital], label=f'{current_orbital} {label}')


            if i == len(orbitals)-1:
                axes[plot_no].axvline(x=E_fermi, color=linecolor, linewidth=18, linestyle='--')

                # Add text at a specific point (without an arrow)
                axes[plot_no].text(0.80, 0.75, element, transform=axes[plot_no].transAxes, fontfamily='sans-serif', fontname='Helvetica', fontsize=180, color='black') 
                axes[plot_no].tick_params(axis='x', which='major', direction='out', length=33, width=10)  # Show ticks
                axes[plot_no].tick_params(labelbottom=False)  # Hide x tick labels
                axes[plot_no].legend()

                    

def plot_pdos_modified(elements, d_orbitals, *dos_datasets, **kwargs):
    """
    Plots the total and partial DOS for multiple Datasets on the same figure.

    The Datasets to be plotted are provided in *args. It is recommended to have a
    maximum of 2 Datasets (*args) to prevent plot overload. In addition to the
    total DOS plotted in the first row, the pDOS is plotted separately for each of
    the elements in d_elements (keys) which has its own subplot numbered according
    to the corresponding values.

    elements : list of str
        A list of elements for which you wish to plot orbital-resolved PDOS curves.
    d_orbitals : dict of str to str
        Orbital names as keys and the corresponding matplotlib linestyles as values.
    *dos_datasets : Dataset
        Dataset objects where a Dataset must contain a VASP density of states calculation.

    plot_pdos_modified: list[str] dict[str][str] Dataset -> None

    Examples:
        NbTaMoW = Dataset(path="/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoW/100_v2/30ps/DOS", lc="blue", ls="solid", label='')
        NbTaMoWV = Dataset(path="/Users/agneskatai/cluster_data/Narval_test/H2O/NbTaMoWV/100_v2/30ps/DOS", lc="red", ls="solid", label='V')

        plot_pdos_modified(elements, {'d': 'solid', 'p': 'dashed', 's': 'dotted'}, NbTaMoW, NbTaMoWV, x_lim=(-10, 10), y_lim=(((-5, 100),) + ((-1, 20),) * 4 + ((-5, 50),) + ((-1, 5),)), labels=("", "- FLiBe"), plot_name='NbTaMoW_vs_NbTaMoWV')
    """
    y_lim = kwargs.get("y_lim")         # tuple of tuples 
    x_lim = kwargs.get("x_lim")         # tuple of tuples 
    dataset_labels = kwargs.get("labels", tuple(list("" for i in range(1, len(dos_datasets)+1))))       # tuple of dataset label 
    plot_name = kwargs.get("plot_name", "pDOS") 
    path_to_fig = kwargs.get("path_to_fig", ".")  


    plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica'],
    'font.size': 64,
    'xtick.labelsize': 92,
    'ytick.labelsize': 92,
    'axes.labelsize': 64,
    'legend.fontsize': 61,      # use 67 for FLiBe and 61 for FLiBe + H2O      
    'legend.loc': 'upper left'
})

    num_elements = len(elements)
    num_plots = num_elements + 1

    fig, axes = plt.subplots(
        nrows=num_plots,
        ncols=1,
        figsize=(48, 80),
        sharex=True,
    )
    fig.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.05, hspace=0.08)

    dip_results = np.empty((len(dos_datasets), 3, num_elements), dtype=object)

    for i in range(len(dos_datasets)):      # each argument in *args is a dataset object for which a DOS calculation can be performed 
        dataset = dos_datasets[i]
        dip_dataset = np.empty((3, num_elements), dtype=object)

        component_elements = dataset.get_elements_partial_dos()
        energies, total_dos, E_fermi = dataset.total_DOS()

        elements_to_plot = []
        
        for e in elements:
            if e in component_elements:
                elements_to_plot.append(e)
                
        print(f'The elements that are available to plot for {dataset.label} is {elements_to_plot}')

        if elements_to_plot == []:
            continue

        else:
            axes[0].plot(energies, total_dos, color=dataset.lc, linewidth=18, linestyle=dataset.ls, label=f"Total {dataset_labels[i]}")
            axes[0].axvline(x=E_fermi, color=dataset.lc, linewidth=18, linestyle='--', label=f'$E_F$={E_fermi:.3f} eV')
            axes[0].text(0.80, 0.75, f'Total', transform=axes[0].transAxes, fontfamily='sans-serif', fontname='Helvetica', fontsize=180, color='black')
            axes[0].tick_params(axis='x', which='major', direction='out', length=33, width=10)  # Show ticks
            axes[0].tick_params(labelbottom=False)  # Hide x tick labels
            axes[0].legend()

            calc = Calculation.from_path(dataset.path)
            pdos_orbital(axes, elements_to_plot, energies, calc, d_orbitals, dataset.lc, dip_dataset, E_fermi=E_fermi, label=dataset_labels[i])
            dip_results[i] = dip_dataset


    [ax.set_autoscale_on(False) for ax in axes]

    if y_lim != None:
        for i in range(len(y_lim)):
            if x_lim != None:
                axes[i].set_xlim(x_lim)
            axes[i].set_ylim(y_lim[i])

    axes[-1].set_xlabel("Energy (eV)", fontsize=122)
    axes[-1].tick_params(axis='x', which='major', direction='out', length=33, width=10)  # Show ticks
    axes[-1].tick_params(labelbottom=True)
    fig.supylabel("Density of States (1/eV)", fontsize=122)

    fig.savefig(path_to_fig, dpi=300, bbox_inches='tight')

    return dip_results

