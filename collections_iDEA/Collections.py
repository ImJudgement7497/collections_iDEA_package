import numpy as np
import copy


class CollectionOfStates():
    r"""
    Collection of key information for non-interacting states

    | states: np.ndarray, Array of states, indexed as states[k], for k excited state
    | up_indices: np.ndarray, Array of the index of up occupied orbitals, indexed as up_indices[k]
    | down_indices: np.ndarray, Array of the index of down occupied orbitals, indexed as down_indices[k]
    | energies: np.ndarray, Array of energies of each state, indexed as energies[k]
    | multiplets: list, List of states that are multiplets
    | multiplets_energies: List, Energies of the corresponding multiplets
    | state_classes: list, List of class objects of each state, indexed as state_classes[k]
    """

    def __init__(self, max_k: int):
        self.states = np.zeros(max_k)
        self.up_indices = np.zeros(max_k)
        self.down_indices = np.zeros(max_k)
        self.energies = np.zeros(max_k)
        self.multiplets = []
        self.multiplet_energies = []
        self.state_classes = []
    
    def add_state_class(self, state_class):
        r"""
        Add a state class object to self.states_classes
        """
        self.state_classes.append(state_class)

    def add_energies(self, energies):
        r"""
        Add an array of energies to self.energies (note this shouldnt be used for analytic energy, use apply_energy_method)"""
        if not len(self.energies) == len(energies):
            raise ValueError(f"Lengths of array do not match. Expected {len(self.energies)}, got {len(energies)}")
        self.energies = energies
    
    def add_multiplet(self, multiplet):
        r"""
        Add a multiplet list to self.multiplets
        """
        self.multiplets.append(multiplet)
    
    def add_multiplet_energy(self, multiplet_energy):
        r"""
        Add a multiplet energy to self.multiplet_energies
        """
        self.multiplet_energies.append(multiplet_energy)
    
    def get_num_of_multiplets(self):
        r"""
        Show the number of multiplets in self.multiplets
        """
        return len(self.multiplets)
    
    def get_deg_of_multiplets(self):
        r"""
        Show the degenracy of each sub-list in self.multiplets
        """
        deg = []
        for multiplet in self.multiplets:
            deg.append(len(multiplet))
        return deg

    def calculate_multiplets(self, tol=1e-12):
        r"""
        Calculate the multiplets from self.energies and add the information to self.multiplets and self.multiplet_energies
        Args:
        
        | tol: float, Tolerance for testing whether the energies are equal, defaulted to 1e-12"""

        if len(self.energies) == 0:
            raise ValueError("No energies in array")
        j = 0
        while j < len(self.energies):
            multiplet = []

            # Go through the list and find the multiplets
            if j > 0 and np.abs(self.energies[j] - self.energies[j-1]) <= tol:

                self.add_multiplet_energy(self.energies[j])
                multiplet.append(j-1)
                multiplet.append(j)

                i = j + 1
                # continue through the list to find the multiplets of the same energy
                while i < len(self.energies):

                    if np.abs(self.energies[i] - self.energies[i-1]) <= tol:
                        multiplet.append(i)
                        i += 1
                    else:
                        self.add_multiplet(multiplet)
                        break
                j = i 
            else:
                j += 1
    
    def check_expected_num_of_multiplets(self, test_multiplets, test_energies, break_first=True):
        r"""
        Tests an array of multiplets against self.multiplets

        Args:

        | test_multiplets: list, Array of multiplets to test
        | test_energies: list, Array of multiplet energies to test
        | break_first: bool, if True, there will only be the first difference shown, defaulted to True

        Returns:

        Either True or a dictionary of differences between the test and self
        """
        
        if test_multiplets == self.multiplets:
            return True
        else:
            diff_indices = []
            diff_elms = {}
            test_copy = copy.deepcopy(test_multiplets)

            i = 0
            while i < min(len(self.multiplets), len(test_copy)):
                if not np.array_equal(self.multiplets[i], test_copy[i]):
                    diff_indices.append(i)
                    if break_first:
                        break

                    # This part needs further development

                    # Attempt to concatenate current and next element in test_copy
                    if i + 1 < len(test_copy):
                        conc = test_copy[i] + test_copy[i+1]
                        if np.array_equal(self.multiplets[i], conc):
                            # Update test_copy to reflect the concatenation
                            test_copy[i] = conc
                            # Remove the next element as it has been merged
                            del test_copy[i+1]
                            # No increment for i since we stay at the same index for the next check
                            continue
                i += 1

            j = 1
            
            for index in diff_indices:
                diff_elms[j] = (f"Got: {test_multiplets[index]} with energy: {test_energies[index]}", 
                                f"Expected: {self.multiplets[index]}", f"Expected energy: {self.multiplet_energies[index]}")
            
                j += 1
            
            return diff_elms