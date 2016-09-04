''' ########################### OVERVIEW ########################### '''
'''
Created 2016-09-02 by Will Bowman.
This script is for plotting core-loss intensity profiles 10PCO PLD SiN
'''

''' ########################### IMPORT MODULES ########################### '''
import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import csv, imp, os
import wills_functions as wf
imp.reload(wf) # reload wf

from mpl_toolkits.mplot3d import Axes3D # for surface plot
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
##

''' ########################### USER-DEFINED ########################### '''
# path to data file
paper_dir = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/' +\
    '16_PCO-gb-valence-mapping/'
fig_name = 'PCO-EELS-2010'
fig_dir = paper_dir + 'figures/' + fig_name + '/'
data_dir = paper_dir + 'data/' + fig_name + '/'
d_in_0 = data_dir +\
    '160716_PCO10-850c5h_EELS-SI_13_S_c2_eels-CL_700meV_3mm--I_profiles.txt'
d_in_1 = data_dir +\
    '160716_PCO10-850c5h_EELS-SI_14_S_c2_eels-CL_700meV_3mm--I_profiles.txt'
d_in_2 = data_dir +\
    '160716_PCO10-850c5h_EELS-SI_11_S_c2_eels-CL_700meV_3mm--I_profiles.txt'
d_in_3 = data_dir +\
    '160716_PCO10-850c5h_EELS-SI_14_S_c2_eels-CL_700meV_3mm.txt'

# ref_d0 =  data_dir + 'CaO_Fm-3m_225_Shen_2001_MatResBull_20275.csv'
# ref_d1 =  data_dir + 'CaO2_F4--mmm_139_Kotov_1941_ZhurFizichKhim_20275.csv'

# path to output directory
output_dir = fig_dir
output_file = fig_name
subfolder_save = True
save = True
# save = False

# naming sequence of figs with successive curves on same axis
# file_anno = [ [ '-0of0' ], [ ] ] # for single fig with all curves
file_anno = [ [  ], [ '-line-scan-2d', '-line-scan-3d' ] ]
fig_size = [ (6.5,3), [(4,1), (4.5,3)] ] # ( wid,hi ) in inches

# font size, resolution (DPI), file type
fsize, dots, file_types = 10, [300], ['png','svg']
cols = [ 'maroon', 'grey', 'black', 'goldenrod' ]
subplot_white_space = 0.05 # see pl.subplots_adjust()

'''can the style infor get abstracted to separate style file for each paper?'''

dash, width = [ 6, 1 ], 1 # [ pix_on pix_off ], linewidth
mark, msize, mwidth = [ 's', 'o', '^', 'v' ], 4, 0.5
leg_ents = [ r'Ce $M_{45}$', 'O K', 'N K', r'Pr $M_{45}$' ]
leg_ents = [ 'Ce M', 'O K', 'N K', 'Pr M' ]
leg_loc = 'upper left'
x_lab = [ 'Distance (nm)', '', '', 'Energy-loss (eV)']
y_lab = [ 'Backgrd-sub. inten. (Counts)', '', '', 'Distance (nm)']
z_lab = [ '', '', '', 'Inten. (Arb. units)']
x_lims = [ [0,10.5], [0,15], [0,16], [350,1e3], [200,1138] ]
y_lims = [ [0,7e5], [0,7e5], [0,7e5] ]
z_lims = [ [], [], [], [0,3e4] ]
y_step = .25 # nm
y_shift_pco, y_shift_ceo2 = 0, -1
# y1_ticks = False
c_map = cm.gist_heat

''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize
    
    
''' ########################### MAIN SCRIPT ########################### '''

''' ### STORE DATA IN VARIABLES ### '''
# d = np.loadtxt( data, skiprows = 1 )
d_0 = np.genfromtxt( d_in_0, delimiter='\t' )
d_1 = np.genfromtxt( d_in_1, delimiter='\t' )
d_2 = np.genfromtxt( d_in_2, delimiter='\t' )
d_2 = np.genfromtxt( d_in_2, delimiter='\t' )
d_3 = np.genfromtxt( d_in_3, delimiter='\t', skiprows=3 )
# d_ref0 = np.genfromtxt( ref_d0, delimiter = ',' )

