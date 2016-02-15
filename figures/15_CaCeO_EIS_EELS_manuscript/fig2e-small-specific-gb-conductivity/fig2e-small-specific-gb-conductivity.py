# import the capacitances for each sample to determine the electrical gb width
# equation is found in Avila-Paredes, Kim 'dopant concentration dependence of
# grain boundary conductivity in GDC'

input_file_dir = 'C:/Users/willb/Dropbox/Crozier Group Users - Will Bowman/Crozier_Lab/Writing/2015_IS EBSD EELS of CaCeria grain boundaries/figures/electrical boundary width specific gb/'

input_file_root_name_1 = '140325_sdCaDC2_100-700c' # 2 mol% Ca
input_file_root_name_2 = '140327_sdCaDC5_100-700c' # 5 mol% Ca
input_file_root_name_3 = '140329_sdCaDC10_100-700c(1)' # 10 mol% Ca
capacitance_file_name_end = '_CalculatedCap_GbEWidth_Err.txt'
conductivity_file_name_end = '_CalculatedConductivityErr.txt'

output_file_dir = input_file_dir
output_file_name = 'fig2e-small-specific-gb-conductivity'
dots = 1200

import numpy as np
import pylab as pl
import matplotlib as mpl

## store data
# import data
C_2Ca = np.loadtxt( input_file_dir + input_file_root_name_1 + capacitance_file_name_end )
C_5Ca = np.loadtxt( input_file_dir + input_file_root_name_2 + capacitance_file_name_end )
C_10Ca = np.loadtxt( input_file_dir + input_file_root_name_3 + capacitance_file_name_end )

S_2Ca = np.loadtxt( input_file_dir + input_file_root_name_1 + conductivity_file_name_end )
S_5Ca = np.loadtxt( input_file_dir + input_file_root_name_2 + conductivity_file_name_end )
S_10Ca = np.loadtxt( input_file_dir + input_file_root_name_3 + conductivity_file_name_end )

Tc_calibrated_2Ca, Cg_2Ca, Cg_err_2Ca, Cgb_2Ca, Cgb_err_2Ca, w_gb_2Ca, w_gb_err_2Ca = C_2Ca.T
Tc_calibrated_5Ca, Cg_5Ca, Cg_err_5Ca, Cgb_5Ca, Cgb_err_5Ca, w_gb_5Ca, w_gb_err_5Ca = C_5Ca.T
Tc_calibrated_10Ca, Cg_10Ca, Cg_err_10Ca, Cgb_10Ca, Cgb_err_10Ca, w_gb_10Ca, w_gb_err_10Ca = C_10Ca.T

w_gb_ave_2Ca = np.ma.masked_invalid( w_gb_2Ca ).mean( 0 ) # calculate mean electrical gb width
w_gb_ave_5Ca = np.ma.masked_invalid( w_gb_5Ca ).mean( 0 )
w_gb_ave_10Ca = np.ma.masked_invalid( w_gb_10Ca ).mean( 0 )

Tc_calibrated_2Ca_S, Sg_2Ca, Sg_err_2Ca, blank, blank, Sgb_2Ca, Sgb_err_2Ca = S_2Ca.T
Tc_calibrated_5Ca_S, Sg_5Ca, Sg_err_5Ca, blank, blank, Sgb_5Ca, Sgb_err_5Ca = S_5Ca.T
Tc_calibrated_10Ca_S, Sg_10Ca, Sg_err_10Ca, blank, blank, Sgb_10Ca, Sgb_err_10Ca = S_10Ca.T

# grain sizes (nm)
dg_ave_2Ca, dg_ave_2Ca_err = 7600, 0
dg_ave_5Ca, dg_ave_5Ca_err = 2300, 0
dg_ave_10Ca, dg_ave_10Ca_err = 1400, 0

## calculate electrical gb widths
# w_gb = C_g / C_gb * d_grain
# w_gb_2Ca = Cg_2Ca / Cgb_2Ca * dg_ave_2Ca
# w_gb_err_2Ca = abs( w_gb_2Ca ) * ( ( Cg_err_2Ca / Cg_2Ca ) ** 2 + 
#     ( Cgb_err_2Ca / Cgb_2Ca ) ** 2 + ( dg_ave_2Ca_err / dg_ave_2Ca ) ** 2 ) ** 0.5
#     
# w_gb_5Ca = Cg_5Ca / Cgb_5Ca * dg_ave_5Ca
# w_gb_err_5Ca = abs( w_gb_5Ca ) * ( ( Cg_err_5Ca / Cg_5Ca ) ** 2 + 
#     ( Cgb_err_5Ca / Cgb_5Ca ) ** 2 + ( dg_ave_5Ca_err / dg_ave_5Ca ) ** 2 ) ** 0.5
#     
# w_gb_10Ca = Cg_10Ca / Cgb_10Ca * dg_ave_10Ca
# w_gb_err_10Ca = abs( w_gb_10Ca ) * ( ( Cg_err_10Ca / Cg_10Ca ) ** 2 + 
#     ( Cgb_err_10Ca / Cgb_10Ca ) ** 2 + ( dg_ave_10Ca_err / dg_ave_10Ca ) ** 2 ) ** 0.5
    
