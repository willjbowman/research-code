''' ########################### OVERVIEW ########################### '''
'''
Created 2016-09-01 by Will Bowman.
This script is for plotting XRD pattern of 10PCO PLD pellet for a figure
'''

''' ########################### IMPORT MODULES ########################### '''
import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import csv, imp, os
import wills_functions as wf
imp.reload(wf) # reload wf 
##

''' ########################### USER-DEFINED ########################### '''
# path to data file
paper_dir = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/' +\
    '16_PCO-gb-valence-mapping/'
fig_name = 'PCO-EELS-Nion'
fig_dir = paper_dir + 'figures/' + fig_name + '/'
data_dir = paper_dir + 'data/' + fig_name + '/'
d_in = data_dir + 'PCO-EELS-Nion.txt'
# ref_d0 =  data_dir + 'CaO_Fm-3m_225_Shen_2001_MatResBull_20275.csv'
# ref_d1 =  data_dir + 'CaO2_F4--mmm_139_Kotov_1941_ZhurFizichKhim_20275.csv'

# path to output directory
output_dir = fig_dir
output_file_name = fig_name
subfolder_save = True
save = True
# save = False

# fig_size = ( 6, 6 ) # ( width, hight ) in inches
fig_size = ( 3, 3 ) # ( width, hight ) in inches

# font size, resolution (DPI), file type
fsize, dots, file_types = 10, [300], ['png','svg']
cols = [ 'maroon', 'grey', 'black', 'goldenrod' ]
dash, width = [ 6, 1 ], 1 # [ pix_on pix_off ], linewidth
norm = 100
# marks, msize, mwidth = [ 's', 'o' ], 7, 0.5
leg_ents = [ 
    [ 'GB', 'Grain' ], # core-loss
    [ '[Ce]', '[Pr]' ],
    [ 'GB', 'Grain' ],
    [ 'Pr 4f' ]
]
leg_loc = 'upper right'
x0_lab, x1_lab = 'Energy-loss (eV)', 'Distance (nm)'
y0_lab, y1_lab = 'Counts (Arbitrary units)', '(B-A)/A'
# naming sequence of figs with successive curves on same axis
file_anno = [ '-0of0' ] # for single fig with all curves
file_anno = [ '-core-loss', '-cation-profile', '-valence', '-prf4-profile' ]
x_lims = [[868,965],[-7,7],[868,965],[-7,7]]
y_lims = [[-.1,2.2],[[.85,.95],[0.05,.15]],[-.1,2.2],[]]
y_shift_on_cl, y_shift_off_cl = 1, 0
y_shift_on_vl, y_shift_off_vl = 1, 0
# y1_ticks = False
subplot_white_space = 0.05 # see pl.subplots_adjust()
# fill_x = [[[870,915],[930,960]],[[870,915],[930,960]]]
fill_xs = [ [ [875, 915], [926, 941] ], [ [875, 915], [925, 940] ] ]
bkgd_xs = [ [ [920, 926], [941, 945] ], [ [920, 925], [940, 945] ] ]
fill_c = wf.colors('pale_gold')
bkgd_c = 'pink'


''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize

# def fill_windows( x, y0, y1, fill_xs, fill_c ):
#     for i, xx in enumerate( fill_xs ):
#         if i < 1: # fill
#             pl.fill_between( x, y0, y1, facecolor=fill_c, edgecolor=fill_c,
#                 where= x > xx )
#         elif i % 2: # odd
#             pl.fill_between( x, y0, y1, facecolor='none', edgecolor=fill_c,
#                     where= x > xx )
#         else: # even
#             pl.fill_between( x, y0, y1, facecolor=fill_c, edgecolor=fill_c,
#                 where= x > xx )

def fill_windows( x, y0, y1, fill_xs, fill_c ):
    for i, xx in enumerate( fill_xs ):
        x_clipped, y_clipped, lims = wf.clip_xy( xx, x, y1 )
        pl.fill_between( x_clipped, y0, y_clipped, facecolor=fill_c, 
            edgecolor=fill_c )
    
