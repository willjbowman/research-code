''' ########################### OVERVIEW ########################### '''
'''
 Created 2015-01-27 by Will Bowman. This figure shows EELS background removal
and plasmons in Ca-doped CeO2 and (b) background-subtracted EELS from 2, 5 and
10 mol% Ca-doped CeO2. This script creates and stores figures in the manuscript 
figures subdirectory and in the script's current directory.
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

# file info
path_data_dir = "C:/Crozier_Lab/Writing/2015_conductvity and chemistry of CaDC grain boundaries/figures/EELS_spectra_2_5_10_mol/"
# (a) background removal and plasmons
coreloss_filename = '141007_2Ca_06.s'
coreloss_stripped_filename = '10Ca_stripped.txt'
plasmon_on_filename = '141007_2Ca_ARM200kV_06_EELS_LL_gb4_6C_2.5mm_OnGb.s'
plasmon_off_filename = '141007_2Ca_ARM200kV_06_EELS_LL_gb4_6C_2.5mm_OffGb.s'
# (b) backround subtracted on/off gb all compositions
# on_10Ca_filename = 
# off_10Ca_filename = 
# on_5Ca_filename = 
# off_5Ca_filename = 
# on_2Ca_filename = 
# off_2Ca_filename = 

# FIGURE PARAMETERS
fig_size = ( wf.mm2in( 90 ), wf.mm2in( 130 ) ) # check journal fig size requirement
manu_fontsize, slide_fontsize = 8, 10 # 8pt for print, 10pt for presentation
output_file_name = 'EELS_spectra_2_5_10_mol'
# absolute path to manuscript sub directory (same as data store dir)
output_file_path = path_data_dir

# PLOT PARAMETERS
# subplot (a) - EELS and background removal
ax_a_limsx, ax_a_limsy = ( 250, 1e3 ), ( 200, 3e5 ) # axis ( min, max )
ax_a_labels = [ 'Energy loss (eV)', 'Counts (Arbitrary units)' ] # axis labels
ax_a_legend = [ 'On G.B.', 'Off G.B.' ] # legend entries
ax_a_inset_coords = [ .54, .745, .35, .2 ] # [ L, bot, W, H ]

# subplot (a) inset - plasmons on/off gb
ax_a_in_limsx, ax_a_in_limsy = ( -10, 80 ), ( 0, 3e5 ) # axis limits

# sublot (b) - all compositions on/off
curve_colors = [ 'maroon', 'grey', 'black' ]
ax_b_limsx, ax_b_limsy = ax_a_limsx, ( -600, 9e4 ) # axis limits
ax_b_labels = ax_a_labels

vshift_sm, vshift_lg = 2e4, 0 # vertical shift to separate spectra and compositions
dash = [ 4, 2 ] # define dashes ( [ pix_on, pix_off ] )
legend_std, legend_10Ca = 'Ca:Ce standard', '10 mol%' # legend text
legend_location = 'upper left' # legend locator
curve_color = 'maroon'

# INTEGRATION WINDOWS PARAMETERS
CaL_BG_min, CaL_BG_max, CaL_I_min, CaL_I_max = 240, 330, 340, 420
OK_BG_min, OK_BG_max, OK_I_min, OK_I_max = 430, 530, 533, 613
CeM_BG_min, CeM_BG_max, CeM_I_min, CeM_I_max = 780, 880, 883, 963
fill_color_BG = ( 192/255, 192/255, 192/255 ) # rgb are values < 1
fill_color_I = ( 255/255, 210/255, 210/255 ) # rgb are values < 1

# ANNOTATIONS PARAMETERS
anno_color = 'black'

# subplot (a) inset
ax_a_annox = [ 390, 553, 900 ] # label x position
ax_a_annoy = [ 24e4, 19e4, 185e3 ] # label y position
ax_a_anno_labels = [ 'Ca $L_{3,2}$', 'O K', 'Ce $M_{5,4}$' ] # label text strings
    
# subplot (a) inset - plasmons on/off gb
ax_a_in_annox = [ 16, 33 ] # label x position
ax_a_in_annoy = [ 26e4, 7e4 ] # label y position
ax_a_in_anno_labels = [ 'Z.L.P.', 'Plasmon' ] # label text strings

''' ########################### FUNCTIONS ########################### '''

