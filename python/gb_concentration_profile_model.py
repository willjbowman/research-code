import numpy as np
import pylab as pl
import wills_functions as wf

##
pl.close( 'all' )

spec_thick = 50 # (nm), specimen thickness
t = spec_thick * 10
t_plot = np.linspace( 1, 50 )
x_max, x_steps = 100, 201
x_plot = np.linspace( 1, x_max ) # specimen width 

gb_fwhm = 2 # gb concenration profile FWHM
gb_max_conc = 0.5

gb_lorentzian = wf.lorentzianate( x_plot, gb_fwhm )

def scale_to_max( curve, max_val ) :
    norm = curve / np.nanmax( curve )
    scaled_to_max = norm * max_val
    return scaled_to_max
    
gb_conc = scale_to_max( gb_lorentzian, gb_max_conc )
# pl.plot( gb_conc )

distribution_2d = np.zeros( ( t, x_max ) )

for i in range( np.size( distribution_2d, 1 ) ) :
    counts = np.rint( gb_conc[ i ] * t )
    atoms = np.ones( counts )
    matrix = np.zeros( t - counts )
    atom_column = np.concatenate( ( atoms, matrix ) )
    np.random.shuffle( atom_column )
    distribution_2d[ :, i ] = atom_column

pl.figure()

pl.subplot( 2, 1, 1 )
pl.pcolor( distribution_2d )
pl.ylabel( 'TEM specimen thickness (nm)' )

pl.subplot( 2, 1, 2 )
pl.plot( gb_conc )
pl.ylabel( 'molar concentration' )
pl.xlabel( 'distance (nm)' )
