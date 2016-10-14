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
# absolute path to figure work directory
paper_dir = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/'+\
    '15_WJB_IS EBSD EELS Ca-Ceria gbs/'
fig_name = 'CCO-arrhenius-GCO10'
data_dir = paper_dir + 'data/' + fig_name + '/'
fig_dir = paper_dir + 'figures/' + fig_name + '/'
# data_dir = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/'+\
#     '15_WJB_IS EBSD EELS Ca-Ceria gbs/data/'+\
#     'CCO-arrhenius-GCO10/CCO-GCO10/'

# electrical and sample data:s
d_ele = [ data_dir + '140325_sdCaDC2_100-700c-PUB_ELECTRICAL.txt',
    data_dir + '140327_sdCaDC5_100-700c_pub_ELECTRICAL.txt',
    data_dir + '140617_sdCa10DC-2_150-700c_PUB_ELECTRICAL_v1.txt',
    data_dir + '140612_sdGDC10-2_150-700c_ELECTRICAL.txt'
    ]
    
d_sam = [ data_dir + '140325_sdCaDC2_100-700c-PUB_SAMPLE.txt',
    data_dir + '140327_sdCaDC5_100-700c_pub_SAMPLE.txt',
    data_dir + '140617_sdCa10DC-2_150-700c_PUB_SAMPLE.txt',
    data_dir + '140612_sdGDC10-2_150-700c_SAMPLE.txt'
    ]

# path to output directory
output_dir = data_dir + wf.date_str() + '/'
output_dir = fig_dir
output_file = 'CCO-arrhenius-GCO10'
subfolder = True
save = True
# save = False

# font size, resolution (DPI), file type
# should have a var for fonr.sans-serif
fsize, dots, file_types = 10, [300], ['png','svg']
cols = [ 'maroon', 'grey', 'black', 'goldenrod' ]
marks, msize = [ 's', 'o', '^', 'x' ], 6
leg_ents = [ '2% Ca', '5% Ca', '10% Ca', '10% Gd' ]
x_lab, y_lab = '1000/T (1/K)', '$log\sigma$ (S/cm)'

# grain boundary thickness (nm)
# del_gb_nm, del_gb_nm_Co5, del_gb_nm_Co1, del_gb_nm_Co2 = 2, 2, 2, 2 # gb width (nm)
# gb width (nm) from EELS compositional width
g_nm, g_nm_er = 3, 0.3 # nm

x_lims, y_lims = [ 1, 2.4 ], [ -15, -1 ]
file_anno = [ '-0of3', '-1of3', '-2of3', '-3of3' ]

''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize

def er_prop_div( A, dA, B, dB ):
    AB = A / B
    d_AB = abs(AB) * ( (dA/A)**2 + (dB/B)**2 )**.5
    return AB, d_AB

def er_prop_mult( A, dA, B, dB ):
    AB = A * B
    d_AB = abs(AB) * ( (dA/A)**2 + (dB/B)**2 )**.5
    return AB, d_AB

    
''' ########################### MAIN SCRIPT ########################### '''
# READ AND STORE DATA IN VARIABLES
# can loop through each input file and append each property to a list. E.g. TC.append(TC_current)

TC_set, TC_cal = [],[]
R_sy, R_sy_er, R_gr, R_gr_er, R_gb, R_gb_er = [],[],[],[],[],[]
Y_gr, Y_gr_er, a_gr, a_gr_er, Y_gb, Y_gb_er, a_gb, a_gb_er = [],[],[],[],[],[],[],[]

for d_ele_i in d_ele: # electrical data
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

t_cm, t_cm_er, a_cm, a_cm_er, d_nm, d_nm_er = [],[],[],[],[],[]
for d_sam_i in d_sam:
    sam = np.loadtxt( d_sam_i, skiprows = 1 )
    t_cm_i, t_cm_er_i, a_cm_i, a_cm_er_i, d_nm_i, d_nm_er_i = sam.T
    
    t_cm.append( t_cm_i )
    t_cm_er.append( t_cm_er_i )
    a_cm.append( a_cm_i )
    a_cm_er.append( a_cm_er_i )
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
# S_g = 1/Rg * (L/A), S_gb = 1/Rgb * (L/A), S_tot = 1/(Rgr+Rgb) * (L/A)

S_gr, S_gr_er, S_gb, S_gb_er, S_tot, S_tot_er = [],[],[],[],[],[]

for i in range( 0, len( R_gr ) ):
    t_a, t_a_er = er_prop_div( t_cm[i], t_cm_er[i], a_cm[i], a_cm_er[i] )
    S, S_er = er_prop_div( t_a, t_a_er, R_gr[i], R_gr_er[i] )
    S_gr.append( S )
    S_gr_er.append( S_er )

    S_gb.append( 1 / R_gb[i] * ( t_cm[i] / a_cm[i] ) )
    S_tot.append( 1 / ( R_gr[i] + R_gb[i] ) * ( t_cm[i] / a_cm[i] ) )


'''CALCULATE SPECIFIC GB CONDUCTIVITY FROM Cg/Cgb (S/cm)'''
# S_gb_sp_cc = 1/R_gb * (L/A) * (C_g/C_gb)

S_gb_sp_cc, S_gb_sp_cc_er =[],[]

for i in range( 0, len( R_gr ) ):
    S_gb_sp_cc.append( S_gb[i] * ( t_cm[i] / a_cm[i] ) * ( C_gr[i] / C_gb[i] ) )
    # S_gb_sp_cc_er.append(  )


'''CALCULATE SPECIFIC GB CONDUCTIVITY FROM d/D (S/cm)'''
# S_gb_sp_dD = 1/R_gb * (L/A) * (d/D)

