#===============================================================================================
# Unit conversion between eV and nm
# Date: 01.03.2022
# Author: Tobias Fritz
#===============================================================================================

from scipy import constants as const

#===============================================================================================

h = const.h         
c = const.c         
J_eV = const.e 


def eV_to_nm(E_eV):
    ''' accept wavelength in nm and returns energy in eV'''
    return ((h*c) / (E_eV * J_eV) ) * 10**9

def nm_to_eV(wl_nm):
    ''' accepts energy in eV and returns wavelength'''
    return ((h*c) / (wl_nm * J_eV)) * 10**9