''' ########################### MAIN SCRIPT ########################### '''

# READ AND STORE DATA IN VARIABLES
# d = np.loadtxt( data, skiprows = 1 )
d = np.genfromtxt( d_in, skiprows=0, delimiter='\t' )
# d_ref0 = np.genfromtxt( ref_d0, delimiter = ',' )

# store columns in variables
d_ev_cl, d_off_cl, d_on_cl, zz, d_nm_cl, d_pr_cl, zz, d_ev_vl, d_off_vl, d_on_vl, zz, d_nm_vl, d_pr_vl = d.T

# # clip raw data to x_lims to avoid .svg rendering issues
# x_pco, y_pco, x_lims_pco = wf.clip_xy( x_lims, d_x_pco, d_y_pco )
# x_ceo2, y_ceo2, x_lims_ceo2 = wf.clip_xy( x_lims, d_x_ceo2, d_y_ceo2 )
y_off_cl, y_on_cl = d_off_cl, d_on_cl
y_off_vl, y_on_vl = d_off_vl, d_on_vl

# # normalize, scale, shift curves for pretty plotting
y_on_cl_p = y_on_cl / np.nanmax( y_on_cl ) + y_shift_on_cl
y_off_cl_p = y_off_cl / np.nanmax( y_off_cl ) + y_shift_off_cl
y_on_vl_p = y_on_vl / np.nanmax( y_on_vl ) + y_shift_on_vl
y_off_vl_p = y_off_vl / np.nanmax( y_off_vl ) + y_shift_off_vl

