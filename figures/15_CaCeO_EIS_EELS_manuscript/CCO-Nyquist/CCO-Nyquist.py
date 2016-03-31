''' ########################### OVERVIEW ########################### '''
'''
Created 2016-03-31 by Will Bowman. This script is for plotting Nyquist plots
of Ca0.1 Ce0.9 O2-d for a figure
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
data_dir = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/15_WJB_IS EBSD EELS Ca-Ceria gbs/figures/CCO-Nyquist/'

data_200 = data_dir + "140617_sd10CaDC-2_200c_32_Fitted.txt"
data_225 = data_dir + "140617_sd10CaDC-2_225c_45_Fitted.txt"
data_250 = data_dir + "140617_sd10CaDC-2_250c_59_Fitted.txt"

# path to output directory
output_dir = data_dir
subfolder_save = True
output_file = 'CCO10-Nyquist'

fig_size = ( 6, 3 ) # ( width, hight ) in inches 
# font size, resolution (DPI), file type
fsize, dots, file_type = 10, [300,1200], 'png'
cols = [ 'maroon', 'grey', 'black', wf.colors('dark_gold') ]
dash, width = [ 4, 2 ], 1.5 # [ pix_on pix_off ], linewidth
norm = 100
marks, msize, mwidth = [ 'o', '^', 's' ], 4, 0.5
# leg_ents = [ 'GB Conductivity (300 $^\circ$C)', 'GB Concentration (EELS)' ]
x0_lab, x1_lab = "Z' ($\Omega$)", ''
y0_lab, y1_lab = '-Z" ($\Omega$)', ''

# naming sequence of figs with successive curves on same axis
# file_anno = [ '-0of1', '-1of1' ]
file_anno = [] # for single fig with all curves
x_lims = [ [0,3.8e5], [0, 1.5e5], [] ]
y_lims = [ [0,3.8e5], [0, 1.5e5], [] ]
major_locators = [ 1e5, 4e4 ]
x_ticks, y1_ticks = False, False

legend_labels = ( '200 $^\circ$C', '225', '250' ) # legend info
legend_location = 'upper left'


''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize
    mpl.rcParams[ 'axes.formatter.limits' ] = -2, 2
    
def save_fig(output_file_name):
    for dot in dots:
        if subfolder_save:
            output_dir = data_dir + wf.date_str() + '/'
            if not os.path.isdir( output_dir ):
                os.mkdir( output_dir )
        output_name = wf.save_name( output_dir, output_file_name, dot, file_type )
        pl.savefig( output_name, format = file_type, dpi = dot, transparent = True )

def format_axes( subplot_number ):
    ax = pl.gca()
    ax.set_xlabel( x0_lab )
    ax.set_ylabel( y0_lab )
    ax.xaxis.major.formatter._useMathText = True
    ax.yaxis.major.formatter._useMathText = True
    majorLocator = mpl.ticker.MultipleLocator( major_locators[ subplot_number ] )
    ax.xaxis.set_major_locator( majorLocator )
    ax.yaxis.set_major_locator( majorLocator )
    pl.minorticks_on() # minor ticks on
    pl.xlim( x_lims[ subplot_number ] ) #define chart limits
    pl.ylim( y_lims[ subplot_number ] )

def plot_curves( curve_number, nyq_x, nyq_y, fit_x, fit_y ):
    pl.plot( nyq_x, nyq_y, marker=marks[ curve_number ],
        color=cols[ curve_number ], ls='', ms=msize, 
        mec=cols[ curve_number ] )
        
    pl.plot( fit_x, fit_y, color=cols[ curve_number ], label='_nolegend_' )
    
''' ########################### MAIN SCRIPT ########################### '''

# READ AND STORE DATA IN VARIABLES
# d = np.loadtxt( data, skiprows = 1 )
# Ca10_200 = np.genfromtxt( '140617_sd10CaDC-2_200c_32_Fitted.txt', skip_header = 2 )

d_200 = np.genfromtxt( data_200, skip_header = 2 )
d_225 = np.genfromtxt( data_225, skip_header = 2 )
d_250 = np.genfromtxt( data_250, skip_header = 2 )

nyq_x_200, nyq_y_200, fit_x_200, fit_y_200 = d_200.T # cols to variables
nyq_x_225, nyq_y_225, fit_x_225, fit_y_225 = d_225.T
nyq_x_250, nyq_y_250, fit_x_250, fit_y_250 = d_250.T


'''GENERATE FIGURES'''

if len( file_anno ) == 0:
    
    pl.close( 'all' ) # close all open figures
    pl.figure( figsize = fig_size ) # create a figure ( w, h )
    # ax0 = pl.gca() # store current axis
    mpl_customizations() # apply customizations to matplotlib
    # wf.slide_art_styles() # figure styling
    fontsize = mpl.rcParams[ 'font.size' ]
    
    # three curves zoomed out
    pl.subplot( 1, 2, 1 )
    plot_curves( 0, nyq_x_200, nyq_y_200, fit_x_200, fit_y_200 )
    plot_curves( 1, nyq_x_225, nyq_y_225, fit_x_225, fit_y_225 )
    plot_curves( 2, nyq_x_250, nyq_y_250, fit_x_250, fit_y_250 )
    format_axes( 0 ) #format subplot axes
    
    pl.legend( legend_labels, loc=legend_location, markerscale=1.5,
        numpoints=1, frameon=False, fontsize=10, labelspacing=.01,
        handletextpad=0, borderpad=0 ) # add legend to subplot (a)
    
    # zoomed in
    pl.subplot( 1, 2, 2 )
    plot_curves( 0, nyq_x_200, nyq_y_200, fit_x_200, fit_y_200 )
    plot_curves( 1, nyq_x_225, nyq_y_225, fit_x_225, fit_y_225 )
    plot_curves( 2, nyq_x_250, nyq_y_250, fit_x_250, fit_y_250 )
    format_axes( 1 ) #format subplot axes
    
    # ax1_leg_hand = mpl.lines.Line2D( [], [], c=cols[0], marker=marks[0], ms=msize, ls='' )    
    # ax1.legend( [ax1_leg_hand], leg_ents, loc = 'upper right',
    #     numpoints =  1, frameon = False, fontsize = 10, labelspacing = .01,
    #     handletextpad = .01 )
    #         
    pl.tight_layout() # can run once to apply to all subplots, i think
    save_fig( output_file )
    

elif len( file_anno ) > 0:
    pass
