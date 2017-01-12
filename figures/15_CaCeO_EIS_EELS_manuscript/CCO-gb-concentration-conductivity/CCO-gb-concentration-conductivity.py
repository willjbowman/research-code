''' ########################### OVERVIEW ########################### '''
'''
 Created 2016-02-21 by Will Bowman. This script is for plotting conductivity and
 composition data for a figure
 Updated 160925 with subfigure showing each measurement w/ errorbar
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
paper_dir ='C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/'+\
    '15_WJB_IS EBSD EELS Ca-Ceria gbs/'
fig_name = 'CCO-gb-concentration-conductivity'
fig_dir = paper_dir + 'figures/' + fig_name + '/'
data_dir = paper_dir + 'data/' + fig_name + '/'

d_in_0, d_in_0_ski = data_dir + 'gb concentrations from EELS profiles.txt', 1
d_in_1, d_in_1_ski = data_dir + 'CCO-gb-conductivity-300C.txt', 1

# naming sequence of figs with successive curves on same axis
file_anno = [ '-0of0' ] # for single fig with all curves
fig_size = ( 6, 3 ) # ( width, hight ) in inches

# path to output directory
output_dir = fig_dir
output_file_name = fig_name
subfolder = True
save = True
# save = False

# font size, resolution (DPI), file type
leg_ents = [ ['10 CCO', '5 CCO', '2 CCO'], 
    [ r'$\sigma_{GB}$ @ 300 $^{\circ}\!$C',
        r'Mean $[Ca^{2+}\!]^{\ GB}$' '\nvia EELS']
    ]
leg_loc = 'lower right'
x_labs = [ r'x in $Ca_{x}Ce_{1-x}O_{2-\delta}$ (Mole frac.)' ]
y_labs = [ r'$[Ca^{2+}\!]^{\ GB}$',
    [ r'$\sigma_{GB}$ (S/cm)', r'$[Ca^{2+}\!]^{\ GB}$' ] ]
x_lims = [[.01, .11]]
y_lims = [ [.0, .7], [ [1e-11, 1e-5], [.1, .6] ] ]

fsize, dots, file_types = 10, [300], ['png','svg']
cols = wf.cols()
marks, msize, mwidth = wf.marks(), 5, 0.5

percent_er = 0.19 # propagated error from k-factor (determined in grain)


''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize
        
''' ########################### MAIN SCRIPT ########################### '''

# READ AND STORE DATA IN VARIABLES
d0 = np.genfromtxt( d_in_0, skiprows=d_in_0_ski )
d1 = np.genfromtxt( d_in_1, skiprows=d_in_1_ski )

gb_id_10, scan_10, Ca_10, Ce_10, gb_id_5, scan_5, Ca_5, Ce_5, gb_id_2, scan_2, Ca_2, Ce_2 = d0.T
x_10 = [ .1 for x in gb_id_10 ] # arrays with nominal [Ca]
x_5 = [ .05 for x in gb_id_5 ]
x_2 = [ .02 for x in gb_id_2 ]

x, x_gb, x_gb_stdev, x_gb_er, S_gb, S_gb_er = d1.T


'''GENERATE FIGURES'''
for i, anno in enumerate( file_anno ):
    
    pl.close( 'all' ) # close all open figures
    pl.figure( figsize=fig_size ) # create a figure ( w, h )
    mpl_customizations() # apply customizations to matplotlib
    
    pl.subplot2grid( (1,2), (0,0) ) # ((rows,cols),(subplot_index))
    ax0 = pl.gca() # store current axis

    # plot the errorbars
    ax0.errorbar( x_2, Ca_2, yerr=percent_er*Ca_2, color=cols[1],
        fmt=marks[0], ms=msize-2, capthick=1 )
    ax0.errorbar( x_5, Ca_5, yerr=percent_er*Ca_5, color=cols[1],
        fmt=marks[0], ms=msize-2, capthick=1 )
    ax0.errorbar( x_10, Ca_10, yerr=percent_er*Ca_10, color=cols[1],
        fmt=marks[0], ms=msize-2, capthick=1 )

    # plot the data points on top
    ax0.plot( x_2, Ca_2, color=cols[0], marker=marks[0], ms=msize, 
        ls='' )
    ax0.plot( x_5, Ca_5, color=cols[0], marker=marks[0], ms=msize, 
        ls='' )
    ax0.plot( x_10, Ca_10, color=cols[0], marker=marks[0], ms=msize, 
        ls='' )

    # label_lim( ax0, [0] )
    ax0.set_xlim( x_lims[0] )
    ax0.set_ylim( y_lims[0] )
    ax0.set_xlabel( x_labs[0] )
    ax0.set_ylabel( y_labs[0] )
    ax0.minorticks_on()

    pl.subplot2grid( (1,2), (0,1) ) # ((rows,cols),(subplot_index))
    ax1 = pl.gca() # store current axis
        
    ax1.errorbar( x, S_gb, yerr=S_gb_er, color=cols[0], fmt=marks[0], 
        capthick=1, ms=msize, ls='--' )
    ax1.set_yscale( 'log' ) # apply axis styling
    ax1.set_xlim( x_lims[0] )
    ax1.set_ylim( y_lims[1][0] )
    ax1.set_xlabel( x_labs[0] )
    ax1.set_ylabel( y_labs[1][0] )
    ax1_leg_hand = mpl.lines.Line2D( [], [], c=cols[0], marker=marks[0],
        ms=msize, ls='' )

    # plot the mean and std dev of [Ca]_GB
    ax2 = ax1.twinx() #create a second x-axis which shares ax1's y-axis
    ax2.errorbar( x, x_gb, yerr=x_gb_er, color=cols[1], fmt=marks[1],
        capthick=1, ms=msize, ls='-' )
    ax2.set_xlim( x_lims[0] )
    ax2.set_ylim( y_lims[1][1] )
    # ax1.set_xlabel( x_labs[0] )
    ax2.set_ylabel( y_labs[1][1] )
    ax2.minorticks_on()
    ax2_leg_hand = mpl.lines.Line2D( [], [], c=cols[1], marker=marks[1],
        ms=msize, ls='' )
    
    legend_handles =  [ ax1_leg_hand, ax2_leg_hand ]
    
    ax2.legend( legend_handles, leg_ents[1], loc=leg_loc,
        numpoints=1, frameon=False, fontsize=fsize, labelspacing=.01,
        handletextpad=.01 )
            
    pl.tight_layout() # can run once to apply to all subplots, i think
    if save:
        wf.save_fig( fig_dir, file_types, dots, output_file_name, anno,
            subfolder_save=subfolder )


''' ########################### REFERENCES ########################### '''
'''
1. 
'''