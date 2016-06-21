''' ########################### OVERVIEW ########################### '''
'''
Created 2016-06-17 by Will Bowman. This script is for simulating Gouy-Chapman
profiles and comparing them to experimental cation profiles.
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

# # path to data file
data_dir = ("C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/"
"15_WJB_IS EBSD EELS Ca-Ceria gbs/figures/CCO-gouy-chapman/CCO10/")
exper_d0 = data_dir + 'map_03_gb_2.txt'
exper_d1 = data_dir + 'map_04_gb_2.txt'
# ref_d0 =  data_dir + 'CaO_Fm-3m_225_Shen_2001_MatResBull_20275.csv'
# ref_d1 =  data_dir + 'CaO2_F4--mmm_139_Kotov_1941_ZhurFizichKhim_20275.csv'

# # path to output directory
output_dir = data_dir
# subfolder_save = False # True by default, uncomment if you want False
output_file = 'CCO-gouy-chapman'

# # constants
# xs = np.arange( 0, 1e-8, 1e-10 ) # m; distance from GB
lambdas = np.arange( 0, 1e-8, 1e-9 ) # m; debye length
# lambdas = np.array([ 5e-9 ]) # m; debye length

dPhis = np.arange( 0, 1, 0.1 ) # V; change in space charge potential
# dPhis = np.array([ 0.41 ]) # V; change in space charge potential
# change in space charge potential (Tuller et al. 2011)

z = -1 # relative charge of mobile species, Ca_Ce// in this case
T = 1000 # K ; temperature (maybe the sintering temperature)

# e = 1.602177e-19 # C ; electronic charge
# e = wf.phys_constant( 'Electronic charge', 'C' ) # 1.602e-19 C; electron charge
e_ = 1 # elementary charge
# e = wf.phys_constant( 'Elementary charge', '' ) # 1; elementary charge
kb = 8.61733e-5 # 8.617e-5 eV/K ; Boltzmann constant
# kb = wf.phys_constant( 'Boltzmann', 'eV/K' ) # 8.617e-5 eV/K ; Boltzmann constant

# empirical parameters
# dPhi = 0.11 # V ; change in space charge potential
# Tuller, Bishop (2011); Cb=1700 ppm; T=773 K

# # font size, resolution (DPI), file type
# fsize, dots, file_types = 10, [300], ['png','svg']
# cols = [ 'maroon', 'grey', 'black', 'goldenrod' ]
# dash, width = [ 4, 2 ], 1.5 # [ pix_on pix_off ], linewidth
# norm = 100
# # marks, msize, mwidth = [ 's', 'o' ], 7, 0.5
# # leg_ents = [ 'GB Conductivity (300 $^\circ$C)', 'GB Concentration (EELS)' ]
# x_lab = '${2\Theta}$ (Degrees)'
# y1_lab, y2_lab = 'Counts (Arbitrary units)', ''
# # naming sequence of figs with successive curves on same axis
# # file_anno = [ '-0of1', '-1of1' ]
# file_anno = [] # for single fig with all curves
# x_lims, y1_lims, y2_lims = [25, 60], [-900, 200], [.1, .6]
# y1_ticks = False


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
    min_ind = np.where( arr_x > lims_x[0] )[0][0]
    max_ind = np.where( arr_x < lims_x[1] )[0][-1]
    x_clip = arr_x[ min_ind:max_ind ]
    y_clip = arr_y[ min_ind:max_ind ]
    return x_clip, y_clip

def calc_profile_param( d_Phi ):
    # return np.tanh( z * e * d_Phi / ( 4 * kb * T ) )
    return np.tanh( z * e_ * d_Phi / ( 4 * kb * T ) )

def calc_GC_CxCb( profile_param, xs, lambd ):
    numer = 1 + profile_param * np.exp( -xs / lambd )
    denom = 1 - profile_param * np.exp( -xs / lambd )
    # print( numer, denom )
    Cx_Cb = ( numer / denom ) ** ( 2 * z ) # array
    # print( Cx_Cb )
    return Cx_Cb

# d_exp = { 'xs_exp': xs_exp, 'Ca_exp': Ca_exp, 'Ca_bulk': Ca_bulk }
# lambdas and dPhis are arrays
# def fit_to_GC( d_exp, dPhi_n, lambd_n ):
#     xs_exp, Ca_exp = d_exp[ 'xs_exp' ], d_exp[ 'Ca_exp' ]
#     CxCb_exp = Ca_exp / d_exp[ 'Ca_bulk' ] # measured concentration ratio

#     lambd_n, dPhi_n = len( lambdas ), len( dPhis )
#     # 3D array for storing calculated GC_CxCb
#     GC_CxCb = np.zeros(( lambd_n, dPhi_n, len(xs_exp) ))
#     # 2D array for difference and absolute difference
#     CxCb_diff = np.zeros(( lambd_n, dPhi_n ))
#     CxCb_abs_diff = np.zeros(( lambd_n, dPhi_n ))

#     for i, dPhi in enumerate( dPhis ): # loop through dPhis
#         prof_param_i = calc_profile_param( dPhi ) # calculate profile parameter

#         for j, lambd in enumerate( lambdas ): # loop through lambdas
#             GC_CxCb_ij = calc_GC_CxCb( prof_param_i, xs_exp, lambd )
#             GC_CxCb[ i, j, : ] = GC_CxCb_ij # store CxCb profile in array 
#             CxCb_diff_ij = CxCb_exp - GC_CxCb_ij # diff between exp and simul
#             CxCb_diff[ i, j ] = CxCb_diff_ij
#             CxCb_abs_diff[ i, j ] = abs( CxCb_diff_ij )

#     min_abs_diff_ijs = np.where( CxCb_abs_diff==np.nanmin( CxCb_abs_diff ) )[0][0]
#     best_i, best_j = min_abs_diff_ijs[0], min_abs_diff_ijs[1]

#     fit_to_GC_result = {
#         'ijs': [ np.arange( 0, dPhi_n ), np.arange( 0, lambd_n ) ],
#         'GC_CxCb': GC_CxCb,
#         'CxCb_diff': CxCb_diff,
#         'CxCb_abs_diff': CxCb_abs_diff,
#         'lambda_ij': lambdas[ best_j ],
#         'dPhi_ij': dPhis[ best_i ],
#         'GC_CxCb_best': GC_CxCb[ best_i, best_j, : ]
#     }
#     return fit_to_GC_result

    
''' ########################### MAIN SCRIPT ########################### '''

