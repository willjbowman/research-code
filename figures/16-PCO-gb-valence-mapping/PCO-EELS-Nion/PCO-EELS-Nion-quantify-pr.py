''' ########################### OVERVIEW ########################### '''
'''
Created 2016-09-04 by Will Bowman.
This script is for plotting k-factor for 10PCO on SiN
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
data_dir = paper_dir + 'data/' + fig_name + '/bkgd-sub/'

# path to output directory
output_dir = data_dir
output_file_name = ''
subfolder_save = True
save = True
# save = False

d_in_0, skip_0 = data_dir +\
    '160627_PCO10-Si3N4-850C_EELS-SI_tags.txt', 1
# d_in_1 = data_dir +\
#     '160627_PCO10-Si3N4-850C_EELS-SI_00_Ref20i_100meV_3mm_200ms--Ce M Edge Map.txt'
# d_in_2 = data_dir +\
#     '160627_PCO10-Si3N4-850C_EELS-SI_00_Ref20i_100meV_3mm_200ms--Pr M Edge Map.txt'
# d_in_3 = data_dir +\
#     '160627_PCO10-Si3N4-850C_EELS-SI_01_Ref20i_100meV_3mm_200ms--Ce M Edge Map.txt'
# d_in_4 = data_dir +\
#     '160627_PCO10-Si3N4-850C_EELS-SI_01_Ref20i_100meV_3mm_200ms--Pr M Edge Map.txt'
d_in = [ '160627_PCO10-Si3N4-850C_EELS-SI_00_Ref20i_100meV_3mm_200ms',
    '160627_PCO10-Si3N4-850C_EELS-SI_01_Ref20i_100meV_3mm_200ms',
    '160627_PCO10-Si3N4-850C_EELS-SI_02_Ref20i_100meV_3mm_200ms',
    '160627_PCO10-Si3N4-850C_EELS-SI_03_Ref20i_100meV_3mm_200ms',
    '160627_PCO10-Si3N4-850C_EELS-SI_04_Ref20i_100meV_3mm_200ms',
    '160627_PCO10-Si3N4-850C_EELS-SI_05_Ref20i_100meV_3mm_200ms',
    '160627_PCO10-Si3N4-850C_EELS-SI_06_Ref20i_100meV_3mm_200ms',
    '160627_PCO10-Si3N4-850C_EELS-SI_07_Ref20i_100meV_3mm_200ms',
    '160627_PCO10-Si3N4-850C_EELS-SI_08_Ref20i_100meV_3mm_200ms' ]

# naming sequence of figs with successive curves on same axis
file_anno = [ '-0of0' ] # for single fig with all curves
file_anno = [ '-area-ave-spectrum' ]
fig_size = [ (9,6), (6,6) ] # ( wid, hi ) in inches

# font size, resolution (DPI), file type
fsize, dots, file_types = 10, [300], ['png'] #,'svg']
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
x_lab = [ 'Distance (nm)' ]
y_lab = [ 'Distance (nm)' ]
x_lims = [ [-0,1], [-10,100], [870,970] ]
y_lims = [ [-.1,2.2], [-.1,11], [-.1,7.5] ]
z_lims = [ [0,0], [-.1,11], [-.1,7.5] ]
x_shift = [ '', 3, .5 ]
y_shift = [ '', .75, .5 ]
subplot_white_space = 0.1 # see pl.subplots_adjust()
# fill_x = [[[870,915],[930,960]],[[870,915],[930,960]]]
fill_xs = [ [ 875, 915, 925, 965 ] ]
fill_cs = [ 'lightgrey', wf.colors('pale_gold') ]
c_map = mpl.cm.gist_heat
c_map = mpl.cm.YlOrRd
c_map = mpl.cm.coolwarm
cbar_shrink = .5

I_ce_scalar = .49 # from t/lambda of the film and CeO2 calibration curve
C_pr_ce = .11 # nominal cation concentration ratio
k_pr_ce = 0.43 # +/- 0.05


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

''' ### STORE DATA IN VARIABLES ### '''
d_0 = np.genfromtxt( d_in_0, delimiter='\t', skiprows=skip_0 )

