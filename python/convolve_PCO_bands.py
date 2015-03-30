''' ########################### OVERVIEW ########################### '''
'''
 Created 2015-03-02 by Will Bowman. This script convolves the density of states
 functions for the O-2p valence band with the Pr and Ce 4f conduction bands to 
 predict the shape of the interband state
'''

''' ########################### IMPORT MODULES ########################### '''
import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import wills_functions as wf
import csv, imp, os

##


''' ########################### USER-DEFINED ########################### '''
O2p_min_energy, O2p_max_energy, O2p_max = -4, 0, 4 # eV, eV, arb. units [1]
# O2p_min_energy, O2p_max_energy, O2p_max = -.1, 0, 50 # eV, eV, arb. units [1]
Pr4f_min_energy, Pr4f_max_energy, Pr4f_max = 1.5, 2, 2
Ce4f_min_energy, Ce4f_max_energy, Ce4f_max = 2, 4.5, 20
Ce5d_min_energy, Ce5d_max_energy, Ce5d_max = 5, 7.5, 4
energy_axis = np.linspace( -10, 10, 200 )
energy_min, energy_max = -10, 10 # eV


''' ########################### FUNCTIONS ########################### '''
# y is an array which will be manipulated via np.piecewise conditions. x_mix and max
# are the bounds of the step function. max_value is the value of the step
def bounded_step_function( y, x_min, x_max, max_value ):
    function = np.piecewise( y,
        [ ( y >= x_min ) & ( y <= x_max ) ], [ max_value ] )
    return function

def bounded_lorentzian_function( x, x_min, x_max, max_value ):
    center_position = ( x_max - x_min ) / 2
    # fwhm = center_position
    lorentzian = wf.lorentzianate( x, center_position )
    return lorentzian

def bounded_gaussian_function( x, x_min, x_max, max_value ):
    fwhm = ( x_max - x_min ) / 2
    center = x_max - fwhm
    std_dev = fwhm / 5
    g = 1 / ( std_dev * np.sqrt( 2 * np.pi ) ) * np.exp( -( x - center ) ** 2 / ( 2 * std_dev ** 2 ) )
    gg = g / np.max( g ) * max_value # scale gaussain to max_value 
    return gg

# closes all open figures
def close_all():
    pl.close( 'all' )
   
    
''' ########################### MAIN SCRIPT ########################### '''
# calculate step functions
O2p_step = bounded_step_function( energy_axis, O2p_min_energy, O2p_max_energy, O2p_max )
Pr4f_step = bounded_step_function( energy_axis, Pr4f_min_energy, Pr4f_max_energy, Pr4f_max )
Ce4f_step = bounded_step_function( energy_axis, Ce4f_min_energy, Ce4f_max_energy, Ce4f_max )
Ce5d_step = bounded_step_function( energy_axis, Ce5d_min_energy, Ce5d_max_energy, Ce5d_max )

# convole step functions
O2p_Pr4f_convolve_step = np.convolve( O2p_step, Pr4f_step, mode = 'same' )
O2p_Ce4f_convolve_step = np.convolve( O2p_step, Ce4f_step, mode = 'same' )
O2p_Ce5d_convolve_step = np.convolve( O2p_step, Ce5d_step, mode = 'same' )

# calculate density of states functions
O2p_DOS = O2p_step # good enough approximation for now
Pr4f_DOS = bounded_gaussian_function( energy_axis, Pr4f_min_energy, Pr4f_max_energy, Pr4f_max )
Ce4f_DOS = bounded_gaussian_function( energy_axis, Ce4f_min_energy, Ce4f_max_energy, Ce4f_max )
Ce5d_DOS = Ce5d_step
# Ce5d_DOS = bounded_gaussian_function( energy_axis, Ce5d_min_energy, Ce5d_max_energy, Ce5d_max )

# convolve density of states functions
O2p_Pr4f_convolve_DOS = np.convolve( O2p_DOS, Pr4f_DOS, mode = 'same' )
O2p_Ce4f_convolve_DOS = np.convolve( O2p_DOS, Ce4f_DOS, mode = 'same' )
O2p_Ce5d_convolve_DOS = np.convolve( O2p_DOS, Ce5d_DOS, mode = 'same' )
summed_convolve_DOS = O2p_Pr4f_convolve_DOS + O2p_Ce4f_convolve_DOS + O2p_Ce5d_convolve_DOS
energy_axis_convolve = np.linspace( energy_min, energy_max, np.size( O2p_Ce4f_convolve_DOS ) )


# plot stuff
close_all() # close open plots

pl.figure( figsize = ( wf.mm2in( 200 ), wf.mm2in( 100 ) ) ) # create new figure
pl.subplot( 1, 2, 1 ) # subplot for step functions
pl.plot( energy_axis, Pr4f_step ) # plot step functions
pl.plot( energy_axis, Ce4f_step )
pl.plot( energy_axis, Ce5d_step )
pl.plot( energy_axis, O2p_step )

pl.subplot( 1, 2, 2 ) # subplot for step functions convolved step function
pl.plot( energy_axis, O2p_Pr4f_convolve_step )
pl.plot( energy_axis, O2p_Ce4f_convolve_step )
pl.plot( energy_axis, O2p_Ce5d_convolve_step )

pl.figure( figsize = ( wf.mm2in( 200 ), wf.mm2in( 100 ) ) ) # create new figure
pl.subplot( 1, 2, 1 ) # subplot for density of states functions
pl.plot( energy_axis, Pr4f_DOS ) # plot density of states functions
pl.plot( energy_axis, Ce4f_DOS )
pl.plot( energy_axis, Ce5d_DOS )
pl.plot( energy_axis, O2p_DOS )

pl.subplot( 1, 2, 2 ) # subplot for convolved density of states functions
pl.plot( energy_axis_convolve, O2p_Pr4f_convolve_DOS )
pl.plot( energy_axis_convolve, O2p_Ce4f_convolve_DOS )
pl.plot( energy_axis_convolve, O2p_Ce5d_convolve_DOS )
pl.plot( energy_axis_convolve, summed_convolve_DOS )

    
''' ########################### REFERENCES ########################### 
1. Locshen C. et al. PHYSICAL REVIEW B 75, 035115 (2007)
'''