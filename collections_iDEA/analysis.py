import numpy as np
import matplotlib.pyplot as plt
import iDEA
import ipywidgets as widgets
from IPython.display import display
from .Collections import CollectionOfStates
from .multiplets import *
import os


def states_density_comparison(states: CollectionOfStates, s: iDEA.system.System, analytic_prob_densities: list, widget=True):
    r"""
    Compare analytical probability densities to states from iDEA

    Args:

    | states: CollectionOfStates, Collection of states from iDEA
    | s: iDEA.system.System, System (only need the system's grid)
    | analytic_prob_densities: list, List of analytical probability densities indexed as analytic_space[k] for k excited state
    | widget=True, Display a widget plot of the states if True, or save all frames to a directory

    Note for two non-interacting states, the analytic prob density is the sum of the single body probability densities

    Returns:

    Either displays a widget of the frames of each excited state or saves them all to a directory

    """
    x = s.x
    orbital_space = []

    for i in range(len(states.state_classes)):
        n = iDEA.observables.density(s, states.state_classes[i])        
        orbital_space.append(n)

    # Ensure the directory for saving images exists
    output_dir = 'frames'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Define the function to plot the array
    def plot_array(k):
        plt.figure(figsize=(10, 6))
        plt.plot(x, orbital_space[k], "black")
        plt.plot(x, analytic_prob_densities[k], "b--")
        plt.title(f'State {k}')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True)
        plt.legend(["Approximate prob. density", "Analytical prob. density"])
        plt.savefig(os.path.join(output_dir, f'fk_{k:03d}.png'))
        plt.show()
    
    if widget:
        # Create a slider widget
        slider = widgets.IntSlider(value=0, min=0, max=len(orbital_space) - 1, step=1, description='k:')
        interactive_plot = widgets.interactive(plot_array, k=slider)
        
        # Display the interactive plot
        display(interactive_plot)
    
    else:
        for k in range(len(orbital_space)):
            plot_array(k)


def run_energy_comparison(analytic: CollectionOfStates, energies_list_1: list, energies_list_2: list, legend: list, break_first=True, zoom=None, tol=1e-12):

    r"""
    Run an energy comparison between two lists and test their multiplets against analytic multiplets

    Args:
    
    | analytic: CollectionOfStates, A collection of analytic results (needed to compare multiplets)
    | energies_list_1: list, First energy list to compare
    | energies_list_2: list, Second energy list to compare
    | legend: list, Legend array (needs to be an array of strings)
    | break_first: bool, Break at the first multiplet difference (check multiplet_methods), defaulted to True
    | zoom: list, Specify a specfic part of the graph to look at (needs to be in the form [x1, x2]), defaulted to None
    | tol: float, A tolerance for comparing the elements of the energy list to each other, defaulted to 1e-12

    Returns:

    Details of the energy comparison run
    """
    
    # plot graph
    plt.plot(np.round(energies_list_1, decimals=4), color="green", marker="x")
    plt.plot(np.round(energies_list_2, decimals=4), color="red", marker="x")
    plt.xlabel("State number")
    plt.ylabel("Energy of state")
    plt.grid()
    if zoom != None:
        plt.xlim(zoom[0], zoom[1])
        plt.title(f"Plot for states {zoom[0]} to {zoom[1]}")
    
    plt.title(f"Plot for states {0} to {len(energies_list_2)-1}")
    plt.legend(legend)

    print(f"Do list 1 and list 2 energies match up: {np.allclose(energies_list_1, energies_list_2)}")


    states_1 = CollectionOfStates(len(energies_list_1))
    states_1.energies = energies_list_1
    
    states_2 = CollectionOfStates(len(energies_list_2))
    states_2.energies = energies_list_2

    states_1.calculate_multiplets(tol)
    states_2.calculate_multiplets(tol)
    for i in range(len(states_1.multiplets)):
        print(f"From List 1: Multiplet: {states_1.multiplets[i]}, Energy: {states_1.multiplet_energies[i]}")
        print(f"From List 2: Multiplet: {states_2.multiplets[i]}, Energy: {states_2.multiplet_energies[i]}")
        print("--")
    
    print(f"List 1 Multiplet comparison: {analytic.check_expected_num_of_multiplets(states_1.multiplets, states_1.multiplet_energies, break_first)}")
    print(f"List 2 Multiplet compatison: {analytic.check_expected_num_of_multiplets(states_2.multiplets, states_2.multiplet_energies, break_first)}")