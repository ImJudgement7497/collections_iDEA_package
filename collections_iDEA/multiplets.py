import numpy as np
from .Collections import CollectionOfStates
import itertools
import pickle
import os
import time
import iDEA

def create_indices(max_level: int):
    r"""
    Creates the indices of occupation for a two particle system and saves it to a file
    
    Args:
    
    | max_level: int, max number of indices (note the number of states tht can be accessed is max_level^2)
    
    Returns:
    
    A pickle file containg the indices (need to apply an energy method to get ordred indices)"""
    file_path = f"indices_up_to_{max_level}.pkl"
    text_path = "max_level.txt"

    # Check if the pickle file for the current max_level exists
    if os.path.exists(file_path):
        print(f"File {file_path} exists")
        with open(file_path, "rb") as file:
            return pickle.load(file)
    # Check if the max_level text file exists
    elif os.path.exists(text_path):
        with open(text_path, "r") as file:
            prev_max_level = int(file.read())
        
        # If current max_level is greater than the previous max level, delete the previous file
        if max_level > prev_max_level:
            prev_file_path = f"indices_up_to_{prev_max_level}.pkl"
            if os.path.exists(prev_file_path):
                print(f"Deleting old file {prev_file_path}")
                os.remove(prev_file_path)
        # If current max_level is less than or equal to the previous max level, use the previous indices
        elif max_level <= prev_max_level:
            prev_file_path = f"indices_up_to_{prev_max_level}.pkl"
            if os.path.exists(prev_file_path):
                print(f"Using indices_up_to_{prev_max_level}.pkl")
                with open(prev_file_path, "rb") as file:
                    return pickle.load(file)

    # If neither file exists, create a new indices file
    print(f"The file {file_path} does not exist. Creating it now")
    index = list(itertools.combinations(range(max_level), 1))
    indices = list(itertools.product(index, index))

    with open(file_path, "wb") as file:
        pickle.dump(indices, file)

    with open(text_path, "w") as file:
        file.write(f"{max_level}")
    
    return indices


def apply_energy_method(energy_method, s: iDEA.system.System, max_k: int, states=None, max_index=20, second_mask=True) -> CollectionOfStates:
    r"""
    Calculate the energy of non-interacting states and the occupation of each state

    Args:

    | energy_method: function, The analytic energy of state k (can only depend on the index)
    | s: iDEA.system.System, The system (only needed for up_count, down_count)
    | max_k: int, Maximum state k considered
    | states: CollectionOfStates, A pre-defined collection (defaulted to None as function will create one)
    | max_index: int, Maximmum index for indices list (can access upto (max_indes)^2 states), defaulted to 20
    | second_mask: bool, Apply second mask to remove reverse indices like [1, 0], [0, 1] (one of these will be removed). See Possible Issues in README.md

    Returns:

    | states: CollectionOfStates
    """
    start = time.perf_counter()

    if (max_index)**2 < max_k:
        raise AssertionError(f"Only {max_index**2} states will be accessed, please decrease the number of states from {max_k} or increase the max index {max_index}")

    if states == None:
        states = CollectionOfStates(max_k)
    
    indices = create_indices(max_index)
    indices = np.array(indices).reshape(-1, 2)  

    if s.up_count == 2 or s.down_count == 2:
        mask_1 = indices[:, 0] != indices[:, 1]
        indices = indices[mask_1]

        if second_mask:
            mask_2 = np.ones(len(indices), dtype=bool)

            seen_pairs = set()

            for i, pair in enumerate(indices):
                sorted_pair = tuple(sorted(pair))
                if sorted_pair in seen_pairs:
                    mask_2[i] = False
                else:
                    seen_pairs.add(sorted_pair)
            indices = indices[mask_2]

    
    # Extract up and down indices
    up_indices = indices[:, 0]
    down_indices = indices[:, 1]
    
    # Compute energies
    up_energies = np.vectorize(energy_method)(up_indices)
    down_energies = np.vectorize(energy_method)(down_indices)
    energies = up_energies + down_energies
    
    # Sort and select top k energies
    energy_indices = np.argsort(energies, kind='stable')[:max_k]
    
    states.states = np.arange(max_k)
    states.up_indices = up_indices[energy_indices]
    states.down_indices = down_indices[energy_indices]
    states.energies = energies[energy_indices]

    end = time.perf_counter()
    print(f"Elapsed Time = {end-start}")

    return states

# def calculate_multiplets(states: CollectionOfStates, tol=1e-12):

#     states.multiplets = []

#     energies_int = states.energies
#     j = 0

#     while j < len(energies_int):
#         multiplet = []
#         if j > 0 and np.abs(energies_int[j] - energies_int[j-1]) <= tol:
#             # states.addMultiplet(j-1)
#             # states.addMultiplet(j)
#             states.add_multiplet_energy(energies_int[j])
#             multiplet.append(j-1)
#             multiplet.append(j)
#             i = j + 1
#             while i < len(energies_int):
#                 if np.abs(energies_int[i] - energies_int[i-1]) <= tol:
#                     # states.addMultiplet(i)
#                     multiplet.append(i)
#                     i += 1
#                 else:
#                     states.add_multiplet(multiplet)
#                     break
#             j = i 
#         else:
#             j += 1
    
#     return states