def annotate_plot( xs, ys, labels, fontsize ):
    for i in np.arange( len( labels ) ):
        wf.centered_annotation( xs[i], ys[i], labels[i], anno_color, fontsize )
        
def apply_xy_labels( label_list ):
    pl.xlabel( label_list[0] ), pl.ylabel( label_list[1] )

def find_index( np_array, value ):
    # np.where returns tuple contatining np.array containing index of value in np_array, hence [0][0]. 
    return np.where( np_array == value )[0][0]
    
def sub_array( np_array, val_min, val_max ):
    min_ind = find_index( np_array, val_min )
    max_ind = find_index( np_array, val_max )
    return np_array[ min_ind : max_ind ]

def sub_arrays( np_array0, np_array1, val_min, val_max ):
    min_ind0 = find_index( np_array0, val_min )
    max_ind0 = find_index( np_array0, val_max )
    return np_array0[ min_ind0 : max_ind0 ], np_array1[ min_ind0 : max_ind0 ]
    
''' ########################### MAIN SCRIPT ########################### '''

# read in data files
coreloss = np.loadtxt( path_data_dir + coreloss_filename )
coreloss_stripped = np.loadtxt( path_data_dir + coreloss_stripped_filename )
plasmon_on = np.loadtxt( path_data_dir + plasmon_on_filename )
plasmon_off = np.loadtxt( path_data_dir + plasmon_off_filename )
# coreloss_10_on = np.loadtxt( path_data_dir + on_10Ca_filename )
# coreloss_10_off = np.loadtxt( path_data_dir + off_10Ca_filename )
# coreloss_5_on = np.loadtxt( path_data_dir + on_10Ca_filename )
# coreloss_5_off = np.loadtxt( path_data_dir + off_5Ca_filename )
# coreloss_2_on = np.loadtxt( path_data_dir + on_10Ca_filename )
# coreloss_2_off = np.loadtxt( path_data_dir + off_2Ca_filename )

# store data as variables
cl_x, cl_y = coreloss.T
cl_strip_x, cl_strip_y = coreloss_stripped.T
pl_on_x, pl_on_y = plasmon_on.T
pl_off_x, pl_off_y = plasmon_off.T
# cl10_on_x, cl10_on_y = coreloss_10_on.T
# cl10_off_x, cl10_off_y = coreloss_10_off.T
# cl5_on_x, cl5_on_y = coreloss_5_on.T
# cl5_off_x, cl5_off_y = coreloss_5_off.T
# cl2_on_x, cl2_on_y = coreloss_2_on.T
# cl2_off_x, cl2_off_y = coreloss_2_off.T

# INTEGRATION WINDOW
winx_BG_CaL, winy_BG_CaL = sub_arrays( cl_x, cl_y, CaL_BG_min, CaL_BG_max )
winx_I_CaL, winy_I_CaL = sub_arrays( cl_x, cl_y, CaL_I_min, CaL_I_max )
winx_BG_OK, winy_BG_OK = sub_arrays( cl_x, cl_y, OK_BG_min, OK_BG_max )
winx_I_OK, winy_I_OK = sub_arrays( cl_x, cl_y, OK_I_min, OK_I_max )
winx_BG_CeM, winy_BG_CeM = sub_arrays( cl_x, cl_y, CeM_BG_min, CeM_BG_max )
winx_I_CeM, winy_I_CeM = sub_arrays( cl_x, cl_y, CeM_I_min, CeM_I_max )

# GENERATE FIGURE
pl.close( 'all' ) # close any open figures
pl.figure( figsize = fig_size ) # create new figure
# generate_plot( manu_fontsize )
# generate_plot( slide_fontsize )

# create subplot (a)
# pl.subplot( 2, 1, 1 )
ax_a = pl.gca()
pl.plot( cl_x, cl_y + 7*vshift_sm, color = 'black' )
pl.plot( cl_x, cl_y + 6*vshift_sm, color = 'black', dashes = (4,1) )
pl.plot( cl_x, cl_y + 4*vshift_sm, color = 'grey' )
pl.plot( cl_x, cl_y + 3*vshift_sm, color = 'grey', dashes = (4,1) )
pl.plot( cl_x, cl_y + 1*vshift_sm, color = curve_color )
pl.plot( cl_x, cl_y, color = curve_color, dashes = (4,1) )

