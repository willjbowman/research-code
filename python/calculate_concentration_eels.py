import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import wills_functions as wf
from os import listdir # listdir(dir_path) returns array of file names in dir_path
from os import mkdir
from os import path
##
k_CaCe, k_OCe = 1.89, 5.81 # calculated from 10Ca 2d scans (x spectra)

# specify path to directory of elemental map files
maps_dir = "c:/Dropbox/SOFC Electrolyte Project/Microscopy/140821_5CaDC_ARM200kV/gb_maps_141226/"
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

def calculate_concentration( i_CeM, i_CaL, i_OK ) :
    kr_CaCe = i_CaL / i_CeM * k_CaCe
    kr_OCe = i_OK / i_CeM * k_OCe
        
    c_Ca_i = kr_CaCe / ( 1 + kr_CaCe )
    c_Ce_i = 1 - c_Ca_i
    c_O_i = 2 - c_Ca_i
    
    return c_Ca_i, c_Ce_i, c_O_i

        
def save_concentration_map( x, i_Ca_Ce, i_O_Ce, c_Ce_i, c_Ca_i, c_O_i, maps_dir, id, gb_id, k_CaCe, k_OCe ) :         
    output_data = np.vstack( ( x, i_Ca_Ce, i_O_Ce, c_Ce_i, c_Ca_i, c_O_i ) )
    output_dir = maps_dir + 'calculated_concentrations/'
    output_file = 'map_' + id + '_gb_' + gb_id + '.txt'
    head = 'gb_id: ' + gb_id + '\nmap_id: ' + id + '\nk_CaCe: ' + str( k_CaCe ) + '\nk_OCe ' + str( k_OCe )
    head = head + '\ndist (nm)\tI_Ca/I_Ce\tI_OK/I_Ce\t[Ce]\t[Ca]\t[O]'
        
    np.savetxt( output_dir + output_file, output_data.T, delimiter='\t', header=head, fmt='%10.3e', newline='\n')

for id in map_ids:
    if id.isdigit():
        file_group = [ ]
        
        for file_name in map_file_names:
            if file_name.__contains__( '_' + id + '_' ):
                file_group.append( maps_dir + file_name )
                
        # get gb id from file name
        # gb_id = get_gb_id( file_group[0], '_gb' )
        gb_id = wf.pluck_sub_string_counter( file_group[ 0 ], '_gb', 2 )
        
        screening_map = np.loadtxt( file_group[1], skiprows = 3 )
        # check map dimensions for 1d or 2d spectrum images
        map_cols = screening_map.shape[ 1 ]
        
        if map_cols > 2 :
            # 2d map
            CeM = np.loadtxt( file_group[1], skiprows = 3 ) # load concentration maps data
            CaL = np.loadtxt( file_group[0], skiprows = 3 )
            OK = np.loadtxt( file_group[2], skiprows = 3 )
            for i in range( 1, map_cols ) :
                x = CeM[ :, 0 ] # distance exported from DM as 1st column
                i_CeM = CeM[ :, i ]
                i_CaL = CaL[ :, i ]
                i_OK = OK[ :, i ]
                
                i_Ca_Ce = i_CaL / i_CeM
                i_O_Ce = i_OK / i_CeM
                
                c_Ca_i, c_Ce_i, c_O_i = calculate_concentration( i_CeM, i_CaL, i_OK )
                
                id_counter = 0.1 # create subcounter string for file name
                id_int = float( id ) + id_counter
                id_form = '%.1f' % id_int
                id = id_form
#                 print( id_float, id_int, id )
                
                # save
                save_concentration_map( x, i_Ca_Ce, i_O_Ce, c_Ce_i, c_Ca_i, c_O_i, maps_dir, id, gb_id, k_CaCe, k_OCe )
        else :
            # 1d map
            x = CeM[ :, 0 ] # distance exported from DM as 1st column
            CeM = np.loadtxt( file_group[1] ) # load concentration maps data
            CaL = np.loadtxt( file_group[0] )
            OK = np.loadtxt( file_group[2] )
            i_CeM = CeM[ :, 1 ]
            i_CaL = CaL[ :, 1 ]
            i_OK = OK[ :, 1 ]
            
            c_Ca_i, c_Ce_i, c_O_i = calculate_concentration( i_CeM, i_CaL, i_OK )
            
            # save
            save_concentration_map( x, c_Ce_i, c_Ca_i, c_O_i, maps_dir, id, gb_id, k_CaCe, k_OCe )
