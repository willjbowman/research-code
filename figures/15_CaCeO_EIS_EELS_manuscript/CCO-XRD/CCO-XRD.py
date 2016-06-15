''' ########################### OVERVIEW ########################### '''
'''
Created 2016-03-24 by Will Bowman. This script is for plotting XRD patterns
of CaxCe1-xO2-d and reference CaO and CaO2 for a figure
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
# path to data file
data_dir = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/15_WJB_IS EBSD EELS Ca-Ceria gbs/figures/CCO-XRD/'
exper_d = data_dir + 'CaDC_XRD_2_5_10_mol_1.csv'
ref_d0 =  data_dir + 'CaO_Fm-3m_225_Shen_2001_MatResBull_20275.csv'
ref_d1 =  data_dir + 'CaO2_F4--mmm_139_Kotov_1941_ZhurFizichKhim_20275.csv'

# path to output directory
output_dir = data_dir
# subfolder_save = True
output_file = 'CCO-XRD'

# font size, resolution (DPI), file type
fsize, dots, file_types = 10, [300], ['png','svg']
cols = [ 'maroon', 'grey', 'black', 'goldenrod' ]
dash, width = [ 4, 2 ], 1.5 # [ pix_on pix_off ], linewidth
norm = 100
# marks, msize, mwidth = [ 's', 'o' ], 7, 0.5
# leg_ents = [ 'GB Conductivity (300 $^\circ$C)', 'GB Concentration (EELS)' ]
x_lab = '${2\Theta}$ (Degrees)'
y1_lab, y2_lab = 'Counts (Arbitrary units)', ''
# naming sequence of figs with successive curves on same axis
# file_anno = [ '-0of1', '-1of1' ]
file_anno = [] # for single fig with all curves
x_lims, y1_lims, y2_lims = [25, 60], [-900, 200], [.1, .6]
y1_ticks = False


''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize
    
def save_fig( output_file_name, subfolder_save=True ):
    # create subfolder with date as name
    if subfolder_save:
        output_dir = data_dir + wf.date_str() + '/'
        if not os.path.isdir( output_dir ):
            os.mkdir( output_dir )

    for file_type in file_types:
        if file_type == 'png':
            for dot in dots:
                output_name = wf.save_name( output_dir, output_file_name, dot, 
                    file_type )
                pl.savefig( output_name, format = file_type, dpi = dot, 
                    transparent = True )
        elif file_type == 'svg':
                output_name = wf.save_name( output_dir, output_file_name, False, 
                    file_type )
                pl.savefig( output_name, format = file_type )

def clip_xy( lims_x, arr_x, arr_y ):
    min_ind = np.where( arr_x >= lims_x[0] )[0][0]
    max_ind = np.where( arr_x <= lims_x[1] )[0][-1]
    x_clip = arr_x[ min_ind:max_ind ]
    y_clip = arr_y[ min_ind:max_ind ]
    return x_clip, y_clip
    
''' ########################### MAIN SCRIPT ########################### '''

# READ AND STORE DATA IN VARIABLES
# d = np.loadtxt( data, skiprows = 1 )
d_exp = np.genfromtxt( exper_d, delimiter = ',' )
d_ref0 = np.genfromtxt( ref_d0, delimiter = ',' )
d_ref1 = np.genfromtxt( ref_d1, delimiter = ',' )

# x, x_gb, x_gb_err, S_gb, S_gb_err = d.T
# x_2p, y_2p = d_exp[:,0], d_exp[:,1]
x_2p, y_2p = clip_xy( x_lims, d_exp[:,0], d_exp[:,1] )
# x_2s, y_2s = d_exp[:,2], d_exp[:,3]
x_2s, y_2s = clip_xy( x_lims, d_exp[:,2], d_exp[:,3] )
# x_5p, y_5p = d_exp[:,4], d_exp[:,5]
x_5p, y_5p = clip_xy( x_lims, d_exp[:,4], d_exp[:,5] )
# x_5s, y_5s = d_exp[:,6], d_exp[:,7]
x_5s, y_5s = clip_xy( x_lims, d_exp[:,6], d_exp[:,7] )
# x_10p, y_10p = d_exp[:,8], d_exp[:,9]
x_10p, y_10p = clip_xy( x_lims, d_exp[:,8], d_exp[:,9] )
# x_10s, y_10s = d_exp[:,10], d_exp[:,11]
x_10s, y_10s = clip_xy( x_lims, d_exp[:,10], d_exp[:,11] )

# x_CaO, y_CaO = d_ref0[:,0], d_ref0[:,1]
x_CaO, y_CaO = clip_xy( x_lims, d_ref0[:,0], d_ref0[:,1] )
# x_CaO2, y_CaO2 = d_ref0[:,0], d_ref1[:,1]
x_CaO2, y_CaO2 = clip_xy( x_lims, d_ref0[:,0], d_ref1[:,1] )

