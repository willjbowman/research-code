# plot conductivity calculated in IsFit2Conductivity.py
# reads in '*_calculatedConductivity.txt' file created with IsFit2Conductivity.py

import numpy as np
import pylab as pl
import matplotlib as mpl

## import file, store values
# to generate arrhenius plot from n files. could make this programmatic within a given folder
# input_file_name_roots = [ '140329_sdCaDC10_100-700c(1)', '140327_sdCaDC5_100-700c', '140325_sdCaDC2_100-700c' ]
input_file_name_roots = [ 
    'C:/Users/willb/Dropbox/Crozier Group Users - Will Bowman/Crozier_Lab/Writing/2015_IS EBSD EELS of CaCeria grain boundaries/figures/arrhenius plot/140329_sdCaDC10_100-700c(1)_CalculatedConductivityErr.txt',
    'C:/Users/willb/Dropbox/Crozier Group Users - Will Bowman/Crozier_Lab/Writing/2015_IS EBSD EELS of CaCeria grain boundaries/figures/arrhenius plot/140327_sdCaDC5_100-700c_CalculatedConductivityErr.txt',
    'C:/Users/willb/Dropbox/Crozier Group Users - Will Bowman/Crozier_Lab/Writing/2015_IS EBSD EELS of CaCeria grain boundaries/figures/arrhenius plot/140325_sdCaDC2_100-700c_CalculatedConductivityErr.txt'
]
inp_files = np.size( input_file_name_roots ) # count input files

output_file_dir = 'C:/Users/willb/Dropbox/Crozier Group Users - Will Bowman/Crozier_Lab/research_PhD/code/github/figures/15_CaCeO_EIS_EELS_manuscript/fig2d-small-arrhenius-average-gb-conductivity/'
output_file_name = 'Ca_2_5_10_arrhenius_specificGB_w_errorbar'

legend_labels = [ '10', '5', '2' ]
markers = [ 'o', '^', 'd' ]
marker_colors = [ 'black', 'slategray', 'maroon' ]
marker_size, legend_marker_size = 4, 6
legend_handles = [ ] # container for legend handles (filled in loop)

ymin, ymax, xmin, xmax = 1e-11, 1e2, 0.9, 2.6 # plot limits

inv_Tk_axis_label = '$10^3 T^{-1} (K^{-1})$' # x1, y, x2 axis labels
y_axis_label = 'log($\sigma$T) (S $cm^{-1}$ K)'
Tc_axis_label = 'T ($^\circ$C)'

# ax2_Tc_ticks = np.linspace( 700, 100, 13 ) # Celcius axis ticks and labels
# ax2_Tc_ticklabels = np.array( [ 700, '', '', '', '', '', 400, '', '', '', 200, '', 100 ] )
ax2_Tc_ticks = np.linspace( 700, 100, 7 ) # Celcius axis ticks and labels
ax2_Tc_ticklabels = np.array( [ 700, '', '', 400, '', 200, 100 ] )

grain_text_label_x, grain_text_label_y = 1.8, 1e0 # text annotation info
grain_text_horiz_align, grain_text_vert_align = 'center', 'center'
gb_text_label_x, gb_text_label_y = 1.6, 1e-9
gb_text_horiz_align, gb_text_vert_align = 'center', 'center'

mpl.rcParams[ 'font.family' ] = 'sans-serif' # modify matplotlib defaults
mpl.rcParams[ 'font.weight' ] = 'normal'
mpl.rcParams[ 'font.size' ] = 10
mpl.rcParams[ 'mathtext.default' ] = 'regular'

major_locators = [ 0.6, 10-4 ]

pl.close( 'all' ) # create figure object
pl.figure( figsize = ( 2.3, 2.4 ) ) #create figure
pl.xlim( [ xmin, xmax ] ) #define chart limits
pl.ylim( [ ymin, ymax ] )
ax1 = pl.gca() # store first axis data (1000/T)
ax2 = ax1.twiny() #create a second x-axis which shares ax1's y-axis

# adjusted error so the top and bottom bar show up (keeping the same approximate gap between)
# sigGb_err_Tk_i_adjusted = [
#     np.array([
#     2.08144536e-07,   4.46322787e-06,   8.92110724e-05,   7.50096374e-04,
#     4.59206903e-03,   0.00000000e+00,   0.00000000e+00,  0.00000000e+00,
#     0.00000000e+00,   0.00000000e+00,   0.00000000e+00,  0.00000000e+00, ]),
#     np.array([
#     3.34985588e-08,   7.51584289e-07,   1.25582689e-05,   3.19698804e-04,
#     0.00000000e+00,   0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
#     0.00000000e+00,   0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ]),
#     np.array([
#     0.00000000e+00,   4.36638955e-11,   3.98458064e-10,   1.21449695e-08,
#     2.94722269e-07,   8.04224260e-06,   0.00000000e+00,   0.00000000e+00,
#     0.00000000e+00,   0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ])
# ]
sigGb_err_Tk_i_adjusted = [
    np.array([
    0.9544536e-07,   1.4322787e-06,   1.52110724e-05,   1.05096374e-04,
    3.9206903e-04,   0.00000000e+00,   0.00000000e+00,  0.00000000e+00,
    0.00000000e+00,   0.00000000e+00,   0.00000000e+00,  0.00000000e+00, ]),
    np.array([
    3.34985588e-08,   7.51584289e-07,   0.25582689e-05,   0.519698804e-04,
    0.00000000e+00,   0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
    0.00000000e+00,   0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ]),
    np.array([
    0.00000000e+00,   4.36638955e-11,   3.98458064e-10,   1.21449695e-08,
    1.94722269e-07,   1.04224260e-06,   0.00000000e+00,   0.00000000e+00,
    0.00000000e+00,   0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ])
]

