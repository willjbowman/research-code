''' ########################### OVERVIEW ########################### '''
'''
Created 2015-03-04 by Will Bowman. This is for a figure plot showing time-
resolved EELS acquisitions from CeO2
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
Ce_data_path = 'C:/Crozier_Lab/research_PhD/code/github/figures/15_ceria_FEFF_EELS_manuscript/140404_7bCeO2crush_Nion100kV_timeResolved-CeM-BKGDSUBSI-870_cal883.txt'
O_data_path = 'C:/Crozier_Lab/research_PhD/code/github/figures/15_ceria_FEFF_EELS_manuscript/140404_7bCeO2crush_Nion100kV_timeResolved-OK-BKGDSUBSI-520_cal533.txt'

Ce_counts_max, O_counts_max = 6e3, 2e3 # set max counts threshold
x_label = 'Energy loss (eV)' # x-axis label text

# 1d plot info
O_spectrum_shift, Ce_spectrum_shift = 5e3, 14e3 # vertical shift each spectrum form clarity
O_y_lims, Ce_y_lims =  ( -7e3, 6e3 ), (   )# eV, x-axis bounds
O_eV_lims, Ce_eV_lims = ( 525, 565 ), ( 870, 915 ) # eV, x-axis bounds
Ce_spectra_displayed = [ 2, 20, 40, 60, 80 ] # spectra to display for comparison
O_spectra_displayed = [ 2, 99, 199, 295 ]
Ce_spectra_summed, O_spectra_summed = 5, 5 # sum spectra for less noisy image
y_label_1d = 'Counts (Arbitrary units)' # y-axis label text
size, col = 2, 'maroon'
mark_O, line_O, mark_Ce, line_Ce = '.', '-.', '.', '-.'
O_labels = [ 'Ce 4f0', 'Ce 5deg', 'Ce 4f1', 'Ce 5dt2g' ]
O_labels_x = [ 533, 536, 537.5, 540 ]
O_labels_y = []
Ce_labels = [ '4a', '4b', '4c', '4d', '3a', '3b', '3c', '3d', '3e' ]
Ce_labels_x = [ 883, 888.5, 901.5, 907, 880.5, 881.5, 896, 899 ]
Ce_labels_y = []

# 2d plot info
Ce_end_spectrum_index, O_end_spectrum_index = 400, 299 # specify last spectrum displayed
y_label_2d = 'Acquisition' # y-axis text
cmap = pl.cm.hot # coler scheme for 2d plot

''' ########################### FUNCTIONS ########################### '''

def array_index( array, values ):
    key_indicies = []
    for value in values:
        key_index = np.where( array == value )[0][0]
        key_indicies.append( key_index )
    return key_indicies
    
''' ########################### MAIN SCRIPT ########################### '''

Ce_data = np.loadtxt( Ce_data_path, skiprows = 3 ) # read data
O_data = np.loadtxt( O_data_path, skiprows = 3 )

eV_Ce = Ce_data[ :, 0 ] # take first column as energy axis values
eV_O = O_data[ :, 0 ]

# counts_Ce = Ce_data[ :, :-1 ] # take slice of remaining array
counts_Ce = Ce_data[ :, 2 : Ce_end_spectrum_index ] # take slice of remaining array
counts_O = O_data[ :, :-1 ]

# get indicies of energy axis plot limits
O_eV_min_index, O_eV_max_index = array_index( eV_O, O_eV_lims )
Ce_eV_min_index, Ce_eV_max_index = array_index( eV_Ce, Ce_eV_lims )

# extract 2d plot data within plot limits
bounded_counts_O = counts_O.T[ :, O_eV_min_index : O_eV_max_index ]
bounded_counts_Ce = counts_Ce.T[ :, Ce_eV_min_index : Ce_eV_max_index ]

# plot stuff
wf.close_all()
pl.figure( figsize = ( wf.mm2in( 190 ), wf.mm2in( 190 ) ) ) # create figure


# 1d plots
# pl.subplot( 2, 2, 1 )
pl.subplot2grid( ( 3, 2 ), ( 0, 0 ), rowspan = 2 )
for index, spectrum in enumerate( O_spectra_displayed ): # sum and plot spectra
    summed_counts = np.sum( counts_O[ :, spectrum : spectrum + O_spectra_summed ], 1 )
    pl.plot( eV_O, summed_counts - index * O_spectrum_shift, marker = mark_O, 
        ms = size, ls = line_O, color = col )
    wf.centered_annotation( 
        O_eV_lims[ 0 ] * 1.005,
        ( summed_counts[ 0 ] - index * O_spectrum_shift ) + O_counts_max,
        str( spectrum - 1 ), col, fontsize = 7
    )

ax = pl.gca()
pl.xlim( O_eV_lims )#, pl.ylim( O_y_lims ) # apply plot limits
pl.minorticks_on()
ax.yaxis.set_ticklabels([]) # y tick labels off
pl.xlabel( x_label ), pl.ylabel( y_label_1d )

# pl.subplot( 2, 2, 2 )
pl.subplot2grid(( 3, 2 ), ( 0, 1 ), rowspan = 2 )
for index, spectrum in enumerate( Ce_spectra_displayed ):
    summed_counts = np.sum( counts_Ce[ :, spectrum : spectrum + Ce_spectra_summed ], 1 )
    pl.plot( eV_Ce, summed_counts - index * Ce_spectrum_shift, marker = mark_Ce,
        ms = size, ls = line_Ce, color = col )
    wf.centered_annotation( 
        Ce_eV_lims[ 0 ] * 1.005,
        ( summed_counts[ 0 ] - index * Ce_spectrum_shift ) + Ce_counts_max,
        str( spectrum - 1 ), col, fontsize = 7
    )

ax = pl.gca()
pl.xlim( Ce_eV_lims ) #, pl.ylim( bottom = -spectrum_shift ) # apply plot limits
pl.minorticks_on()
ax.yaxis.set_ticklabels([]) # y tick labels off
pl.xlabel( x_label ) #, pl.ylabel( y_label_1d )


# 2d plots
# pl.subplot( 2, 2, 3 )
pl.subplot2grid( ( 3, 2 ), ( 2, 0 ) )
pl.imshow( bounded_counts_O, cmap = cmap, interpolation = 'None', 
    norm = mpl.colors.Normalize( vmin = 0, vmax = O_counts_max, clip = False ) )

ax = pl.gca()
ax.xaxis.set_ticklabels([])
pl.minorticks_on()
pl.ylabel( y_label_2d )

# pl.subplot( 2, 2, 4 )
pl.subplot2grid( ( 3, 2 ), ( 2, 1 ) )
pl.imshow( bounded_counts_Ce, cmap = cmap, interpolation = 'None', 
    norm = mpl.colors.Normalize( vmin = 0, vmax = Ce_counts_max, clip = False ) )

ax = pl.gca()
ax.xaxis.set_ticklabels([])
pl.minorticks_on()
# pl.ylabel( y_label_2d )



    
''' ########################### REFERENCES ########################### '''