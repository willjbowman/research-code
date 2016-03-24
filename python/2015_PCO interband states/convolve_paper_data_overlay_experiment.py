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

data_path = "C:/Users/willb/Dropbox/WillB/Crozier_Lab/Writing/2015_PCO10 interband states/figures/Dholobhai et al ceria PDOS_addPr_NoLowOcP_Eg35_25meV.txt" # path to data file
# data_path = "C:/Users/willb/Dropbox/WillB/Crozier_Lab/Writing/2015_PCO10 interband states/figures/Dholobhai et al ceria PDOS_addPr_NoLowOcP_Eg35_25meV_double_peak.txt" # path to data file
experiment_data_path = 'C:/Users/willb/Dropbox/WillB/Crozier_Lab/Writing/2015_PCO10 interband states/data/pco-valence-loss.txt'
# data_path = "C:/Crozier_Lab/Writing/2015_PCO10 interband states/Dholobhai et al ceria PDOS_addPr.txt" # path to data file
curve_names = [ 'oc-s', 'oc-p',	'oc-d',	'oc-f',	'un-s',	'un-p',	'un-d',	'un-f',	'pr-f-0', 'pr-f-1' ]

# convolution_type = 'same'
convolution_type = 'same'
# broadening_fwhm = 5 # eV
broadening_fwhm = .025 # eV

x_str = 'Energy (eV)'
y_str = 'DOS/eV'
x_tick_shift = 4 # eV
x_min, x_max = -5, 15 # eV
x_min_conv, x_max_conv = 0, 15 # eV

x_min_eels, x_max_eels = 0, 5 # eV
y_min_eels, y_max_eels = -2, 5.5 # eV

exp_scalar = 1 / 120 # scale experimental data

wf.slide_art_styles()

DOS_colors = [ 'red', 'orange', 'grey', 'maroon', 'black', 'red', 'orange', 'grey', 'maroon' ]
convolution_colors = [ 'grey', 'black', 'orange', 'maroon', 'red', 'white', 'green', 'grey', 'white' ]
# convolution_colors = [ 'red', 'orange', 'grey', 'maroon', 'black', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue' ]
# con_p_f_pr, con_d_f_pr, con_p_f, con_d_f, con_s_p, con_p_s, con_p_d, con_d_p, con_f_d 

dashstyles = [ [1,1], [2,2], [4,2], [6,2], [10000,1], [1,1], [2,2], [4,2], [6,2], [10000,1] ]

output_file_path = 'C:/Crozier_Lab/Writing/2015_PCO10 interband states/figures/single-scattering-model/'
output_file_name = 'single-scattering-model-150825-full-convolution'


# # specify selected orbitals for convolution
# s_p = False
# 
# p_s = False
# p_d = False
# p_f = False # hybridization
# p_f_pr = False # hybridization
# 
# d_p = False
# d_f = False
# d_f_pr = False
# 
# f_d = False

''' figure flags '''
# [ plot, save, dpi ]
plot_DOS_curves = False # this is just the DOS plots for CeO2 and PCO
plot_full_convolution = False # symmetry-projected convolutions, summed compared
plot_selected_convolution = False # symmetry-projected convolutions, summed compared
DOS_compare_sum_reduced_shifted = [ True, True, 300 ]
plot_DOS_convolution_single_scattering = [ False, True, 1200 ]

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
        pl.plot( x, curve_n, color = DOS_colors[ index ], lw = 0.9, dashes = dashstyles[ index ] )
        # pl.plot( x, curve_n, color = DOS_colors[ index ], lw = 0.9, ls = '-' )
    
def plot_DOSs_rotated( x, curves ):
    for index, curve_n in enumerate( curves ):
        pl.plot( curve_n, x, color = DOS_colors[ index ], lw = 0.9, ls = '-' )
    
# def plot_convolutions( curves ):
#     for index, curve_n in enumerate( curves ):
#         pl.plot( curve_n, color = convolution_colors[ index ] )
    
