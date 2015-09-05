''' ########################### OVERVIEW ########################### '''
'''
 Created 2015-09-05 by Will Bowman. This creates a figure with valence loss data
 from PCO nanoparticles and CeO2 fragments.
'''

''' ########################### IMPORT MODULES ########################### '''
import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import wills_functions as wf
import csv, imp, os
import math as math

##


''' ########################### USER-DEFINED ########################### '''
# this is the name of the figure working directory. the output figure will be
# saved here with a file name containing the directory name
fig_dir = 'valence-loss-eels'
# this is the full path to figure directory (for reading data and writing files)
figs_dir = 'C:/Users/willb/Dropbox/WillB/Crozier_Lab/Writing/2015_PCO10 interband states/figures/' + fig_dir + '/'

# PCO particles
d_0 = figs_dir + 'pco-valence-loss.txt'
d_0_skiprows = 1
# ceria fragments
d_1 = figs_dir + '140207_7bCeO2crush_Nion_EELS10_100kV_Ref20i_slit_1mm_5meV_25meV_5s_1frame.txt'
d_1_skiprows = 1

# font size, resolution (DPI), file type, fig_size
# create a figure of size ( width", height" )
font_size, dots, file_type, fig_size = 10, [ 300, 1200 ], 'png', ( 4.75, 2.2 )
# sub_plots = ( 2, 1, 1 ) # suplot 0 ( sub_y, sub_x, sub_i )

# subplot 0 (sp0): length fraction v misorientation angle
sp0_ax_labs = [ 'Energy-loss / eV', 'Counts / Arb. units' ]
sp0_entries = ( 'Raw data', 'Background\nsubtracted' ) # legend entries
sp0_c = [ 'grey', 'maroon' ] # line colors
sp0_m, sp0_m_width = [ None, None ], 1 # markers
sp0_ls = [ '--', '-' ] # line styles
sp0_lims = [ [ 0.1, 4.9 ], [ 0, 700 ] ] # x, y axis limits
sp0_maj_loc = [ 15, 0.1 ] # [x,y] major tick locators
sp0_leg_loc = 'upper left'

# subplot1 (sp1): length fraction v concentration
sp1_ax_labs = [ 'Energy-loss / eV', False ]
sp1_entries = ( None )
sp1_c = [ 'maroon' ] # line colors
sp1_m, sp1_m_width = [ None, None ], 1 # markers
sp1_ls = [ '-' ] # line styles
sp1_lims = [ [ 0.1, 4.9 ], [ 0, 16e3 ] ] # axis limits
sp1_maj_loc = [ 5, 0.02 ] # [x,y] major tick locators
sp1_leg_loc = 'best'


''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( font_size ) # pass the figure's fontsize
    # wf.slide_art_styles()
    mpl.rc( 'font', family='serif', serif='Times New Roman', weight='normal' )
    mpl.rc( 'lines', ls='', mew=0.01, markersize=4 )
    mpl.rc( 'legend', numpoints=1, handletextpad=0.5, borderpad=0.5 )

def sp0_style( ax ):
    wf.ax_limits( sp0_lims )
    pl.minorticks_on()
    wf.ax_labels( sp0_ax_labs )
    # wf.major_ticks( ax, sp0_maj_loc )
    pl.legend( sp0_entries, loc=sp0_leg_loc ) # locate legend x,y from bottom left
    ax.yaxis.set_ticklabels([]) # y tick labels off
    # ax.set_yticks([])

def sp1_style( ax ):
    wf.ax_limits( sp1_lims )
    pl.minorticks_on()
    wf.ax_labels( sp1_ax_labs )
    # wf.major_ticks( ax, sp1_maj_loc )
    # pl.legend( sp1_entries, loc=sp1_leg_loc ) # locate legend x,y from bottom left
    ax.yaxis.set_ticklabels([]) # y tick labels off
    # ax.set_yticks([])


''' ########################### MAIN SCRIPT ########################### '''

# read data, skip header rows
sp0_x, sp0_y0, sp0_y1 = np.loadtxt( d_0, skiprows=d_0_skiprows ).T
sp1_x, sp1_y0 = np.loadtxt( d_1, skiprows=d_1_skiprows ).T

pl.close( 'all' ) # close all open figures
pl.figure( figsize = fig_size ) # create a figure of size ( width", height" )
ax = pl.gca() # store current axis

mpl_customizations() # apply customizations to matplotlib

pl.subplot( 1, 2, 1 ) # suplot 0 ( sub_y, sub_x, sub_i )
ax0 = pl.gca()
pl.plot( sp0_x, sp0_y0, c=sp0_c[0], marker=sp0_m[0], ls=sp0_ls[0] )
pl.plot( sp0_x, sp0_y1, c=sp0_c[1], marker=sp0_m[1], ls=sp0_ls[1] )
sp0_style( ax0 )

pl.subplot( 1, 2, 2 ) # suplot 1 ( sub_y, sub_x, sub_i )
ax1 = pl.gca()
pl.plot( sp1_x, sp1_y0, c=sp1_c[0], marker=sp1_m[0], ls=sp1_ls[0] )
sp1_style( ax1 )

# applies to all subplots, h_pad defined vertical spacing
pl.tight_layout( pad=0.3, h_pad=0.6 )

# output file info
output_dir = figs_dir
output_file = fig_dir

for dot in dots:
    output_name = wf.save_name( figs_dir, output_file, dot, file_type )
    pl.savefig( output_name, format = file_type, dpi = dot, transparent = True )

''' ########################### REFERENCES ########################### '''