# integration_windows()
pl.fill_between( winx_BG_CaL, winy_BG_CaL+ 0*vshift_sm, color = fill_color_BG )
pl.fill_between( winx_I_CaL, winy_I_CaL+ 0*vshift_sm, color = fill_color_I )
pl.fill_between( winx_BG_OK, winy_BG_OK+ 0*vshift_sm, color = fill_color_BG )
pl.fill_between( winx_I_OK, winy_I_OK+ 0*vshift_sm, color = fill_color_I )
pl.fill_between( winx_BG_CeM, winy_BG_CeM+ 0*vshift_sm, color = fill_color_BG )
pl.fill_between( winx_I_CeM, winy_I_CeM+ 0*vshift_sm, color = fill_color_I )
pl.xlim( ax_a_limsx ), pl.ylim( ax_a_limsy ) # apply plot limits
pl.minorticks_on() # minor ticks on
ax_a.yaxis.set_ticklabels([]) # y tick labels off
pl.legend( ax_a_legend, frameon = False, fontsize = slide_fontsize, labelspacing = .01, handletextpad = 0.2, loc = 'upper left' )
apply_xy_labels( ax_a_labels )

annotate_plot( ax_a_annox, ax_a_annoy, ax_a_anno_labels, slide_fontsize )

# create subplot (a) inset axes
ax_a_in = pl.axes( ax_a_inset_coords )
pl.xlim( ax_a_in_limsx ), pl.ylim( ax_a_in_limsy )
pl.plot( pl_on_x, pl_on_y, color = curve_color )
pl.plot( pl_off_x, pl_off_y, color = curve_color, dashes = dash )

pl.minorticks_on() # minor ticks on
ax_a_in.set_xticks( np.linspace( 0, 70, 8 ) ) # xticks position
ax_a_in.set_yticks([]) # yticks off

annotate_plot( ax_a_in_annox, ax_a_in_annoy, ax_a_in_anno_labels, slide_fontsize )

'''
# create subplot (b)
pl.subplot( 2, 1, 2 )
ax_b = pl.gca()
# pl.plot( cl10_on_x, cl10_on_y )
# pl.plot( cl10_off_x, cl10_off_y )
# pl.plot( cl5_on_x, cl5_on_y )
# pl.plot( cl5_off_x, cl5_off_y )
# pl.plot( cl2_on_x, cl2_on_y )
# pl.plot( cl2_off_x, cl2_off_y )
# vshift_low = 3e4
# separation = 1e4
# for i in np.arange( len( curve_colors ) ):
#     for j in np.arange( 2 ):
#         vshift_0 = vshift_low * j
#         vshift_1 = vshift_0 + separation
#         pl.plot( cl_strip_x, cl_strip_y + vshift_0, color = curve_colors[ i ] )
#         pl.plot( cl_strip_x, cl_strip_y + vshift_0, color = curve_colors[ i ] )

pl.plot( cl_strip_x, cl_strip_y + 7*vshift_sm, color = 'black' )
pl.plot( cl_strip_x, cl_strip_y + 6*vshift_sm, color = 'black', dashes = (4,1) )
pl.plot( cl_strip_x, cl_strip_y + 4*vshift_sm, color = 'grey' )
pl.plot( cl_strip_x, cl_strip_y + 3*vshift_sm, color = 'grey', dashes = (4,1) )
pl.plot( cl_strip_x, cl_strip_y + vshift_sm, color = curve_color )
pl.plot( cl_strip_x, cl_strip_y, color = curve_color, dashes = (4,1) )
pl.xlim( ax_b_limsx ), pl.ylim( ax_b_limsy ) # apply plot limits
pl.minorticks_on() # minor ticks on
ax_b.yaxis.set_ticklabels([]) # y tick labels off
apply_xy_labels( ax_b_labels )
'''

# change font size of axis objects
for item in ( [ ax_a.xaxis.label, ax_a.yaxis.label, ax_a_in.xaxis.label, ax_a_in.yaxis.label ] + ax_a.get_xticklabels() + ax_a.get_yticklabels() + ax_a_in.get_xticklabels() + ax_a_in.get_yticklabels() ):
    item.set_fontsize( slide_fontsize )

pl.tight_layout()
    
''' ########################### REFERENCES ########################### '''
'''

'''