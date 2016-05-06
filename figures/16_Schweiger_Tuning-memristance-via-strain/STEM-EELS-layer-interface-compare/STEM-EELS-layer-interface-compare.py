''' ########################### OVERVIEW ########################### '''
'''
 Created 2016-05-02 by Will Bowman. For plotting multiple EELS edges to compare
 different spectra.
 
 This script will save a figure with the script's file name to a subfolder
 whose name is the current date yyyymmdd
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
# path to data
data_dir = 'C:/Users/Besitzer/Dropbox/WillB/ETH/writing/16_Schweiger S etal_' +\
    'Tuning Memristance through Strain in Resistive Switching Devices/data/' +\
    '160429_GDCERO-6_HD-STEM-EELS/'

d_Ce_lay = data_dir + 'Ce-M45-layer_160429_GDCERO-6_EELS_03_2mm-10s-700meV.txt'
d_Ce_int = data_dir + 'Ce-M45-interface_160429_GDCERO-6_EELS_06_2mm-10s-700meV.txt'
d_Gd_lay = data_dir + 'Gd-M45-layer_160429_GDCERO-6_EELS_03_2mm-10s-700meV.txt'
d_Gd_int = data_dir + 'Gd-M45-interface_160429_GDCERO-6_EELS_06_2mm-10s-700meV.txt'
d_GCO20_ref = data_dir + 'GCO20-ref-SSI-fig-4a.txt'

# path to output directory
output_dir = data_dir
output_file = 'STEM-EELS-layer-interface-compare'
subfolder_save = True

fig_size = ( 5, 3.5 ) # ( width, hight ) in inches
subplot_white_space = 0.05 # see pl.subplots_adjust()
# font size, resolution (DPI), file type
fsize, dots, file_type = 10, [300,1200], 'png'
# wf.colors('col_name')
cols = [ wf.colors('eth_blue'), 'black', 'grey', 'goldenrod' ]
marks, msize = [ 's', 'o', '^', 'x' ], 6
lines = [ '-', '' ]
leg_ents = [ 'Layer', 'Interface', 'Reference' ]
leg_loc = 'upper right'
x_lab, y_lab = 'Energy loss (eV)', 'Counts (Arbitrary units)'
x_lims, y_lims = [ [860,960], [1155,1240] ], [ [-1000,1.2e4], [-1500,3000] ]
x_maj_tick_loc = ['', 20]
x_maj_tick_lab = [
    [ '', '880', '900', '920', '940' ],
    [ '', '', '1180', '', '1220' ]
    ]
file_anno = [''] # create multiple images each with an additional curve
scale_x, scale_y = [], [7, 4, 0.6]
shift_x, shift_y = [], [5e3, 1e3, -1700]

# generate data objects from .txt
Ce_lay = np.genfromtxt( d_Ce_lay, skiprows = 1, delimiter = '\t' )
Ce_int = np.genfromtxt( d_Ce_int, skiprows = 1, delimiter = '\t' )
Gd_lay = np.genfromtxt( d_Gd_lay, skiprows = 1, delimiter = '\t' )
Gd_int = np.genfromtxt( d_Gd_int, skiprows = 1, delimiter = '\t' )
GCO20_ref = np.genfromtxt( d_GCO20_ref, skiprows = 1, delimiter = '\t' )

# store columns as variables
Ce_lay_x, Ce_lay_y = Ce_lay.T
Ce_int_x, Ce_int_y = Ce_int.T
Gd_lay_x, Gd_lay_y = Gd_lay.T
Gd_int_x, Gd_int_y = Gd_int.T
GCO20_ref_x, GCO20_ref_y = GCO20_ref.T

# scale and shift data for plotting
Ce_lay_y_pl = Ce_lay_y / scale_y[0] +shift_y[0]
Gd_lay_y_pl = Gd_lay_y / scale_y[1] +shift_y[1]
GCO20_ref_y_pl = GCO20_ref_y * scale_y[2] +shift_y[2]

''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize
    
def save_fig(output_file_name):
    for dot in dots:
        if subfolder_save:
            output_dir = data_dir + wf.date_str() + '/'
            if not os.path.isdir( output_dir ):
                os.mkdir( output_dir )
        output_name = wf.save_name( output_dir, output_file_name, dot, file_type )
        pl.savefig( output_name, format = file_type, dpi = dot, transparent = True )
    

''' ########################### MAIN SCRIPT ########################### '''