def plot_convolutions( curves, x = None ):
    for index, curve_n in enumerate( curves ):
        if x == None:
            pl.plot( curve_n, color = convolution_colors[ index ], lw = 0.9, ls = '-' )
        else:
            pl.plot( x, curve_n, color = convolution_colors[ index ], lw = 0.9, dashes = dashstyles[ index ] )

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
oc_d = interpolate( data[ :, 3 ] )
# oc_d = interpolate( data[ :, 3 ] ) / 2 # used for presentation
oc_f = interpolate( data[ :, 4 ] )
un_s = interpolate( data[ :, 5 ] )
un_p = interpolate( data[ :, 6 ] )
un_d = interpolate( data[ :, 7 ] )
un_f = interpolate( data[ :, 8 ] )
un_f_pr = interpolate( data[ :, 10 ] )
# un_f_pr = interpolate( data[ :, 10 ] ) * 2

'''
The occupied DOSs are passed to reverse() so that when the unoccupied DOSs
are convolved with the (reversed) occupied DOSs, the lowest channels of the 
convolution output are the resuls of convolving the valence band maxima
with the conduction band minimum. This is physically what is happening during
EELS: transition from the VB max to the CB min is the lowest energy 
transfer.
'''

# con_s_s
con_s_p = convolve( reverse( oc_s ), un_p )
# con_s_d
# con_s_f
# con_s_f_pr

con_p_s = convolve( reverse( oc_p ), un_s )
# con_p_p
con_p_d = convolve( reverse( oc_p ), un_d )
con_p_f = convolve( reverse( oc_p ), un_f ) # hybridization
con_p_f_pr = convolve( reverse( oc_p ), un_f_pr ) # hybridization

# con_d_s
con_d_p = convolve( reverse( oc_d ), un_p )
# con_d_d
con_d_f = convolve( reverse( oc_d ), un_f )
con_d_f_pr = convolve( reverse( oc_d ), un_f_pr )

# con_f_s
# con_f_p
con_f_d = convolve( reverse( oc_f ), un_d )
# con_f_f
# con_f_f_pr

# read experimental data (background subtracted valence loss)
experiment_data = np.loadtxt( experiment_data_path )
experiment_ev, experiment_raw, experiment_processed = experiment_data.T

# wf.close_all()


# pl.figure()
DOSs = ( oc_s, oc_p, oc_d, oc_f, un_s, un_p, un_d, un_f )
# for rotated comparison plot with DOSs_pr DONT USE FOR CALCULATIONS!
DOSs_for_pr_compare = ( oc_s, oc_p, oc_d, oc_f, un_s, un_p, un_d, un_f, un_f )
# DOSs_convolved = ( con_s_p, con_p_d, con_p_f, con_d_f )
# con_sum = con_s_p + con_p_d + con_p_f + con_d_f
DOSs_convolved = ( con_s_p, con_p_s, con_p_d, con_p_f, con_d_p, con_d_f, con_f_d )
con_sum = con_s_p + con_p_s + con_p_d + con_p_f + con_d_p + con_d_f + con_f_d
con_sum_broadened = broaden( con_sum )
energy_convolved = np.linspace( energy[ 0 ], energy[ -1 ], num = np.size( con_sum, axis = 0 ) )
energy_convolved = energy_convolved + x_tick_shift
# 
# pl.subplot( 2, 2, 1 )
# plot_DOSs( energy, DOSs )
# pl.legend( ( 's', 'p', 'd', 'f' ), loc = 'best' )
# style_plot( convolved = False )
# pl.subplot( 2, 2, 2 )
# plot_convolutions( DOSs_convolved, x = energy_convolved )
# pl.legend( ( 's*p', 'p*d', 'p*f', 'd*f' ) )
# pl.legend( ( 's*p', 'p*s', 'p*d', 'p*f', 'd*p', 'd*f', 'f*d' ), loc = 'best' )
# style_plot()
# pl.subplot( 2, 2, 3 )
# pl.plot( energy_convolved, con_sum, color = 'blue' )
# pl.plot( energy_convolved, wf.normalize_to_max( con_sum_broadened, con_sum )[0], color = 'maroon' )
# pl.legend( ('CeO2', 'broadened'), loc = 'best' )
# style_plot()
# pl.subplot( 2, 2, 4 )
# pl.legend( ( 'CeO2 broad' ), loc = 'best' )
# style_plot()