''' ### GENERATE FIGURES ### '''
for i, anno in enumerate( file_anno ):
# if len( file_anno ) == 0:
    
    pl.close( 'all' ) # close all open figures
    pl.figure( figsize=fig_size ) # create a figure ( w, h )
    mpl_customizations() # apply customizations to matplotlib
    fontsize = mpl.rcParams[ 'font.size' ]

    if i == 0:
        # pl.subplot2grid( (2,2), (0,0) ) # ((rows,cols),(subplot_index))
        # pl.subplot2grid( (4,4), (0,0), colspan=2, rowspan=2 ) # ((rows,cols),(subplot_index))
        pl.plot( d_ev_cl, y_on_cl_p, color=cols[0], lw=width )
        pl.plot( d_ev_cl, y_off_cl_p, color=cols[1], lw=width, dashes=dash )
        fill_windows( d_ev_cl, y_lims[0][0], y_on_cl_p, fill_xs[0], fill_c )
        fill_windows( d_ev_cl, y_lims[0][0], y_on_cl_p, bkgd_xs[0], bkgd_c )
        
        ax0 = pl.gca() # store current axis
        ax0.set_xlim( x_lims[0] )
        ax0.set_ylim( y_lims[0] )
        ax0.set_xlabel( x0_lab )
        ax0.set_ylabel( y0_lab )
        # ax0.set_yticks([])
        ax0.set_yticklabels([])
        ax0.minorticks_on()
        ax0.legend( leg_ents[0], loc='best', frameon=False, labelspacing=.1,
            handletextpad=.1 )

    elif i == 1:
        pl.subplot2grid( (2,1), (0,0) ) # ((rows,cols),(subplot_index))
        # pl.subplot2grid( (4,4), (0,2), colspan=2, rowspan=1 ) # ((rows,cols),(subplot_index))
        d_ce_cl = 1 - d_pr_cl
        pl.errorbar( d_nm_cl, d_ce_cl, yerr=.01, c=cols[0], fmt='o',
            capthick=1, markersize=4 )
        pl.errorbar( d_nm_cl, d_pr_cl, yerr=.01, c=cols[1], fmt='s',
            capthick=1, markersize=4 )
        pl.fill_between( d_nm_cl, 0, d_ce_cl, facecolor=fill_c, 
            edgecolor=fill_c, where= d_ce_cl <= .88 )
        
        ax1 = pl.gca() # store current axis
        ax1.set_xlim( x_lims[1] )
        ax1.set_ylim( y_lims[1][0] )
        # ax1.set_xlabel( x1_lab )
        ax1.set_ylabel( '(Mole frac.)' )
        # ax1.set_yticks([])
        ax1.set_xticklabels([])
        ax1.minorticks_on()
        ax1.legend( leg_ents[1], loc='best', frameon=False, labelspacing=.1,
            handletextpad=.1, numpoints=1 )

        pl.subplot2grid( (2,1), (1,0) ) # ((rows,cols),(subplot_index))
        # pl.subplot2grid( (4,4), (1,2), colspan=2, rowspan=1 ) # ((rows,cols),(subplot_index))
        
        # pl.errorbar( d_nm_cl, 1-d_pr_cl, yerr=.01, c=cols[0], fmt='o',
        #     capthick=1, markersize=5 )
        pl.errorbar( d_nm_cl, d_pr_cl, yerr=.01, c=cols[1], fmt='s',
            capthick=1, markersize=5 )
        pl.fill_between( d_nm_cl, 0, d_pr_cl, facecolor=fill_c, 
            edgecolor=fill_c, where= d_pr_cl >= .12 )
        
        ax1 = pl.gca() # store current axis
        ax1.set_xlim( x_lims[1] )
        ax1.set_ylim( y_lims[1][1] )
        ax1.set_xlabel( x1_lab )
        ax1.set_ylabel( ' ' )
        # ax1.set_yticks([])
        ax1.minorticks_on()
        # ax1_leg_hand = mpl.lines.Line2D( [], [], c=cols[0], marker=marks[0],
            # ms=msize, ls='' )    
        # ax1.legend( leg_ents[1], loc='best', frameon=False, labelspacing=.1,
        #     handletextpad=.1, numpoints=1 )

        pl.subplots_adjust( wspace=subplot_white_space, bottom=0.15 )

    elif i == 2:
        # pl.subplot2grid( (2,2), (1,0) ) # ((rows,cols),(subplot_index))
        # pl.subplot2grid( (4,4), (2,0), colspan=2, rowspan=2 ) # ((rows,cols),(subplot_index))

        pl.plot( d_ev_cl, y_on_vl_p, color=cols[0], lw=width )
        pl.plot( d_ev_cl, y_off_vl_p, color=cols[1], lw=width, dashes=dash )
        fill_windows( d_ev_cl, y_lims[0][0], y_on_cl_p, fill_xs[1], fill_c )
        
        ax2 = pl.gca() # store current axis
        ax2.set_xlim( x_lims[2] )
        ax2.set_ylim( y_lims[2] )
        ax2.set_xlabel( x0_lab )
        ax2.set_ylabel( y0_lab )
        # ax2.set_yticks([])
        ax2.set_yticklabels([])
        ax2.minorticks_on()
        ax2.legend( leg_ents[2], loc='best', frameon=False, labelspacing=.1,
            handletextpad=.1 )

    elif i == 3:
        # pl.subplot2grid( (2,2), (1,1) ) # ((rows,cols),(subplot_index))
        # pl.subplot2grid( (4,4), (2,2), colspan=2, rowspan=2 ) # ((rows,cols),(subplot_index))
        
        pl.errorbar( d_nm_cl, 1-d_pr_cl, yerr=.01, c=cols[0], fmt='o',
            capthick=1, markersize=5 )
        
        ax3 = pl.gca() # store current axis
        ax3.set_xlim( x_lims[3] )
        # ax3.set_ylim( y0_lims )
        ax3.set_xlabel( x1_lab )
        ax3.set_ylabel( y1_lab )
        # ax3.set_yticks([])
        ax3.minorticks_on()
        # ax3.legend( leg_ents[3], loc='best', frameon=False, labelspacing=.1,
        #     handletextpad=.1, numpoints=1 )


    pl.tight_layout() # can run once to apply to all subplots, i think
    pl.show()
    if save:
        wf.save_fig( fig_dir, file_types, dots, output_file_name, anno )

''' ########################### REFERENCES ########################### '''
'''
1. 
'''