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
data_dir = 'C:/Users/crozier/Dropbox/WillB/Crozier_Lab/Writing/15_WJB_IS EBSD EELS Ca-Ceria gbs/figures/arrhenius-CCO-GCO10/CCO-GCO10/' # path to data file

# electrical and sample data:s
d_ele = [ data_dir + '140612_sdGDC10-2_150-700c_ELECTRICAL.txt',
    data_dir + '140325_sdCaDC2_100-700c-PUB_ELECTRICAL.txt',
    data_dir + '140327_sdCaDC5_100-700c_pub_ELECTRICAL.txt',
    data_dir + '140617_sdCa10DC-2_150-700c_PUB_ELECTRICAL.txt'
    ]
    
d_sam = [ data_dir + '140612_sdGDC10-2_150-700c_SAMPLE.txt',
    data_dir + '140325_sdCaDC2_100-700c-PUB_SAMPLE.txt',
    data_dir + '140327_sdCaDC5_100-700c_pub_SAMPLE.txt',
    data_dir + '140617_sdCa10DC-2_150-700c_PUB_SAMPLE.txt'
    ]

# path to output directory
output_dir = data_dir
output_file = 'arrhenius-CCO-GCO10'

# font size, resolution (DPI), file type
fsize, dots, file_type = 10, [300,1200], 'png'
cols = [ 'maroon', 'grey', 'black', 'gold' ]
marks = [ 's', 'o', '^', 'x' ]
leg_ents = [ 'GCO-10', 'CCO-2', 'CCO-5', 'CCO-10' ]
x_lab, y_lab = '1000/T (1/K)', '$log\sigma$ (S/cm)'

# grain boundary thickness (nm)
# del_gb_nm, del_gb_nm_Co5, del_gb_nm_Co1, del_gb_nm_Co2 = 2, 2, 2, 2 # gb width (nm)
deg_gb_nm = 2 # gb width (nm)

''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize

    
''' ########################### MAIN SCRIPT ########################### '''
# READ AND STORE DATA IN VARIABLES
# can loop through each input file and append each property to a list. E.g. TC.append(TC_current)

TC_set, TC_cal = [],[]
R_sy, R_sy_er, R_gr, R_gr_er, R_gb, R_gb_er = [],[],[],[],[],[]
Y_gr, Y_gr_er, a_gr, a_gr_er, Y_gb, Y_gb_er, a_gb, a_gb_er = [],[],[],[],[],[],[],[]

for d_ele_i in d_ele:
    ele = np.loadtxt( d_ele_i, skiprows = 1 )
    TC_set_i, TC_cal_i, R_sy_i, R_sy_er_i, R_gr_i, R_gr_er_i, R_gb_i, R_gb_er_i, Y_gr_i, Y_gr_er_i, a_gr_i, a_gr_er_i, Y_gb_i, Y_gb_er_i, a_gb_i, a_gb_er_i = ele.T
    
    TC_set.append( TC_set_i )
    TC_cal.append( TC_cal_i )
    R_sy.append( R_sy_i )
    R_sy_er.append( R_sy_er_i )
    R_gr.append( R_gr_i )
    R_gr_er.append( R_gr_er_i )
    R_gb.append( R_gb_i )
    R_gb_er.append( R_gb_er_i )
    Y_gr.append( Y_gr_i )
    Y_gr_er.append( Y_gr_er_i )
    a_gr.append( a_gr_i )
    a_gr_er.append( a_gr_er_i )
    Y_gb.append( Y_gb_i )
    Y_gb_er.append( Y_gb_er_i )
    a_gb.append( a_gb_i )
    a_gb_er.append( a_gb_er_i )

t_cm, t_cm_err, a_cm, a_cm_err, d_nm, d_nm_er = [],[],[],[],[],[]
for d_sam_i in d_sam:
    sam = np.loadtxt( d_sam_i, skiprows = 1 )
    t_cm_i, t_cm_err_i, a_cm_i, a_cm_err_i, d_nm_i, d_nm_er_i = sam.T
    
    t_cm.append( t_cm_i )
    t_cm_err.append( t_cm_err_i )
    a_cm.append( a_cm_i )
    a_cm_err.append( a_cm_err_i )
    d_nm.append( d_nm_i )
    d_nm_er.append( d_nm_er_i )


