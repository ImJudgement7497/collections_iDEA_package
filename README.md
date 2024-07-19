# collections_iDEA_package

To install, first fork this repository, then clone then run `pip install .` in the directory.

# Motivation

During the course of my summer project I studied how multiplets are formed within the [iDEA software](https://github.com/iDEA-org/iDEA). The analysis that I needed to do when calling `iDEA.methods.non_interacting.solve()` to solve non-interacting problems were slowed down due to how iDEA utilises its `get_occupation` function. When solving two body non interacting problems, the indexing of occupied orbitals are not system dependent i.e. for a `ud` configuration in an infinte square well the state indexed at [0, 0] is a valid state. This is the same for an `ud` configuration in the quantum harmonic oscillator. The energy of each single-body orbital will be system dependent.

Thus instead of creating this indice list for every excited state (which gets more computationally expensive the higher excited state), `collections_iDEA.create_indices()` will create the list once for a `max_index` and saves it to file. This file is then utilised in other methods in the package to get the analysis I needed during the project. Doing this reduced the time of getting key information significantly.

# Features

- A central place to store many states at once.
- Get key results like analytic energy and multiplets quickly for two-body analytical systems.
- Provides easy to use functions to compare energies and densities.
- Provides analytical wavefunctions for quantum harmonic oscillator and particle in a box.


# Tutorial

To find analytically where the multiplets of a two body quantum harmonic oscillator system up to the 50th excited state:
```python

import collections_iDEA
import numpy as np
import iDEA

# Initialize the system
points = 231
l = 10
x = np.linspace(-l, l, points)
omega = 0.3275
v_ext = 0.5 * omega**2 * (x**2)
v_int = np.zeros([len(x), len(x)])
qho_double = iDEA.system.System(x, v_ext, v_int, electrons="ud")

def qho_energy(index):
    return omega*(index+0.5)

analytic_collection = collections_iDEA.multiplets.apply_energy_method(qho_energy, qho_double, 50)
analytic_collection.calculate_multiplets()
print(analytic_collection.multiplets)
```

# Possible issues

- It is unclear if iDEA gives states that are distingushable or indistingushable for the `interacting` method on systems such as `uu`. 
- Due to the nature of `np.argsort()`, the indices may not exactly match iDEA's outputs when considering multiplets, but the correct indices will still be given, just in a slightly different order to iDEA.



# Possible developments

~~Change `apply_energy_method` so that you can pass it a CollectionOfStates, but by default it gives you one.~~
~~Change the defintionS of CollectionOFStates so it can be used as a general collection, not just analytic.~~
Change `create_indices()` so that it will work for a more than two body system