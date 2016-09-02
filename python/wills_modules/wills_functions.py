''' ########################### IMPORT MODULES ########################### '''
import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import csv, imp, os
import wills_functions as wf
import datetime as dt

''' ############################### NOTES ################################ '''
'''
to reload a module:
>>>import imp
>>>imp.reload( module_name )
'''
    

''' ########################## normalize ########################## 

return list, 'curve', normalized to specified max value, 'normalized_max'

Example [CCO-XRD.py]:

ys = [ y_2p, y_2s, y_5p, y_5s, y_10p, y_10s, y_CaO, y_CaO2 ] 
norm_ys = []

for i in np.arange( len(ys) ):
    norm_ys.append( wf.normalize( ys[i], norm ) - ( 1.2 * i * norm ) )


ys is a list of lists to be normalized (e.g. stacking curves for figurs).
norm_ys is a list to be populated with normalized lists in ys.
ys[i] is the list to be normalized to the max value of norm.
'''

def normalize( curve, normalized_max ):
    curve_max = np.nanmax( curve )
    scalar = normalized_max / curve_max
    return curve * scalar
    

''' ########################## colors ########################## 

return custom colors as RGB tuple

Example [CCO-XRD.py]:

>>> cols = [ 'maroon', 'grey', 'black', wf.colors('dark_gold') ]

>>> pl.plot( x_CaO, norm_ys[6], color=cols[3], lw = width )

wf.colors() takes a name string of a custom color (defined in wills_functions.py)
and returns an RGB tuple (normalized to 1) which can be used in pl.plot()

to define new custom colors just add an entry to the dictionary in the function 
below
'''

def colors( color_name ):
    custom_colors_RGB = {
    'pale_gold': [255, 240, 155],
    'eth_blue': [31, 64, 122],
    'eth_green': [130, 190, 30],
    'dark_grey': [100, 100, 100]
    }
    RGB = custom_colors_RGB[ color_name ]
    normalized_RGB = [ x/255 for x in RGB ]
    return normalized_RGB
    

''' ########################## normal ########################## 

generate normal distribution

Example:

>>> bins_100 = np.linspace( 0, 100, 101 ) # bins for calcuating normal distribution
>>> mu, sigma = [ 13, 26, 62 ], [ 3, 7, 13 ] # mean concentration and std dev [pr, gd, ce]
>>> pr = normal( bins_100, mu[0], sigma[0] ) # calcuate Gaussian

ax is pl.gca()
sp1_maj_loc is a list of numbers which define the major tick intervals: [ x, y ]
'''

# add 'random sampling' result based on the measured mean and std dev.
def normal( bins, mean, stddev ):
    gaussian = 1 / ( stddev * np.sqrt( 2 * np.pi ) ) * np.exp( -( bins - mean )**2 / (2 * stddev**2 ) )
    return gaussian


''' ########################## major_ticks ########################## 

Applies axis limits to a pylab plot

Example:
>>> wf.major_ticks( ax, sp1_maj_loc )

ax is pl.gca()
sp1_maj_loc is a list of numbers which define the major tick intervals: [ x, y ]
'''

def major_ticks( ax, maj_locs, scientific=False ):
    if maj_locs[0]:
        ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( maj_locs[0] ) )
    if maj_locs[1]:
        ax.yaxis.set_major_locator( mpl.ticker.MultipleLocator( maj_locs[1] ) )
    if scientific:
        ax.yaxis.get_major_formatter().set_powerlimits((0, 1))
        ax.xaxis.get_major_formatter().set_powerlimits((0, 1))


''' ########################## clip_xy ########################## 

clips x and y data arrays according to the x axis limit values such that curves
do not extend beyond the y-axes. This addresses a rendering bug in the svg
backend of matplotlib. returns clipped x and y values arrays, and x axis limits
as a list which can be used in e.g. ax.set_xlim( lims_x_clip )

Example [CCO-XRD.py]:
>>> x_5p, y_5p, x_5p_lims = clip_xy( x_lims, d_exp[:,4], d_exp[:,5] )

lims_x is a list [ x_min, x_max ]
arr_x, arr_y are np arrays (not sure what the dimensional requirements are...?)
'''

def clip_xy( lims_x, arr_x, arr_y ):
    min_ind = np.where( arr_x > lims_x[0] )[0][0]
    max_ind = np.where( arr_x < lims_x[1] )[0][-1]
    x_clip = arr_x[ min_ind:max_ind ]
    y_clip = arr_y[ min_ind:max_ind ]
    lims_x_clip = [ x_clip[0], x_clip[-1] ]
    return x_clip, y_clip, lims_x_clip


''' ########################## ax_limits ########################## 

Applies axis limits to a pylab plot

Example:
>>> wf.ax_limits( sp1_lims )

sp1_lims is a list of lists containing x and y min and max [[x_min,x_max],[y_min,y_max]]
'''

