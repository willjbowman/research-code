import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import wills_functions as wf
from os import listdir # listdir(dir_path) returns array of file names in dir_path
from os import mkdir
from os import path
##
# from wills_functions import pluck_sub_string_counter
# filename: 'map_xx_gb_y' where xx and yy are counters

# specify path to directory of elemental map files
maps_dir = "c:/Dropbox/SOFC Electrolyte Project/Microscopy/141118_10Ca_ARM200kV/gb_maps/calculated_concentrations/"
map_files = listdir( maps_dir ) # get map file names

pl.close( 'all' )

def label_and_save_current():
    ax = pl.gca()
    title = 'GB_' + str( gb_num )
    ax.set_title( title )
    ax.set_xlabel( 'distance (nm)' )
    ax.set_ylabel( 'Concentration' )
    
    if title != 'GB_None' :
        output_dir = path.join( maps_dir, 'plots/' )
        if not path.exists( output_dir ) :
            mkdir( output_dir )
        pl.savefig( output_dir + title + '.png', format = 'png', dpi = 500 )

gb_num = None
for file in map_files:
    if file.endswith( '.txt' ) :
        gb_num_i = wf.pluck_sub_string_counter( file, '_gb_', 2 )
        d = np.loadtxt( maps_dir + file )
    
#     wf.shift_curve( d, x, 0 )
        x = d[ :, 0 ]
        y = d[ :, 1 ]
        min_y = np.min( y )
        max_y = np.max( y )
        mean_y = np.mean( y )
        if ( max_y - mean_y ) > ( mean_y - min_y ) :
            yy = y.tolist()
            shift_index = yy.index( max_y )
            shift_value = x[ shift_index ]
        else:
            yy = y.tolist()
            shift_index = yy.index( min_y )
            shift_value = x[ shift_index ]
    
        col_num = map_files.index( file )
        col = wf.color_list( col_num )
        mark = wf.marker_list( col_num )
    
        if gb_num_i == gb_num:
            wf.plot_multiple_1d( d, color = col, shift = ( shift_value, 0 ), style = mark )
            
        else:
            # label previous figure if it exists
            label_and_save_current()
            # or create one if it doesn't
            pl.figure() # create new figure
            wf.plot_multiple_1d( d, color = col, shift = ( shift_value, 0 ), style = mark )
        
        gb_num = gb_num_i

# the last iteration will result in a figure that needs to be saved
label_and_save_current()
    
##

'''
equations for solving k-factor [2]
ca/cb = ia/ib * k
k = ca/cb * ib/ia

references
1. DM plugin called dumpSItotext
2. Williams and Carter 'Transmission Electron Microscopy, A Textbook for Materials Science'
'''
