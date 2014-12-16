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

gb_num = None
for file in map_files:
    gb_num_i = wf.pluck_sub_string_counter( file, '_gb_', 2 )
    d = np.loadtxt( maps_dir + file )
    
    col_num = map_files.index( file )
    col = wf.color_list( col_num )
    
    if gb_num_i == gb_num:
        wf.plot_multiple_1d( d, color = col )
            
    else:
        pl.figure()
        wf.plot_multiple_1d( d, color = col )
        
    gb_num = gb_num_i
    

# from wills_eels_modules import plot_gb_composition
# plot_gb_composition( output_dir )
##

'''
equations for solving k-factor [2]
ca/cb = ia/ib * k
k = ca/cb * ib/ia

references
1. DM plugin called dumpSItotext
2. Williams and Carter 'Transmission Electron Microscopy, A Textbook for Materials Science'
'''