## plot stuff
pl.close( 'all' )
pl.figure( figsize = ( 2.3, 2.3 ) )
ax1 = pl.gca()

mpl.rcParams[ 'font.family' ] = 'sans-serif' # modify matplotlib parameters
mpl.rcParams[ 'font.weight' ] = 'normal'
mpl.rcParams[ 'font.size' ] = 10
mpl.rcParams[ 'mathtext.default' ] = 'regular'

color_2, color_5, color_10 = 'maroon', 'slategray', 'black'
markers = [ '^', 'v', '<', '>', 's', 'd', 'p', 'h', 'H', 'D', 'o', '*' ]
marker_size, legend_marker_size = 4, 6

ax1.set_xlabel( '[Ca$^{2+}$] (mol %)', labelpad = 0 )
# ax1.set_ylabel( '$\delta_{G.B.}$ (nm)' )
ax1.set_ylabel( 'log($\sigma_{G.B.}$*) (S cm$^{-1}$)', labelpad = 0 )


ax1.set_xticks( np.linspace( 2, 10, 3 ) )
# ax1.tick_params( axis = 'x', which = 'minor', bottom = 'off', top = 'off' )

data_points_2 = np.size( w_gb_2Ca )
data_points_5 = np.size( w_gb_5Ca )
data_points_10 = np.size( w_gb_10Ca )

x_2 = 2 * np.ones( data_points_2 )
x_5 = 5 * np.ones( data_points_5 )
x_10 = 10 * np.ones( data_points_10 )

legend_title = r'  T ($^\circ$C)'
legend_labels = [ ]
legend_handles = [ ] # container for legend handles (filled in loop)

# for i in range( data_points_2 ) :
#     ax1.plot( x_2[ i ] , w_gb_2Ca[ i ] * 1e9, mec = color_2, marker = markers[ i ],
#         fillstyle = 'none', mew = 1, markersize = marker_size )
#     ax1.plot( x_5[ i ], w_gb_5Ca[ i ] * 1e9, mec = color_5, marker = markers[ i ],
#         fillstyle = 'none', mew = 1, markersize = marker_size )
#     ax1.plot( x_10[ i ], w_gb_10Ca[ i ] * 1e9, mec = color_10, marker = markers[ i ],
#         fillstyle = 'none', mew = 1, markersize = marker_size )

# ax2 = ax1.twinx()
for i in range( data_points_2 ) :
    ax1.plot( x_2[ i ] , Sgb_2Ca[ i ], color = color_2, marker = markers[ i ],
        fillstyle = 'full', mew = 1, mec = color_2, markersize = marker_size )
    ax1.plot( x_5[ i ], Sgb_5Ca[ i ], color = color_5, marker = markers[ i ],
        fillstyle = 'full', mew = 1, mec = color_5, markersize = marker_size )
    ax1.plot( x_10[ i ], Sgb_10Ca[ i ], color = color_10, marker = markers[ i ],
        fillstyle = 'full', mew = 1, mec = color_10, markersize = marker_size )
    
    if not np.isnan( w_gb_2Ca[ i ] ) or not np.isnan( w_gb_5Ca[ i ] ) or not np.isnan( w_gb_10Ca[ i ] ) :
        # legend handler for ith curve
        legend_info_i = mpl.lines.Line2D( [], [], color = 'black', marker = markers[i], 
            markersize = legend_marker_size, fillstyle = 'none', linestyle = '' )
        legend_handles.append( legend_info_i ) # append ith legend handler to legend handles
        legend_labels.append( str( int( Tc_calibrated_5Ca[ i ] ) ) )

ax1.set_xlim( 1, 11 )
# ax1.set_ylim( 0, 9 )

ax1.set_ylim( 10**-16, 10**-8 )
# ax2.set_ylabel( '$\sigma_{G.B.}^*$ (S cm$^{-1}$)' )
ax1.set_yscale( 'log' ) # mirror the y-axis about x, add log scale
y_ticks = np.logspace( -16, -8, num = 3 )
ax1.set_yticks( y_ticks )
ax1.set_yticklabels( [ -16, -12, -8 ] )
ax1.minorticks_on()

# ax1.arrow( 1.65, 7.85, -0.3, 0, head_width = 0.1, head_length = 0.25, fc = 'k', ec = 'k' )
# ax1.arrow( 10.35, 4.15, 0.3, 0, head_width = 0.1, head_length = 0.25, fc = 'k', ec = 'k' )

# legend_loc =  ( 5.7 / 11, 4.2 / 7 )
legend_loc = ( 4.5 / 11, 0 )
ax1.legend( legend_handles, legend_labels, loc = legend_loc,
    numpoints = 1, frameon = False, fontsize = 10, labelspacing = .01,
    handletextpad = 0.2, title = legend_title )

pl.tight_layout()
pl.show()
pl.savefig( output_file_dir + output_file_name + '-' + str( dots ) + 'dpi.png', format = 'png', dpi = dots )
# pl.savefig( output_file_name + '.png', format = 'png', dpi = 500 )