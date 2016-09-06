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
fig_name = 'CeO2-EELS-standard'
fig_dir = paper_dir + 'figures/' + fig_name + '/'
data_dir = paper_dir + 'data/' + fig_name + '/'
d_in_0, d_in_0_skip = data_dir +\
    'CeO2_crushed_STD_t-lambda.txt', 1
d_in_1, d_in_1_skip = data_dir +\
    'CeO2_crushed_STD_low-loss.txt', 2
d_in_2, d_in_2_skip = data_dir +\
    'CeO2_crushed_STD_core-loss.txt', 2

# naming sequence of figs with successive curves on same axis
file_anno = [ '-0of0' ] # for single fig with all curves
file_anno = [ '-A-vs-t', '-spectra' ]
fig_size = [ (3,3), (6,6) ] # ( wid, hi ) in inches

# path to output directory
output_dir = fig_dir
output_file_name = fig_name
subfolder_save = True
save = True
# save = False

# font size, resolution (DPI), file type
fsize, dots, file_types = 10, [300], ['png','svg']
cols = [ 'maroon', 'grey', 'black', 'goldenrod' ]
dash, width = [ 6, 1 ], 1 # [ pix_on pix_off ], linewidth
mark, msize, mwidth = [ 'o', '^', 'v', 's' ], 7, 0.5
leg_ents = [ 
    [ r'$I_{Ce}^{M_5}$/$I_{Ce}^{M_4}$', 
        r'$I_{Ce}^{925-965}$/$I_{Ce}^{870-915}$' ], # core-loss
    [ '[Ce]', '[Pr]' ],
    [ 'GB', 'Grain' ],
    [ 'Pr 4f' ]
]
leg_loc = 'upper right'
x_lab = [ [ r't / $\lambda$', 'Thickness (nm)' ], 'Energy-loss (eV)', 
    'Energy-loss (eV)' ]
y_lab = [ '', 'Counts (Arbitrary units)', '' ]
x_lims = [ [-0,1], [-10,100], [870,970] ]
y_lims = [ [-.1,2.2], [-.1,11], [-.1,7.5] ]
x_shift = [ '', 3, .5 ]
y_shift = [ '', .75, .5 ]
subplot_white_space = 0.1 # see pl.subplots_adjust()
# fill_x = [[[870,915],[930,960]],[[870,915],[930,960]]]
fill_xs = [ [], [ [-5, 5], [5, 50] ], [ 875, 915, 925, 965 ] ]
fill_cs = [ 'lightgrey', wf.colors('pale_gold') ]
lambda_ceo2 = 1


''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize

def norm( col, norm_max ):
    return col / np.nanmax( col ) * norm_max

def trendline( x, y, polyfit_degree ):
        tl = np.polyfit( x, y, polyfit_degree )
        tlp = pl.poly1d( tl )
        return x, tlp(x)
    
''' ########################### MAIN SCRIPT ########################### '''

# READ AND STORE DATA IN VARIABLES
d_0 = np.genfromtxt( d_in_0, delimiter='\t', skiprows=d_in_0_skip )
d_1 = np.genfromtxt( d_in_1, delimiter='\t', skiprows=d_in_1_skip )
d_2 = np.genfromtxt( d_in_2, delimiter='\t', skiprows=d_in_2_skip )

# store columns in variables
d_x_0, d_y_0 = d_0.T
d_d_1 = d_1.T
d_x_1, d_y_1 = d_d_1[0,:]+x_shift[1], d_d_1[1:np.shape(d_d_1)[0]]
d_d_2 = d_2.T
d_x_2, d_y_2 = d_d_2[0,:], d_d_2[1:np.shape(d_d_1)[0]]

ce_sta, ce_end, pr_sta, pr_end = wf.array_index( d_x_2, fill_xs[2] )
m5_sta, m4_end = ce_sta, ce_end
m5_end, m4_sta = wf.array_index( d_x_2, [893,893] )

