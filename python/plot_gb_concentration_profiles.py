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

maps_dir = "c:/Dropbox/SOFC Electrolyte Project/Microscopy/141118_10Ca_ARM200kV/gb_maps_141229/calculated_concentrations/"
maps_label = '10Ca_' 

# maps_dir = "c:/Dropbox/SOFC Electrolyte Project/Microscopy/140821_5CaDC_ARM200kV/gb_maps_141230/calculated_concentrations/"
# maps_label = '5CaDC_'

# maps_dir = "c:/Dropbox/SOFC Electrolyte Project/Microscopy/141007_2Ca_ARM200kV/gb_maps_141230/calculated_concentrations/"
# maps_label = '2Ca_'


''' ########################### FUNCTIONS ########################### '''

def label_and_save_current():
    ax = pl.gca()
    title = 'GB_' + str( gb_num )
    ax.set_title( maps_label + title )
    ax.set_xlabel( 'distance (nm)' )
    ax.set_ylabel( 'Concentration' )
    
    if title != 'GB_None' :
        output_dir = path.join( maps_dir, 'plots/' )
        if not path.exists( output_dir ) :
            mkdir( output_dir )
        pl.savefig( output_dir + maps_label + title + '.png', format = 'png', dpi = 500 )
    
    
''' ########################### MAIN SCRIPT ########################### '''

map_files = listdir( maps_dir ) # get map file names

pl.close( 'all' ) # close all open figures

gb_num = None
for file in map_files: # iterate through items in map data directory
    if file.endswith( '.txt' ) : # check that item is file, not directory 
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
    
        col_num = map_files.index( file )
        col = wf.color_list( col_num )
        mark = wf.marker_list( col_num )
    
        if gb_num_i == gb_num: # if data is from current gb plot along side on current figure
            wf.plot_multiple_1d( d, 3, 6, color = col, shift = ( shift_value, 0 ), style = mark )
            
        else: # if data is from new gb save current and create new figure
            # label previous figure if it exists
            label_and_save_current()
            # or create one if it doesn't
            pl.figure() # create new figure
            wf.plot_multiple_1d( d, 3, 6, color = col, shift = ( shift_value, 0 ), style = mark )
        
        gb_num = gb_num_i # reset gb id counter

# the last iteration will result in a figure that needs to be saved
label_and_save_current()
    
    
''' ########################### REFERENCES ########################### '''
    
'''
equations for solving k-factor [2]
ca/cb = ia/ib * k
k = ca/cb * ib/ia

references
1. DM plugin called dumpSItotext
2. Williams and Carter 'Transmission Electron Microscopy, A Textbook for Materials Science'

'''
