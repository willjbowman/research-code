''' ########################### OVERVIEW ########################### '''
'''
 Created 2016-02-21 by Will Bowman. This script is for plotting conductivity and
 composition data for a figure
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
data_dir = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/15_WJB_IS EBSD EELS Ca-Ceria gbs/figures/gb-concentration-conductivity/'
data = data_dir + 'CCO-gb-conductivity-concentration.txt'

# path to output directory
output_dir = data_dir
subfolder_save = True
output_file = 'CCO-gb-conductivity-concentration'

# font size, resolution (DPI), file type
fsize, dots, file_type = 10, [300,1200], 'png'
cols = [ 'maroon', 'grey' ]
marks, msize, mwidth = [ 's', 'o' ], 7, 0.5
leg_ents = [ 'GB Conductivity (300 $^\circ$C)', 'GB Concentration (EELS)' ]
x_lab = 'x in $Ca_xCe_{1-x}O_{2-\delta}$'
y1_lab, y2_lab = '$\sigma_{GB}$ (S/cm)', '$[Ca]_{GB}$'
file_anno = [ '-0of1', '-1of1' ]
x_lims, y1_lims, y2_lims = [.01, .11], [1e-11, 1e-5], [.1, .6]


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

# READ AND STORE DATA IN VARIABLES
d = np.loadtxt( data, skiprows = 1 )
x, x_gb, x_gb_err, S_gb, S_gb_err = d.T


'''GENERATE FIGURES'''

for h in range( 1, len( file_anno ) + 1 ):
    
    pl.close( 'all' ) # close all open figures
    pl.figure( figsize = ( 4.4, 3 ) ) # create a figure ( w, h )
    ax1 = pl.gca() # store current axis
    mpl_customizations() # apply customizations to matplotlib
    # wf.slide_art_styles() # figure styling
    fontsize = mpl.rcParams[ 'font.size' ]
        
    ax1.errorbar( x, S_gb, yerr = S_gb_err, color = cols[0], marker = marks[0],
        markersize = msize, linestyle = '--' )
    ax1.set_yscale( 'log' ) # apply axis styling
    ax1.set_xlim( x_lims )
    ax1.set_ylim( y1_lims )
    ax1.set_xlabel( x_lab )
    ax1.set_ylabel( y1_lab )
    ax1_leg_hand = mpl.lines.Line2D( [], [], c=cols[0], marker=marks[0], ms=msize, ls='' )

    if h == 1:
    
        ax1.legend( [ax1_leg_hand], leg_ents, loc = 'upper right',
            numpoints =  1, frameon = False, fontsize = 10, labelspacing = .01,
            handletextpad = .01 )
                
        pl.tight_layout() # can run once to apply to all subplots, i think
        
        save_fig( output_file + file_anno[h-1] )
        
    if h == 2:

        ax2 = ax1.twinx() #create a second x-axis which shares ax1's y-axis
        ax2.errorbar( x, x_gb, yerr = x_gb_err, color = cols[1], marker = marks[1],
            markersize = msize, capsize=20 )
        ax2.set_ylabel( y2_lab )
        ax2.set_xlim( x_lims )
        ax2.set_ylim( y2_lims )
        ax2.minorticks_on()
        ax2_leg_hand = mpl.lines.Line2D( [], [], c=cols[1], marker=marks[1], ms=msize, ls='' )
        
        legend_handles =  [ ax1_leg_hand, ax2_leg_hand ]
        
        ax2.legend( legend_handles, leg_ents, loc = 'upper right',
            numpoints = 1, frameon = False, fontsize = 10, labelspacing = .01,
            handletextpad = .01 )
                
        pl.tight_layout() # can run once to apply to all subplots, i think
        save_fig( output_file + file_anno[h-1] )
                


''' ########################### REFERENCES ########################### '''
'''
1. 
'''