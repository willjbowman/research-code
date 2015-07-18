# import the capacitances for each sample to determine the electrical gb width
# equation is found in Avila-Paredes, Kim 'dopant concentration dependence of
# grain boundary conductivity in GDC'

input_file_dir = 'C:/Users/willb/Dropbox/Crozier Group Users - Will Bowman/Crozier_Lab/Writing/2015_IS EBSD EELS of CaCeria grain boundaries/figures/gb-potentials/'

input_file_name = 'CaCeO-2-5-10-gb-potential.txt' #potentials

output_file_dir = input_file_dir
output_file_name = 'fig2f-small-CaCeO-2-5-10-gb-potential'
dots = 1200

import numpy as np
import pylab as pl
import matplotlib as mpl

## store data
# import data
d = np.loadtxt( input_file_dir + input_file_name, skiprows = 1 )

Tc_2Ca, phi0_2Ca, Tc_5Ca, phi0_5Ca, Tc_10Ca, phi0_10Ca = d.T
    
## plot stuff
pl.close( 'all' )
pl.figure( figsize = ( 2.3, 2.1 ) )
ax1 = pl.gca()

mpl.rcParams[ 'font.family' ] = 'sans-serif' # modify matplotlib parameters
mpl.rcParams[ 'font.weight' ] = 'normal'
mpl.rcParams[ 'font.size' ] = 10
mpl.rcParams[ 'mathtext.default' ] = 'regular'

color_2, color_5, color_10 = 'maroon', 'slategray', 'black'
mark_2, mark_5, mark_10 = '^', 'v', '<'
marker_size, legend_marker_size = 4, 6

ax1.set_xlabel( r'T ($^\circ$C)', labelpad = 0 )
ax1.set_ylabel( '$\Delta\Phi_{0}$ (V)', labelpad = 0 )

ax1.plot( Tc_2Ca, phi0_2Ca, color = color_2, marker = mark_2, linestyle = 'none',
    fillstyle = 'full', mew = 1, mec = color_2, markersize = marker_size )
ax1.plot( Tc_5Ca, phi0_5Ca, color = color_5, marker = mark_5, linestyle = 'none',
    fillstyle = 'full', mew = 1, mec = color_5, markersize = marker_size )
ax1.plot( Tc_10Ca, phi0_10Ca, color = color_10, marker = mark_10, linestyle = 'none',
    fillstyle = 'full', mew = 1, mec = color_10, markersize = marker_size ) 
    
# ax1.set_xlim( 100, 500 )
ax1.set_ylim( 0.1, 0.45 )

ax1.set_xticks( np.linspace( 100, 500, 5 ) )
# ax1.set_xticklabels( np.linspace( 100, 500, 5 ) )
ax1.set_yticks( [ 0.1, 0.2, 0.3, 0.4 ] )
ax1.minorticks_on()

legend_labels = [ '2', '5', '10' ]
legend_loc = 'best' # ( 4.5 / 11, 0 )
ax1.legend( legend_labels, loc = legend_loc,
    numpoints = 1, frameon = False, fontsize = 10, labelspacing = .01,
    handletextpad = 0.2 )

pl.tight_layout()
pl.show()
pl.savefig( output_file_dir + output_file_name + '-' + str( dots ) + 'dpi.png', format = 'png', dpi = dots )