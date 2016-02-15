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

# electrical and sample data
d_ele = [
'140612_sdGDC10-2_150-700c_ELECTRICAL.txt',
'140404_sd0.5CoGDC10_100-700c_ELECTRICAL.txt',
'140408_sd1CoGDC10_100-700c_ELECTRICAL.txt',
'140404_sd2CoGDC10_100-700c_ELECTRICAL.txt'
]

d_sam = [
'140612_sdGDC10-2_150-700c_SAMPLE.txt',
'140404_sd0.5CoGDC10_100-700c_SAMPLE.txt',
'140408_sd1CoGDC10_100-700c_SAMPLE.txt',
'140404_sd2CoGDC10_100-700c_SAMPLE.txt'
]

d_ele_GCO = data_dir + '140612_sdGDC10-2_150-700c_ELECTRICAL.txt'
d_sam_GCO = data_dir + '140612_sdGDC10-2_150-700c_SAMPLE.txt'

d_ele_Co5 = data_dir + '140404_sd0.5CoGDC10_100-700c_ELECTRICAL.txt'
d_sam_Co5 = data_dir + '140404_sd0.5CoGDC10_100-700c_SAMPLE.txt'

d_ele_Co1 = data_dir + '140408_sd1CoGDC10_100-700c_ELECTRICAL.txt'
d_sam_Co1 = data_dir + '140408_sd1CoGDC10_100-700c_SAMPLE.txt'

d_ele_Co2 = data_dir + '140404_sd2CoGDC10_100-700c_ELECTRICAL.txt'
d_sam_Co2 = data_dir + '140404_sd2CoGDC10_100-700c_SAMPLE.txt'

# path to output directory
output_dir = data_dir
output_file = 'electrical-propeties'

# font size, resolution (DPI), file type
fsize, dots, file_type = 10, [300,1200], 'png'
cols = [ 'maroon', 'grey', 'gold', 'black' ]
marks = [ 's', 'o', '^' ]
leg_ents = [ '0', '0.5', '1', '2' ]
x_lab, y_lab = '1000/T (1/K)', '$log\sigma$ (S/cm)'

# grain boundary thickness (nm)
del_gb_nm, del_gb_nm_Co5, del_gb_nm_Co1, del_gb_nm_Co2 = 2, 2, 2, 2 # gb width (nm)

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

ele_Co5 = np.loadtxt( d_ele_Co5, skiprows = 1 )
sam_Co5 = np.loadtxt( d_sam_Co5, skiprows = 1 )

TC_set_Co5, TC_cal_Co5, R_sy_Co5, R_sy_er_Co5, R_gr_Co5, R_gr_er_Co5, R_gb_Co5, R_gb_er_Co5, Y_gr_Co5, Y_gr_er_Co5, a_gr_Co5, a_gr_er_Co5, Y_gb_Co5, Y_gb_er_Co5, a_gb_Co5, a_gb_er_Co5 = ele_Co5.T
t_cm_Co5, t_cm_err_Co5, a_cm_Co5, a_cm_err_Co5, d_nm_Co5, d_nm_er_Co5 = sam_Co5.T

ele_Co1 = np.loadtxt( d_ele_Co1, skiprows = 1 )
sam_Co1 = np.loadtxt( d_sam_Co1, skiprows = 1 )

TC_set_Co1, TC_cal_Co1, R_sy_Co1, R_sy_er_Co1, R_gr_Co1, R_gr_er_Co1, R_gb_Co1, R_gb_er_Co1, Y_gr_Co1, Y_gr_er_Co1, a_gr_Co1, a_gr_er_Co1, Y_gb_Co1, Y_gb_er_Co1, a_gb_Co1, a_gb_er_Co1 = ele_Co1.T
t_cm_Co1, t_cm_err_Co1, a_cm_Co1, a_cm_err_Co1, d_nm_Co1, d_nm_er_Co1 = sam_Co1.T

ele_Co2 = np.loadtxt( d_ele_Co2, skiprows = 1 )
sam_Co2 = np.loadtxt( d_sam_Co2, skiprows = 1 )