pl.close('all')
for i, file_name in enumerate(d_in):
    d_ce = data_dir + file_name + '--Ce M Edge Map.txt'
    d_pr = data_dir + file_name + '--Pr M Edge Map.txt'
    I_Ce = np.genfromtxt( d_ce, delimiter='\t' )
    I_Pr = np.genfromtxt( d_pr, delimiter='\t' )

    ''' ### COMPUTE CONCENTRATIONS FROM BKGD-SUB EELS INTENSITY ### '''
    # apply overlap correction to remove Ce component from Pr signal
    I_Pr_cor = I_Pr - I_ce_scalar * I_Ce
    # compute intensity ratio for k-factor equation
    I_Pr_cor_I_Ce = I_Pr_cor / I_Ce
    # compute the Pr concentration from k-factor
    alph = I_Pr_cor_I_Ce * k_pr_ce
    C_Pr = alph / ( 1 + alph )
    C_Ce = 1 - C_Pr

    ''' ### GENERATE FIGURES ### '''
    p_size = d_0[ i, 1 ]
    lims = [ p_size*x for x in [ 0, np.shape(I_Ce)[1], 0, np.shape(I_Ce)[0] ]]

    pl.figure( figsize=fig_size[0] )

    '''( (rows,cols), (subplot_index), colspan=2, rowspan=1 )'''
    pl.subplot2grid( (2,3), (0,0) )
    ax = pl.gca()
    # BKGD-SUB signal Ce
    pl.imshow( I_Ce, cmap=c_map, extent=lims, vmin=z_lims[0][0] )
    pl.colorbar( shrink=cbar_shrink )
    ax.set_title( 'I_Ce BKGD-SUB' )
    ax.set_xlabel( x_lab[0] )
    ax.set_ylabel( y_lab[0] )

    # BKGD-SUB signal Pr
    pl.subplot2grid( (2,3), (1,0) )
    pl.imshow( I_Pr, cmap=c_map, extent=lims, vmin=z_lims[0][0] )
    pl.colorbar( shrink=.5 )
    pl.gca().set_title( 'I_Pr BKGD-SUB' )

    pl.subplot2grid( (2,3), (0,1) )
    I_Pr_cor = I_Pr - I_ce_scalar * I_Ce
    pl.imshow( I_Pr_cor, cmap=c_map, extent=lims, vmin=0 )
    pl.colorbar( shrink=.5 )
    pl.gca().set_title( 'I_Pr_corr' )

    pl.subplot2grid( (2,3), (1,1) )
    I_Pr_cor_I_Ce = I_Pr_cor / I_Ce
    pl.imshow( I_Pr_cor_I_Ce, cmap=c_map, extent=lims, vmin=0, vmax=1 )
    pl.colorbar( shrink=.5 )
    pl.gca().set_title( 'I_Pr* / I_Ce' )

    pl.subplot2grid( (2,3), (1,2) )
    alph = I_Pr_cor_I_Ce * k_pr_ce
    C_Pr = alph / ( 1 + alph )
    pl.imshow( C_Pr, cmap=c_map, extent=lims, vmin=0, vmax=.5 )
    pl.colorbar( shrink=.5 )
    pl.gca().set_title( '[Pr]; areal ave. = ' + str(np.nanmean(C_Pr))[0:4] )

    pl.subplot2grid( (2,3), (0,2) )
    C_Ce = 1 - C_Pr
    pl.imshow( C_Ce, cmap=c_map, extent=lims, vmin=.5, vmax=1 )
    pl.colorbar( shrink=.5 )
    pl.gca().set_title( '[Ce]; areal ave. = ' + str(np.nanmean(C_Ce))[0:4] )

    pl.tight_layout()
    pl.show()
    if save:
        wf.save_fig( fig_dir, file_types, dots, output_file_name, file_name )

# # store columns in variables
# # d_x_0, d_y_0 = d_0.T
# d_d_0 = d_0.T
# d_x_0, d_y_0 = d_d_0[0,:], d_d_0[1:np.shape(d_d_0)[0]]

