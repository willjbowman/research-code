''' ########################### IMPORT MODULES ########################### '''
import numpy as np
import pylab as pl
import matplotlib as mpl
import wills_functions as wf

'''
to reload a module:

import imp
imp.reload( module_name )
'''

'''
fills a figure object with data contained in vertical columns (see np.vstack().T) ranging between columns labelled col_0 to col_n. I.e. first column is the x-axis data and all other columns contain y-axis data.

Example(s): python/plot_gb_concentration_profiles.py
'''
def plot_multiple_1d( data, col_0, col_n, color='', style='', shift='' ):
    columns = data.shape[1]
    x = data[ :, 0 ]
    
    if len( shift ) == 2 :
        shift_value = shift[ 0 ]
        shift_center = shift[ 1 ]
        x = x + ( shift_center - shift_value )
    
    for i in range( col_0, col_n ):
        pl.plot( x, data[ :, i ], color = color, marker = style )
        pl.minorticks_on()
    pl.show()
    
def marker_list( ind ):
    markers = [ 'o', 'v', '^', 's', 'D', 'x', '+', '*' ]
    markers = markers + markers + markers + markers + markers
    return markers[ ind ]
    
def color_list( ind ):
    colors = [ 'black', 'red', 'blue', 'green', 'magenta', 'cyan' ]
    colors = colors + colors + colors + colors + colors
    return colors[ ind ]
    
'''
pluck a counter pattern (e.g. an incrementing number in filenames) from a string. For a string 'files_gb_03', sub_pattern is '_gb_', counter length is 2 ('03' has two characters). Returns '03'.

Example(s): python/plot_gb_concentration_profiles.py
'''
def pluck_sub_string_counter( string, sub_pattern, counter_length ):
    #     if isinstance( string, str ) and string.__contain__( sub_string ) # check that both are str and one contains other
    if isinstance( string, str ) and string.__contains__( sub_pattern ):
        pattern_index = np.core.defchararray.find( string, sub_pattern )
        counter_index = pattern_index + len( sub_pattern )
        counter = string[ counter_index : counter_index + counter_length ]
        return counter

# add a text annotation to a plot. centered at x, y (in data coordinates), 
# string is the text, color is the text color. REQUIRES PYLAB
def centered_annotation( x, y, string, color ):
    pl.text( x, y, string, color = color, ha = 'center', va = 'center' )
    
# plot column 1 vs. column 2
def plot_2col_txt( file_name, close_all ):
    d = np.loadtxt( file_name )
    if close_all:
        pl.close( 'all' )
    x, y = d.T
    pl.plot( x, y )
    
def plot_xy( x, y ):
    pl.figure()
    pl.plot( x, y )
#     pl.show()

# output common image sizes as tubple of inches for use in pl.figure( figsize = ( 6, 6 ) )
# def elsevier_artwork_sizing( size_key ):
#     one_col_width, three_halves_col_width, two_col_width = 90/25.4, 140/25.4, 190/25.4 # mm to in
# 
#     size_tuples = { 
#         '1' : ( one_col_width, one_col_width ),
#         '1.5' : ( three_halves_col_width, three_halves_col_width ),
#         '2' : ( two_col_width, two_col_width )
#     }
#         
#     size_tuples.get( size_key )
# 
# def fig_size( height_cols, width_cols ):
    
    
#     height_mm = 
#     width_inches = 
#     return ( height_inches * height_cols, width_inches * width_cols )
    
def slide_art_styles( ):
    mpl.rcParams[ 'font.family' ] = 'Times New Roman'
    mpl.rcParams[ 'font.weight' ] = 'normal' # modify matplotlib defaults
    mpl.rcParams[ 'font.size' ] = 10
#     mpl.rcParams[ 'mathtext.default' ] = 'regular'
    
def elsvier_art_styles( ):
    mpl.rcParams[ 'font.family' ] = 'Times New Roman'
    mpl.rcParams[ 'font.weight' ] = 'medium' # modify matplotlib defaults
    mpl.rcParams[ 'font.size' ] = 7
#     mpl.rcParams[ 'mathtext.default' ] = 'regular'
    
# normalize two spectra, shrink the one with more counts to have same max val as smaller one
def normalize_to_max( y0, y1 ):
    y0_max, y1_max = np.nanmax( y0 ), np.nanmax( y1 )
    if y0_max > y1_max: # y0 is larger
        scale = y1_max / y0_max # small_max / large_max
        
        y0_norm = y0 * scale # scale large to have max val = small_max
        y1_norm = y1
        
        
    else: # y1 is larger
        scale = y0_max / y1_max # small_max / large_max
        
        y0_norm = y0
        y1_norm = scale * y1 # scale large to have max val = small_max
        
    return y0_norm, y1_norm
    
# convert mm to in
def mm2in( mm ):
    inch = mm / 25.4
    return inch
    
# add letter label (e.g. '(a)') to upper left corner of current axis
def add_letter_label( fractional_offset, string, color ):
    axis = pl.gca() # get current axis
    x_min, x_max = axis.get_xlim() # query axis limits, store as variables
    y_min, y_max = axis.get_ylim()
    x_coord = x_min + fractional_offset * ( x_max - x_min ) # calculate label coordinates
    y_coord = y_max - fractional_offset * ( y_max - y_min )
    wf.centered_annotation( x_coord, y_coord, string, color ) # add centered text annotation

# create a step function of step width fwhm and height max and minimum of zero
def step_function( y, fwhm, max ):
    fwqm = fwhm / 2
    function = np.piecewise( y, 
        [ ( y >= -fwqm ) & ( y <= fwqm ), ( y < -fwqm ) & ( y > fwqm ) ],
        [ max, 0 ] )
    return function

# return array of lorenztian function with FWHM [r] over range [x]
def lorentzianate( x, r ):
    lorentzian = 1 / ( x ** 2 + r ** 2 )
    reversed_lorenzian = lorentzian[::-1] # reverse it
#     maxima = np.nanmax( lorentzian ) + np.nanmin( lorentzian ) # set a maxima value
#     lorentzian_180 = np.append( np.array( [ maxima ] ), lorentzian ) # append
    lorentzian = np.insert( lorentzian, 0, reversed_lorenzian ) # prepend
    return lorentzian

# return x' and y' of function x, y rotated angle in radians ang_rads
def rotate_func( x, y, ang_rads ) :
    x_rotated = x * np.cos( ang_rads ) - y * np.sin( ang_rads )
    y_rotated = x * np.sin( ang_rads ) + y * np.cos( ang_rads )
    return x_rotated, y_rotated