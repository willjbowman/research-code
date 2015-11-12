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

# grain boundary thickness (nm)
del_gb_nm = 2

''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize

    
''' ########################### MAIN SCRIPT ########################### '''
# READ AND STORE DATA IN VARIABLES
# can loop through each input file and append each property to a list. E.g. TC.append(TC_current)
ele_GCO = np.loadtxt( d_ele_GCO, skiprows = 1 ) # read data
sam_GCO = np.loadtxt( d_sam_GCO, skiprows = 1 )

TC_set, TC_cal, R_sy, R_sy_er, R_gr, R_gr_er, R_gb, R_gb_er, Y_gr, Y_gr_er, a_gr, a_gr_er, Y_gb, Y_gb_er, a_gb, a_gb_er = ele_GCO.T
t_cm, t_cm_err, a_cm, a_cm_err, d_nm, d_nm_er = sam_GCO.T

# ele_Co5 = np.loadtxt( d_ele_Co5, skiprows = 1 )
# sam_Co5 = np.loadtxt( d_sam_Co5, skiprows = 1 )
# 
# ele_Co1 = np.loadtxt( d_ele_Co1, skiprows = 1 )
# sam_Co1 = np.loadtxt( d_sam_Co1, skiprows = 1 )
# 
# ele_Co2 = np.loadtxt( d_ele_Co2, skiprows = 1 )
# sam_Co2 = np.loadtxt( d_sam_Co2, skiprows = 1 )

# TC_all = []
# TC_set.append( TC_set_curr )

# CONVERT TEMP TO INVERSE K
TK_cal = TC_cal + 273
TK_cal_inv = 1 / TK_cal

# CALCULATE CAPACITANCE C=(R**(1-a*Y))**(1/a)
C_gr = ( R_gr ** ( 1 - a_gr ) * Y_gr ) ** ( 1 / a_gr )
# C_gr_err =
C_gb = ( R_gb ** ( 1 - a_gb ) * Y_gb ) ** ( 1 / a_gb )
# C_gb_err =

# CALCULATE CONDUCTIVITY (S/cm) S_g = L / (R*A), Sgb = (RC)_g / (RC)_gb * S_g
S_gr = t_cm / ( R_gr * a_cm )
# S_gr_er =
S_gb = ( R_gr * C_gr ) / ( R_gb * C_gb ) * S_gr
# S_gb_er =

# CALCULATE TRUE GB CONDUCTIVITY (S/cm) S_gb_tr = L*del_gb / (A*R_gb*d_g)
S_gb_tr = t_cm * del_gb_nm / ( a_cm * R_gb * d_nm )
# S_gb_tr_er =

# CALCULATE LOG(), LN()

# GENERATE FIGURES
pl.close( 'all' ) # close all open figures
pl.figure( figsize = ( 3.4, 3 ) ) # create a figure
ax = pl.gca() # store current axis

mpl_customizations() # apply customizations to matplotlib
wf.slide_art_styles() # figure styling
fontsize = mpl.rcParams[ 'font.size' ]

pl.plot( TK_cal_inv, S_gr )
pl.plot( TK_cal_inv, S_gb )
pl.plot( TK_cal_inv, S_gb_tr )

pl.tight_layout() # can run once to apply to all subplots, i think

for dot in dots:
    pass
    # output_name = wf.save_name( data_dir, output_file, dot, file_type )
    # pl.savefig( output_name, format = file_type, dpi = dot, transparent = True )


''' ########################### REFERENCES ########################### '''