# DOSs_pr = ( oc_s, oc_p, oc_d, oc_f, un_s, un_p, un_d, un_f, un_f_pr )
# DOSs_pr_convolved = ( con_s_p, con_p_d, con_p_f, con_d_f, con_p_f_pr, con_d_f_pr )
DOSs_pr = ( oc_s, oc_p, oc_d, oc_f, un_f_pr, un_s, un_p, un_d, un_f )
DOSs_pr_occ = ( oc_s, oc_p, oc_d, oc_f )
DOSs_pr_sum = [ sum( x ) for x in zip( *DOSs_pr_occ ) ] # [2]

''' including only dipole-selected convolutions '''
DOSs_pr_convolved = ( con_p_f_pr, con_d_f_pr, con_p_f, con_d_f, con_s_p, con_p_s, con_p_d, con_d_p, con_f_d ) # rearranged for paper
# DOSs_pr_convolved = ( con_p_f, con_p_f_pr, con_d_f, con_d_f_pr, con_f_d, con_s_p, con_p_s, con_p_d, con_d_p )
con_sum_pr = con_s_p + con_p_s + con_p_d + con_p_f + con_p_f_pr + con_d_p + con_d_f + con_d_f_pr + con_f_d

''' including all convolutions '''
DOSs_pr_convolved = ( con_p_f_pr, con_d_f_pr, con_p_f, con_d_f, con_s_p, con_p_s, con_p_d, con_d_p, con_f_d ) # rearranged for paper
# DOSs_pr_convolved = ( con_p_f, con_p_f_pr, con_d_f, con_d_f_pr, con_f_d, con_s_p, con_p_s, con_p_d, con_d_p )
con_sum_pr = con_s_p + con_p_s + con_p_d + con_p_f + con_p_f_pr + con_d_p + con_d_f + con_d_f_pr + con_f_d

''' sum convolutions '''
con_sum_pr_broadened = broaden( con_sum_pr )

if plot_DOS_curves:
    pl.figure()
    plot_DOSs( energy, DOSs_pr )
    pl.legend( ( 's', 'p', 'd', 'f' ), loc = 'best' )
    style_plot( convolved = False )
    
if plot_full_convolution:
    oc_sum = oc_s + oc_p + oc_d + oc_f
    un_sum = un_s + un_p + un_d + un_f + un_f_pr
    con_full = convolve( reverse( oc_sum ), un_sum )
    pl.figure()
    pl.plot( energy_convolved, con_full, lw = 0.9, ls = '-' )
    exp_scalar_full_conv = 1 / 45 # scale experimental data
    pl.plot( experiment_ev, experiment_processed * exp_scalar_full_conv, ls = 'None', marker = '.', ms = 1, color = 'grey' )
    pl.ylim( 0, 15 )
    pl.xlim( x_min_eels, 5 )
    

# if True:
if False:

    # figure showing various important plots: 1. PCO DOS, 2. selected convolution
    pl.figure()
    
    pl.subplot( 2, 2, 1 )
    plot_DOSs( energy, DOSs_pr )
    pl.legend( ( 's', 'p', 'd', 'f' ), loc = 'best' )
    style_plot( convolved = False )
    pl.subplot( 2, 2, 2 )
    plot_convolutions( DOSs_pr_convolved, x = energy_convolved )
    pl.legend( ( 'p*f_Pr', 'd*f_Pr', 'p*f', 'd*f', 's*p', '', 'p*d', 'd*p', '' ), loc = 'best' )
    style_plot()
    pl.subplot( 2, 2, 3 )
    pl.plot( energy_convolved, con_sum_broadened, color = 'maroon', lw = 0.8, dashes = [ 2, 2 ] )
    pl.plot( energy_convolved, con_sum_pr_broadened, color = 'maroon' )
    pl.plot( experiment_ev, experiment_processed * exp_scalar, ls = 'None', marker = '.', ms = 1, color = 'grey' )
    pl.legend( ( 'CeO2', 'PCO', 'Exp.' ), loc = 'best' )
    # style_plot()
    # pl.xlim( x_min_eels, x_max_eels )
    pl.xlim( x_min_eels, 4.9 )
    pl.ylim( y_min_eels, y_max_eels )
    pl.xlabel( x_str )
    pl.ylabel( y_str )
    pl.minorticks_on()
    
    pl.subplot( 2, 2, 4 )
    pl.plot( energy_convolved, con_sum, color = 'blue' )
    pl.plot( energy_convolved, con_sum_pr, color = 'maroon' )
    pl.legend( ( 'CeO2', 'PCO' ), loc = 'best' )
    style_plot()

