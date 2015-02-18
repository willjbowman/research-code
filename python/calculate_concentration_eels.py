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
k_CaCe, k_OCe, k_CaO, k_OCa = 5.935e-1, 2.999, 1.982e-1, 5.202 # k-factors calculated from 10Ca 2d scans (x spectra)

output_dir_name = 'quantification_results_scaled_OCa' # name of output directory for results 

# specify path to directory of elemental map files
# specify load order,z, of each element in the map (see np.loadtxt( filegroup[ z ] )

maps_dir = "c:/Dropbox/SOFC Electrolyte Project/Microscopy/141118_10Ca_ARM200kV/gb_maps_141229/"
z_Ca, z_O, z_Ce = 1, 2, 0
# dictionary callable using map id as key (12eV integration window used)
# scalar is low/high; need to multiply high by scalar to make sections equal
Ce_scalar = { '00' : 0.972, '01' : 0.972, '03' : 0.994, '04' : 0.971, '06' : 0.976,
 '07' : 0.976, '08' : 0.975, '10' : 0.976, '11' : 0.974, '12' : 0.982 }

# maps_dir = "c:/Dropbox/SOFC Electrolyte Project/Microscopy/140821_5CaDC_ARM200kV/gb_maps_141230/"
# z_Ca, z_O, z_Ce = 0, 2, 1
# Ce_scalar = { '01' : 0.781, '02' : 0.781 }

# maps_dir = "c:/Dropbox/SOFC Electrolyte Project/Microscopy/141007_2Ca_ARM200kV/gb_maps_141230/"
# z_Ca, z_O, z_Ce = 0, 2, 1
# Ce_scalar = {}

common_sub_str = 'EELS' # define common patterns to locate unique file IDs
sub_str_pattern = 'EELS_XX_'


''' ########################### FUNCTIONS ########################### '''
# calculate elemental concentrations from assumed chemical formulae and composition ratios ([A]/[B]*k_AB)
def calculate_concentration( c_Ca_Ce, c_O_Ce, c_O_Ca ):
    c_Ca_i = c_Ca_Ce / ( 1 + c_Ca_Ce ) # Ca concentration (assume [Ca] = 1 - [Ce])
    c_Ce_i = 1 - c_Ca_i # Ce concentration ([Ce] = 1 - [Ca])
    c_O_i_Ce = c_O_Ce * c_Ce_i # O concentration (from EELS O/Ce concentration ratio)
    c_O_i_Ca = c_O_Ca * c_Ca_i # O concentration (from EELS O/Ca concentration ratio)
    # can you do a weigthed average based on the eels intensities??
    
    return c_Ca_i, c_Ce_i, c_O_i_Ce, c_O_i_Ca

        
def save_output_file( x, i_Ca_Ce, i_O_Ce, i_O_Ca, c_Ca_Ce, c_O_Ce, c_O_Ca, c_Ca_i, c_Ce_i, c_O_i_Ce, c_O_i_Ca, maps_dir, id, gb_id, k_CaCe, k_OCe, k_OCa ) :         
    output_data = np.vstack( ( x, i_Ca_Ce, i_O_Ce, i_O_Ca, c_Ca_Ce, c_O_Ce, c_O_Ca, c_Ca_i, c_Ce_i, c_O_i_Ce, c_O_i_Ca ) )
    output_dir = maps_dir + output_dir_name + '/'
    output_file = 'map_' + id + '_gb_' + gb_id + '.txt'
    head = 'gb_id: ' + gb_id + '\nmap_id: ' + id + '\nk_CaCe: ' + str( k_CaCe ) + '\nk_OCe ' + str( k_OCe ) + '\nk_OCa ' + str( k_OCa )
    head = head + '\ndist (nm) \tI_CaL/I_CeM \tI_OK/I_CeM \tI_OK/I_CaL \tC_CaL/C_CeM \tC_OK/C_CeM \tC_OK/C_CaL \t[Ca] \t[Ce] \t[O_Ce] \t[O_Ca]'
        
    np.savetxt( output_dir + output_file, output_data.T, delimiter='\t', header=head, fmt='%10.3e', newline='\n')
    
