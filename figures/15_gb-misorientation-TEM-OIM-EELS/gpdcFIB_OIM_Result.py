import numpy as np
import pylab as pl

## print figure 'C:\\crozier_lab\\research_phd\\microscopy_proc\\140415_gpdcFIB_Astar_PROC'
pl.close( 'all' )

d_mack200 = np.genfromtxt( 'mackenzie_200_bins.txt', delimiter = ';', 
    skip_header = 7, skip_footer = 10 )
d_gbLenFrac = np.genfromtxt( 'GPDCfib_gbLengthFraction.txt', delimiter = '  ' )
d_cslLenFrac = np.genfromtxt( 'GPDCfib_cslLengthFraction.txt' )

gb_misor_angle = d_gbLenFrac[ :, 0 ]
gb_length_fraction = d_gbLenFrac[ :, 1 ]

mack_misor_angle = d_mack200[ :, 0 ]
mack_number_fraction = d_mack200[ :, 2 ] * 14 - 0.005

csl = np.linspace( 1, 49, 49 )
csl_length_fraction = d_cslLenFrac

##
# calculate CSL fraction of total gb length
csl_length = 0

for i in np.nditer( csl_length_fraction ):
    if i > 0:
        csl_length += i

##
# generate figures for print and slides

pl.rc( 'font', size = 14, family = 'serif', weight = 'normal' )

pl.figure( figsize = ( 14, 4 ), dpi = 80 ).canvas.set_window_title( 
    'GPDCfib_oimPrintFigure' )

# gb misorientation angle distribution subplot
pl.subplot( 1, 3, 2 )

pl.plot( gb_misor_angle, gb_length_fraction, color = 'maroon', 
    marker = 'o', linestyle = '' )
pl.plot( mack_misor_angle, mack_number_fraction, color = 'grey', 
    linewidth = 1.0, linestyle = '-' )

pl.legend( ('GPDC', 'Mackenzie \n(random)'), loc = 'upper left', 
    numpoints = 1, frameon = False, fontsize = 14 )

pl.xlim( 0, 65 )
pl.xticks( np.linspace( 0, 65, 14, endpoint = True ) )
pl.ylim( 0, 0.2 )

pl.ylabel( 'Length fraction' )
pl.xlabel( 'Misorientation angle ($^\circ$)' )

# csl distribution subplot
pl.subplot( 1, 3, 3 )

bar_shift = 0.4
pl.bar( csl - bar_shift, csl_length_fraction, facecolor = 'white', 
    edgecolor = 'maroon' )

pl.xlim( 0, 50 )
pl.xticks( np.linspace( 1, 49, 13 ) )
pl.minorticks_on()

pl.ylabel( 'Length fraction' )
pl.xlabel( 'Coincidence site lattice (CSL) $\Sigma$' )

pl.tight_layout()
pl.show()

## slide figure
# gb misorientation angle distribution subplot
pl.close( 'all' )

pl.rc( 'font', size = 14, family = 'arial', weight = 'bold' )

pl.figure( figsize = ( 14, 4 ), dpi = 80 ).canvas.set_window_title( 
    'GPDCfib_oimSlideFigure' )

pl.subplot( 1, 3, 2 )

pl.plot( gb_misor_angle, gb_length_fraction, color = 'maroon', 
    marker = 'o', linestyle = '' )
pl.plot( mack_misor_angle, mack_number_fraction, color = 'grey', 
    linewidth = 2.0, linestyle = '-' )

pl.legend( ('GPDC', 'Mackenzie \n(random)'), loc = 'upper left', 
    numpoints = 1, frameon = False, fontsize = 14 )

pl.xlim( 0, 65 )
pl.xticks( np.linspace( 0, 65, 14, endpoint = True ) )
pl.ylim( 0, 0.2 )

pl.ylabel( '`' )
pl.xlabel( '`' )

# returns current axis limits
ax = pl.axis()

pl.text( -0.175*ax[1], ax[3]/2, 'Length fraction', rotation = 90, va = 'center' )
pl.text( ax[1]/2, -0.175*ax[3], 'Misorientation angle ($^\circ$)', ha = 'center' )

# csl distribution subplot
pl.subplot( 1, 3, 3 )
csl = np.linspace( 1, 49, 49 )
csl_length_fraction = d_cslLenFrac

bar_shift = 0.4
pl.bar( csl - bar_shift, csl_length_fraction, facecolor = 'white', 
    edgecolor = 'maroon' )

pl.xlim( 0, 50 )
pl.xticks( np.linspace( 1, 49, 13 ) )
pl.minorticks_on()

pl.ylabel( '`' )
pl.xlabel( '`' )

# returns current axis limits
ax = pl.axis()

pl.text( -0.175*ax[1], ax[3]/2, 'Length fraction', rotation = 90, va = 'center' )
pl.text( ax[1]/2, -0.175*ax[3], 'Coincidence site lattice (CSL) $\Sigma$', ha = 'center' )

# annotate with text box
pl.text( ax[1]/2, 0.75*ax[3], 'CSL / Total = 0.23', va = 'center', ha = 'center' )

pl.tight_layout()
pl.show()
        