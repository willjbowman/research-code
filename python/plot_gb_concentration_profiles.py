''' ########################### IMPORT MODULES ########################### '''
import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import wills_functions as wf
from os import listdir # listdir(dir_path) returns array of file names in dir_path
from os import mkdir
from os import path

##


''' ########################### USER-DEFINED ########################### '''
# from wills_functions import pluck_sub_string_counter
# filename: 'map_xx_gb_y' where xx and yy are counters

# specify path to directory of eels intensity map files and label for output files

# maps_dir = "c:/Dropbox/SOFC Electrolyte Project/Microscopy/141118_10Ca_ARM200kV/gb_maps_141229/150218_scaled_StdK-edx_50acqK-eels/"
# maps_label = '10Ca_' 

# maps_dir = "c:/Dropbox/SOFC Electrolyte Project/Microscopy/140821_5CaDC_ARM200kV/gb_maps_141230/150218_scaled_StdK-edx_50acqK-eels/"
# maps_label = '5CaDC_'

maps_dir = "c:/Dropbox/SOFC Electrolyte Project/Microscopy/141007_2Ca_ARM200kV/gb_maps_141230/150218_scaled_StdK-edx_50acqK-eels/"
maps_label = '2Ca_'

I_ratio, C_ratio, C_ion = 'EELS intensity ratio', 'EELS concentration ratio', 'EELS concentration'
I_ratio_col_0, I_ratio_col_1, C_ratio_col_0, C_ratio_col_1  = 4, 6, 6, 8
C_col_0, C_col_1 = 8, 11

''' ########################### FUNCTIONS ########################### '''

def label_current_axis( title, x_label, y_label ) :
    ax = pl.gca()
    ax.set_title( title )
    ax.set_xlabel( x_label )
    ax.set_ylabel( y_label )
    
def save_current_figure( ax_title='GB_None' ):
    if ax_title != 'GB_None' :
        output_dir = path.join( maps_dir, 'plots/' )
        if not path.exists( output_dir ) :
            mkdir( output_dir )
        pl.savefig( output_dir + ax_title + '.png', format = 'png', dpi = 500 )
    
    
''' ########################### MAIN SCRIPT ########################### '''

map_files = listdir( maps_dir ) # get map file names

pl.close( 'all' ) # close all open figures

gb_num = None
for file in map_files: # iterate through items in map data directory
    if file.endswith( '.txt' ) : # check that item is a file, not a directory 
        gb_num_i = wf.pluck_sub_string_counter( file, '_gb_', 1 ) # get gb number
        d = np.loadtxt( maps_dir + file ) # load data file
    
#     wf.shift_curve( d, x, 0 )
        # shift curves to center gb at zero
        x = d[ :, 0 ]
        y = d[ :, 3 ]
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
    
        '''this is not so good bc curves look the same and are hard to discern'''
        col_num = map_files.index( file ) # get index of file in directory
        mark_color = wf.color_list( col_num ) # pick a color from list
        mark = wf.marker_list( col_num ) # pick a marker from list
        
        ax_title = maps_label + 'GB_' + str( gb_num ) # create axis title with info about linescan
        x_label = 'distance (nm)' # define axis x label
        
        '''create a plot for each gb'''
    
        '''this logic plots linescans together with others from same grain boundary'''
        if gb_num_i == gb_num: # if data is from current gb plot along side on current figure
            pl.subplot( 1, 3, 1 ) # subplot for integrated intensity ratio
            wf.plot_multiple_1d( d, I_ratio_col_0, I_ratio_col_1, color = mark_color, shift = ( shift_value, 0 ), style = mark )
            label_current_axis( ax_title, x_label, I_ratio )
            
            pl.subplot( 1, 3, 2 ) # subplot for concentration ratio
            wf.plot_multiple_1d( d, C_ratio_col_0, C_ratio_col_1, color = mark_color, shift = ( shift_value, 0 ), style = mark )
            label_current_axis( ax_title, x_label, C_ratio )
            
            pl.subplot( 1, 3, 3 ) # subplot for concentration
            wf.plot_multiple_1d( d, C_col_0, C_col_1, color = mark_color, shift = ( shift_value, 0 ), style = mark )
            label_current_axis( ax_title, x_label, C_ion )
            
        else: # if data is from new gb save current and create new figure
            # label previous figure if it exists
            save_current_figure( ax_title )
            # create one if it doesn't
            pl.figure( figsize = ( wf.mm2in( 300 ), wf.mm2in( 100 ) ) ) # create new figure
            
            pl.subplot( 1, 3, 1 ) # subplot for integrated intensity ratio
            wf.plot_multiple_1d( d, I_ratio_col_0, I_ratio_col_1, color = mark_color, shift = ( shift_value, 0 ), style = mark )
            label_current_axis( ax_title, x_label, 'EELS intensity ratio' )
            
            pl.subplot( 1, 3, 2 ) # subplot for concentration ratio
            wf.plot_multiple_1d( d, C_ratio_col_0, C_ratio_col_1, color = mark_color, shift = ( shift_value, 0 ), style = mark )
            label_current_axis( ax_title, x_label, 'EELS concentration ratio' )
            
            pl.subplot( 1, 3, 3 ) # subplot for concentration
            wf.plot_multiple_1d( d, C_col_0, C_col_1, color = mark_color, shift = ( shift_value, 0 ), style = mark )
            label_current_axis( ax_title, x_label, 'EELS concentration' )
        
        gb_num = gb_num_i # reset gb id counter

# the last iteration will result in a figure that needs to be saved
save_current_figure( ax_title )
    
    
''' ########################### REFERENCES ########################### '''

'''
equations for solving k-factor [2]
ca/cb = ia/ib * k
k = ca/cb * ib/ia

references
1. DM plugin called dumpSItotext
2. Williams and Carter 'Transmission Electron Microscopy, A Textbook for Materials Science'

'''
