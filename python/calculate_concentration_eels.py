import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
from os import listdir # listdir(dir_path) returns array of file names in dir_path
from os import mkdir
from os import path
##
k_CaCe, k_OCe = 1.89, 5.81

# specify path to directory of elemental map files
maps_dir = "c:/Dropbox/SOFC Electrolyte Project/Microscopy/141118_10Ca_ARM200kV/gb_maps/"
map_file_names = listdir( maps_dir ) # get map file names
common_sub_str = 'EELS'
sub_str_pattern = 'EELS_XX_'

# pluck 2-digit map ids (e.g. '00') from file names
map_ids = [] # list of map ids
for file_name in map_file_names:
    if np.core.defchararray.find( file_name, common_sub_str ):
        uniq_sub_index = np.core.defchararray.find( file_name, common_sub_str )
        uniq_id_index = uniq_sub_index + len( sub_str_pattern )
        map_ids.append( file_name[ uniq_id_index : uniq_id_index + 2 ] ) # pluck 2-digit map id from file name

# list(set()) removes duplicates, sorted() performs ascending sort
map_ids = sorted( list( set( map_ids ) ) )

def get_gb_id( file_name, sub_str ):
    gb_str_index = np.core.defchararray.find( file_name, sub_str )
    gb_id = file_name[ gb_str_index + len( sub_str ) ]
    return gb_id
    
if not path.isdir( maps_dir + 'calculated_concentrations' ):
    mkdir ( maps_dir + 'calculated_concentrations' )

for id in map_ids:
    if id.isdigit():
        file_group = [ ]
        
        for file_name in map_file_names:
            if file_name.__contains__( '_' + id + '_' ):
                file_group.append( maps_dir + file_name )
        
        CeM = np.loadtxt( file_group[0], skiprows = 3 )
        CaL = np.loadtxt( file_group[1], skiprows = 3 )
        OK = np.loadtxt( file_group[2], skiprows = 3 )
        
        gb_id = get_gb_id( file_group[0], '_gb' )
    
        x = CeM[ :, 0 ]
        
        i_CeM = CeM[ :, 1 ]
        i_CaL = CaL[ :, 1 ]
        i_OK = OK[ :, 1 ]
        
        kr_CaCe = i_CaL / i_CeM * k_CaCe
        kr_OCe = i_OK / i_CeM * k_OCe
        
        c_Ca_i = kr_CaCe / ( 1 + kr_CaCe )
        c_Ce_i = 1 - c_Ca_i
        c_O_i = 2 - c_Ca_i
        
        output_data = np.vstack( ( x, c_Ce_i, c_Ca_i, c_O_i ) )
        output_dir = maps_dir + 'calculated_concentrations/'
        output_file = 'map_' + id + '_gb_0' + gb_id + '.txt'
        head = 'gb_id: ' + gb_id + '\nmap_id: ' + id + '\nk_CaCe: ' + str( k_CaCe ) + '\nk_OCe ' + str( k_OCe )
        
        np.savetxt( output_dir + output_file, output_data.T, delimiter='\t', header=head, fmt='%10.3e', newline='\n')

# from wills_eels_modules import plot_gb_composition
# plot_gb_composition( output_dir )
##
# from wills_functions import pluck_sub_string_counter
# filename: 'map_xx_gb_y' where xx and yy are counters

data_dir = output_dir
map_files = listdir( data_dir )

def plot_multiple_1d( data ): # add styel arg for marks or lines or both, optional args for curve alignment
    columns = data.shape[1]
    x = data[ :, 0 ]
    pl.figure()
    for i in range( columns - 1 )
        pl.plot( x, data[ :, i ] )
    pl.show()

# gb_ids = []
gb_num = None
for file in map_files:
    gb_num_i = pluck_sub_string_counter( file, '_gb_', 2 )
    d = np.loadtxt( file )
    
    if gb_num_i == gb_num:
        cols = d.shape[1]
        x = d[ :, 0 ]
        for i in range( cols - 1 ):
            pl.plot( x, d[ :, i ] )
            
    else:
        pl.figure()
        cols = d.shape[1]
        x = d[ :, 0 ]
        for i in range( cols - 1 ):
            pl.plot( x, d[ :, i ] )
        
#     gb_ids.append( pluck_sub_string_counter( file, '_gb_', 2 ) )
    
# create figure with n_gb subplots

for gb in gb_ids:
    pl.figure()
    for file in map_files:
        if file.__contain__( '_gb_
    


'''
pluck a counter number from a string like a filename where file basename contains repeated pattern. For a string 'file1_gb_03', sub_str_pattern is '_gb_', counter length is 2 ('03' has two characters). Returns '03'.
'''
def pluck_sub_string_counter( string, sub_str_pattern, counter_length ):
#     if isinstance( string, str ) and string.__contain__( sub_string ) # check that both are str and one contains other
    if isinstance( string, str ) and string.__contain__( sub_str_pattern ):
        pattern_index = np.core.defchararray( string, sub_str_pattern )
        counter_index = string[ pattern_index + len( sub_str_pattern ) ]
        counter = string[ counter_index : counter_index + counter_length ]
        return counter



    
'''






equations for solving k-factor [2]
ca/cb = ia/ib * k
k = ca/cb * ib/ia

references
1. DM plugin called dumpSItotext
2. Williams and Carter 'Transmission Electron Microscopy, A Textbook for Materials Science'
'''