if plot_DOS_convolution_single_scattering[0]:
    
    # figure for paper showing DOS, convolved DOS up to 5 eV and sum convolve compared w/ data  
      
    output_path_single_scattering = 'C:/Users/willb/Dropbox/WillB/Crozier_Lab/Writing/2015_PCO10 interband states/figures/single-scattering-model/'
    output_file_single_scattering = 'single-scattering-model-broad-150825'
    
    pl.figure( figsize = ( 3.4, 7 ) )
    wf.slide_art_styles() # presentation styling
    fontsize = mpl.rcParams[ 'font.size' ]
    
    # pl.subplot( 2, 1, 1 )
    pl.subplot( 3, 1, 1 )
    plot_DOSs( energy, DOSs_pr )
    pl.legend( ( '$s_{CeO_{2}}$', '$p_{CeO_{2}}$', '$d_{CeO_{2}}$', '$f_{CeO_{2}}$', '$f_{Pr^{4+}}$' ), loc = 'upper left', fontsize = fontsize, labelspacing = .01, handletextpad = 0.2 )
    
    pl.xlim( x_min, x_max )
    pl.minorticks_on()
    wf.ticks_off( 'y' )
    
    pl.subplot( 3, 1, 2 )
    plot_convolutions( DOSs_pr_convolved, x = energy_convolved )
    # pl.legend( ( 's*p', 'p*s', 'p*d', 'p*f', 'p*f_Pr', 'd*p', 'd*f_Pr', 'd*f', 'f*d' ), loc = 'best' )
    pl.legend( ( '$p_{CeO_{2}}*f_{Pr^{4+}}$', '$d_{CeO_{2}}*f_{Pr^{4+}}$',
    '$p_{CeO_{2}}*f_{CeO_{2}}$', '$d_{CeO_{2}}*f_{CeO_{2}}$' ), loc = 'upper left',
    fontsize = fontsize, labelspacing = .01, handletextpad = 0.2 )
    
    pl.xlim( x_min_eels, 4.9 )
    pl.ylim( 0.02, 2.5 )
    pl.ylabel( y_str )
    pl.minorticks_on()
    wf.ticks_off( 'y' )
    
    # pl.subplot( 2, 1, 2 )
    pl.subplot( 3, 1, 3 )
    pl.plot( energy_convolved, con_sum_broadened, color = 'maroon', dashes = [ 2, 2 ] )
    pl.plot( energy_convolved, con_sum_pr_broadened, color = 'maroon' )
    pl.plot( experiment_ev, experiment_processed * exp_scalar, ls = 'None', marker = '.', ms = 0.8, color = 'grey' )
    pl.legend( ( r'$ \mathrm{CeO_{2}}$ model', 'PCO model', 'PCO experiment' ), loc = 'best', fontsize = fontsize, labelspacing = .01, handletextpad = 0.2 )
    
    pl.xlim( x_min_eels, x_max_eels )
    pl.xlim( x_min_eels, 4.9 )
    pl.ylim( 0, y_max_eels )
    pl.xlabel( x_str )
    pl.ylabel( '' )
    pl.minorticks_on()
    wf.ticks_off( 'y' )
    pl.tight_layout()
    
    if plot_DOS_convolution_single_scattering[1]:
        dots = plot_DOS_convolution_single_scattering[2]
        pl.savefig( output_path_single_scattering + output_file_single_scattering + '-' + str( dots ) + 'dpi.png', format = 'png', dpi = dots )


