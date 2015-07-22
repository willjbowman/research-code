# plot the composition profiles of 10CCO gb2 map3 and 2CCO gb5 map9

input_file_dir = 'C:/Users/willb/Dropbox/Crozier Group Users - Will Bowman/Crozier_Lab/Writing/2015_IS EBSD EELS of CaCeria grain boundaries/figures/FIGURE-PANELS/panel_04-stem-eels/figb-composition-profiles/'

input_file_name = 'comp-profiles-10-2-CCO.txt'

output_file_dir = input_file_dir
output_file_name = 'fig4b-comp-profiles-10-2-CCO'
dots = 1200

import numpy as np
import pylab as pl
import matplotlib as mpl

## store data
# import data
d = np.genfromtxt( input_file_dir + input_file_name, skiprows = 5, delimiter = '\t' )

dist_10, Ca_10, Ce_10, O_10, dist_2, Ca_2, Ce_2, O_2 = d.T[ 0 ], d.T[ 1 ], d.T[ 2 ], d.T[ 3 ], d.T[ 5 ], d.T[ 6 ], d.T[ 7 ], d.T[ 8 ]
    
## plot stuff
pl.close( 'all' )
pl.figure( figsize = ( 2.3, 2.3 ) ) # ( width, height )

mpl.rcParams[ 'font.family' ] = 'sans-serif' # modify matplotlib parameters
mpl.rcParams[ 'font.weight' ] = 'normal'
mpl.rcParams[ 'font.size' ] = 10
mpl.rcParams[ 'mathtext.default' ] = 'regular'

col_10, col_2 = 'maroon', 'slategray'
fill_10, fill_2 = 'full', 'none'
O_mark, Ce_mark, Ca_mark = 'o', '^', 'v'
marker_size, mark_width = 4, 0.5
shift_2, shift_10, shift_both = 0, 4.0, -7.5

# plot 10CCO
pl.plot( dist_10 + shift_10 + shift_both, O_10, color = col_10, marker = O_mark, linestyle = 'none',
    fillstyle = fill_10, mew = mark_width, mec = col_10, markersize = marker_size )
pl.plot( dist_10 + shift_10 + shift_both, Ce_10, color = col_10, marker = Ce_mark, linestyle = 'none',
    fillstyle = fill_10, mew = mark_width, mec = col_10, markersize = marker_size )
pl.plot( dist_10 + shift_10 + shift_both, Ca_10, color = col_10, marker = Ca_mark, linestyle = 'none',
    fillstyle = fill_10, mew = mark_width, mec = col_10, markersize = marker_size )
    
# plot 10CCO
pl.plot( dist_2 + shift_both, O_2, color = col_2, marker = O_mark, linestyle = 'none',
    fillstyle = fill_2, mew = mark_width, mec = col_2, markersize = marker_size )
pl.plot( dist_2 + shift_both, Ce_2, color = col_2, marker = Ce_mark, linestyle = 'none',
    fillstyle = fill_2, mew = mark_width, mec = col_2, markersize = marker_size )
pl.plot( dist_2 + shift_both, Ca_2, color = col_2, marker = Ca_mark, linestyle = 'none',
    fillstyle = fill_2, mew = mark_width, mec = col_2, markersize = marker_size )

ax = pl.gca()
ax.set_xlabel( 'Distance (nm)', labelpad = 0 )
ax.set_ylabel( 'Composition (mol/mol)', labelpad = 0 )  
ax.set_xlim( -6, 6 )
ax.set_ylim( 0, 2.1 )

# ax.set_xticklabels( [] )
# ax.set_yticks( np.linspace( 0, 4e-2, 9 ) )
# ax.yaxis.set_major_locator( mpl.ticker.MultipleLocator( 2e-2 ) )
ax.minorticks_on()
# ax.set_yticklabels( np.linspace( 0, 4e-2, 3 ) )
# ax.set_yticks( [ 0.1, 0.2, 0.3, 0.4 ] )

# legend_labels = [ 'Exp.', 'Theor.' ]
# legend_loc = 'best' # ( 4.5 / 11, 0 )
# ax.legend( legend_labels, loc = legend_loc,
#     numpoints = 1, frameon = False, fontsize = 10, labelspacing = .01,
#     handletextpad = 0.2 )


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

pl.tight_layout()
pl.show()
pl.savefig( output_file_dir + output_file_name + '-' + str( dots ) + 'dpi.png', format = 'png', dpi = dots )