TC_set_Co2, TC_cal_Co2, R_sy_Co2, R_sy_er_Co2, R_gr_Co2, R_gr_er_Co2, R_gb_Co2, R_gb_er_Co2, Y_gr_Co2, Y_gr_er_Co2, a_gr_Co2, a_gr_er_Co2, Y_gb_Co2, Y_gb_er_Co2, a_gb_Co2, a_gb_er_Co2 = ele_Co2.T
t_cm_Co2, t_cm_err_Co2, a_cm_Co2, a_cm_err_Co2, d_nm_Co2, d_nm_er_Co2 = sam_Co2.T

# TC_all = []
# TC_set.append( TC_set_curr )

# CONVERT TEMP TO INVERSE K
T_num = 1e3
TK_cal = TC_cal + 273
TK_cal_inv = T_num / TK_cal

TK_cal_Co5 = TC_cal_Co5 + 273
TK_cal_inv_Co5 = T_num / TK_cal_Co5

TK_cal_Co1 = TC_cal_Co1 + 273
TK_cal_inv_Co1 = T_num / TK_cal_Co1

TK_cal_Co2 = TC_cal_Co2 + 273
TK_cal_inv_Co2 = T_num / TK_cal_Co2

'''CALCULATE CAPACITANCE C=(R**(1-a*Y))**(1/a)'''
C_gr = ( R_gr ** ( 1 - a_gr ) * Y_gr ) ** ( 1 / a_gr )
# C_gr_err =
C_gb = ( R_gb ** ( 1 - a_gb ) * Y_gb ) ** ( 1 / a_gb )
# C_gb_err =

C_gr_Co5 = ( R_gr_Co5 ** ( 1 - a_gr_Co5 ) * Y_gr_Co5 ) ** ( 1 / a_gr_Co5 )
# C_gr_err =
C_gb_Co5 = ( R_gb_Co5 ** ( 1 - a_gb_Co5 ) * Y_gb_Co5 ) ** ( 1 / a_gb_Co5 )
# C_gb_err =

C_gr_Co1 = ( R_gr_Co1 ** ( 1 - a_gr_Co1 ) * Y_gr_Co1 ) ** ( 1 / a_gr_Co1 )
# C_gr_err =
C_gb_Co1 = ( R_gb_Co1 ** ( 1 - a_gb_Co1 ) * Y_gb_Co1 ) ** ( 1 / a_gb_Co1 )
# C_gb_err =

C_gr_Co2 = ( R_gr_Co2 ** ( 1 - a_gr_Co2 ) * Y_gr_Co2 ) ** ( 1 / a_gr_Co2 )
# C_gr_err =
C_gb_Co2 = ( R_gb_Co2 ** ( 1 - a_gb_Co2 ) * Y_gb_Co2 ) ** ( 1 / a_gb_Co2 )
# C_gb_err =

'''CALCULATE EFFECTIVE CONDUCTIVITY (S/cm)'''
# S_g = 1/Rg * (L/A), S_gb_ef = 1/Rgb * (L/A), Sgb_sp = (RC)_g / (RC)_gb * S_g, Stot = L / (Rtot*A)

S_gr = t_cm / ( R_gr * a_cm )
# S_gr_er =
S_gb = 1 / R_gb * ( t_cm / a_cm )
# S_gb_er =
S_tot = t_cm / ( R_gr + R_gb * a_cm )
# S_tot_err =

S_gr_Co5 = t_cm_Co5 / ( R_gr_Co5 * a_cm_Co5 )
# S_gr_er_Co5 =
S_gb_Co5 = 1 / R_gb_Co5 * ( t_cm_Co5 / a_cm_Co5 )
# S_gb_er_Co5 =
S_tot_Co5 = t_cm_Co5 / ( R_gr_Co5 + R_gb_Co5 * a_cm_Co5 )
# S_tot_err_Co5 =

S_gr_Co1 = t_cm_Co1 / ( R_gr_Co1 * a_cm_Co1 )
# S_gr_er_Co1 =
S_gb_Co1 = 1 / R_gb_Co1 * ( t_cm_Co1 / a_cm_Co1 )
# S_gb_er_Co1 =
S_tot_Co1 = t_cm_Co1 / ( R_gr_Co1 + R_gb_Co1 * a_cm_Co1 )
# S_tot_err_Co1 =