'''
read in the data (1/2 profile array)
compute CxCb_exp
loop through dPhis to get matching CxCb min and max
loop through lambdas to optimize debye length
return values and plot exp and theo
'''

# # READ AND STORE DATA IN VARIABLES
# d = np.loadtxt( data, skiprows = 1 )
exp_d0 = np.loadtxt( exper_d0, skiprows=4 )
# exp_d1 = np.loadtxt( exper_d1, skiprows=4 )

# # x, I_CaL, I_OK, I_CeM, I_Ca/Ce, I_O/Ce, I_Ca/Ce, C_Ca, C_Ce, C_O = exp_d0.T
x_d0 = exp_d0[:,0] * 10e-9
Ca_d0 = exp_d0[:,8]
Ce_d0 = exp_d0[:,9]
O_d0 = exp_d0[:,10]

xs_exp = x_d0[ 1:20 ]
Ca_exp = Ca_d0[ 0:19 ][ ::-1 ] # reverse arrays so GB is at x=0
Ca_bulk = 0.1 # bulk concentration (mol/mol)
d_exp = {
    'xs_exp': xs_exp,
    'Ca_exp': Ca_exp,
    'Ca_bulk': Ca_bulk
}


# GC_fit_result = fit_to_GC( d_exp, dPhi_n, lambd_n )
'''start'''
xs_exp, Ca_exp = d_exp[ 'xs_exp' ], d_exp[ 'Ca_exp' ]
CxCb_exp = Ca_exp / d_exp[ 'Ca_bulk' ] # measured concentration ratio