# ce_sta, ce_end, pr_sta, pr_end = wf.array_index( d_x_0, fill_xs[0] )
# # m5_sta, m4_end = ce_sta, ce_end
# # m5_end, m4_sta = wf.array_index( d_x_2, [893,893] )

# k_pr_ce = []
# for h in range( len(d_y_0) ):
#     spec = d_y_0[h,:]
#     I_ce = np.sum( spec[ ce_sta: ce_end ] )
#     I_pr = np.sum( spec[ pr_sta: pr_end ] )
#     I_pr_cor = I_pr - ( I_ce * I_ce_scalar )
#     I_pr_cor_ce = I_pr_cor / I_ce
#     k_pr_ce.append( C_pr_ce / I_pr_cor_ce )

# pl.figure()
# pl.plot( k_pr_ce, marker='o' )
# pl.gca().set_title( 'mean = ' + str(np.mean(k_pr_ce))[0:4] + ' std = ' +\
#     str(np.std(k_pr_ce))[0:4] )


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




# for i, anno in enumerate( file_anno ):
# # if len( file_anno ) == 0:
    
#     pl.close( 'all' ) # close all open figures
#     pl.figure( figsize=fig_size[i] ) # create a figure ( w, h )
#     mpl_customizations() # apply customizations to matplotlib
#     fontsize = mpl.rcParams[ 'font.size' ]

#     if i == 0:
#         # pl.subplot2grid( (1,2), (0,0) ) # ((rows,cols),(subplot_index))
#         # pl.subplot2grid( (4,4), (0,0), colspan=2, rowspan=2 ) # ((rows,cols),(subplot_index))
#         pl.plot( d_y_0, I_m5_m4, c=cols[0], marker=mark[0], linestyle='none' )
#         pl.plot( d_y_0, I_pr_ce, c=cols[1], marker=mark[1], linestyle='none' )
        
#         tl = np.polyfit( d_y_0, I_m5_m4, 1 )
#         tlp = pl.poly1d( tl )
#         pl.plot( d_y_0, tlp(d_y_0), c=cols[0], ls='--' )
        
#         tl = np.polyfit( d_y_0, I_pr_ce, 1 )
#         tlp = pl.poly1d( tl )
#         pl.plot( d_y_0, tlp(d_y_0), c=cols[1], ls='--' )

#         # pl.plot( d_ev_cl, y_off_cl_p, color=cols[1], lw=width, dashes=dash )
#         # fill_windows( d_ev_cl, y_lims[0][0], y_on_cl_p, fill_xs[0], fill_c )
        
#         ax0 = pl.gca() # store current axis
#         # ax0.set_xlim( x_lims[0] )
#         # ax0.set_ylim( y_lims[0] )
#         ax0.set_xlabel( x_lab[0][0] )
#         ax0.set_ylabel( y_lab[0] )
#         # ax0.set_yticks([])
#         # ax0.set_yticklabels([])
#         ax0.minorticks_on()
#         ax0.legend( leg_ents[0], loc='best', frameon=True, labelspacing=.1,
#             handletextpad=.1, numpoints=1)
#         pl.tight_layout()

#     elif i == 1:
#         '''((rows,cols),(subplot_index))'''
#         # pl.subplot2grid( (4,4), (0,2), colspan=2, rowspan=1 ) 
#         pl.subplot2grid( (1,2), (0,0) )
#         RGB, rgb_step = [128,0,0], 10
#         # for j in range( np.shape( d_y_1 )[0] ):
#         for j, si in enumerate( d_x_0 ):
#             rgb = [ x/255 for x in RGB ]
#             # d_y_1_p = norm( d_y_1[si,:], 15 )+j*y_shift[1]
#             d_y_1_p = wf.normalize( d_y_1[si,:], 15 ) + j * y_shift[1]
#             pl.plot( d_x_1, d_y_1_p, c=rgb, lw=1 )
#             t_lambda = d_y_0[j]
#             wf.centered_annotation( 90, np.nanmin( d_y_1_p )+.3, str( t_lambda ),
#                 color=rgb, fontsize=fontsize )
#             for ii, x in enumerate( RGB ):
#                 if x+rgb_step < 255:
#                     x = x+rgb_step
#                 else:
#                     x = 255
#                 RGB[ii] = x

