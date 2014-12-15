import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
from os import listdir # listdir(dir_path) returns array of file names in dir_path
##

# specify path to directory of elemental map files
maps_dir = "c:/Dropbox/SOFC Electrolyte Project/Microscopy/141118_10Ca_ARM200kV/gb_maps/"
map_file_names = listdir( maps_dir ) # get map file names
map_ids = [ '05_grain2', '09_grain3', '13_grain4', '14_grain4' ]
C_Ce, C_Ca, C_O = 0.9, 0.1, 1.90 # molar concentrations

k_CaCe = []
k_OCe = []
for id in map_ids:
    file_group = []
    for file_name in map_file_names:
        if file_name.__contains__( id ):
            file_group.append( maps_dir + file_name ) # add filename to list of grouped names
    
    i_CeM = np.loadtxt( file_group[ 0 ], skiprows = 3 )
    i_CaL = np.loadtxt( file_group[ 1 ], skiprows = 3 )
    i_OK = np.loadtxt( file_group[ 2 ], skiprows = 3 )
    
    i_CeM[ :, 0 ] = 0
    i_CaL[ :, 0 ] = 0
    i_OK[ :, 0 ] = 0
    
    k_CaCe_i = C_Ca / C_Ce * np.sum( i_CeM ) / np.sum( i_CaL )
    k_OCe_i = C_O / C_Ce * np.sum( i_CeM ) / np.sum( i_OK )
    
    k_CaCe.append( k_CaCe_i )
    k_OCe.append( k_OCe_i )
    
'''
equations for solving k-factor [2]
ca/cb = ia/ib * k
k = ca/cb * ib/ia

references
1. DM plugin called dumpSItotext
2. Williams and Carter 'Transmission Electron Microscopy, A Textbook for Materials Science'
'''