# store columns in variables
d_x_0, d_y_0_c, d_y_0_n, d_y_0_o, d_y_0_ce, d_y_0_pr = d_0
d_x_1, d_y_1_c, d_y_1_n, d_y_1_o, d_y_1_ce, d_y_1_pr = d_1
d_x_2, d_y_2_c, d_y_2_n, d_y_2_o, d_y_2_ce, d_y_2_pr = d_2
d_d_3 = d_3.T
d_x_3 = d_d_3[0,:]
xstart_ind = np.where( d_x_3 > x_lims[3][0] )[0][0]
xend_ind = np.where( d_x_3 > x_lims[3][1] )[0][0]
# [colstart:colend,rowstart:rowend]
d_y_3 = d_d_3[ 20:35, xstart_ind:xend_ind ]
d_y_3 = d_d_3[ 1:-1, xstart_ind:xend_ind ]

# # clip raw data to x_lims to avoid .svg rendering issues
# x_pco, y_pco, x_lims_pco = wf.clip_xy( x_lims, d_x_pco, d_y_pco )
# x_ceo2, y_ceo2, x_lims_ceo2 = wf.clip_xy( x_lims, d_x_ceo2, d_y_ceo2 )

# # normalize, scale, shift curves for pretty plotting
x_3_p = d_x_3[ xstart_ind:xend_ind ]
y_3_p = d_y_3 / np.nanmax( d_y_3 ) * 10
# y_ceo2_p = y_ceo2 / np.nanmax( y_ceo2 ) + y_shift_ceo2

''' ### GENERATE FIGURES ### '''
for i, anno in enumerate( file_anno[0] ):
# if len( file_anno ) == 0:
    
    pl.close( 'all' ) # close all open figures
    pl.figure( figsize=fig_size[0] ) # create a figure ( w, h )
    mpl_customizations() # apply customizations to matplotlib
    fontsize = mpl.rcParams[ 'font.size' ]

    if i == 0:
        '''# ((rows,cols),(subplot_index))'''
        pl.subplot2grid( (1,3), (0,0) )
        
        pl.plot( d_x_0, d_y_0_ce, c=cols[0], marker=mark[0] )
        pl.plot( d_x_0, d_y_0_o, c=cols[1], marker=mark[1] )
        pl.plot( d_x_0, d_y_0_n, c=cols[2], marker=mark[2] )
        pl.plot( d_x_0, d_y_0_pr, c=cols[3], marker=mark[3] )
        
        ax0 = pl.gca() # store current axis
        ax0.set_xlim( x_lims[0] )
        ax0.set_ylim( y_lims[0] )
        ax0.set_xlabel( x_lab )
        ax0.set_ylabel( y0_lab )
        # ax0.set_yticks([])
        ax0.ticklabel_format( style='sci', useOffset=False )
        ax0.yaxis.get_major_formatter().set_powerlimits((0, 1))
        # ax1.set_xticklabels([])
        ax0.minorticks_on()
        ax0.legend( leg_ents, loc=leg_loc, frameon=False, labelspacing=.1,
            handletextpad=.3, numpoints=1 )

        '''# ((rows,cols),(subplot_index))'''
        pl.subplot2grid( (1,3), (0,1) )
        
        pl.plot( d_x_1, d_y_1_ce, c=cols[0], marker=mark[0] )
        pl.plot( d_x_1, d_y_1_o, c=cols[1], marker=mark[1] )
        pl.plot( d_x_1, d_y_1_n, c=cols[2], marker=mark[2] )
        pl.plot( d_x_1, d_y_1_pr, c=cols[3], marker=mark[3] )
        
        ax1 = pl.gca() # store current axis
        ax1.set_xlim( x_lims[1] )
        ax1.set_ylim( y_lims[1] )
        ax1.set_xlabel( x_lab )
        # ax1.set_ylabel( y0_lab )
        ax1.set_yticklabels([])
        # ax1.set_yticks([])
        # ax1.set_xticklabels([])
        ax1.minorticks_on()
        # ax1.legend( leg_ents, loc=leg_loc, frameon=False, labelspacing=.1,
        #     handletextpad=.1 )

        '''# ((rows,cols),(subplot_index))'''
        pl.subplot2grid( (1,3), (0,2) )
        
        pl.plot( d_x_2, d_y_2_ce, c=cols[0], marker=mark[0] )
        pl.plot( d_x_2, d_y_2_o, c=cols[1], marker=mark[1] )
        pl.plot( d_x_2, d_y_2_n, c=cols[2], marker=mark[2] )
        pl.plot( d_x_2, d_y_2_pr, c=cols[3], marker=mark[3] )
        
        ax2 = pl.gca() # store current axis
        ax2.set_xlim( x_lims[2] )
        ax2.set_ylim( y_lims[2] )
        ax2.set_xlabel( x_lab )
        # ax2.set_ylabel( y0_lab )
        ax2.set_yticklabels([])
        # ax2.set_yticks([])
        # ax2.set_xticklabels([])
        ax2.minorticks_on()

    if i == 1:
        '''# ((rows,cols),(subplot_index))'''
        pl.subplot2grid( (1,3), (0,0) )
        
        pl.plot( d_x_0, d_y_0_ce, c=cols[0], marker=mark[0] )
        pl.plot( d_x_0, d_y_0_o, c=cols[1], marker=mark[1] )
        pl.plot( d_x_0, d_y_0_n, c=cols[2], marker=mark[2] )
        pl.plot( d_x_0, d_y_0_pr, c=cols[3], marker=mark[3] )
        
        ax0 = pl.gca() # store current axis
        ax0.set_xlim( x_lims[0] )
        ax0.set_ylim( y_lims[0] )
        ax0.set_xlabel( x_lab )
        ax0.set_ylabel( y0_lab )
        # ax0.set_yticks([])
        ax0.ticklabel_format( style='sci', useOffset=False )
        ax0.yaxis.get_major_formatter().set_powerlimits((0, 1))
        # ax1.set_xticklabels([])
        ax0.minorticks_on()
        ax0.legend( leg_ents, loc=leg_loc, frameon=False, labelspacing=.1,
            handletextpad=.3, numpoints=1 )

    pl.tight_layout() # can run once to apply to all subplots, i think
    # pl.subplots_adjust( wspace=subplot_white_space, bottom=0.15 )
    # pl.subplots_adjust( wspace=subplot_white_space )
    # pl.show()

    if save:
        wf.save_fig( fig_dir, file_types, dots, output_file, anno )


