import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
from os import listdir # listdir(dir_path) returns array of file names in dir_path
##

# specify path to directory of elemental map files
maps_dir = "c:/Dropbox/SOFC Electrolyte Project/Microscopy/141118_10Ca_ARM200kV/kfactor_maps_141229/"
map_file_names = listdir( maps_dir ) # get map file names
map_ids = [ '05_grain2', '09_grain3', '13_grain4', '14_grain4' ] # map file unique substrings
C_Ce, C_Ca, C_O = 0.9, 0.1, 1.90 # sample molar concentrations
C_CaCe = 0.0941 # from EDX via std EDX k-factor

CaL, OK, CeM = [], [], [] # lists for intensities
k_CaCe, k_OCe, k_CaO, k_OCa = [],[],[],[] # containers for calculated k factors

for id in map_ids: # iterate through map ids
    file_group = [] # list for filenames of all elements of given map
    for file_name in map_file_names: # iterate through map filenames in dir
        if file_name.__contains__( id ): # check for unique substrings (i.e. map id)
            file_group.append( maps_dir + file_name ) # add filename to list of grouped names
    
    i_CeM = np.loadtxt( file_group[ 0 ], skiprows = 3 ) # load element map files
    i_CaL = np.loadtxt( file_group[ 1 ], skiprows = 3 ) # assign to variables
    i_OK = np.loadtxt( file_group[ 2 ], skiprows = 3 )
    
    i_CeM[ :, 0 ] = 0 # set first column to zeros 
    i_CaL[ :, 0 ] = 0 # (DM plugin outputs 1st col as distance for 2d maps [1])
    i_OK[ :, 0 ] = 0
    
    CaL.append( i_CaL.ravel().tolist() )
    OK.append( i_OK.ravel().tolist() )
    CeM.append( i_CeM.ravel().tolist() )
    
    k_CaCe_i = C_Ca / C_Ce * np.sum( i_CeM ) / np.sum( i_CaL ) # calculate k-factor
    k_OCe_i = C_O / C_Ce * np.sum( i_CeM ) / np.sum( i_OK )
    k_CaO_i = C_Ca / C_O * np.sum( i_OK ) / np.sum( i_CaL )
    k_OCa_i = C_O / C_Ca * np.sum( i_CaL ) / np.sum( i_OK )
    
    k_CaCe.append( k_CaCe_i ) # add k-factor to conatiner
    k_OCe.append( k_OCe_i )
    k_CaO.append( k_CaO_i )
    k_OCa.append( k_OCa_i )
    
k_CaCe.append( np.mean( k_CaCe ) ) # append mean k-factor column to array
k_OCe.append( np.mean( k_OCe ) )
k_CaO.append( np.mean( k_CaO ) )
k_OCa.append( np.mean( k_OCa ) )

CaL = [item for sublist in CaL for item in sublist]
OK = [item for sublist in OK for item in sublist]
CeM = [item for sublist in CeM for item in sublist]

CaL = list( filter( ( 0.0 ).__ne__, CaL ) ) # remove 0.0 values [3]
OK = list( filter( ( 0.0 ).__ne__, OK ) )
CeM = list( filter( ( 0.0 ).__ne__, CeM ) )

intensities_output_data = np.vstack( ( CaL, OK, CeM ) ).T
intensities_head = 'I_CaL\tI_OK\tI_CeM'
intensities_output_file_name = '2d_intensities.txt'

np.savetxt( maps_dir + intensities_output_file_name, intensities_output_data, delimiter='\t', header=intensities_head, fmt='%10.3e', newline='\n')
    
# save k-factors as .txt
# output_data = np.vstack( ( k_CaCe, k_OCe, k_CaO, k_OCa ) )
# output_dir = maps_dir
# output_file = 'kfactors.txt'
# head = 'rows: k_CaCe, k_OCe, k_CaO, k_OCa; last col: mean k-factor'
# np.savetxt( output_dir + output_file, output_data, delimiter='\t', header=head, fmt='%10.3e', newline='\n')
'''
equations for solving k-factor [2]
ca/cb = ia/ib * k
k = ca/cb * ib/ia

references
1. DM plugin called dumpSItotext 
2. Williams and Carter 'Transmission Electron Microscopy, A Textbook for Materials Science'
3. http://stackoverflow.com/questions/1157106/remove-all-occurences-of-a-value-from-a-python-list
'''