def ax_limits( lims ):
    if lims[0]:
        pl.xlim( lims[0] )
    if lims[1]:
        pl.ylim( lims[1] )
    

''' ########################## ax_labels ########################## 

Applies axis labels to a pylab plot

Example:
>>> wf.ax_labels( sp1_ax_labs, pad )

sp1_ax_labs is a list of strings [ 'x_label', 'y_label' ]
pad is the labelpad, default is 0.5
'''

def ax_labels( labs, pad=0.5 ):
    if labs[0]:
        pl.xlabel( labs[0], labelpad=pad )
    if labs[1]:
        pl.ylabel( labs[1], labelpad=pad )
    

''' ########################## stack ########################## 

Shifts the top_curve vertically so its at the max of the bottom curve.

Example:
>>> pl.plot( d_ev, stack( d_off, d_on ) )

top_curve and bottom_curve are 1D arrays which are to be plotted together.
'''
    
def stack( top_curve, bottom_curve ):
    shifted_top = top_curve + np.max( bottom_curve ) - np.min( bottom_curve )
    return shifted_top


''' ########################## wills_mpl ########################## 

set rc params to customize matplotlib for will. This file in under git, 
matplotlibrc is not. This serves as the base level of customization for will,
and is analagous to hard-coding changes to matplotlibrc.
Usage:
>>> wf.wills_mpl()

I put this in a funciton called mpl_customizations() which sits in each figure
script so each figure can be customized futher.
'''

def wills_mpl( fontsize ):
    mpl.rc( 'lines', linewidth=1.0, mew=0.01, markersize=3 )
    # mpl.rc( 'pathces' )
    mpl.rc( 'font', family='sans-serif', serif='Arial', weight='normal',
        size=fontsize )
    # mpl.rc( 'text' )
    # mpl.rc( 'axes' )
    # mpl.rc( 'ticks' )
    # mpl.rc( 'grids' )
    mpl.rc( 'legend', fancybox=False, borderpad=0.1, labelspacing=0.1,
        fontsize=fontsize )
    # mpl.rc( 'figure' )
    mpl.rc( 'mathtext', default='regular' )

''' ########################## date_str ########################## 

generate a string with current date formatted 'XXXXYYZZ', where XXXX is year
YY is month and ZZ is day
Usage:
>>> today_date = wf.date_str( mill='' )

'''

def date_str( mill='' ):
    return str( dt.date.today() ).replace('-','').replace('20',mill)

''' ########################## save_fig ########################## 

save figure as .png or .svg.
Usage:
>>> wf.save_fig( output_file_name, subfolder_save=True )

'''
    
def save_fig( fig_dir, file_types, dots, output_file_name, anno,
    subfolder_save=True ):
    # create subfolder with date as name
    if subfolder_save:
        output_dir = fig_dir + wf.date_str() + '/'
        if not os.path.isdir( output_dir ):
            os.mkdir( output_dir )

    for file_type in file_types:
        if file_type == 'png':
            for dot in dots:
                output_name = wf.save_name( output_dir, output_file_name, anno,
                dot, file_type )
                pl.savefig( output_name, format=file_type, dpi=dot, 
                    transparent=True )
        elif file_type == 'svg':
                output_name = wf.save_name( output_dir, output_file_name, anno,
                False, file_type )
                pl.savefig( output_name, format=file_type, transparent=True )

''' ########################## save_name ########################## 

generate an output file name for saving figures.
Usage:
>>> wf.save_name( dir, name, anno, dpi, file_type )

'''

def save_name( dir, name, anno, dpi, file_type ):
    basename = dir + name
    date = '-' + str( dt.date.today() ).replace('-','').replace('20','')
    if dpi:
        dots = '-' + str( dpi ) + 'dpi'
    else:
        dots = ''
    outname = basename + date + anno + dots + '.' + file_type
    print( 'file name: ' + outname )
    return outname


''' ########################## ticks off ########################## 

turns off the ticks on the current plot's axis specified by argument. 
Usage:
>>> wf.ticks_off( axis )
axis = 'y' or 'x'
'''

def ticks_off( axis ):
    ax = pl.gca()
    if axis == 'y':
        ax.set_yticks([])
    elif axis == 'x':
        ax.set_xticks([])


''' ########################## phys_constant ########################## '''
''''returns physical constant with specified name and in specified units.
Usage:
>>>kb = wf.phys_constant( 'Boltzmann', 'eV/K' )
returns k_b in J/K if boolean_0 = true, or eV/K if boolean_1 = true.
'''

# def phys_constant( constant_name, units ):
    # contants = {
    #     'Boltzmann': {
    #         'eV/K': 8.61733e-5,
    #         'J/K': 
    #     },
    #     'Electronic charge': {
    #         'C': 1.602177e-19
    #     }
    # }

    # if constants[ constant_name[ units ] ]:
    #     return constants[ constant_name[ units ] ]
    # else
    #     print( constant_name + ' was not found.' )