d_y_2[:,1]
I_m5_m4, I_pr_ce = [], []
for h in range( len(d_y_0) ):
    spec = d_y_2[h,:]
    # I_ce_m5/I_ce_m4
    I_m5_m4.append(
        np.sum( spec[m5_sta:m5_end] ) / np.sum( spec[m4_sta:m4_end] ) )
    # I_ce_pr/I_ce_ce
    I_pr_ce.append( 
        np.sum( spec[pr_sta:pr_end] ) / np.sum( spec[ce_sta:ce_end] ) )


# # clip raw data to x_lims to avoid .svg rendering issues
# x_pco, y_pco, x_lims_pco = wf.clip_xy( x_lims, d_x_pco, d_y_pco )
# x_ceo2, y_ceo2, x_lims_ceo2 = wf.clip_xy( x_lims, d_x_ceo2, d_y_ceo2 )
# y_off_cl, y_on_cl = d_off_cl, d_on_cl
# y_off_vl, y_on_vl = d_off_vl, d_on_vl

# # normalize, scale, shift curves for pretty plotting
# y_on_cl_p = y_on_cl / np.nanmax( y_on_cl ) + y_shift_on_cl
# y_off_cl_p = y_off_cl / np.nanmax( y_off_cl ) + y_shift_off_cl
# y_on_vl_p = y_on_vl / np.nanmax( y_on_vl ) + y_shift_on_vl
# y_off_vl_p = y_off_vl / np.nanmax( y_off_vl ) + y_shift_off_vl

