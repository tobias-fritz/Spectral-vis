#===============================================================================================
# Script for applying gaussian broadening to a dataset of VEE and osc. strength
# Date: 01.03.2022
# Author: Tobias Fritz
# Summary:
# Accepts an array of excitation energy and corresponding osc. strength and applies gaussian 
# line-broadening to obtain a spectrum
#===============================================================================================

import numpy as np

def gaussian_broadening(energy , oscillator, sigma , x_var):
    ''' apply gaussian line broadening to a given set of excitation energies and oscillator strengths
    parameters:
      energy : single or list of excitation energies from escf computation
      oscillator :single or list of oscillator strength from escf computation
      sigma: broadening applied to the curve
      x_var : x-axis of absorption plot (list of energy values)
    
    returns: 
      spectrum : list of extinction values corrsponding to varaible / x-axis values
    '''
    
    spectrum = []
    
    # iterate over x-axis
    for e_i in x_var:
       
        tot = 0
        
        # iterate over all energies and corresponding oscillator strengths
        for e_j, osc in zip(list(energy),list(oscillator)):
          
            tot += osc * np.exp( -(( ( (e_j - e_i) / sigma )**2) ))
            
        spectrum.append(tot)
        
    return spectrum