for i, anno in enumerate( file_anno[1] ):
# if len( file_anno ) == 0:
    
    xmi, xma, x1 = x_3_p[0], x_3_p[-1], x_3_p[1]
    xx = np.arange( xmi, xma+x1-xmi, x1-xmi ) # drops last row of d_x
    xx = np.arange( xmi, xma, x1-xmi ) # drops last row of d_x
    yy = np.arange( 0, (np.shape( d_y_3 )[0]) )
    x, y, = np.meshgrid( xx, yy )

    if i == 0:
        
        pl.close( 'all' ) # close all open figures
        pl.figure( figsize=fig_size[1][i] ) # create a figure ( w, h )
        mpl_customizations() # apply customizations to matplotlib
        # fontsize = mpl.rcParams[ 'font.size' ]

        ax3 = pl.gca()
        # pl.imshow( y_3_p, cmap=c_map )
        # ax3.set_xlabel( x_lab[3] )
        # ax3.set_xticks( xx )
        # ax3.set_ylabel( y_lab[3] )
        # ax3.set_yticklabels( yy*y_step )

    if i == 1:
        
        # pl.close( 'all' ) # close all open figures
        fig_1 = pl.figure( figsize=fig_size[1][i] ) # create a figure ( w, h )
        mpl_customizations() # apply customizations to matplotlib
        # fontsize = mpl.rcParams[ 'font.size' ]

        ax4 = pl.gca( projection='3d' )
        surf = ax4.plot_surface( x, y*y_step, y_3_p, rstride=1, cstride=1, 
            cmap=c_map, linewidth=0, antialiased=False )

        fig_1.colorbar( surf, shrink=0.5, aspect=10 )
        # ax4.set_xlabel( x_lab[3], labelpad=1 )
        ax4.xaxis.set_major_locator( mpl.ticker.MultipleLocator( 200 ) )
        # ax4.set_ylabel( y_lab[3], labelpad=1 )
        ax4.yaxis.set_major_locator( mpl.ticker.MultipleLocator( 4 ) )
        # ax4.set_zlabel( z_lab[3], labelpad=1 )
        # ax4.set_xlim( x_lims[3] )
        # ax4.set_zlim( z_lims[3] )
        ax4.set_zticklabels([])
        ax4.view_init( azim=-125, elev=15 )

    pl.tight_layout() # can run once to apply to all subplots, i think
    # pl.subplots_adjust( wspace=subplot_white_space, bottom=0.15 )
    # pl.subplots_adjust( wspace=subplot_white_space )
    # pl.show()

    if save:
        wf.save_fig( fig_dir, file_types, dots, output_file, anno )

''' ########################### REFERENCES ########################### '''
'''
1. 
'''