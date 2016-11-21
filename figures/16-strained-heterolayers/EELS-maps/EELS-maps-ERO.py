''' ########################### OVERVIEW ########################### '''
'''
 Created 2016-11-19 by Will Bowman. This script plots EELS linescan signals.
 Input files are .txt generated from the DM plugin 'ExportAsTabbedText.s'.
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
    '16_WJB_Heterolayer strain mapping/'
fig_name = 'EELS-maps-ERO'
fig_dir = paper_dir + 'figures/' + fig_name + '/'
data_dir = paper_dir + 'data/' + fig_name + '/'

# d_in_0, d_in_0_ski = data_dir + 'gb concentrations from EELS profiles.txt', 1
# d_in_1, d_in_1_ski = data_dir + 'CCO-gb-conductivity-300C.txt', 1

# naming sequence of figs with successive curves on same axis
# file_anno = [ '-0of0' ] # for single fig with all curves
fig_size = ( 9, 9 ) # ( width, hight ) in inches

# path to output directory
output_dir = data_dir # save output figs with the data
output_file_name = fig_name
subfolder = True
save = True
# save = False

# font size, resolution (DPI), file type
leg_ents = [
    [ 'O K', 'F', 'Ce M5', 'Ce M4', 'Ce M45', 'Gd M45', 'Er M5' ], 
    [ 'I Gd/Ce', 'I Ce_M4/M5' ]
    ]
leg_loc = 'best'
x_labs = [ 'distance (nm)', 'Distance (nm)' ]
y_labs = [ 'Counts (Arb. units)', 'Counts (Arb. units)' ]
x_lims = [ [.01, .11] ]
y_lims = [ [.0, .7], [ -.5, 2.5 ] ]

fsize, dots, file_types = 10, [300], ['png']
cols = wf.cols()
marks, msize, mwidth = wf.marks(), 5, 0.5

anno = ''
percent_er = 0.19 # propagated error from k-factor (determined in grain)

''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize
        
''' ########################### MAIN SCRIPT ########################### '''

# READ AND STORE DATA IN VARIABLES

pl.close( 'all' ) # close all open figures

'''GENERATE FIGURES'''
for i, fname in enumerate( os.listdir( data_dir ) ):

    d = np.genfromtxt( data_dir+fname, delimiter='\t' )
    nm, iOK, iF, iCeM5, iCeM4, iCeM, iGdM, iErM5 = d
    
    pl.figure( figsize=fig_size ) # create a figure ( w, h )
    mpl_customizations() # apply customizations to matplotlib
    
    # PLOT BKGD-SUBTRACTED SIGNAL INTENSITIES
    # pl.subplot2grid( (1,2), (0,0) ) # ((rows,cols),(subplot_index))
    pl.subplot2grid( (2,2), (0,0), rowspan=2 ) # ((rows,cols),(subplot_index))
    ax0 = pl.gca() # store current axis

    ax0.plot( d[0], d[1::].T ) # plot signals vs. distance

    # label_lim( ax0, [0] )
    # ax0.set_xlim( x_lims[0] )
    # ax0.set_ylim( y_lims[0] )
    ax0.set_xlabel( x_labs[0] )
    ax0.set_ylabel( y_labs[0] )
    ax0.minorticks_on()

    ax0.legend( leg_ents[0], loc=leg_loc,
        numpoints=1, frameon=False, fontsize=fsize, labelspacing=.1,
        handletextpad=.3 )
    
    # PLOT BKGD-SUBTRACTED SIGNAL INTENSITIES
    # pl.subplot2grid( (1,2), (0,0) ) # ((rows,cols),(subplot_index))
    pl.subplot2grid( (2,2), (0,1) ) # ((rows,cols),(subplot_index))
    ax0 = pl.gca() # store current axis

    ax0.plot( d[0], d[1::].T ) # plot signals vs. distance

    # label_lim( ax0, [0] )
    # ax0.set_xlim( x_lims[0] )
    # ax0.set_ylim( y_lims[0] )
    ax0.set_xlabel( x_labs[0] )
    ax0.set_ylabel( y_labs[0] )
    ax0.minorticks_on()

    ax0.legend( leg_ents[0], loc=leg_loc,
        numpoints=1, frameon=False, fontsize=fsize, labelspacing=.1,
        handletextpad=.3 )

    # pl.subplot2grid( (1,2), (0,1) ) # ((rows,cols),(subplot_index))
    pl.subplot2grid( (2,2), (1,1) ) # ((rows,cols),(subplot_index))
    ax1 = pl.gca() # store current axis

    ax1.plot( d[0], iGdM/iCeM, marker=marks[0] )
    ax1.plot( d[0], iCeM4/iCeM5, marker=marks[0] )
    ax1.plot( d[0], iErM5/iCeM, marker=marks[0] )

    # label_lim( ax1, [1] )
    # ax1.set_xlim( x_lims[1] )
    ax1.set_ylim( y_lims[1] )
    ax1.set_xlabel( x_labs[1] )
    ax1.set_ylabel( y_labs[1] )
    ax1.minorticks_on()

    ax1.legend( leg_ents[1], loc=leg_loc,
        numpoints=1, frameon=False, fontsize=fsize, labelspacing=.1,
        handletextpad=.3 )
            
    pl.tight_layout() # can run once to apply to all subplots, i think
    if save:
        wf.save_fig( output_dir, file_types, dots, fname, anno,
            subfolder_save=subfolder )


''' ########################### REFERENCES ########################### '''
'''
1. 
'''