dPhi_n, lambd_n = len( dPhis ), len( lambdas )
# 3D array for storing calculated GC_CxCb and difference curves
GC_CxCb = np.zeros(( dPhi_n, lambd_n, len(xs_exp) ))
CxCb_diff = np.zeros(( dPhi_n, lambd_n, len(xs_exp) ))
# 2D array for mean of difference curve and absolute difference
profile_params = np.zeros( dPhi_n )
CxCb_diff_mean = np.zeros(( dPhi_n, lambd_n ))
CxCb_abs_diff_mean = np.zeros(( dPhi_n, lambd_n ))

# pl.figure()

for i, dPhi in enumerate( dPhis ): # loop through dPhis
    prof_param_i = calc_profile_param( dPhi ) # calculate profile parameter
    profile_params[i] = prof_param_i
    # print( prof_param_i )

    for j, lambd in enumerate( lambdas ): # loop through lambdas
        GC_CxCb_ij = calc_GC_CxCb( prof_param_i, xs_exp, lambd )
        # pl.plot( xs_exp, GC_CxCb_ij )
        GC_CxCb[ i, j, : ] = GC_CxCb_ij # store CxCb profile in array 
        CxCb_diff_ij = CxCb_exp - GC_CxCb_ij # diff between exp and simul
        CxCb_diff[ i, j, : ] = CxCb_diff_ij # difference curve
        CxCb_diff_mean[ i, j ] = CxCb_diff_ij.mean() # mean of difference curve
        CxCb_abs_diff_mean[ i, j ] = abs( CxCb_diff_ij.mean() )

# [http://stackoverflow.com/questions/3230067/numpy-minimum-in-row-column-format]
min_abs_diff_mean_ijs = np.unravel_index(
    CxCb_abs_diff_mean.argmin(), CxCb_abs_diff_mean.shape )
best_i, best_j = min_abs_diff_mean_ijs[0], min_abs_diff_mean_ijs[1]

# fit_to_GC_result = {
GC_fit_result = {
    'ijs': [ np.arange( 0, dPhi_n ), np.arange( 0, lambd_n ) ], # i, j values
    'GC_CxCb': GC_CxCb, # 3D array of all GC profiles calculated
    'CxCb_diff': CxCb_diff[ best_i, best_j, : ], # 1D array best difference curve
    'CxCb_diff_mean': CxCb_diff_mean[ best_i, best_j ], # int with mean of CxCb_diff
    'CxCb_abs_diff_mean': CxCb_abs_diff_mean, # int with absolute value of CxCb_diff_mean
    'lambda_ij': lambdas[ best_j ], # Debye length from best fit
    'dPhi_ij': dPhis[ best_i ], # Potential from best fit
    'GC_CxCb_best': GC_CxCb[ best_i, best_j, : ] # CxCb profile from best fit
}
'''end'''

# parse the results and store in variables
ijs = GC_fit_result[ 'ijs' ]
GC_CxCb = GC_fit_result[ 'GC_CxCb' ]
CxCb_diff_mean = GC_fit_result[ 'CxCb_diff_mean' ]
CxCb_abs_diff_mean = GC_fit_result[ 'CxCb_abs_diff_mean' ]
lambda_ij = GC_fit_result[ 'lambda_ij' ]
dPhi_ij = GC_fit_result[ 'dPhi_ij' ]
GC_CxCb_best = GC_fit_result[ 'GC_CxCb_best' ]

'''OUTPUT'''
# surface plots of CxCb_diff and CxCb_abs_diff
#     [is], [js], 
# best lamd_ij, dPhi_ij, CxCb_ij

''''PLOTS'''
# print( lambda_ij, dPhi_ij )
# plot(xs_exp, [CxCb_exp, CxCb_ij])

