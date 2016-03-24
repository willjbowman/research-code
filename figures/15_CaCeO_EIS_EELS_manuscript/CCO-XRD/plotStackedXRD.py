from normalize import normalize
import numpy as np
import pylab as pl
import matplotlib as mpl


data = np.genfromtxt( 'CaDC_XRD_2_5_10_mol_1.csv', delimiter = ',' )
##

shift = 1500

two_theta_2mol_calc = data[ :, 0 ]
counts_2mol_calc = normalize( data[ :, 1 ], shift )
two_theta_2mol_sint = data[ :, 2 ]
counts_2mol_sint = normalize( data[ :, 3 ], shift )

two_theta_5mol_calc = data[ :, 4 ]
counts_5mol_calc = normalize( data[ :, 5 ], shift )
two_theta_5mol_sint = data[ :, 6 ]
counts_5mol_sint = normalize( data[ :, 7 ], shift )

two_theta_10mol_calc = data[ :, 8 ]
counts_10mol_calc = normalize( data[ :, 9 ], shift )
two_theta_10mol_sint = data[ :, 10 ]
counts_10mol_sint = normalize( data[ :, 11 ], shift )

## paper figure

pl.close( 'all' )

mpl.rcParams[ 'font.family' ] = 'Times New Roman'
mpl.rcParams[ 'font.weight' ] = 'normal'
mpl.rcParams[ 'font.size' ] = 10

pl.figure( figsize = ( 3.5, 3.5 ) )
ax = pl.gca()

dash = [ 2, 2 ] # [ pix_on pix_off ]

pl.plot( two_theta_2mol_calc, counts_2mol_calc,
    color = 'maroon', dashes = dash )
pl.plot( two_theta_2mol_sint, counts_2mol_sint + shift,
    color = 'maroon' )
pl.plot( two_theta_5mol_calc, counts_5mol_calc + 2 * shift,
    color = 'grey', dashes = dash )
pl.plot( two_theta_5mol_sint, counts_5mol_sint + 3 * shift, 
    color = 'grey' )
pl.plot( two_theta_10mol_calc, counts_10mol_calc + 4 * shift,
    color = 'black', dashes = dash )
pl.plot( two_theta_10mol_sint, counts_10mol_sint + 5 * shift,
    color = 'black' )

pl.xlim( 25, 90 )
ylim_max = 1e4
pl.ylim( -200, ylim_max )

# curve labels
x_ax_trans = 40 # degrees
y_ax_trans_2 = 0.5 * shift
pl.text( x_ax_trans, y_ax_trans_2, '2 mol%', color = 'maroon', ha = 'center', va = 'center' )
y_ax_trans_5 = 2.5 * shift
pl.text( x_ax_trans, y_ax_trans_5, '5 mol%', color = 'grey', ha = 'center', va = 'center' )
y_ax_trans_10 = 4.5 * shift    
pl.text( x_ax_trans, y_ax_trans_10, '10 mol%', color = 'black', ha = 'center', va = 'center' )
# peak labels
pl.text( 28.5, 0.95e4, '(111)', color = 'black', ha = 'center', va = 'center' )
pl.text( 33, 0.85e4, '(200)', color = 'black', ha = 'center', va = 'center' )
pl.text( 47.5, 0.85e4, '(220)', color = 'black', ha = 'center', va = 'center' )
pl.text( 56.5, 0.85e4, '(311)', color = 'black', ha = 'center', va = 'center' )
pl.text( 60, 0.8e4, '(222)', color = 'black', ha = 'center', va = 'center' )
pl.text( 69.5, 0.8e4, '(400)', color = 'black', ha = 'center', va = 'center' )
pl.text( 76.5, 0.85e4, '(331)', color = 'black', ha = 'center', va = 'center' )
pl.text( 79, 0.8e4, '(420)', color = 'black', ha = 'center', va = 'center' )
pl.text( 86.5, 0.8e4, '(422)', color = 'black', ha = 'center', va = 'center' )
# calcine/sinter labels
pl.text( 89.5, 0.715e4, 'sintered', color = 'black', ha = 'right', va = 'center' )
pl.text( 89.5, 0.64e4, 'as-calcined', color = 'black', ha = 'right', va = 'center' )

pl.xlabel( '2$\Theta$ (degrees)' )
pl.ylabel( 'Arbitrary units' )

pl.tick_params( 'y', labelleft = 'off', left = 'off', right = 'off' )
ax.xaxis.set_minor_locator( pl.MultipleLocator(1) ) # xTickMinor

pl.tight_layout()
pl.show()
pl.savefig( 'CaDC_XRD_2_5_10_mol_pub.png', format = 'png', dpi = 500 )