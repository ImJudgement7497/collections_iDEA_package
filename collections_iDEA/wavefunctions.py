import numpy as np
import scipy.special as sp

def qho_wave_function(index: int, omega: float, x: np.ndarray):
    r"""
    Returns the quantum harmonic oscialltor wavefunction for a given index
    
    Args
    
    | index: int, Index of excited state (index=0 being the ground state)
    | omega: float, Value of omega in the QHO potential
    | x: np.ndarray, Array of x-values to apply the wave function onto
    
    Returns
    
    wave_func: np.ndarray, Array of wavefunction values
    """
    exponent = -(omega * (x**2)) / (2)
    wave_func = np.sqrt(1 / ((2**index) * sp.factorial(index))) * pow((omega/np.pi), 0.25) * np.exp(exponent) * sp.eval_hermite(index, np.sqrt(omega)*x)

    return wave_func

def pib_wave_function_1(index: int, l: float, x: np.ndarray):
    r"""
    Returns the particle in a box wavefunction for a given index and length 
    
    Args
    
    | index: int, Index of excited state (index=0 being the ground state)
    | l: float, Length of the system (from 0)
    | x: np.ndarray, Array of x-values to apply the wave function onto
    
    Returns
    
    wave_func: np.ndarray, Array of wavefunction values
    """
    if x[0] != 0:
        raise ValueError(f"This wavefunction is for a box at 0 to L, not at {x[0]}")
    return np.sqrt(2/l) * np.sin((np.pi) * x * (n+1) / l)