ys = [ y_2p, y_2s, y_5p, y_5s, y_10p, y_10s, y_CaO, y_CaO2 ]
norm_ys = []

for i in np.arange( len(ys) ):
    norm_ys.append( wf.normalize( ys[i], norm ) - ( 1.2 * i * norm ) )


'''GENERATE FIGURES'''

if len( file_anno ) == 0:
    
    pl.close( 'all' ) # close all open figures
    pl.figure( figsize = ( 3.5, 3.5 ) ) # create a figure ( w, h )
    ax0 = pl.gca() # store current axis
    mpl_customizations() # apply customizations to matplotlib
    # wf.slide_art_styles() # figure styling
    fontsize = mpl.rcParams[ 'font.size' ]
    
    pl.plot( x_2p, norm_ys[0], color=cols[0], lw = width )
    pl.plot( x_2s, norm_ys[1], color=cols[0], dashes=dash, lw = width )
    pl.plot( x_5p, norm_ys[2], color=cols[1], lw = width )
    pl.plot( x_5s, norm_ys[3], color=cols[1], dashes=dash, lw = width )
    pl.plot( x_10p, norm_ys[4], color=cols[2], lw = width )
    pl.plot( x_10s, norm_ys[5], color=cols[2], dashes=dash, lw = width )
    pl.plot( x_CaO, norm_ys[6], color=cols[3], lw = width )
    pl.plot( x_CaO2, norm_ys[7], color=cols[3], dashes=dash, lw = width )
    
    ax0.set_xlim( x_lims )
    ax0.set_ylim( y1_lims )
    ax0.set_xlabel( x_lab )
    ax0.set_ylabel( y1_lab )
    ax0.set_yticks([])
    ax0.minorticks_on()
    
    # ax1_leg_hand = mpl.lines.Line2D( [], [], c=cols[0], marker=marks[0], ms=msize, ls='' )    
    # ax1.legend( [ax1_leg_hand], leg_ents, loc = 'upper right',
    #     numpoints =  1, frameon = False, fontsize = 10, labelspacing = .01,
    #     handletextpad = .01 )
    #         
    pl.tight_layout() # can run once to apply to all subplots, i think
    save_fig( output_file )
    

elif len( file_anno ) > 0:
    pass
    
# for h in range( 1, len( file_anno ) + 1 ):
#     
#     pl.close( 'all' ) # close all open figures
#     pl.figure( figsize = ( 4.4, 3 ) ) # create a figure ( w, h )
#     ax1 = pl.gca() # store current axis
#     mpl_customizations() # apply customizations to matplotlib
#     # wf.slide_art_styles() # figure styling
#     fontsize = mpl.rcParams[ 'font.size' ]
#         
#     ax1.errorbar( x, S_gb, yerr = S_gb_err, color = cols[0], marker = marks[0],
#         markersize = msize, linestyle = '--' )
#     ax1.set_yscale( 'log' ) # apply axis styling
#     ax1.set_xlim( x_lims )
#     ax1.set_ylim( y1_lims )
#     ax1.set_xlabel( x_lab )
#     ax1.set_ylabel( y1_lab )
#     ax1_leg_hand = mpl.lines.Line2D( [], [], c=cols[0], marker=marks[0], ms=msize, ls='' )
# 
#     if h == 1:
#     
#         ax1.legend( [ax1_leg_hand], leg_ents, loc = 'upper right',
#             numpoints =  1, frameon = False, fontsize = 10, labelspacing = .01,
#             handletextpad = .01 )
#                 
#         pl.tight_layout() # can run once to apply to all subplots, i think
#         
#         save_fig( output_file + file_anno[h-1] )
#         
#     if h == 2:
# 
#         ax2 = ax1.twinx() #create a second x-axis which shares ax1's y-axis
#         ax2.errorbar( x, x_gb, yerr = x_gb_err, color = cols[1], marker = marks[1],
#             markersize = msize, capsize=20 )
#         ax2.set_ylabel( y2_lab )
#         ax2.set_xlim( x_lims )
#         ax2.set_ylim( y2_lims )
#         ax2.minorticks_on()
#         ax2_leg_hand = mpl.lines.Line2D( [], [], c=cols[1], marker=marks[1], ms=msize, ls='' )
#         
#         legend_handles =  [ ax1_leg_hand, ax2_leg_hand ]
#         
#         ax2.legend( legend_handles, leg_ents, loc = 'upper right',
#             numpoints = 1, frameon = False, fontsize = 10, labelspacing = .01,
#             handletextpad = .01 )
#                 
#         pl.tight_layout() # can run once to apply to all subplots, i think
#         save_fig( output_file + file_anno[h-1] )


''' ########################### REFERENCES ########################### '''
'''
'''