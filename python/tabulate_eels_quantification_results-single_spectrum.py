''' ########################### OVERVIEW ########################### '''
'''
 Created 2015-02-18 by Will Bowman. This takes t_over_lambda_raw_DM_output.txt 
 and creates a list of file names and t/lambda values calculated from low-loss
 EELS. The input file of this script is the output file of my DM script titled
 'batch_calc_t_over_lambda.s', which used DM's EELS module to batch calculate 
 t/lambda for a gob of low-loss spectra.
'''

''' ########################### IMPORT MODULES ########################### '''
import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import wills_functions as wf
import csv, imp, os, re # csv, import, operatiting system, regex modules

##

''' ########################### USER-DEFINED ########################### '''
# tabluate_DM_eels_quantification_results( file_path, [ col_headers ], counter_prefix, counter_length, [ unique_strings ] )
# tabluate_DM_tlambda_quantification_results(  )

# indicate which modules to exucute and the date file names.
# t_over_lambda = false
# t_over_lambda_file_name = ''
# integrated_intensity = true
integrated_intensity_file_name = 'DM-EELS-Quantification-Results.txt'

# indicate path of the directory containing the data
data_directory = "C:/Dropbox/Crozier Group Users - Will Bowman/active_research/microscopy/150527_Magnetoplumbite-UCI_ARM200kV/"

# t_over_lambda_file_path = data_directory + t_over_lambda_file_name
core_loss_file_path = data_directory + integrated_intensity_file_name
# core_loss_file_path = data_directory + integrated_intensity_file_name

output_file_name = 'DM-EELS-Quantification-Results-Table.txt'
output_file_column_headers = [ 'id', 'file name', 'I_pre', 'unc_I_pre',
 'I_L3', 'unc_I_L3', 'I_L2', 'unc_I_L2 ']
# output_file_column_headers = [ 'id', 'file name', 't/lambda', 'I_pre', 'unc_I_pre',
 # 'I_L3', 'unc_I_L3', 'I_L2', 'unc_I_L2 ']
output_file_delimiter = '\t' # for generating a tab delimited text file output

file_name_counter_prefix_coreloss = "EELS_" # to find file counter
# file_name_counter_prefix_coreloss = "EELS_CL_" # to find file counter
file_name_counter_length = 2 # number of characters in counter

file_name_prefix_core_loss = "EELS Analysis of " # text inserted by DM

# t_over_lambda_data_string_prefix = "Relative sample thickness = " # to find t/lambda value
# t_over_lambda_data_string_length = 4

core_loss_unique_string = "Hartree-Slater"
# define EELS lines used for DM quantification, and real label for signal
# unique_strings = [
#     [ 'Te', 'M', 'pre' ],
#     [ 'Cr', 'L', 'L3' ],
#     [ 'I', 'M', 'L2' ]
# ]
# I_regex, unc_regex = '     (.+?) ±', '± (.+?)         '
Ca_unique_string, O_unique_string, Ce_unique_string = 'Te', 'Cr', 'I'
Ca_I_regex, Ca_unc_regex = 'Te     (.+?) ±', '± (.+?)         M' # [3]
O_I_regex, O_unc_regex = 'Cr     (.+?) ±', '± (.+?)         L'
Ce_I_regex, Ce_unc_regex = 'I      (.+?) ±', '± (.+?)         M'



''' ########################### FUNCTIONS ########################### '''

def read_text_file( file_path ):
    list = [ line.strip() for line in open( file_path ) ] # [1]
    return list
    
def regex_text( pattern, string ):
    regex = re.search( pattern, string )
    if regex:
        found_text = regex.group( 1 )
    else:
        found_text = 'pattern not found'
    
    return found_text
    
    
    
''' ########################### MAIN SCRIPT ########################### '''

# t_over_lambda_data_list = read_text_file( t_over_lambda_file_path )
# # empty lists to fill with information from input file
# t_over_lambda_file_counters, t_over_lambda_file_names, t_over_lambdas = [], [], []
# 
# for line_string in t_over_lambda_data_list: # extract data from t/lambda results file
#     
#     if line_string.__contains__( file_name_counter_prefix_lowloss ):
#         file_counter = wf.pluck_sub_string_counter( line_string, file_name_counter_prefix_lowloss, file_name_counter_length )
#         t_over_lambda_file_names.append( line_string )
#         t_over_lambda_file_counters.append( file_counter )
# #         print( file_counter )
#         
#     elif line_string.__contains__( t_over_lambda_data_string_prefix ):
#         t_over_lambda = wf.pluck_sub_string_counter( line_string, t_over_lambda_data_string_prefix, t_over_lambda_data_string_length )
#         t_over_lambdas.append( t_over_lambda )
# #         print( t_over_lambda )
#         
# t_over_lambda_stacked_output = np.vstack( ( t_over_lambda_file_counters, t_over_lambda_file_names, t_over_lambdas ) ).T
# 
# 
core_loss_data_list = read_text_file( core_loss_file_path )
core_loss_file_counters, core_loss_file_names, I_CaL, unc_I_CaL, I_OK, unc_I_OK, I_CeM, unc_I_CeM = [], [], [], [], [], [], [], []

for line_string in core_loss_data_list:
    
    # if line contains the spectrum's file name store name and file counter
    if line_string.__contains__( file_name_counter_prefix_coreloss ):
        file_counter = wf.pluck_sub_string_counter( line_string, file_name_counter_prefix_coreloss, file_name_counter_length )
        core_loss_file_counters.append( file_counter )
        
        # strip line string prefix [2]
        if line_string.startswith( file_name_prefix_core_loss ):
            core_loss_file_names.append( line_string[ len( file_name_prefix_core_loss ): ] )
        else:
            core_loss_file_names.append( line_string )

    elif line_string.__contains__( core_loss_unique_string ):
        if line_string.__contains__( Ca_unique_string ):
            I_CaL.append( regex_text( Ca_I_regex, line_string ) )
            unc_I_CaL.append( regex_text( Ca_unc_regex, line_string ) )
            
        elif line_string.__contains__( O_unique_string ):
            I_OK.append( regex_text( O_I_regex, line_string ) )
            unc_I_OK.append( regex_text( O_unc_regex, line_string ) )
            
        elif line_string.__contains__( Ce_unique_string ):
            I_CeM.append( regex_text( Ce_I_regex, line_string ) )
            unc_I_CeM.append( regex_text( Ce_unc_regex, line_string ) )
            
core_loss_quantification_stacked_output = np.vstack( (
core_loss_file_counters, core_loss_file_names, I_CaL, unc_I_CaL, I_OK, unc_I_OK, I_CeM, unc_I_CeM
) ).T

# results_stacked_output = np.vstack( (
# t_over_lambda_file_counters, t_over_lambda_file_names, t_over_lambdas, I_CaL, unc_I_CaL, I_OK, unc_I_OK, I_CeM, unc_I_CeM
# ) ).T

# save the output
head = core_loss_file_names[ 0 ] + '\n'
head = head + output_file_delimiter.join( output_file_column_headers )
np.savetxt( data_directory + output_file_name, core_loss_quantification_stacked_output, 
delimiter = output_file_delimiter, fmt = '%s', header = head, newline = '\n')



''' ########################### REFERENCES ########################### 
1. http://stackoverflow.com/questions/3277503/python-read-file-line-by-line-into-array
2. http://stackoverflow.com/questions/1038824/how-do-i-remove-a-substring-from-the-end-of-a-string-in-python
3. http://stackoverflow.com/questions/4666973/how-to-extract-a-substring-from-inside-a-string-in-python
'''
