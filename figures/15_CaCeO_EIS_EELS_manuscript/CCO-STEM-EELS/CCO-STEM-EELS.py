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


# plot the eels data on and off of the gbin 10CCO
data_dir = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/15_WJB_IS EBSD EELS Ca-Ceria gbs/figures/FIGURE-PANELS/panel_04-stem-eels/fig4a-eels-data/'

input_file_dir = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/15_WJB_IS EBSD EELS Ca-Ceria gbs/figures/FIGURE-PANELS/CCO-STEM-EELS/fig4a-eels-data/'

input_file_name = '141118_10Ca_EELS_03_gb2-splice.txt'

output_file_dir = input_file_dir
output_file_name = 'CCO-STEM-EELS'
dots = 1200


## store data
# import data
d = np.genfromtxt( input_file_dir + input_file_name, skiprows = 3, delimiter = '\t' )

# dist_10, Ca_10, Ce_10, O_10, dist_2, Ca_2, Ce_2, O_2 = d.T[ 0 ], d.T[ 1 ], d.T[ 2 ], d.T[ 3 ], d.T[ 5 ], d.T[ 6 ], d.T[ 7 ], d.T[ 8 ]
ev_Ca, counts_Ca_off, counts_Ca_on, ev_O, counts_O_off, counts_O_on, ev_Ce, counts_Ce_off, counts_Ce_on = d.T
    
## plot stuff
pl.close( 'all' )
pl.figure( figsize = ( 3.4, 2.1 ) ) # ( width, height )

mpl.rcParams[ 'font.family' ] = 'sans-serif' # modify matplotlib parameters
mpl.rcParams[ 'font.weight' ] = 'normal'
mpl.rcParams[ 'font.size' ] = 10
mpl.rcParams[ 'mathtext.default' ] = 'regular'

col_off, col_on = 'maroon', 'slategray'
ls_off, ls_on = '-', ''
fill_10, fill_2 = 'full', 'none'
dash = ( 4, 1 )
Ca_major, O_major, Ce_major = 20, 40, 20

Ca_min_x, Ca_max_x = 335, 375
O_min_x, O_max_x = 525, 560
Ce_min_x, Ce_max_x = 870, 925

y_min_multiple, y_max_multiple = 0.1, 1.5

Ca_max_y = np.nanmax( counts_Ca_on ) * y_max_multiple
O_max_y = np.nanmax( counts_O_off ) * y_max_multiple
Ce_max_y = np.nanmax( counts_Ce_off ) * y_max_multiple

Ca_min_y = np.nanmax( counts_Ca_on ) * -y_min_multiple
O_min_y = np.nanmax( counts_O_off ) * -y_min_multiple
Ce_min_y = np.nanmax( counts_Ce_off ) * -y_min_multiple

# plot Ca
pl.subplot( 1, 3, 1 )
pl.plot( ev_Ca, counts_Ca_on, color = col_on, dashes = dash )
pl.plot( ev_Ca, counts_Ca_off, color = col_off, dashes = dash )

ax = pl.gca()
ax.set_ylabel( 'Counts (Arbitrary units)', labelpad = 0 )
ax.set_xlim( Ca_min_x, Ca_max_x )
ax.set_ylim( Ca_min_y, Ca_max_y )
ax.minorticks_on()
ax.set_xticklabels( [ '', '340', '', '', '355', '', '', '370' ] )
ax.set_yticklabels( [] )
# ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( Ca_major ) )

# LEGEND ON FIRST SUBPLOT
legend_labels = [ 'On GB', 'Off GB' ]
legend_loc = 'best' # ( 4.5 / 11, 0 )
ax.legend( legend_labels, loc = legend_loc, handlelength = 1.5,
    frameon = False, fontsize = 10, labelspacing = .01,
    handletextpad = 0.2, borderpad = 0 )

# plot O
pl.subplot( 1, 3, 2 )
pl.plot( ev_O, counts_O_on, color = col_on, dashes = dash )
pl.plot( ev_O, counts_O_off, color = col_off, dashes = dash )

ax = pl.gca()
# ax.set_xlabel( 'Distance (nm)', labelpad = 0 ) 
ax.set_xlim( O_min_x, O_max_x )
ax.set_ylim( O_min_y, O_max_y )

ax.minorticks_on()
ax.set_xticklabels( [ '', '', '535','', '', '550' ] )
ax.set_yticklabels( [] )
# ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( O_major ) )
ax.set_xlabel( 'Energy-loss (eV)', labelpad = 0 )
    
# plot Ce
pl.subplot( 1, 3, 3 )
pl.plot( ev_Ce, counts_Ce_on, color = col_on, dashes = dash )
pl.plot( ev_Ce, counts_Ce_off, color = col_off, dashes = dash )
# pl.plot( dist_2 + shift_both, Ca_2, color = col_2, marker = Ca_mark, linestyle = 'none',
#     fillstyle = fill_2, mew = mark_width, mec = col_2, markersize = marker_size )


# ax.set_xticklabels( [] )
# ax.set_yticks( np.linspace( 0, 4e-2, 9 ) )
# ax.yaxis.set_major_locator( mpl.ticker.MultipleLocator( 2e-2 ) )
ax = pl.gca()
ax.set_xlim( Ce_min_x, Ce_max_x )
ax.set_ylim( Ce_min_y, Ce_max_y )
ax.minorticks_on()
ax.set_xticklabels( [ '', '880','', '', '910' ] )
ax.set_yticklabels( [] )
# ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( Ce_major ) )
# ax.set_yticks( [ 0.1, 0.2, 0.3, 0.4 ] )

pl.subplots_adjust( wspace = 0.00 )

# plot 5CCO
# pl.subplot( 2, 1, 2 )
# pl.plot( deg_5, num_5, color = mark_col, marker = mark, linestyle = 'none',
#     fillstyle = 'full', mew = 1, mec = mark_col, markersize = marker_size )
# pl.plot( deg_5, ran_len_5, color = rand_col, linestyle = '-' )
# 
# ax = pl.gca()
# ax.set_yticks( np.linspace( 0, 4e-2, 9 ) )
# ax.yaxis.set_major_locator( mpl.ticker.MultipleLocator( 2e-2 ) )
# ax.minorticks_on()
# ax.set_xlabel( r'Misorientation angle ($^\circ$)', labelpad = 0 )
# ax.set_ylabel( 'Number fraction', labelpad = 0 )

 

# ax1.set_xticks( np.linspace( 100, 500, 5 ) )
# ax1.set_xticklabels( np.linspace( 100, 500, 5 ) )
# ax1.set_yticks( [ 0.1, 0.2, 0.3, 0.4 ] )
# ax.minorticks_on()

# pl.tight_layout()
pl.show()
pl.savefig( output_file_dir + output_file_name + '-' + str( dots ) + 'dpi.png', format = 'png', dpi = dots, bbox_inches = 'tight', transparent = True )