for h in range( 1, len( file_anno ) + 1 ):
  
    pl.close( 'all' )
    pl.figure( figsize = fig_size ) # ( width, height )

    # ls_off, ls_on = '-', '' 
    # fill_10, fill_2 = 'full', 'none'
    # dash = ( 4, 1 )
    # Ca_major, O_major, Ce_major = 20, 40, 20

    # Ca_min_x, Ca_max_x = 335, 375
    # O_min_x, O_max_x = 525, 560
    # Ce_min_x, Ce_max_x = 870, 925

    # y_min_multiple, y_max_multiple = 0.1, 1.5

    # Ca_max_y = np.nanmax( counts_Ca_on ) * y_max_multiple
    # O_max_y = np.nanmax( counts_O_off ) * y_max_multiple
    # Ce_max_y = np.nanmax( counts_Ce_off ) * y_max_multiple

    # Ca_min_y = np.nanmax( counts_Ca_on ) * -y_min_multiple
    # O_min_y = np.nanmax( counts_O_off ) * -y_min_multiple
    # Ce_min_y = np.nanmax( counts_Ce_off ) * -y_min_multiple

    # pl.subplot( 1, 2, 1 ) # subplot( height, width, subplot_number )
    # gridspec( (rows,cols), (plot_location), colspan )
    pl.subplot2grid( (1,3), (0,0), colspan=2 )
    pl.plot( Ce_lay_x, Ce_lay_y_pl, c=cols[0], ls=lines[0] )
    pl.plot( Ce_int_x, Ce_int_y, c=cols[1], ls=lines[0] )
    pl.plot( GCO20_ref_x, GCO20_ref_y_pl-1e4, c=cols[2], ls=lines[0] )
    # pl.plot( ev_Ca, counts_Ca_off, color = col_off, dashes = dash )

    ax = pl.gca()
    ax.set_ylabel( y_lab, labelpad=0 )
    ax.set_xlabel( x_lab, labelpad=0, horizontalalignment='left' )
    ax.set_xlim( x_lims[0][0], x_lims[0][1] )
    ax.set_ylim( y_lims[0][0], y_lims[0][1] )
    ax.minorticks_on()
    ax.set_xticklabels( x_maj_tick_lab[0] )
    ax.set_yticklabels([])
    # ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( Ca_major ) )

    # LEGEND ON FIRST SUBPLOT
    ax.legend( leg_ents, loc=leg_loc, handlelength=1.5, frameon=False, 
        fontsize=fsize, labelspacing=.5, handletextpad=0.3, borderpad=0.1 )
    pl.setp(ax.get_legend().get_lines(), linewidth=2) # the legend linewidth

    # pl.subplot( 1, 2, 2 )
    pl.subplot2grid( (1,3), (0,2) )
    pl.plot( Gd_lay_x, Gd_lay_y_pl, c=cols[0], ls=lines[0] )
    pl.plot( Gd_int_x, Gd_int_y, c=cols[1], ls=lines[0] )
    pl.plot( GCO20_ref_x, GCO20_ref_y_pl, c=cols[2], ls=lines[0] )
    # pl.plot( ev_O, counts_O_on, color = col_on, dashes = dash )
    # pl.plot( ev_O, counts_O_off, color = col_off, dashes = dash )

    ax = pl.gca()
    ax.set_xlim( x_lims[1][0], x_lims[1][1] )
    ax.set_ylim( y_lims[1][0], y_lims[1][1] )

    ax.minorticks_on()
    ax.set_yticklabels([])
    ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( x_maj_tick_loc[1] ) )
    ax.set_xticklabels( x_maj_tick_lab[1] )
        
    # pl.subplot( 1, 3, 3 )
    # pl.plot( ev_Ce, counts_Ce_on, color = col_on, dashes = dash )
    # pl.plot( ev_Ce, counts_Ce_off, color = col_off, dashes = dash )
    # pl.plot( dist_2 + shift_both, Ca_2, color = col_2, marker = Ca_mark, linestyle = 'none',
    #     fillstyle = fill_2, mew = mark_width, mec = col_2, markersize = marker_size )


    # ax.set_xticklabels( [] )
    # ax.set_yticks( np.linspace( 0, 4e-2, 9 ) )
    # ax.yaxis.set_major_locator( mpl.ticker.MultipleLocator( 2e-2 ) )
    # ax = pl.gca()
    # ax.set_xlim( Ce_min_x, Ce_max_x )
    # ax.set_ylim( Ce_min_y, Ce_max_y )
    # ax.minorticks_on()
    # ax.set_xticklabels( [ '', '880','', '', '910' ] )
    # ax.set_yticklabels( [] )
    # ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( Ce_major ) )
    # ax.set_yticks( [ 0.1, 0.2, 0.3, 0.4 ] )

    pl.subplots_adjust( wspace=subplot_white_space, bottom=0.15 )

    # plot 5CCO
    # pl.subplot( 2, 1, 2 )
    # pl.plot( deg_5, num_5, color = mark_col, marker = mark, linestyle = 'none',
    #     fillstyle = 'full', mew = 1, mec = mark_col, markersize = marker_size )
    # pl.plot( deg_5, ran_len_5, color = rand_col, linestyle = '-' )
    # 
    # ax = pl.gca()
    # ax.set_yticks( np.linspace( 0, 4e-2, 9 ) )
    # ax.yaxis.set_major_locator( mpl.ticker.MultipleLocator( 2e-2 ) )
    # ax.minorticks_on()
    # ax.set_xlabel( r'Misorientation angle ($^\circ$)', labelpad = 0 )
    # ax.set_ylabel( 'Number fraction', labelpad = 0 )

     

    # ax1.set_xticks( np.linspace( 100, 500, 5 ) )
    # ax1.set_xticklabels( np.linspace( 100, 500, 5 ) )
    # ax1.set_yticks( [ 0.1, 0.2, 0.3, 0.4 ] )
    # ax.minorticks_on()

    # pl.tight_layout()
    pl.show()
    # pl.savefig( output_file_dir + output_file_name + '-' + str( dots ) + 'dpi.png', format = 'png', dpi = dots, bbox_inches = 'tight', transparent = True )