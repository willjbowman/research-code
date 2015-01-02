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
k_CaCe, k_OCe = 0.593, 2.999 # k-factors calculated from 10Ca 2d scans (x spectra)

output_dir_name = 'quantification_results' # name of output directory for results 

# specify path to directory of elemental map files
maps_dir = "c:/Dropbox/SOFC Electrolyte Project/Microscopy/141118_10Ca_ARM200kV/gb_maps_141229/"
# maps_dir = "c:/Dropbox/SOFC Electrolyte Project/Microscopy/140821_5CaDC_ARM200kV/gb_maps_141230/"
# maps_dir = "c:/Dropbox/SOFC Electrolyte Project/Microscopy/141007_2Ca_ARM200kV/gb_maps_141230/"

# specify load order,z, of each element in the map (see np.loadtxt( filegroup[ z ] )
z_Ca, z_O, z_Ce = 1, 2, 0

common_sub_str = 'EELS' # define common patterns to locate unique file IDs
sub_str_pattern = 'EELS_XX_'


''' ########################### FUNCTIONS ########################### '''
# calculate elemental concentrations from assumed chemical formulae and composition ratios ([A]/[B]*k_AB)
def calculate_concentration( c_Ca_Ce, c_O_Ce ):
    c_Ca_i = c_Ca_Ce / ( 1 + c_Ca_Ce ) #Ca concentration (assume [Ca] = 1 - [Ce])
    c_O_i = - c_O_Ce / ( 1 - c_O_Ce ) #O concentration (assume [Ce] = [O] - 1)
    c_Ce_i = 1 - c_Ca_i #Ce concentration ([Ce] = 1 - [Ca]).
    
    return c_Ca_i, c_Ce_i, c_O_i

        
def save_output_file( x, i_Ca_Ce, i_O_Ce, c_Ca_Ce, c_O_Ce, c_Ce_i, c_Ca_i, c_O_i, maps_dir, id, gb_id, k_CaCe, k_OCe ) :         
    output_data = np.vstack( ( x, i_Ca_Ce, i_O_Ce, c_Ca_Ce, c_O_Ce, c_Ce_i, c_Ca_i, c_O_i ) )
    output_dir = maps_dir + output_dir_name + '/'
    output_file = 'map_' + id + '_gb_' + gb_id + '.txt'
    head = 'gb_id: ' + gb_id + '\nmap_id: ' + id + '\nk_CaCe: ' + str( k_CaCe ) + '\nk_OCe ' + str( k_OCe )
    head = head + '\ndist (nm)\tI_Ca/I_Ce\tI_OK/I_Ce\tC_Ca/C_Ce\tC_OK/C_Ce\t[Ce]\t[Ca]\t[O]'
        
    np.savetxt( output_dir + output_file, output_data.T, delimiter='\t', header=head, fmt='%10.3e', newline='\n')
    
    
''' ########################### MAIN SCRIPT ########################### '''
map_file_names = listdir( maps_dir ) # get map file names

# pluck 2-digit map ids (e.g. '00') from file names
map_ids = [] # list of map ids
for file_name in map_file_names:
    if np.core.defchararray.find( file_name, common_sub_str ): #if find sub string
        uniq_sub_index = np.core.defchararray.find( file_name, common_sub_str ) #get substr index
        uniq_id_index = uniq_sub_index + len( sub_str_pattern ) #get uniq ID index
        map_ids.append( file_name[ uniq_id_index : uniq_id_index + 2 ] ) # pluck 2-digit map id from file name

# list(set()) removes duplicates, sorted() performs ascending sort
map_ids = sorted( list( set( map_ids ) ) )
    
if not path.isdir( maps_dir + output_dir_name ): #create dir if not exists
    mkdir ( maps_dir + output_dir_name )