S_gr_Co2 = t_cm_Co2 / ( R_gr_Co2 * a_cm_Co2 )
# S_gr_er_Co2 =
S_gb_Co2 = 1 / R_gb_Co2 * ( t_cm_Co2 / a_cm_Co2 )
# S_gb_er_Co2 =
S_tot_Co2 = t_cm_Co2 / ( R_gr_Co2 + R_gb_Co2 * a_cm_Co2 )
# S_tot_err_Co2 =


'''CALCULATE SPECIFIC GB CONDUCTIVITY FROM Cg/Cgb (S/cm)'''
# Sgb_sp = 1/R_gb * (L/A) * (C_g/C_gb)

S_gb_sp_cc = ( R_gr * C_gr ) / ( R_gb * C_gb ) * S_gr
# S_gb_er =

S_gb_sp_cc_Co5 = ( R_gr_Co5 * C_gr_Co5 ) / ( R_gb_Co5 * C_gb_Co5 ) * S_gr_Co5
# S_gb_er_Co5 =

S_gb_sp_cc_Co1 = ( R_gr_Co1 * C_gr_Co1 ) / ( R_gb_Co1 * C_gb_Co1 ) * S_gr_Co1
# S_gb_er_Co1 =

S_gb_sp_cc_Co2 = ( R_gr_Co2 * C_gr_Co2 ) / ( R_gb_Co2 * C_gb_Co2 ) * S_gr_Co2
# S_gb_er_Co2 =

'''CALCULATE SPECIFIC GB CONDUCTIVITY FROM d/D (S/cm)'''
# Sgb_sp = 1/R_gb * (L/A) * (d/D)

S_gb_sp_dD = 1/R_gb * (t_cm / a_cm) * (del_gb_nm / d_nm)
# S_gb_er =

S_gb_sp_dD_Co5 = 1/R_gb_Co5 * (t_cm_Co5 / a_cm_Co5) * (del_gb_nm_Co5 / d_nm_Co5)
# S_gb_er_Co5 =

S_gb_sp_dD_Co1 = 1/R_gb_Co1 * (t_cm_Co1 / a_cm_Co1) * (del_gb_nm_Co1 / d_nm_Co1)
# S_gb_er_Co1 =

S_gb_sp_dD_Co2 = 1/R_gb_Co2 * (t_cm_Co2 / a_cm_Co2) * (del_gb_nm_Co2 / d_nm_Co2)
# S_gb_er_Co2 =

# CALCULATE TRUE GB CONDUCTIVITY (S/cm) S_gb_tr = del_gb / d_g * S_gb (eq. 5 from [1])
S_gb_tr_dD = del_gb_nm / d_nm * S_gb
# S_gb_tr_dD_er =
S_gb_tr_dD_Co5 = del_gb_nm_Co5 / d_nm_Co5 * S_gb_Co5
# S_gb_tr_dD_er_Co5 =
S_gb_tr_dD_Co1 = del_gb_nm_Co1 / d_nm_Co1 * S_gb_Co1
# S_gb_tr_dD_er_Co1 =
S_gb_tr_dD_Co2 = del_gb_nm_Co2 / d_nm_Co2 * S_gb_Co2
# S_gb_tr_dD_er_Co2 =

# CALCULATE log10(), LN()

'''GENERATE FIGURES'''

'''GRAIN, TOTAL AND SPECIFIC BOUNDARY CONDUCTIVITY'''
pl.close( 'all' ) # close all open figures
pl.figure( figsize = ( 3.4, 3 ) ) # create a figure
ax = pl.gca() # store current axis

mpl_customizations() # apply customizations to matplotlib
wf.slide_art_styles() # figure styling
fontsize = mpl.rcParams[ 'font.size' ]

pl.plot( TK_cal_inv, np.log10( S_gr ), color = cols[0], marker = marks[0] )
pl.plot( TK_cal_inv_Co5, np.log10( S_gr_Co5 ), color = cols[1], marker = marks[0] )
pl.plot( TK_cal_inv_Co1, np.log10( S_gr_Co1 ), color = cols[2], marker = marks[0] )
pl.plot( TK_cal_inv_Co2, np.log10( S_gr_Co2 ), color = cols[3], marker = marks[0] )

