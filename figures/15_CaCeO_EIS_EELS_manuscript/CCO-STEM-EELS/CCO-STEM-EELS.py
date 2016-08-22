''' ########################### OVERVIEW ########################### '''
'''
 Updated 2016-03-31 by Will Bowman. This script is for plotting EELS spectra
 acquired on and off grain boundary in 10CCO for a paper figure
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
# path to data file
data_dir = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/'+\
	'15_WJB_IS EBSD EELS Ca-Ceria gbs/figures/'+\
	'CCO-STEM-EELS/EELS-data/'

d = data_dir +\
	'141118_10Ca_EELS_03_gb2-splice.txt'

# path to output directory
# output_file_dir = input_file_dir
output_dir = data_dir + wf.date_str() + '/'
# output_file_name = 'CCO-STEM-EELS'
output_file = 'CCO-STEM-EELS'
# subfolder_save = False
save = True
# save = False

fig_size = ( 4.5, 2.5 ) # ( width, height ) in inches
subplot_white_space = 0.03 # see pl.subplots_adjust()
# font size, resolution (DPI), file type
fsize, dots, file_types = 10, [300], ['png','svg']
cols = [ 'maroon', 'grey', 'black', 'goldenrod' ]
lins = [ (4,1), '-', '' ]
leg_ents = [ 'On GB', 'Off GB' ] 
leg_loc, leg_pad = 'best', 0.2
x_lab, y_lab = 'Energy loss (eV)', 'Counts (Arbitrary units)'
x_lims = [ [335, 375], [520, 575], [870, 925] ]
y_lims = [ [-1e4,15e4], [-1e4,15e4], [-1e4,15e4] ]
x_maj_tic_loc = [ 10, 10, 10 ]
x_maj_tic_lab = [
	[ '', '530', '', '550', '', '570' ],
	[ '', '530', '', '550', '', '570' ],
	[ '', '', '880', '', '900', '', '920' ]
	]
# scaling y-axis to percentage of curve maxima
y_min_multiple, y_max_multiple = 0.1, 1.5
shifty_fac = 0.2


''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize

def shifty( data, shifty_factor ):
	# return data + np.nanmin( data ) / shifty_factor
	shift = ( np.nanmax( data ) - np.nanmin( data ) ) * shifty_factor
	return data + shift
    
''' ########################### MAIN SCRIPT ########################### '''
# READ AND STORE DATA IN VARIABLES
d = np.genfromtxt( d, skiprows=3, delimiter='\t' )

# dist_10, Ca_10, Ce_10, O_10, dist_2, Ca_2, Ce_2, O_2 = d.T[ 0 ], d.T[ 1 ], d.T[ 2 ], d.T[ 3 ], d.T[ 5 ], d.T[ 6 ], d.T[ 7 ], d.T[ 8 ]
ev_Ca, counts_Ca_off, counts_Ca_on, ev_O, counts_O_off, counts_O_on, ev_Ce, counts_Ce_off, counts_Ce_on = d.T
    

## plot stuff
pl.close( 'all' )
pl.figure( figsize=fig_size ) # ( width, height )
mpl_customizations()

Ca_min_x, Ca_max_x = x_lims[0][0], x_lims[0][1]
O_min_x, O_max_x = x_lims[1][0], x_lims[1][1]
Ce_min_x, Ce_max_x = x_lims[2][0], x_lims[2][1]

Ca_max_y = np.nanmax( counts_Ca_on ) * y_max_multiple
O_max_y = np.nanmax( counts_O_off ) * y_max_multiple
Ce_max_y = np.nanmax( counts_Ce_off ) * y_max_multiple

Ca_min_y = np.nanmax( counts_Ca_on ) * -y_min_multiple
O_min_y = np.nanmax( counts_O_off ) * -y_min_multiple
Ce_min_y = np.nanmax( counts_Ce_off ) * -y_min_multiple

# plot Ca
pl.subplot( 1, 3, 1 )
pl.plot( ev_Ca, counts_Ca_on, c=cols[0], dashes=lins[0] )
pl.plot( ev_Ca, counts_Ca_off, c=cols[1], ls=lins[1] )

ax = pl.gca()
ax.set_ylabel( y_lab, labelpad=0 )
ax.set_xlim( Ca_min_x, Ca_max_x )
ax.set_ylim( Ca_min_y, Ca_max_y )
ax.minorticks_on()
ax.set_yticklabels([])
ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( x_maj_tic_loc[0] ) )
# ax.set_xticklabels( x_maj_tic_lab[0] )

# LEGEND ON FIRST SUBPLOT
ax.legend( leg_ents, loc=leg_loc, handlelength=1.5, frameon=False, 
	fontsize=fsize, labelspacing=leg_pad, handletextpad=leg_pad,
	borderpad=leg_pad )

# plot O
pl.subplot( 1, 3, 2 )
pl.plot( ev_O, counts_O_on, c=cols[0], dashes=lins[0] )
pl.plot( ev_O, shifty( counts_O_off, shifty_fac ), c=cols[1], ls=lins[1] )

ax = pl.gca()
ax.set_xlim( O_min_x, O_max_x )
ax.set_ylim( O_min_y, O_max_y )

ax.minorticks_on()
ax.set_yticklabels([])
# ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( x_maj_tic_loc[1] ) )
ax.set_xticklabels( x_maj_tic_lab[1] )
ax.set_xlabel( x_lab, labelpad=0 )
    
# plot Ce
pl.subplot( 1, 3, 3 )
pl.plot( ev_Ce, counts_Ce_on, c=cols[0], dashes=lins[0] )
pl.plot( ev_Ce, shifty( counts_Ce_off, shifty_fac ), c=cols[1], ls=lins[1] )
# pl.plot( dist_2 + shift_both, Ca_2, color = col_2, marker = Ca_mark, linestyle = 'none',
#     fillstyle = fill_2, mew = mark_width, mec = col_2, markersize = marker_size )


# ax.set_xticklabels( [] )
# ax.set_yticks( np.linspace( 0, 4e-2, 9 ) )
# ax.yaxis.set_major_locator( mpl.ticker.MultipleLocator( 2e-2 ) )
ax = pl.gca()
ax.set_xlim( Ce_min_x, Ce_max_x )
ax.set_ylim( Ce_min_y, Ce_max_y )
ax.minorticks_on()
ax.set_yticklabels([])
ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( x_maj_tic_loc[2] ) )
ax.set_xticklabels( x_maj_tic_lab[2] )
# ax.set_yticks( [ 0.1, 0.2, 0.3, 0.4 ] )

pl.subplots_adjust( wspace=subplot_white_space )

# pl.tight_layout()
pl.show()
if save:
	wf.save_fig( data_dir, file_types, dots, output_file )
# pl.savefig( output_file_dir + output_file_name + '-' + str( dots ) + 'dpi.png', format = 'png', dpi = dots, bbox_inches = 'tight', transparent = True )