for id in map_ids: # iterate through unique map ids
    if id.isdigit(): # check that map id is a number
        file_group = [ ] # create container for map file names w/ like ids
        
        for file_name in map_file_names: # iterate through map file names in directory
            if file_name.__contains__( '_' + id + '_' ): # check if file name contains map id
                file_group.append( maps_dir + file_name ) # store file paths of maps w/ like id
                
        # get gb id from file name. (different from map file id; could have mulitple maps per gb.) 
        gb_id = wf.pluck_sub_string_counter( file_group[ 0 ], '_gb', 1 )
        
        screening_map = np.loadtxt( file_group[1], skiprows = 3 ) # load map file to check dimensions
        # check map dimensions to verify if 1d or 2d spectrum image
        map_cols = screening_map.shape[ 1 ]
        
        if map_cols > 2 : # if > 2 columns map is 2d spectrum image
            CeM = np.loadtxt( file_group[ z_Ce ], skiprows = 3 ) # load eels integrated intesity maps data
            CaL = np.loadtxt( file_group[ z_Ca ], skiprows = 3 )
            OK = np.loadtxt( file_group[ z_O ], skiprows = 3 )
            
            for i in range( 1, map_cols ) : # create 1d linescan from each row of 2d spectrum image
            
                # process_integrated_intensity( CeM, CaL, OK, i ) :
    
                x = CeM[ :, 0 ] # distance exported from DM as 1st column
                i_CeM = CeM[ :, i ] # integrated eels intensity from ith row of 2d SI
                i_CaL = CaL[ :, i ]
                i_OK = OK[ :, i ]
                
                # scaling factors need to be integrated here
                
                i_Ca_Ce = i_CaL / i_CeM # calculate integrated intensity ratios
                i_O_Ce = i_OK / i_CeM
                
                c_Ca_Ce = i_Ca_Ce * k_CaCe # calculate concentration ratios from ...
                c_O_Ce = i_O_Ce * k_OCe # integrated intensity ratios and k-factors

                # calculate concentrations from assumed* chemical formulae
                c_Ca_i, c_Ce_i, c_O_i = calculate_concentration( c_Ca_Ce, c_O_Ce )
                
                id_counter = 0.1 # create subcounter string for file name
                id_int = float( id ) + id_counter
                id_form = '%.1f' % id_int
                id = id_form
#                 print( id_float, id_int, id )
                
                # save
                save_output_file( x, i_Ca_Ce, i_O_Ce, c_Ca_Ce, c_O_Ce, c_Ce_i, c_Ca_i, c_O_i, maps_dir, id, gb_id, k_CaCe, k_OCe )
                
        else : # 1d map
            CeM = np.loadtxt( file_group[ z_Ce ] ) # load concentration maps data
            CaL = np.loadtxt( file_group[ z_Ca ] )
            OK = np.loadtxt( file_group[ z_O ] )
            
            # process_integrated_intensity( CeM, CaL, OK, 1 ) :
                
            x = CeM[ :, 0 ] # distance exported from DM as 1st column
            i_CeM = CeM[ :, 1 ]
            i_CaL = CaL[ :, 1 ]
            i_OK = OK[ :, 1 ]
                
            # scaling factors need to be integrated here
            
            i_Ca_Ce = i_CaL / i_CeM # calculate integrated intensity ratios
            i_O_Ce = i_OK / i_CeM
            
            c_Ca_Ce = i_Ca_Ce * k_CaCe # calculate concentration ratios from ...
            c_O_Ce = i_O_Ce * k_OCe # integrated intensity ratios and k-factors

            # calculate concentrations from assumed* chemical formulae
            c_Ca_i, c_Ce_i, c_O_i = calculate_concentration( c_Ca_Ce, c_O_Ce )
            
            # save - should output intensity ratio (after scaling/splicing), concentration ratio at minimnum)
            save_output_file( x, i_Ca_Ce, i_O_Ce, c_Ca_Ce, c_O_Ce, c_Ce_i, c_Ca_i, c_O_i, maps_dir, id, gb_id, k_CaCe, k_OCe )
