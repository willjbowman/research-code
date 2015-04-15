''' ########################### OVERVIEW ########################### '''
'''
 Created 2015-04-01by Will Bowman. This script convoles the data from Pratik's
 PCO DFT paper to predict the low loss spectrum for comparison with Katia EELS.
 This script convolves the unoccupied DOSs above the Fermi level with those 
 below which are occupied. I've also added a Pr f interband state which is also
 convolved in order to compute the joint DOSs for undoped and doped cerias. The
 joint DOSs are convolved with a broadening gaussian function whose standard 
 deviation is called 'broadening_fwhm'.
'''

''' ########################### IMPORT MODULES ########################### '''
import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import wills_functions as wf
import imp, os
from scipy import signal

##


''' ########################### USER-DEFINED ########################### '''

data_path = "C:/Crozier_Lab/Writing/2015_PCO10 interband states/Dholobhai et al ceria PDOS_addPr_NoLowOcP_Eg35.txt" # path to data file
# data_path = "C:/Crozier_Lab/Writing/2015_PCO10 interband states/Dholobhai et al ceria PDOS_addPr.txt" # path to data file
curve_names = [ 'oc-s', 'oc-p',	'oc-d',	'oc-f',	'un-s',	'un-p',	'un-d',	'un-f',	'pr-f-0', 'pr-f-1' ]

# convolution_type = 'same'
convolution_type = 'same'
broadening_fwhm = 5 # eV

x_str = 'Relative energy (eV)'
y_str = 'DOS/eV'
x_tick_shift = 4 # eV
x_min, x_max = -5, 15 # eV
x_min_conv, x_max_conv = 0, 5 # eV

wf.slide_art_styles()

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

def broaden( signal_in, normalize = True ):
    # br_x = np.linspace( -5, 5, num = np.size( signal_in, axis = 0 ) )
    # br = wf.lorentzianate( br_x, broadening_fwhm )
    # br = br[ 0 : np.size( signal_in, axis = 0 ) ]
    br = signal.gaussian( np.size( signal_in, axis = 0 ), std = broadening_fwhm )
    if normalize:
        br = br / np.max( br )
    broadened = np.convolve( signal_in, br, mode = 'same' )
    return broadened

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
    
# def plot_convolutions( curves ):
#     for index, curve_n in enumerate( curves ):
#         pl.plot( curve_n, color = convolution_colors[ index ] )
    
def plot_convolutions( curves, x = None ):
    for index, curve_n in enumerate( curves ):
        if x == None:
            pl.plot( curve_n, color = convolution_colors[ index ] )
        else:
            pl.plot( x, curve_n, color = convolution_colors[ index ] )

def style_plot( convolved = True ):
    pl.xlim( x_min, x_max )
    pl.xlabel( x_str )
    pl.ylabel( y_str )
    pl.minorticks_on()
    if convolved:
        pl.xlim( x_min_conv, x_max_conv )
    
''' ########################### MAIN SCRIPT ########################### '''

data = np.loadtxt( data_path, skiprows = 1 ) # read data, ignore first three rows

energy = data[ :, 0 ]
oc_s = interpolate( data[ :, 1 ] )
oc_p = interpolate( data[ :, 2 ] )  
oc_d = interpolate( data[ :, 3 ] ) / 2
oc_f = interpolate( data[ :, 4 ] )
un_s = interpolate( data[ :, 5 ] )
un_p = interpolate( data[ :, 6 ] )
un_d = interpolate( data[ :, 7 ] )
un_f = interpolate( data[ :, 8 ] )
un_f_pr = interpolate( data[ :, 10 ] )
# un_f_pr = interpolate( data[ :, 10 ] ) * 2

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


pl.figure()
DOSs = ( oc_s, oc_p, oc_d, oc_f, un_s, un_p, un_d, un_f )
DOSs_convolved = ( con_s_p, con_p_d, con_p_f, con_d_f )
con_sum = con_s_p + con_p_d + con_p_f + con_d_f
# DOSs_convolved = ( con_s_p, con_p_d, con_d_f )
# con_sum = con_s_p + con_p_d + con_d_f
con_sum_broadened = broaden( con_sum )
energy_convolved = np.linspace( energy[ 0 ], energy[ -1 ], num = np.size( con_sum, axis = 0 ) )
energy_convolved = energy_convolved + x_tick_shift

pl.subplot( 2, 2, 1 )
plot_DOSs( energy, DOSs )
pl.legend( ( 's', 'p', 'd', 'f' ) )
style_plot( convolved = False )
pl.subplot( 2, 2, 2 )
plot_convolutions( DOSs_convolved, x = energy_convolved )
pl.legend( ( 's*p', 'p*d', 'p*f', 'd*f' ) )
# pl.legend( ( 's*p', 'p*d', 'd*f' ) )
style_plot()
pl.subplot( 2, 2, 3 )
pl.plot( energy_convolved, con_sum, color = 'blue' )
pl.plot( energy_convolved, wf.normalize_to_max( con_sum_broadened, con_sum )[0], color = 'maroon' )
pl.legend( ('CeO2', 'broadened') )
style_plot()
pl.subplot( 2, 2, 4 )
pl.legend( ( 'CeO2 broad' ) )
style_plot()



pl.figure()
DOSs_pr = ( oc_s, oc_p, oc_d, oc_f, un_s, un_p, un_d, un_f, un_f_pr )
DOSs_pr_convolved = ( con_s_p, con_p_d, con_p_f, con_d_f, con_p_f_pr, con_d_f_pr )
con_sum_pr = con_s_p + con_p_d + con_p_f + con_d_f + con_p_f_pr + con_d_f_pr
con_sum_pr_broadened = broaden( con_sum_pr )

pl.subplot( 2, 2, 1 )
plot_DOSs( energy, DOSs_pr )
pl.legend( ( 's', 'p', 'd', 'f' ) )
style_plot( convolved = False )
pl.subplot( 2, 2, 2 )
plot_convolutions( DOSs_pr_convolved, x = energy_convolved )
pl.legend( ( 's*p', 'p*d', 'p*f', 'd*f', 'p*f_Pr', 'd*f_Pr' ), loc = 'best' )
style_plot()
pl.subplot( 2, 2, 3 )
pl.plot( energy_convolved, con_sum_broadened, color = 'blue' )
pl.plot( energy_convolved, con_sum_pr_broadened, color = 'maroon' )
pl.legend( ( 'CeO2', 'PCO' ) )
style_plot()
pl.subplot( 2, 2, 4 )
pl.plot( energy_convolved, con_sum, color = 'blue' )
pl.plot( energy_convolved, con_sum_pr, color = 'maroon' )
pl.legend( ( 'CeO2', 'PCO' ) )
style_plot()

''' ########################### REFERENCES ###########################
1. http://stackoverflow.com/questions/6518811/interpolate-nan-values-in-a-numpy-array
'''