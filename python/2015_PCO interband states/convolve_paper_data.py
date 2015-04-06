''' ########################### OVERVIEW ########################### '''
'''
 Created 2015-04-01by Will Bowman. This script convoles the data from Pratik's
 PCO DFT paper to predict the low loss spectrum for comparison with Katia EELS.
'''

''' ########################### IMPORT MODULES ########################### '''
import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import wills_functions as wf
import imp, os

##


''' ########################### USER-DEFINED ########################### '''

data_path = "C:/Crozier_Lab/Writing/2015_PCO10 interband states/Dholobhai et al ceria PDOS_addPr_lowloss-states.txt" # path to data file
curve_names = [ 'oc-s', 'oc-p',	'oc-d',	'oc-f',	'un-s',	'un-p',	'un-d',	'un-f',	'pr-f-0', 'pr-f-1' ]

# convolution_type = 'same'
convolution_type = 'full' 

DOS_colors = [ 'orange', 'blue', 'green', 'red', 'orange', 'blue', 'green', 'red', 'black' ]
convolution_colors = [ 'orange', 'blue', 'green', 'red', 'black', 'grey' ]

''' ########################### FUNCTIONS ########################### '''

def interpolate( col ):
    ok = -np.isnan( col )
    xp = ok.ravel().nonzero()[0]
    fp = col[ -np.isnan( col ) ]
    x  = np.isnan( col ).ravel().nonzero()[0]
    col[ np.isnan( col ) ] = np.interp( x, xp, fp )
    return col

def reverse( arr ):
    return arr[ ::-1 ]

def convolve( y0, y1 ):
    convolution = np.convolve( y0, y1, convolution_type )
    # return reverse( convolution )
    return convolution

def plot_figure( x, y1, y2, y1y2_conv ):
    pl.figure()
    pl.subplot( 2, 1, 1 )
    pl.plot( x, y1 )
    pl.plot( x, y2 )
    pl.subplot( 2, 1, 2 )
    pl.plot( y1y2_conv )
    
def plot_DOSs( x, curves ):
    for index, curve_n in enumerate( curves ):
        pl.plot( x, curve_n, color = DOS_colors[ index ] )
    
def plot_convolutions( curves ):
    for index, curve_n in enumerate( curves ):
        pl.plot( curve_n, color = convolution_colors[ index ] )
    
''' ########################### MAIN SCRIPT ########################### '''

data = np.loadtxt( data_path, skiprows = 1 ) # read data, ignore first three rows

energy = data[ :, 0 ]
oc_s = interpolate( data[ :, 1 ] )
oc_p = interpolate( data[ :, 2 ] )
oc_d = interpolate( data[ :, 3 ] )
oc_f = interpolate( data[ :, 4 ] )
un_s = interpolate( data[ :, 5 ] )
un_p = interpolate( data[ :, 6 ] )
un_d = interpolate( data[ :, 7 ] )
un_f = interpolate( data[ :, 8 ] )
# un_f_pr = interpolate( data[ :, 10 ] )
un_f_pr = interpolate( data[ :, 10 ] ) * 2

# the occupied DOSs are passed to reverse() so that when the unoccupied DOSs
# are convolved with the (reversed) occupied DOSs, the lowest channels of the 
# convolution output are the resuls of convolveing the valence band maxima
# with the conduction band minimum. This is physically what is happening during
# EELS: transitions from the VB max to the CB min is the lowest energy 
# ioniziation.
con_s_p = convolve( reverse( oc_s ), un_p )
con_p_d = convolve( reverse( oc_p ), un_d )
con_p_f = convolve( reverse( oc_p ), un_f ) # hybridization
con_d_f = convolve( reverse( oc_d ), un_f )
con_p_f_pr = convolve( reverse( oc_p ), un_f_pr ) # hybridization
con_d_f_pr = convolve( reverse( oc_d ), un_f_pr )

# wf.close_all()

# plot_figure( energy, oc_s, un_p, con_s_p )
# plot_figure( energy, oc_p, un_d, con_p_d )
# plot_figure( energy, oc_p, un_f, con_p_f )
# plot_figure( energy, oc_d, un_f, con_d_f )
# plot_figure( energy, oc_p, un_f_pr, con_p_f_pr )
# plot_figure( energy, oc_d, un_f_pr, con_d_f_pr )


pl.figure()
DOSs = ( oc_s, oc_p, oc_d, oc_f, un_s, un_p, un_d, un_f )
DOSs_convolved = ( con_s_p, con_p_d, con_p_f, con_d_f )
con_sum = con_s_p + con_p_d + con_p_f + con_d_f

pl.subplot( 3, 1, 1 )
plot_DOSs( energy, DOSs )
pl.legend( ( 's', 'p', 'd', 'f' ) )
pl.xlabel( 'eV' )
pl.ylabel( 'DOS/eV' )
pl.subplot( 3, 1, 2 )
plot_convolutions( DOSs_convolved )
pl.legend( ( 's*p', 'p*d', 'p*f', 'd*f' ) )
pl.subplot( 3, 1, 3 )
pl.plot( con_sum, color = 'red' )
pl.legend( ('CeO2', 'PCO') )

pl.figure()
DOSs_pr = ( oc_s, oc_p, oc_d, oc_f, un_s, un_p, un_d, un_f, un_f_pr )
DOSs_pr_convolved = ( con_s_p, con_p_d, con_p_f, con_d_f, con_p_f_pr, con_d_f_pr )
con_sum_pr = con_s_p + con_p_d + con_p_f + con_d_f + con_p_f_pr + con_d_f_pr

pl.subplot( 3, 1, 1 )
plot_DOSs( energy, DOSs_pr )
pl.legend( ( 's', 'p', 'd', 'f' ) )
pl.xlabel( 'eV' )
pl.ylabel( 'DOS/eV' )
pl.subplot( 3, 1, 2 )
plot_convolutions( DOSs_pr_convolved )
pl.legend( ( 's*p', 'p*d', 'p*f', 'd*f', 'p*f_Pr', 'd*f_Pr' ) )
pl.subplot( 3, 1, 3 )
pl.plot( con_sum, color = 'red' )
pl.plot( con_sum_pr, color = 'blue' )
pl.legend( ( 'CeO2', 'PCO' ) )

''' ########################### REFERENCES ###########################
1. http://stackoverflow.com/questions/6518811/interpolate-nan-values-in-a-numpy-array
'''