''' ########################## elementary charge ########################## '''
''''returns Boltzmann constant in specified units.
Usage:
>>>k_b = wf.boltzmann( boolean_0, boolean_1 )
returns k_b in J/K if boolean_0 = true, or eV/K if boolean_1 = true.
'''

def electron_charge():
    return 1.60217657e-19 # coulombs


''' ########################## Boltzmann constant ########################## '''
''''returns Boltzmann constant in specified units.
Usage:
>>>k_b = wf.boltzmann( boolean_0, boolean_1 )
returns k_b in J/K if boolean_0 = true, or eV/K if boolean_1 = true.
'''

def boltzmann_constant( JperK, eVperK ):
    if JperK:
        return 1.3806488e-23
    elif eVperK:
        return 8.6173324e-5


''' ########################## list manipulation ########################## '''
''''returns list after manipulation of each element via math operations
Usage:
>>>list_after = wf.multiply_list( list, scalar )
returns list where each element is multiplied by scalar
'''

def multiply_list( list, scalar ):
    return [ i * scalar for i in list ]

def add_to_list( list, scalar ):
    return [ i + scalar for i in list ]


''' ########################## current_script_info() ########################## '''
''''returns the filename and storage directory of the script in which this 
function is called
Usage:
script_filename, script_direcetory_path = wf.current_script_info()

Requires: 
import os, inspect
'''
def current_script_info():
    import os, inspect
    script_filename = inspect.getfile( inspect.currentframe() )
    script_dirname = os.path.dirname( os.path.abspath ( script_filename ) )
    return script_filename, script_dirname


''' ########################## read_csv_2col() ########################## '''

''' imports 2 column (i.e. [ x_i, y_i ]) .csv file and returns columns. Requires
csv module.

Usage: x1, x2 = read_csv_2col( file_path )
file_path is path to .csv file with '.csv' included in text string.
**IMPORTANT** header rows are ignored via <code>if len(row) != 2:</code>, so 
make sure that the header rows do not have entries in the first two columns. 
header rows may have 1 or >2 entries.

REFS:
[1] https://thenewcircle.com/s/post/1572/python_for_beginners_reading_and_manipulating_csv_files#opening-a-csv-file
[2] https://docs.python.org/2/library/csv.html
'''
def read_csv_2col( file_path ):
    f = open( file_path ) # create a TextIOWrapper object
    d = csv.reader( f ) # create csv reader object
    x, y = [], [] # create blank lists to store datas
    for row in d: # iterate through rows of input .csv file
        if len( row ) == 2: # ignore row if it doesn't have (*only) 2 entries
#         need to convert to float!!!
            x.append( float( row[ 0 ] ) ) # append row entries to lists
            y.append( float( row[ 1 ] ) )
    
    return x, y # return lists containing .csv columns


'''
fills a figure object with data contained in vertical columns 
(see np.vstack().T) ranging between columns labelled col_0 to col_n. 
I.e. first column is the x-axis data and all other columns contain y-axis data.

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
def centered_annotation( x, y, string, color, fontsize='' ):
    pl.text( x, y, string, color = color, ha = 'center', va = 'center', fontsize = fontsize )
    
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

def hex_gold():
    return '#FFA500'
    
def slide_art_styles( ):
    # mpl.rcParams[ 'font.family' ] = 'Times New Roman'
    mpl.rcParams[ 'font.family' ] = 'Sans Serif'
    mpl.rcParams[ 'font.weight' ] = 'normal' # modify matplotlib defaults
    mpl.rcParams[ 'font.size' ] = 10
    mpl.rcParams[ 'lines.linewidth' ] = 1.5
#     mpl.rcParams[ 'mathtext.default' ] = 'regular'
    
def elsvier_art_styles( ):
#     mpl.rcParams[ 'font.family' ] = 'Times New Roman'
#     mpl.rcParams[ 'font.weight' ] = 'medium' # modify matplotlib defaults
#     mpl.rcParams[ 'font.size' ] = 7
    mpl.rcParams[ 'font.family' ] = 'Times New Roman'
    mpl.rcParams[ 'font.weight' ] = 'medium' # modify matplotlib defaults
    mpl.rcParams.update( { 'font.size' : 8 } )
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

# closes all open figures
def close_all():
    pl.close( 'all' )
    
# get key index of value(s) from np array. pass single value or tuple, returns list
def array_index( array, values ):
    try:
        key_indicies = []
        for value in values:
            key_index = np.where( array == value )[0][0]
            key_indicies.append( key_index )
        return key_indicies
        pl.close( 'all' )
    except:
        value_index = np.where( array == values )[0][0]
        return value_index