pl.plot( TK_cal_inv, np.log10( S_gb_sp_dD ), color = cols[0], marker = marks[1] )
pl.plot( TK_cal_inv, np.log10( S_tot ), color = cols[0], marker = marks[2] )
# pl.plot( TK_cal_inv, np.log10( S_gb_tr ), color = cols[0] )

pl.plot( TK_cal_inv_Co5, np.log10( S_gb_sp_dD_Co5 ), color = cols[1], marker = marks[1] )
pl.plot( TK_cal_inv_Co5, np.log10( S_tot_Co5 ), color = cols[1], marker = marks[2] )
# pl.plot( TK_cal_inv_Co5, np.log10( S_gb_tr_Co5 ), color = cols[1] )

pl.plot( TK_cal_inv_Co1, np.log10( S_gb_sp_dD_Co1 ), color = cols[2], marker = marks[1] )
pl.plot( TK_cal_inv_Co1, np.log10( S_tot_Co1 ), color = cols[2], marker = marks[2] )
# pl.plot( TK_cal_inv_Co1, np.log10( S_gb_tr_Co1 ), color = cols[2] )

pl.plot( TK_cal_inv_Co2, np.log10( S_gb_sp_dD_Co2 ), color = cols[3], marker = marks[1] )
pl.plot( TK_cal_inv_Co2, np.log10( S_tot_Co2 ), color = cols[3], marker = marks[2] )
# pl.plot( TK_cal_inv_Co2, np.log10( S_gb_tr_Co2 ), color = cols[3] )

# pl.tight_layout() # can run once to apply to all subplots, i think
pl.legend( leg_ents )
pl.ylabel( y_lab, labelpad=0.5 )
pl.xlabel( x_lab, labelpad=0.5 )


'''COMPARE EFFECTIVE AND SPECIFIC BOUNDARY CONDUCTIVITY (calculated from d/D and Cg/Cgb)'''
pl.figure( figsize = ( 3.4, 3 ) ) # create a figure
ax = pl.gca() # store current axis

mpl_customizations() # apply customizations to matplotlib
wf.slide_art_styles() # figure styling
fontsize = mpl.rcParams[ 'font.size' ]

pl.plot( TK_cal_inv, np.log10( S_gb ), color = cols[0], marker = marks[1] )
pl.plot( TK_cal_inv_Co5, np.log10( S_gb_Co5 ), color = cols[1], marker = marks[1] )
pl.plot( TK_cal_inv_Co1, np.log10( S_gb_Co1 ), color = cols[2], marker = marks[1] )
pl.plot( TK_cal_inv_Co2, np.log10( S_gb_Co2 ), color = cols[3], marker = marks[1] )

pl.plot( TK_cal_inv, np.log10( S_gb_sp_dD ), color = cols[0] )
pl.plot( TK_cal_inv_Co5, np.log10( S_gb_sp_dD_Co5 ), color = cols[1] )
pl.plot( TK_cal_inv_Co1, np.log10( S_gb_sp_dD_Co1 ), color = cols[2] )
pl.plot( TK_cal_inv_Co2, np.log10( S_gb_sp_dD_Co2 ), color = cols[3] )

pl.plot( TK_cal_inv, np.log10( S_gb_sp_cc ), color = cols[0], ls='--' )
pl.plot( TK_cal_inv_Co5, np.log10( S_gb_sp_cc_Co5 ), color = cols[1], ls='--' )
pl.plot( TK_cal_inv_Co1, np.log10( S_gb_sp_cc_Co1 ), color = cols[2], ls='--' )
pl.plot( TK_cal_inv_Co2, np.log10( S_gb_sp_cc_Co2 ), color = cols[3], ls='--' )

# pl.tight_layout() # can run once to apply to all subplots, i think
pl.legend( leg_ents )
pl.ylabel( y_lab, labelpad=1.5 )
pl.xlabel( x_lab, labelpad=1.5 )

for dot in dots:
    pass
    # output_name = wf.save_name( data_dir, output_file, dot, file_type )
    # pl.savefig( output_name, format = file_type, dpi = dot, transparent = True )


''' ########################### REFERENCES ########################### '''
'''
1. should use brick-layer model e.g. Christie '96 SSI
'''