# if True:
if False:
    # figure for paper showing ceria and PCO DOS (symmetry projected)
    
    output_file_path_DOS_compare = 'C:/Crozier_Lab/Writing/2015_PCO10 interband states/figures/DOS-compare/'
    output_file_name_DOS_compare = 'DOS-compare'
    
    
    pl.figure( figsize = ( 3.4, 4.5 ) )
    wf.slide_art_styles() # presentation styling
    fontsize = mpl.rcParams[ 'font.size' ]
    
    pl.subplot( 2, 1, 1 ) # DOS w/out Pr state
    plot_DOSs_rotated( energy, DOSs_pr )
    pl.legend( ( '$s_{CeO_{2}}$', '$p_{CeO_{2}}$', '$d_{CeO_{2}}$', '$f_{CeO_{2}}$', '$f_{Pr^{4+}}$' ), loc = 'lower right', fontsize = fontsize, labelspacing = .01, handletextpad = 0.2 )
    
    pl.xlim( 0.02, 2.5 )
    pl.ylim( -1, 4 )
    pl.ylabel( x_str )
    pl.minorticks_on()
    wf.ticks_off( 'x' )
    
    pl.subplot( 2, 1, 2 ) # DOS w/out Pr state
    plot_DOSs_rotated( energy, DOSs_pr )
    pl.legend( ( '$s_{CeO_{2}}$', '$p_{CeO_{2}}$', '$d_{CeO_{2}}$', '$f_{CeO_{2}}$', '$f_{Pr^{4+}}$' ), loc = 'lower right', fontsize = fontsize, labelspacing = .01, handletextpad = 0.2 )
    
    pl.xlim( 0.02, 2.5 )
    pl.ylim( -1, 4 )
    pl.xlabel( y_str )
    pl.ylabel( x_str )
    pl.minorticks_on()
    wf.ticks_off( 'x' )

# pl.savefig( output_file_path_DOS_compare + output_file_name_DOS_compare + '-1000dpi.png', format = 'png', dpi = 1000 )


if DOS_compare_sum_reduced_shifted[0]:
    # figure for paper showing symmerty-summed PCO DOS with bottom Pr shifted +0.3eV
    
    output_file_path_DOS_compare_sum = 'C:/Users/willb/Dropbox/WillB/Crozier_Lab/Writing/2015_PCO10 interband states/figures/DOS-compare/DOS-compare-sum-reduced-shifted-150825/'
    output_file_name_DOS_compare_sum = 'DOS-compare-sum-reduced-shifted-150825'
    
    ce_4f_dashes = [6,2]    
    vb_dashes = [3,2]
    
    pl.figure( figsize = ( 3.4, 4.5 ) )
    # wf.slide_art_styles() # presentation styling
    fontsize = mpl.rcParams[ 'font.size' ]
    
    pl.subplot( 2, 1, 1 ) # DOS w/out Pr state
    pl.plot( un_f, energy, color = 'maroon', lw = 0.9, dashes = ce_4f_dashes )
    pl.plot( un_f_pr, energy, color = 'black', lw = 0.9, ls = '-' )
    pl.plot( DOSs_pr_sum, energy, color = 'grey', lw = 0.9, dashes = vb_dashes )
    pl.legend( ( r'$f_{Ce^{4+}}$', r'$f_{Pr^{4+}}$', 'VB' ), loc = 'lower right', fontsize = fontsize, labelspacing = .01, handletextpad = 0.2, frameon = False )
    
    pl.xlim( 0.02, 2.5 )
    pl.ylim( -2, 4 )
    pl.ylabel( x_str )
    pl.minorticks_on()
    wf.ticks_off( 'x' )
    pl.tight_layout()
    
    pl.subplot( 2, 1, 2 ) # DOS w/out Pr state
    pl.plot( un_f, energy, color = 'maroon', lw = 0.9, dashes = ce_4f_dashes )
    pl.plot( un_f_pr, energy + 0.3, color = 'black', lw = 0.9, ls = '-' )
    pl.plot( DOSs_pr_sum, energy, color = 'grey', lw = 0.9, dashes = vb_dashes )
    pl.legend( ( r'$f_{Ce^{4+}}$', r'$f_{Pr^{3+}}$', 'VB' ), loc = 'lower right', fontsize = fontsize, labelspacing = .01, handletextpad = 0.2, frameon = False )
    
    pl.xlim( 0.02, 2.5 )
    pl.ylim( -2, 4 )
    pl.xlabel( y_str )
    pl.ylabel( x_str )
    pl.minorticks_on()
    wf.ticks_off( 'x' )
    pl.tight_layout()

    if DOS_compare_sum_reduced_shifted[1]:
        dots = DOS_compare_sum_reduced_shifted[2]
        pl.savefig( output_file_path_DOS_compare_sum + output_file_name_DOS_compare_sum + '-' + str( dots ) + 'dpi.png', format = 'png', dpi = dots )

''' ########################### REFERENCES ###########################
1. http://stackoverflow.com/questions/6518811/interpolate-nan-values-in-a-numpy-array
2. http://stackoverflow.com/questions/3223043/how-do-i-sum-the-columns-in-2d-list
'''