# pl.close( 'all' ) # close all open figures
pl.figure()
pl.plot( xs_exp, CxCb_exp ) # experimental data
pl.plot( xs_exp, GC_CxCb_best ) # fit
ax = pl.gca()
ax.set_ylabel( 'C(x)/C_bulk' )
ax.set_xlabel( 'Distance from GB (m)' )
ax.set_title( 'dPhi = '+str(dPhi_ij)+' V; lambda = '+str(lambd)+' m; '+
     'z = '+str(z)+'; T = '+str(T)+' K' )
# print( lambda_ij, dPhi_ij )

# pl.figure()
# pl.plot( dPhis, profile_param )
# ax = pl.gca()

#     pl.figure( figsize = ( 3.5, 3.5 ) ) # create a figure ( w, h )
#     ax0 = pl.gca() # store current axis
#     mpl_customizations() # apply customizations to matplotlib

# pl.figure()
# pl.semilogy( xs, CxCb[0] )
# ax = pl.gca()
# ax.set_title( 'dPhi = '+str(dPhi)+' V; z = '+str(z)+'; T = '+str(T)+
#     ' K; lambda= '+str(lambd)+' m')

# pl.figure()
# pl.plot( dPhis, profile_param )



# pl.figure()
# surface plot of CxCb_diff CxCb_abs_diff

# x_d1 = exp_d1[:,0]
# Ca_d1 = exp_d1[:,8]
# Ce_d1 = exp_d1[:,9]
# O_d1 = exp_d1[:,10]

# # x_2p, y_2p = d_exp[:,0], d_exp[:,1]
# x_2p, y_2p = clip_xy( x_lims, d_exp[:,0], d_exp[:,1] )
# # x_2s, y_2s = d_exp[:,2], d_exp[:,3]
# x_2s, y_2s = clip_xy( x_lims, d_exp[:,2], d_exp[:,3] )
# # x_5p, y_5p = d_exp[:,4], d_exp[:,5]
# x_5p, y_5p = clip_xy( x_lims, d_exp[:,4], d_exp[:,5] )
# # x_5s, y_5s = d_exp[:,6], d_exp[:,7]
# x_5s, y_5s = clip_xy( x_lims, d_exp[:,6], d_exp[:,7] )
# # x_10p, y_10p = d_exp[:,8], d_exp[:,9]
# x_10p, y_10p = clip_xy( x_lims, d_exp[:,8], d_exp[:,9] )
# # x_10s, y_10s = d_exp[:,10], d_exp[:,11]
# x_10s, y_10s = clip_xy( x_lims, d_exp[:,10], d_exp[:,11] )

# # x_CaO, y_CaO = d_ref0[:,0], d_ref0[:,1]
# x_CaO, y_CaO = clip_xy( x_lims, d_ref0[:,0], d_ref0[:,1] )
# # x_CaO2, y_CaO2 = d_ref0[:,0], d_ref1[:,1]
# x_CaO2, y_CaO2 = clip_xy( x_lims, d_ref0[:,0], d_ref1[:,1] )

# ys = [ y_2p, y_2s, y_5p, y_5s, y_10p, y_10s, y_CaO, y_CaO2 ]
# norm_ys = []

# for i in np.arange( len(ys) ):
#     norm_ys.append( wf.normalize( ys[i], norm ) - ( 1.2 * i * norm ) )


# '''GENERATE FIGURES'''

# if len( file_anno ) == 0:
    
#     pl.close( 'all' ) # close all open figures
#     pl.figure( figsize = ( 3.5, 3.5 ) ) # create a figure ( w, h )
#     ax0 = pl.gca() # store current axis
#     mpl_customizations() # apply customizations to matplotlib
#     # wf.slide_art_styles() # figure styling
#     fontsize = mpl.rcParams[ 'font.size' ]
    