''' ### GENERATE FIGURES ### '''
for i, anno in enumerate( file_anno ):
# if len( file_anno ) == 0:
    
    pl.close( 'all' ) # close all open figures
    pl.figure( figsize=fig_size[i] ) # create a figure ( w, h )
    mpl_customizations() # apply customizations to matplotlib
    fontsize = mpl.rcParams[ 'font.size' ]

    if i == 0:
        # pl.subplot2grid( (1,2), (0,0) ) # ((rows,cols),(subplot_index))
        # pl.subplot2grid( (4,4), (0,0), colspan=2, rowspan=2 ) # ((rows,cols),(subplot_index))
        pl.plot( d_y_0, I_m5_m4, c=cols[0], marker=mark[0], linestyle='none' )
        pl.plot( d_y_0, I_pr_ce, c=cols[1], marker=mark[1], linestyle='none' )
        
        tl = np.polyfit( d_y_0, I_m5_m4, 1 )
        tlp = pl.poly1d( tl )
        pl.plot( d_y_0, tlp(d_y_0), c=cols[0], ls='--' )
        
        tl = np.polyfit( d_y_0, I_pr_ce, 1 )
        tlp = pl.poly1d( tl )
        pl.plot( d_y_0, tlp(d_y_0), c=cols[1], ls='--' )

        # pl.plot( d_ev_cl, y_off_cl_p, color=cols[1], lw=width, dashes=dash )
        # fill_windows( d_ev_cl, y_lims[0][0], y_on_cl_p, fill_xs[0], fill_c )
        
        ax0 = pl.gca() # store current axis
        # ax0.set_xlim( x_lims[0] )
        # ax0.set_ylim( y_lims[0] )
        ax0.set_xlabel( x_lab[0][0] )
        ax0.set_ylabel( y_lab[0] )
        # ax0.set_yticks([])
        # ax0.set_yticklabels([])
        ax0.minorticks_on()
        ax0.legend( leg_ents[0], loc='best', frameon=True, labelspacing=.1,
            handletextpad=.1, numpoints=1)
        pl.tight_layout()

    elif i == 1:
        '''((rows,cols),(subplot_index))'''
        # pl.subplot2grid( (4,4), (0,2), colspan=2, rowspan=1 ) 
        pl.subplot2grid( (1,2), (0,0) )
        RGB, rgb_step = [128,0,0], 10
        # for j in range( np.shape( d_y_1 )[0] ):
        for j, si in enumerate( d_x_0 ):
            rgb = [ x/255 for x in RGB ]
            # d_y_1_p = norm( d_y_1[si,:], 15 )+j*y_shift[1]
            d_y_1_p = wf.normalize( d_y_1[si,:], 15 ) + j * y_shift[1]
            pl.plot( d_x_1, d_y_1_p, c=rgb, lw=1 )
            t_lambda = d_y_0[j]
            wf.centered_annotation( 90, np.nanmin( d_y_1_p )+.3, str( t_lambda ),
                color=rgb, fontsize=fontsize )
            for ii, x in enumerate( RGB ):
                if x+rgb_step < 255:
                    x = x+rgb_step
                else:
                    x = 255
                RGB[ii] = x

            # ((rows,cols),(subplot_index))
            # d_ce_cl = 1 - d_pr_cl
            # pl.errorbar( d_nm_cl, d_ce_cl, yerr=.01, c=cols[0], fmt='o',
            #     capthick=1, markersize=4 )
            wf.fill_windows( d_x_1, y_lims[1][0], d_y_1_p,
                fill_xs[1][0], fill_cs[0] )
            wf.fill_windows( d_x_1, y_lims[1][0], d_y_1_p,
                fill_xs[1][1], fill_cs[1] )
            
            ax1 = pl.gca() # store current axis
            ax1.set_xlim( x_lims[1] )
            ax1.set_ylim( y_lims[1] )
            ax1.set_xlabel( x_lab[1] )
            ax1.set_ylabel( y_lab[1] )
            # # ax1.set_yticks([])
            # ax1.set_xticklabels([])
            ax1.minorticks_on()
            # ax1.legend( leg_ents[1], loc='best', frameon=False, labelspacing=.1,
            #     handletextpad=.1, numpoints=1 )

        '''((rows,cols),(subplot_index))'''
        pl.subplot2grid( (1,2), (0,1) ) # ((rows,cols),(subplot_index))
        RGB = [128,0,0]

        for k, si in enumerate( d_x_0 ):
            rgb = [ x/255 for x in RGB ]
            # d_y_2_p = norm( d_y_2[si,:], 1 )+k*y_shift[2]
            d_y_2_p = wf.normalize( d_y_2[si,:], 1 ) + k * y_shift[2]
            pl.plot( d_x_2, d_y_2_p, c=rgb, lw=1 )
            for ii, x in enumerate( RGB ):
                if x+rgb_step < 255:
                    x = x+rgb_step
                else:
                    x = 255
                RGB[ii] = x
            t_lambda = d_y_0[k]

            # pl.subplot2grid( (4,4), (1,2), colspan=2, rowspan=1 ) # ((rows,cols),(subplot_index))
            
            # pl.errorbar( d_nm_cl, 1-d_pr_cl, yerr=.01, c=cols[0], fmt='o',
            #     capthick=1, markersize=5 )
            # pl.errorbar( d_nm_cl, d_pr_cl, yerr=.01, c=cols[1], fmt='s',
            #     capthick=1, markersize=5 )
            # pl.fill_between( d_nm_cl, 0, d_pr_cl, facecolor=fill_c, 
            #     edgecolor=fill_c, where= d_pr_cl >= .12 )
            wf.fill_windows( d_x_2, y_lims[2][0], d_y_2_p, fill_xs[2], fill_c )
            
            ax2 = pl.gca() # store current axis
            ax2.set_xlim( x_lims[2] )
            ax2.set_ylim( y_lims[2] )
            ax2.set_xlabel( x_lab[2] )
            # ax2.set_ylabel( y_lab[2] )
            # ax1.set_yticks([])
            ax2.minorticks_on()
            # ax1_leg_hand = mpl.lines.Line2D( [], [], c=cols[0], marker=marks[0],
                # ms=msize, ls='' )    
            # ax1.legend( leg_ents[1], loc='best', frameon=False, labelspacing=.1,
            #     handletextpad=.1, numpoints=1 )

        pl.subplots_adjust( wspace=subplot_white_space, bottom=0.15 )

    # pl.tight_layout() # can run once to apply to all subplots, i think
    pl.show()
    if save:
        wf.save_fig( fig_dir, file_types, dots, output_file_name, anno )

''' ########################### REFERENCES ########################### '''
'''
1. 
'''