S_gb_sp_dD, S_gb_sp_dD_er = [],[]

for i in range( 0, len( R_gr ) ):
    t_a, t_a_er = er_prop_div( t_cm[i], t_cm_er[i], a_cm[i], a_cm_er[i] )
    g_G, g_G_er = er_prop_div( g_nm, g_nm_er, d_nm[i], d_nm_er[i] )
    t_g, t_g_er = er_prop_mult( t_a, t_a_er, g_G, g_G_er )
    S, S_er = er_prop_div( t_g, t_g_er, R_gb[i], R_gb_er[i] )
    # S_gb_sp_dD.append( S_gb[i] * ( t_cm[i] / a_cm[i] ) * (del_gb_nm / d_nm[i]) )

    S_gb_sp_dD.append( S )
    S_gb_sp_dD_er.append( S_er )


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
S_gb_sp_dD_1 = S_gb_sp_dD[1] # w/ outliers
S_gb_sp_dD[1][5:-1]=np.nan # nan outliers
'''GRAIN, TOTAL AND SPECIFIC BOUNDARY CONDUCTIVITY'''
pl.close( 'all' ) # close all open figures
pl.figure( figsize = ( 3.4, 3 ) ) # create a figure
ax = pl.gca() # store current axis
# ax2 = ax.twiny() #create a second x-axis which shares ax1's y-axis

mpl_customizations() # apply customizations to matplotlib
# wf.slide_art_styles() # figure styling
fontsize = mpl.rcParams[ 'font.size' ]

legend_handles = [] # container for legend handles (filled in loop)

for h in range( 1, len( file_anno ) + 1 ):
    
    pl.close( 'all' ) # close all open figures
    pl.figure( figsize = ( 3.4, 3 ) ) # create a figure
    ax = pl.gca() # store current axis
    # ax2 = ax.twiny() #create a second x-axis which shares ax1's y-axis
    
    mpl_customizations() # apply customizations to matplotlib
    # wf.slide_art_styles() # figure styling
    fontsize = mpl.rcParams[ 'font.size' ]

    for i in range( 0, h ):
    # for i in range( 0, 1 ):
        col, mark = cols[i], marks[i]
        pl.plot( TK_inv[i], np.log10( S_gr[i] ), c=cols[i], 
            marker=marks[i], markersize=msize )

        # pl.plot( TK_inv[i], np.log10( S_tot[i] ), marker=marks[i] )
        # pl.plot( TK_inv[i], np.log10( S_gb_sp_cc[i]), c=cols[i], 
        #     marker=marks[i], ls='--', markersize=msize )
        pl.plot( TK_inv[i], np.log10( S_gb_sp_dD[i] ),
            c=cols[i], marker=marks[i], ls='--', markersize=msize )

        # pl.errorbar( TK_inv[i], np.log10( S_gr[i] ), 
        #     yerr = [ S_gr_er[i]*0, np.log10( S_gr_er[i] )/10 ], capthick=1,
        #     c=cols[i], marker=marks[i], markersize=msize )

        # pl.errorbar( TK_inv[i], np.log10( S_gb_sp_dD[i] ), 
        #     yerr = np.log10( S_gb_sp_dD_er[i] )/10, capthick=1,
        #     c=cols[i], marker=marks[i], ls='--', markersize=msize )
    
    # apply legend to each figure
    leg_info = mpl.lines.Line2D( [], [], color=cols[h-1], marker=marks[h-1], 
        markersize=msize, linestyle='-' )
    legend_handles.append( leg_info )
    
    # pl.legend( leg_ents )
    pl.ylabel( y_lab, labelpad=1.5 )
    pl.xlabel( x_lab, labelpad=1.5 )
    ax.set_xlim( x_lims )
    ax.set_ylim( y_lims )
    
    ax2 = ax.twiny() #create a second x-axis which shares ax1's y-axis
    Tc_axis_label = 'T ($^\circ$C)'
    ax2_Tc_ticks = np.linspace( 700, 150, 12 ) # Celcius axis ticks and labels
    ax2_Tc_ticklabels = np.array( [ 700, '', '', '', 500, '', 400, '',
        300, '', 200, '' ] )
    #calculate 2nd axis tick locations
    ax2_tick_Tk_locations = 1000 / ( ax2_Tc_ticks + 273 ) 
    ax2_tick_Tc_locations = ( ax2_tick_Tk_locations - x_lims[0] ) / \
        ( x_lims[1] - x_lims[0] )
    ax2.set_xticks( ax2_tick_Tc_locations ) #add ticks and labels to 2nd axis
    ax2.set_xticklabels( ax2_Tc_ticklabels )
    ax2.set_xlabel( Tc_axis_label )
    
    pl.tight_layout() # can run once to apply to all subplots, i think
    
    
    # # pl.tight_layout() # can run once to apply to all subplots, i think
    # ax.legend( leg_ents )
    ax.legend( legend_handles, leg_ents, loc = 'lower left',
        numpoints = 1, frameon = False, fontsize = 10, labelspacing = .01,
        handletextpad = .2 )
    # pl.ylabel( y_lab, labelpad=1.5 )
    # pl.xlabel( x_lab, labelpad=1.5 )
    
    if save:
        # wf.save_fig( data_dir, file_types, dots, output_file+file_anno[h-1] )
        wf.save_fig( output_dir, file_types, dots, fig_name, anno=file_anno[h-1],
            subfolder_save=subfolder )


''' ########################### REFERENCES ########################### '''
'''
1. should use brick-layer model e.g. Christie '96 SSI
'''