''' ########################### OVERVIEW ########################### '''
'''
 Created 2015-11-05 by Will Bowman. This script is for manipulating Co-GDC 
 electrical properties data
'''

''' ########################### IMPORT MODULES ########################### '''
import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import wills_functions as wf
import csv, imp, os

##


''' ########################### USER-DEFINED ########################### '''
# make gui to pick files?
data_dir = 'C:/Users/willb/Dropbox/WillB/Crozier_Lab/Writing/2015_Co GDC gb electrical conductivity/figures/electrical-properties/' # path to data file

# electrical and sample data:
d_ele_GCO = data_dir + '140612_sdGDC10-2_150-700c_ELECTRICAL.txt'
d_sam_GCO = data_dir + '140612_sdGDC10-2_150-700c_SAMPLE.txt'

# d_ele_Co5 = data_dir + '140612_sdGDC10-2_150-700c_ELECTRICAL.txt'
# d_sam_Co5 = data_dir + '140612_sdGDC10-2_150-700c_SAMPLE.txt'
# 
# d_ele_Co1 = data_dir + '140612_sdGDC10-2_150-700c_ELECTRICAL.txt'
# d_sam_Co1 = data_dir + '140612_sdGDC10-2_150-700c_SAMPLE.txt'
# 
# d_ele_Co2 = data_dir + '140612_sdGDC10-2_150-700c_ELECTRICAL.txt'
# d_sam_Co2 = data_dir + '140612_sdGDC10-2_150-700c_SAMPLE.txt'

# path to output directory
output_dir = data_dir
output_file = 'electrical-propeties'

# font size, resolution (DPI), file type
fsize, dots, file_type = 10, [300,1200], 'png'

''' ########################### FUNCTIONS ########################### '''

# CONVERT TEMP TO INVERSE K
# CALCULATE CAPACITANCE
# CALCULATE CONDUCTIVITY
# CALCULATE TRUE GB CONDUCTIVITY
# CALCULATE LOG(), LN()

    
''' ########################### MAIN SCRIPT ########################### '''
_data = np.loadtxt( _data_path, skiprows = 3 ) # read data, ignore first three rows

pl.close( 'all' ) # close all open figures
pl.figure( figsize = ( 3.4, 3 ) ) # create a figure
ax = pl.gca() # store current axis

wf.mpl_customizations() # apply customizations to matplotlib
wf.slide_art_styles() # figure styling
fontsize = mpl.rcParams[ 'font.size' ]


pl.tight_layout() # can run once to apply to all subplots, i think

for dot in dots:
    # output_name = wf.save_name( data_dir, output_file, dot, file_type )
    # pl.savefig( output_name, format = file_type, dpi = dot, transparent = True )
    
''' ########################### REFERENCES ########################### '''