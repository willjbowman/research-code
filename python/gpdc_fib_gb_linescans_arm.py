''' ########################### OVERVIEW ########################### '''
'''
 Created xxxx-xx-xx by Will Bowman. This ...
1. raw data to adjusted I-ratios (adjusted based on CeO2_STD Ce signal overlaps)
2. calculate k-factor at each point in linescans (assuming nominal composition)
3. manually determine k-factor from grain sections of linescans
4. apply k-factor from (3) to all spectra to estimate composition
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
data_dir_140203 = 'C:\Dropbox\Crozier Group Users - Will Bowman\active_research\microscopy\140203_3aGPDCfib_ARM\140203_3aGPDCfib_CeM54-PrM-Gdm' # path to data file


# nominal compositions
C_Ce, C_Pr, C_Gd = 0.85, 0.04, 0.11 # mol/mol

# k-factors determined from grain section of 150729 linescans
# 9 scans, 310 data points
k_PrCe, k_GdCe = 1.4, 2.3 # 


''' ########################### FUNCTIONS ########################### '''
    
    
''' ########################### MAIN SCRIPT ########################### '''
# READ DATA
_data = np.loadtxt( _data_path, skiprows = 3 ) # read data, ignore first three rows

# (1) CONVERT TO COLUMNS AND ADJUST RAW INTENSITIES TO ACCOUNT FOR SIGNAL OVERLAP

# (2) CALCULATE K-FACTOR FOR EACH POINT IN LINESCAN

# (4) APPLY MANUALLY DETERMINED K-FACTOR (3) TO ALL ADJUSTED SPECTRA (1)
    
''' ########################### REFERENCES ########################### '''