for i in range( inp_files ) :
    file_name_i = input_file_name_roots[ i ]
    calcd_cond = np.loadtxt( file_name_i ) # read in conductivity data file

    Tc_calibrated = calcd_cond[ :, 0 ]
    Tk_calibrated = Tc_calibrated + 273
    inv_Tk_i = 1000 / Tk_calibrated
    
    sigG = calcd_cond[ :, 1 ]
    sigG_Tk_i = sigG * Tk_calibrated
    
    sigG_err = calcd_cond[ :, 2 ]
    sigG_err_Tk_i = sigG_err * Tk_calibrated
    
    sigGb = calcd_cond[ :, 3 ]
    sigGb_Tk_i = sigGb * Tk_calibrated
    
    sigGb_err = calcd_cond[ :, 4 ]
    # sigGb_err_Tk_i = sigGb_err * Tk_calibrated
    sigGb_err_Tk_i = sigGb_err_Tk_i_adjusted[ i ]
    # print( sigGb_err_Tk_i )
    
    color = marker_colors[ i ] # get ith curve styling
    marker = markers[ i ]
    # plot grain and grain boundary curves on 1st axis
    ax1.errorbar( inv_Tk_i, sigG_Tk_i, yerr = sigG_err_Tk_i,
        marker = marker, color = color, linestyle = '', markersize = marker_size,
        markerfacecolor = 'none', markeredgecolor = color )
    # ax1.errorbar( inv_Tk_i, sigG_Tk_i, yerr = sigG_err_Tk_i,
    #     marker = marker, color = color, linestyle = '', markersize = marker_size,
    #     markerfacecolor = 'none', markeredgecolor = color )
    ax1.errorbar( inv_Tk_i, sigGb_Tk_i, yerr = sigGb_err_Tk_i,
        marker = marker, color = color, linestyle = '', markersize = marker_size,
        markerfacecolor = color , markeredgecolor = color )
        
    ax1.xaxis.set_major_locator( mpl.ticker.MultipleLocator( major_locators[ 0 ] ) )
    ax1.yaxis.set_major_locator( mpl.ticker.MultipleLocator( major_locators[ 1 ] ) )
    
    # legend handler for ith curve
    legend_info_i = mpl.lines.Line2D( [], [], color = color, marker = marker, 
        markersize = legend_marker_size, fillstyle = 'right', linestyle = '' )
    legend_handles.append( legend_info_i ) # append ith legend handler to legend handles

ax1.set_yscale( 'log' ) # apply axis styling
y_ticks = np.logspace( -10, 2, num = 4 )
ax1.set_yticks( y_ticks )
ax1.set_yticklabels( [ -10, -6, -2, 2 ] )
# ax1.get_xaxis().set_major_formatter( mpl.ticker.ScalarFormatter() )
# # ax2.set_yticklabels( np.logspace( -14, 2, num=9 ) )
# y_tick_labels = y_ticks
# for tick in range( np.size( y_tick_labels ) ) :
#     if not tick % 2 == 0 :
# #         print(tick)
#         y_tick_labels[ tick ] = 'nan'
# ax1.set_yticklabels( y_tick_labels )
ax1.set_xlabel( inv_Tk_axis_label, labelpad = 0 )
ax1.set_ylabel( y_axis_label, labelpad = 0 )
ax1.minorticks_on()

ax1.legend( legend_handles, legend_labels, loc = 'upper right',
    numpoints = 1, frameon = False, fontsize = 10, labelspacing = .01,
    handletextpad = .0, borderpad = 0 )
ax1.text( gb_text_label_x, gb_text_label_y, 
    'G.B.', ha = gb_text_horiz_align, va = gb_text_vert_align )
ax1.text( grain_text_label_x, grain_text_label_y, 
    'Grain', ha = grain_text_horiz_align, va = grain_text_vert_align )

# this didn't quite work, and i'm not sure why...
# # query 1st axis for chart limits to calculate 2nd axis tick locations
# ax1_xlims = ax1.xaxis.get_majorticklocs()
# ax1_Tk_xmin = ax1_xlims[ 0 ]
# ax1_Tk_xmax = ax1_xlims[ 1 ]

ax2_tick_Tk_locations = 1000 / ( ax2_Tc_ticks + 273 ) #calculate 2nd axis tick locations
ax2_tick_Tc_locations = ( ax2_tick_Tk_locations - xmin ) / ( xmax - xmin )
ax2.set_xticks( ax2_tick_Tc_locations ) #add ticks and labels to 2nd axis
ax2.set_xticklabels( ax2_Tc_ticklabels )
ax2.set_xlabel( Tc_axis_label )

pl.tight_layout()
pl.show()
# pl.savefig( output_file_name + '.png', format = 'png', dpi = 500 )
dots = 1200
pl.savefig( output_file_dir + output_file_name + '-' + str( dots ) + 'dpi.png', format = 'png', dpi = dots )