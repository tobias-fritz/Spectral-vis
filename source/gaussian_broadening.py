# ===============================================================================================
# Script for applying gaussian broadening to a dataset of VEE and osc. strength
# Date: 01.03.2022
# Author: Tobias Fritz
# Summary:
# Accepts an array of excitation energy and corresponding osc. strength and applies gaussian 
# line-broadening to obtain a spectrum
# ===============================================================================================
import math
import csv
import numpy as np
import matplotlib.pyplot as plt
from typing import Union

h = 6.62607015e-34  # Planck constant in J·s
c = 299792458       # Speed of light in m/s
J_eV = 1.602176634e-19  # Joules per eV

def nm_to_eV(l_nm: list) -> list:
    '''Accepts energy in eV and returns wavelength'''
    return ((h * c) / (np.array(l_nm) * J_eV)) * 10**9

def eV_to_nm(E_eV: list) -> list:
    '''Accept wavelength in nm and returns energy in eV'''
    return ((h * c) / (np.array(E_eV) * J_eV)) * 10**9

class Spectrum:
    """Class to calculate and plot the spectrum of a given data

    Attributes:
        fname (str): path to the csv file containing the excitation energies and oscillator strengths
        sigma (float): broadening applied to the curve
        OSC (list): list of list containing all pairs of uneven columns
        E (list): list of list containing all pairs of even columns
        energy_unit (str): unit of the excitation energies, either 'eV' or 'nm'
        spectrum_eV (list): spectrum in eV
        spectrum_nm (list): spectrum in nm
        range_eV (list): range of energy values in eV
        range_nm (list): range of wavelength values in nm
    """

    h = 6.62607015e-34  # Planck constant in J·s
    c = 299792458       # Speed of light in m/s
    J_eV = 1.602176634e-19  # Joules per eV

    def __init__(self, fname: str):
        """Initialize the Spectrum class
        
        Args:
            fname (str): path to the csv file containing the excitation energies and oscillator strengths
        """
        self.fname = fname
        self.sigma = None
        
        with open(fname, 'r') as f:
            # read the csv file, skip the header
            data = list(csv.reader(f))[1:]
        # extract the data

        # list of list containing all pairs of uneven columns
        self.OSC = [list(map(float, row[::2])) for row in data]
        # list of list containing all pairs of even columns
        self.E = [list(map(float, row[1::2])) for row in data]
        
        self.energy_unit = 'eV' if self.E[0][0] < 10 else 'nm'

        self.spectrum_eV = None
        self.spectrum_nm = None
        self.range_eV = None
        self.range_nm = None

    def __repr__(self):
        return f'Spectrum(fname={self.fname}, sigma={self.sigma})'
    
    def __str__(self):
        return f'Spectrum object with data from {self.fname}'

    def calculate_spectrum(self, unit: str, 
                           range_eV: list = np.linspace(1, 5, num=1000, endpoint=True),
                           range_nm: list = np.linspace(200, 800, num=1000, endpoint=True), 
                           sigma: float = 0.2) -> None:
        """Calculate the spectrum of the given data
        
        Args:
            unit (str): unit of the spectrum, either 'eV' or 'nm'
            range_eV (list): range of energy values in eV
            range_nm (list): range of wavelength values in nm
            sigma (float): broadening applied to the curve

        Returns:
            None
        """
        assert unit in ['eV', 'nm'], 'unit must be either "eV" or "nm"'
        
        if not self.sigma:
          self.sigma = sigma

        print(f'Calculating spectrum in {unit} (sigma = {self.sigma})')

        self.range_eV = range_eV
        self.range_nm = range_nm

        if self.energy_unit == 'eV' and unit == 'eV':
            self.spectrum_eV = np.mean([self.gaussian_broadening(E, OSC, self.sigma, range_eV) 
                                        for E, OSC in zip(self.E, self.OSC)], axis=0)
        elif self.energy_unit == 'nm' and unit == 'eV':
            self.spectrum_eV = np.mean([self.gaussian_broadening(self._nm_to_eV(E), OSC, self.sigma, range_eV) 
                                        for E, OSC in zip(self.E, self.OSC)], axis=0)
        elif self.energy_unit == 'nm' and unit == 'nm':
            self.spectrum_nm = np.mean([self.gaussian_broadening_wavelength(E, OSC, self.sigma, range_nm) 
                                        for E, OSC in zip(self.E, self.OSC)], axis=0)
        else:
            self.spectrum_nm = np.mean([self.gaussian_broadening(self._eV_to_nm(E), OSC, self.sigma, range_nm) 
                                        for E, OSC in zip(self.E, self.OSC)], axis=0)
    
    def plot_spectrum(self, unit: str = None, sigma: float=None) -> None:
        """Plot the spectrum of the given data
        
        Args:
            unit (str): unit of the spectrum, either 'eV' or 'nm'

        Returns:
            None
        """
        if sigma:
            self.sigma = sigma

        plt.figure(figsize=(6, 2.4))
        if unit is not None:
            assert unit in ['eV', 'nm'], 'unit must be either "eV" or "nm"'
            # check if the spectrum in unit is already calculated
            if unit == 'eV' and self.spectrum_eV is None:
                self.calculate_spectrum(unit)
            elif unit == 'nm' and self.spectrum_nm is None:
                self.calculate_spectrum(unit)
        else:
            # check if the spectrum in eV is already calculated
            if self.spectrum_eV is None and self.spectrum_nm is None:
                raise ValueError('Please calculate the spectrum first or specify the unit here')
            elif self.spectrum_eV is not None and self.spectrum_nm is not None:
                raise ValueError('Please specify the unit to plot the spectrum')
            elif self.spectrum_eV is not None and self.spectrum_nm is None:
                unit = 'eV'
            else:
                unit = 'nm'
        if unit == 'eV':
            plt.plot(self.range_eV, self.spectrum_eV, label='Broadened spectrum', color='k')
            plt.xlabel('Energy [eV]')
            plt.xlim(self.range_eV[0], self.range_eV[-1])
            plt.ylim(0, self._round_up_to_nice_number(max(self.spectrum_eV)))
            plt.title(f'$\sigma$ = {self.sigma}, max energy = {self.range_eV[np.argmax(self.spectrum_eV)]:.2f} eV')
        else:
            plt.plot(self.range_nm, self.spectrum_nm, label='Broadened spectrum', color='k')
            plt.xlabel('Wavelength [nm]')
            plt.xlim(self.range_nm[0], self.range_nm[-1])
            plt.ylim(0, self._round_up_to_nice_number(max(self.spectrum_nm)))
            plt.title(f'$\sigma$ = {self.sigma}, lambda max = {self.range_nm[np.argmax(self.spectrum_nm)]:.1f} nm')
        plt.ylabel('Intensity [a.u.]')
        plt.grid()
        plt.tight_layout()
        plt.show()

    def _round_up_to_nice_number(self, value: Union[int, float], base: int = 10) -> Union[int, float]:
        '''Round up a given value to the nearest nice number'''
        if value <= base:
            return math.ceil(value)
        else:
            return base * self._round_up_to_nice_number(value / base, base)
    
    def _eV_to_nm(self, E_eV):
        '''Accept wavelength in nm and returns energy in eV'''
        return ((self.h * self.c) / (np.array(E_eV) * self.J_eV)) * 10**9
    
    def _nm_to_eV(self, wl_nm):
        '''Accepts energy in eV and returns wavelength'''
        return ((self.h * self.c) / (np.array(wl_nm) * self.J_eV)) * 10**9

    @staticmethod
    def help():
        """Display the help information for the Spectrum class."""
        help(Spectrum)

    @staticmethod
    def gaussian_broadening(energy: list, oscillator: list, sigma: float, x_var: list) -> list:
        '''Apply gaussian line broadening to a given set of excitation energies and oscillator strengths
        
        Args:
            energy : single or list of excitation energies from escf computation
            oscillator : single or list of oscillator strength from escf computation
            sigma: broadening applied to the curve
            x_var : x-axis of absorption plot (list of energy values)
        
        Returns: 
            spectrum : list of extinction values corresponding to variable / x-axis values
        '''
        spectrum = []
        
        # iterate over x-axis
        for e_i in x_var:
            tot = 0
            
            # iterate over all energies and corresponding oscillator strengths
            for e_j, osc in zip(list(energy), list(oscillator)):
                tot += osc * math.exp(-(((e_j - e_i) / sigma) ** 2))
                
            spectrum.append(tot)
            
        return spectrum
    
    @staticmethod
    def gaussian_broadening_wavelength(wavelength: list, oscillator: list, sigma: float, x_var: list) -> list:
        '''Apply gaussian line broadening to a given set of excitation wavelengths and oscillator strengths
        
        Args:
            wavelength : single or list of excitation wavelengths from escf computation
            oscillator : single or list of oscillator strength from escf computation
            sigma: broadening applied to the curve
            x_var : x-axis of absorption plot (list of wavelength values)
        
        Returns: 
            spectrum : list of extinction values corresponding to variable / x-axis values
        '''
        spectrum = []
        
        # iterate over x-axis
        for e_i in x_var:
            tot = 0

            # iterate over all energies and corresponding oscillator strengths
            for e_j, os in zip(wavelength, oscillator):
                tot += (13.06025740) * (os / (1 /eV_to_nm(sigma))) * math.exp(
                    -(((1 / e_i) - (1 / e_j)) / (1 / eV_to_nm(sigma))) ** 2)
            
            spectrum.append(tot)

        return spectrum