def process_integrated_intensity( CeM, CaL, OK, i, k_CaCe, k_OCe, k_OCa, Ce_scale_factor ) :
    x = CeM[ :, 0 ] # distance exported from DM as 1st column
    i_CeM = CeM[ :, i ] # integrated eels intensity from ith row of 2d SI
    i_CaL = CaL[ :, i ]
    i_OK = OK[ :, i ]
    
    i_CeM = i_CeM * Ce_scale_factor # 'id' is manipulated in this loop, get Ce_scalar val outside of loop
    
    i_Ca_Ce = i_CaL / i_CeM # calculate integrated intensity ratios
    i_O_Ce = i_OK / i_CeM
    i_O_Ca = i_OK / i_CaL
    
    c_Ca_Ce = i_Ca_Ce * k_CaCe # calculate concentration ratios from ...
    c_O_Ce = i_O_Ce * k_OCe # integrated intensity ratios and k-factors
    c_O_Ca = i_O_Ca * k_OCa
    
    return x, i_Ca_Ce, i_O_Ce, i_O_Ca, c_Ca_Ce, c_O_Ce, c_O_Ca # return scan data and calculated quantities
    
    
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
    mkdir( maps_dir + output_dir_name )

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
            
            if len( Ce_scalar ) > 0:
                Ce_scale_factor = Ce_scalar[ id ] # get dictionary key with value of id before loop starts
            else:
                Ce_scale_factor = 1 # if no scaling factor, scale by 1
            
            for i in range( 1, map_cols ) : # create 1d linescan from each row of 2d spectrum image
                # calculate intensity and concentration ratios from eels intensity data
                x, i_Ca_Ce, i_O_Ce, i_O_Ca, c_Ca_Ce, c_O_Ce, c_O_Ca = process_integrated_intensity( CeM, CaL, OK, i, k_CaCe, k_OCe, k_OCa, Ce_scale_factor )

                # calculate concentrations from eels concentration ratios (*and assumptions about material)
                c_Ca_i, c_Ce_i, c_O_i_Ce, c_O_i_Ca = calculate_concentration( c_Ca_Ce, c_O_Ce, c_O_Ca )
                
                id_counter = 0.1 # create subcounter string for file name
                id_int = float( id ) + id_counter
                id_form = '%.1f' % id_int
                id = id_form
#                 print( id_float, id_int, id )
                
                # save
                save_output_file( x, i_Ca_Ce, i_O_Ce, i_O_Ca, c_Ca_Ce, c_O_Ce, c_O_Ca, c_Ca_i, c_Ce_i, c_O_i_Ce, c_O_i_Ca, maps_dir, id, gb_id, k_CaCe, k_OCe, k_OCa )
                
        else : # 1d map
            CeM = np.loadtxt( file_group[ z_Ce ] ) # load concentration maps data
            CaL = np.loadtxt( file_group[ z_Ca ] )
            OK = np.loadtxt( file_group[ z_O ] )
                
            if len( Ce_scalar ) > 0:
                Ce_scale_factor = Ce_scalar[ id ] # set scaling factor if needed
            else:
                Ce_scale_factor = 1 # if no scaling factor, scale by 1
            
            # calculate intensity and concentration ratios from eels intensity data
            x, i_Ca_Ce, i_O_Ce, i_O_Ca, c_Ca_Ce, c_O_Ce, c_O_Ca = process_integrated_intensity( CeM, CaL, OK, 1, k_CaCe, k_OCe, k_OCa, Ce_scale_factor )

            # calculate concentrations from assumed* chemical formulae
            c_Ca_i, c_Ce_i, c_O_i_Ce, c_O_i_Ca = calculate_concentration( c_Ca_Ce, c_O_Ce, c_O_Ca )
            
            # save - should output intensity ratio (after scaling/splicing), concentration ratio at minimnum)
            save_output_file( x, i_Ca_Ce, i_O_Ce, i_O_Ca, c_Ca_Ce, c_O_Ce, c_O_Ca, c_Ca_i, c_Ce_i, c_O_i_Ce, c_O_i_Ca, maps_dir, id, gb_id, k_CaCe, k_OCe, k_OCa )
    
    
''' ########################### REFERENCES ########################### '''