#             # ((rows,cols),(subplot_index))
#             # d_ce_cl = 1 - d_pr_cl
#             # pl.errorbar( d_nm_cl, d_ce_cl, yerr=.01, c=cols[0], fmt='o',
#             #     capthick=1, markersize=4 )
#             wf.fill_windows( d_x_1, y_lims[1][0], d_y_1_p,
#                 fill_xs[1][0], fill_cs[0] )
#             wf.fill_windows( d_x_1, y_lims[1][0], d_y_1_p,
#                 fill_xs[1][1], fill_cs[1] )
            
#             ax1 = pl.gca() # store current axis
#             ax1.set_xlim( x_lims[1] )
#             ax1.set_ylim( y_lims[1] )
#             ax1.set_xlabel( x_lab[1] )
#             ax1.set_ylabel( y_lab[1] )
#             # # ax1.set_yticks([])
#             # ax1.set_xticklabels([])
#             ax1.minorticks_on()
#             # ax1.legend( leg_ents[1], loc='best', frameon=False, labelspacing=.1,
#             #     handletextpad=.1, numpoints=1 )

#         '''((rows,cols),(subplot_index))'''
#         pl.subplot2grid( (1,2), (0,1) ) # ((rows,cols),(subplot_index))
#         RGB = [128,0,0]

#         for k, si in enumerate( d_x_0 ):
#             rgb = [ x/255 for x in RGB ]
#             # d_y_2_p = norm( d_y_2[si,:], 1 )+k*y_shift[2]
#             d_y_2_p = wf.normalize( d_y_2[si,:], 1 ) + k * y_shift[2]
#             pl.plot( d_x_2, d_y_2_p, c=rgb, lw=1 )
#             for ii, x in enumerate( RGB ):
#                 if x+rgb_step < 255:
#                     x = x+rgb_step
#                 else:
#                     x = 255
#                 RGB[ii] = x
#             t_lambda = d_y_0[k]

#             # pl.subplot2grid( (4,4), (1,2), colspan=2, rowspan=1 ) # ((rows,cols),(subplot_index))
            
#             # pl.errorbar( d_nm_cl, 1-d_pr_cl, yerr=.01, c=cols[0], fmt='o',
#             #     capthick=1, markersize=5 )
#             # pl.errorbar( d_nm_cl, d_pr_cl, yerr=.01, c=cols[1], fmt='s',
#             #     capthick=1, markersize=5 )
#             # pl.fill_between( d_nm_cl, 0, d_pr_cl, facecolor=fill_c, 
#             #     edgecolor=fill_c, where= d_pr_cl >= .12 )
#             wf.fill_windows( d_x_2, y_lims[2][0], d_y_2_p, fill_xs[2], fill_c )
            
#             ax2 = pl.gca() # store current axis
#             ax2.set_xlim( x_lims[2] )
#             ax2.set_ylim( y_lims[2] )
#             ax2.set_xlabel( x_lab[2] )
#             # ax2.set_ylabel( y_lab[2] )
#             # ax1.set_yticks([])
#             ax2.minorticks_on()
#             # ax1_leg_hand = mpl.lines.Line2D( [], [], c=cols[0], marker=marks[0],
#                 # ms=msize, ls='' )    
#             # ax1.legend( leg_ents[1], loc='best', frameon=False, labelspacing=.1,
#             #     handletextpad=.1, numpoints=1 )

#         pl.subplots_adjust( wspace=subplot_white_space, bottom=0.15 )

#     # pl.tight_layout() # can run once to apply to all subplots, i think
#     pl.show()
#     if save:
#         wf.save_fig( fig_dir, file_types, dots, output_file_name, anno )

''' ########################### REFERENCES ########################### '''
'''
1. 
'''