# import the gbpd data and plot for manuscript and presentation

input_file_dir = 'C:/Users/willb/Dropbox/Crozier Group Users - Will Bowman/Crozier_Lab/Writing/2015_IS EBSD EELS of CaCeria grain boundaries/figures/FIGURE-PANELS/panel_03-sem-ebsd/fig3be-small-gbpd/'

input_file_name_2CCO = 'report_all_segments_2mol.txt'
input_file_name_5CCO = 'report_all_segments_5mol.txt'

output_file_dir = input_file_dir
output_file_name = 'fig3be-small-gbpd-number-fraction'
dots = 1200

import numpy as np
import pylab as pl
import matplotlib as mpl

## store data
# import data
d2 = np.loadtxt( input_file_dir + input_file_name_2CCO, skiprows = 1, delimiter = '\t' )
d5 = np.loadtxt( input_file_dir + input_file_name_5CCO, skiprows = 1, delimiter = '\t' )

deg_2, len_2, num_2, ran_num_2, ran_len_2 = d2.T
deg_5, len_5, num_5, ran_num_5, ran_len_5 = d5.T
    
## plot stuff
pl.close( 'all' )
pl.figure( figsize = ( 3, 3 ) ) # ( width, height )
ax1 = pl.gca()

mpl.rcParams[ 'font.family' ] = 'sans-serif' # modify matplotlib parameters
mpl.rcParams[ 'font.weight' ] = 'normal'
mpl.rcParams[ 'font.size' ] = 10
mpl.rcParams[ 'mathtext.default' ] = 'regular'

mark_col, rand_col = 'maroon', 'slategray'
mark = 'o'
marker_size = 4

# plot 2CCO
pl.subplot( 2, 1, 1 )
pl.plot( deg_2, num_2, color = mark_col, marker = mark, linestyle = 'none',
    fillstyle = 'full', mew = 1, mec = mark_col, markersize = marker_size )
pl.plot( deg_2, ran_len_2, color = rand_col, linestyle = '-' )

ax = pl.gca()
# ax.set_ylabel( 'Number fraction', labelpad = 0 )

ax.set_xticklabels( [] )
ax.set_yticks( np.linspace( 0, 4e-2, 9 ) )
ax.yaxis.set_major_locator( mpl.ticker.MultipleLocator( 2e-2 ) )
ax.minorticks_on()
# ax.set_yticklabels( np.linspace( 0, 4e-2, 3 ) )
# ax.set_yticks( [ 0.1, 0.2, 0.3, 0.4 ] )

legend_labels = [ 'Exp.', 'Theor.' ]
legend_loc = 'best' # ( 4.5 / 11, 0 )
ax.legend( legend_labels, loc = legend_loc,
    numpoints = 1, frameon = False, fontsize = 10, labelspacing = .01,
    handletextpad = 0.2 )


# plot 5CCO
pl.subplot( 2, 1, 2 )
pl.plot( deg_5, num_5, color = mark_col, marker = mark, linestyle = 'none',
    fillstyle = 'full', mew = 1, mec = mark_col, markersize = marker_size )
pl.plot( deg_5, ran_len_5, color = rand_col, linestyle = '-' )

ax = pl.gca()
ax.set_yticks( np.linspace( 0, 4e-2, 9 ) )
ax.yaxis.set_major_locator( mpl.ticker.MultipleLocator( 2e-2 ) )
ax.minorticks_on()
ax.set_xlabel( r'Misorientation angle ($^\circ$)', labelpad = 0 )
# ax.set_ylabel( 'Number fraction', labelpad = 0 )

    
# ax1.set_xlim( 100, 500 )
# ax1.set_ylim( 0.1, 0.45 )

# ax1.set_xticks( np.linspace( 100, 500, 5 ) )
# ax1.set_xticklabels( np.linspace( 100, 500, 5 ) )
# ax1.set_yticks( [ 0.1, 0.2, 0.3, 0.4 ] )
# ax.minorticks_on()

pl.tight_layout()
pl.show()
pl.savefig( output_file_dir + output_file_name + '-' + str( dots ) + 'dpi.png', format = 'png', dpi = dots )