#     pl.plot( x_2p, norm_ys[0], color=cols[0], lw = width )
#     pl.plot( x_2s, norm_ys[1], color=cols[0], dashes=dash, lw = width )
#     pl.plot( x_5p, norm_ys[2], color=cols[1], lw = width )
#     pl.plot( x_5s, norm_ys[3], color=cols[1], dashes=dash, lw = width )
#     pl.plot( x_10p, norm_ys[4], color=cols[2], lw = width )
#     pl.plot( x_10s, norm_ys[5], color=cols[2], dashes=dash, lw = width )
#     pl.plot( x_CaO, norm_ys[6], color=cols[3], lw = width )
#     pl.plot( x_CaO2, norm_ys[7], color=cols[3], dashes=dash, lw = width )
    
#     ax0.set_xlim( x_lims )
#     ax0.set_ylim( y1_lims )
#     ax0.set_xlabel( x_lab )
#     ax0.set_ylabel( y1_lab )
#     ax0.set_yticks([])
#     ax0.minorticks_on()
    
#     # ax1_leg_hand = mpl.lines.Line2D( [], [], c=cols[0], marker=marks[0], ms=msize, ls='' )    
#     # ax1.legend( [ax1_leg_hand], leg_ents, loc = 'upper right',
#     #     numpoints =  1, frameon = False, fontsize = 10, labelspacing = .01,
#     #     handletextpad = .01 )
#     #         
#     pl.tight_layout() # can run once to apply to all subplots, i think
#     save_fig( output_file )
    

# elif len( file_anno ) > 0:
#     pass
    
# # for h in range( 1, len( file_anno ) + 1 ):
# #     
# #     pl.close( 'all' ) # close all open figures
# #     pl.figure( figsize = ( 4.4, 3 ) ) # create a figure ( w, h )
# #     ax1 = pl.gca() # store current axis
# #     mpl_customizations() # apply customizations to matplotlib
# #     # wf.slide_art_styles() # figure styling
# #     fontsize = mpl.rcParams[ 'font.size' ]
# #         
# #     ax1.errorbar( x, S_gb, yerr = S_gb_err, color = cols[0], marker = marks[0],
# #         markersize = msize, linestyle = '--' )
# #     ax1.set_yscale( 'log' ) # apply axis styling
# #     ax1.set_xlim( x_lims )
# #     ax1.set_ylim( y1_lims )
# #     ax1.set_xlabel( x_lab )
# #     ax1.set_ylabel( y1_lab )
# #     ax1_leg_hand = mpl.lines.Line2D( [], [], c=cols[0], marker=marks[0], ms=msize, ls='' )
# # 
# #     if h == 1:
# #     
# #         ax1.legend( [ax1_leg_hand], leg_ents, loc = 'upper right',
# #             numpoints =  1, frameon = False, fontsize = 10, labelspacing = .01,
# #             handletextpad = .01 )
# #                 
# #         pl.tight_layout() # can run once to apply to all subplots, i think
# #         
# #         save_fig( output_file + file_anno[h-1] )
# #         
# #     if h == 2:
# # 
# #         ax2 = ax1.twinx() #create a second x-axis which shares ax1's y-axis
# #         ax2.errorbar( x, x_gb, yerr = x_gb_err, color = cols[1], marker = marks[1],
# #             markersize = msize, capsize=20 )
# #         ax2.set_ylabel( y2_lab )
# #         ax2.set_xlim( x_lims )
# #         ax2.set_ylim( y2_lims )
# #         ax2.minorticks_on()
# #         ax2_leg_hand = mpl.lines.Line2D( [], [], c=cols[1], marker=marks[1], ms=msize, ls='' )
# #         
# #         legend_handles =  [ ax1_leg_hand, ax2_leg_hand ]
# #         
# #         ax2.legend( legend_handles, leg_ents, loc = 'upper right',
# #             numpoints = 1, frameon = False, fontsize = 10, labelspacing = .01,
# #             handletextpad = .01 )
# #                 
# #         pl.tight_layout() # can run once to apply to all subplots, i think
# #         save_fig( output_file + file_anno[h-1] )


''' ########################### REFERENCES ########################### '''
'''
'''