# CONVERT TEMP TO INVERSE K
T_num, TK_cal, TK_inv = 1e3, [],[]
for TC in TC_set:
    TK_cal_i = TC + 273
    TK_cal.append( TK_cal_i )
    TK_inv.append( T_num / TK_cal_i )


'''CALCULATE CAPACITANCE'''
# C=(R**(1-a*Y))**(1/a)
C_gr, C_gr_er, C_gb, C_gb_er = [],[],[],[]

for i in range( 0, len( R_gr ) ):
    C_gr.append( ( R_gr[i] ** ( 1 - a_gr[i] ) * Y_gr[i] ) ** ( 1 / a_gr[i] ) )
    C_gb.append( ( R_gb[i] ** ( 1 - a_gb[i] ) * Y_gb[i] ) ** ( 1 / a_gb[i] ) )


'''CALCULATE EFFECTIVE CONDUCTIVITY (S/cm)'''
# S_g = 1/Rg * (L/A), S_gb_ef = 1/Rgb * (L/A)

S_gr, S_gr_er, S_gb, S_gb_er, S_tot, S_tot_err = [],[],[],[],[],[]

for i in range( 0, len( R_gr ) ):
    S_gr.append( t_cm[i] / ( R_gr[i] * a_cm[i] ) )
    S_gb.append( 1 / R_gb[i] * ( t_cm[i] / a_cm[i] ) )
    S_tot.append( t_cm[i] / ( R_gr[i] + R_gb[i] * a_cm[i] ) )


'''CALCULATE SPECIFIC GB CONDUCTIVITY FROM Cg/Cgb (S/cm)'''
# Sgb_sp = 1/R_gb * (L/A) * (C_g/C_gb)

S_gb_sp_cc, S_gb_sp_cc_err =[],[]

for i in range( 0, len( R_gr ) ):
    S_gb_sp_cc.append( ( R_gr[i] * C_gr[i] ) / ( R_gb[i] * C_gb[i] ) * S_gr[i] )
    # S_gb_sp_cc_err.append(  )


'''CALCULATE SPECIFIC GB CONDUCTIVITY FROM d/D (S/cm)'''
# Sgb_sp = 1/R_gb * (L/A) * (d/D)

S_gb_sp_dD, S_gb_sp_dD_err = [],[]

for i in range( 0, len( R_gr ) ):
    S_gb_sp_dD.append( ( 1/R_gb[i] * (t_cm[i] / a_cm[i]) * (del_gb_nm / d_nm[i]) ) )
    # S_gb_sp_dD_err.append(  )


# # CALCULATE TRUE GB CONDUCTIVITY (S/cm) S_gb_tr = del_gb / d_g * S_gb (eq. 5 from [1])
# S_gb_tr_dD = del_gb_nm / d_nm * S_gb
# # S_gb_tr_dD_er =
# S_gb_tr_dD_Co5 = del_gb_nm_Co5 / d_nm_Co5 * S_gb_Co5
# # S_gb_tr_dD_er_Co5 =
# S_gb_tr_dD_Co1 = del_gb_nm_Co1 / d_nm_Co1 * S_gb_Co1
# # S_gb_tr_dD_er_Co1 =
# S_gb_tr_dD_Co2 = del_gb_nm_Co2 / d_nm_Co2 * S_gb_Co2
# # S_gb_tr_dD_er_Co2 =

# CALCULATE log10(), LN()

'''GENERATE FIGURES'''

'''GRAIN, TOTAL AND SPECIFIC BOUNDARY CONDUCTIVITY'''
pl.close( 'all' ) # close all open figures
pl.figure( figsize = ( 3.4, 3 ) ) # create a figure
ax = pl.gca() # store current axis

mpl_customizations() # apply customizations to matplotlib
wf.slide_art_styles() # figure styling
fontsize = mpl.rcParams[ 'font.size' ]

for i in range( 0, len( R_gr ) ):
    pl.plot( TK_inv[i], np.log10(S_gr[i]), c=cols[i], marker=marks[i] )
    # pl.plot( TK_inv[i], np.log10( S_tot[i] ) )
    pl.plot( TK_inv[i], np.log10( S_gb[i]), c=cols[i], marker=marks[i], ls='--' )


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