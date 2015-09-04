''' ########################### OVERVIEW ########################### '''
'''
 Created 2015-09-03 by Will Bowman. This creates a figure with GPDC boundary 
 composition and character data 
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
# path to data file (make gui to pick files?)
data_dir = 'C:/Users/willb/Dropbox/WillB/Crozier_Lab/Writing/2015_gb misorientation OIM EELS/figures/gpdc-gb-character/'

# misorientation angle distribution (MAD)
d_mad = data_dir + 'misorientation-distribution/GPDCfib_gbLengthFraction.txt'
d_mad_skiprows = 0
# coincidence site lattice (CSL)
d_csl = data_dir + 'misorientation-distribution/GPDCfib_cslLengthFraction.txt'
d_csl_skiprows = 0
# mackenzian distribution
d_mack = data_dir + 'misorientation-distribution/mackenzie_200_bins-tdl.txt'
d_mack_skiprows = 7


# output file info
output_dir = data_dir
output_file = 'gpdc-gb-character'

# font size, resolution (DPI), file type
fsize, dots, file_type = 10, [300], 'png'

# subplot 0 (sp0): concentration v angle plot
sp0_x_lab, sp0_y_lab = 'Misorientation angle (Deg.)', 'Concentration (Mole frac.)'
sp0_entries = ( '$Ce_{G.B.}$', '$Ce_{Gr.}$', '$Gd_{G.B.}$', '$Gd_{Gr.}$', 
    '$Pr_{G.B.}$', '$Pr_{Gr.}$' ) # legend
sp0_c = [ 'maroon', 'grey', 'black' ] # line colors
sp0_m, m_width = [ 'o', 'D', 's' ], 1 # markers
sp0_x, sp0_y = [ 15, 65 ], [ 0, 1 ] # axis limits
sp0_maj_loc = [ 10, 0.5 ] # [x,y] major tick locators

# subplot1 (sp1): length fraction v concentration
sp1_x_lab, sp1_y_lab = 'Concentration (Mole frac.)', 'Length fraction'
sp1_entries = ( 'Pr', 'Gd', 'Ce' )
sp1_c = [ 'black', wf.hex_gold(), 'maroon' ] # line colors
sp1_x_lim, sp1_y_lim = [ -1, 17 ], [ 0, 0.7 ] # axis limits
sp1_maj_loc = [ 4, 0.2 ] # [x,y] major tick locators
sp1_x_tick_labs = [ None, '<5', '21-25', '41-45', '61-65', '81-85' ] # tick labels
conc_y = [ 0, 0.75 ]
bar_shift = -0.4
pr_c, gd_c, ce_c = 'maroon', 'grey', 'black'


''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize
    # wf.nanoletters_mpl()
    mpl.rc( 'font', family='sans-serif', serif='Helvetica', weight='normal' )
    mpl.rc( 'lines', ls='', mew=0.01, markersize=4 )
    mpl.rc( 'legend', numpoints=1, handletextpad=-0.5, borderpad=-0.5 )

def sp0_style( ax ):
    pl.xlim( sp0_x )
    pl.ylim( sp0_y )
    pl.minorticks_on()
    ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( sp0_maj_loc[0] ) )
    ax.yaxis.set_major_locator( mpl.ticker.MultipleLocator( sp0_maj_loc[1] ) )
    # ax.yaxis.set_ticklabels([]) # y tick labels off

def sp1_style( ax ):
    pl.xlim( sp1_x_lim )
    pl.ylim( sp1_y_lim )
    pl.minorticks_on()
    ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( sp1_maj_loc[0] ) )
    ax.yaxis.set_major_locator( mpl.ticker.MultipleLocator( sp1_maj_loc[1] ) )
    ax.xaxis.set_ticklabels( sp1_x_tick_labs ) # x tick labels
    mpl.rc( 'legend', numpoints=1, handletextpad=0.5, borderpad=1 )


''' ########################### MAIN SCRIPT ########################### '''
# read data, skip header rows
angle, ce_gr, ce_gb, ce_av, pr_gr, pr_gb, _pr_av, gd_gr, gd_gb, gd_av = np.loadtxt( d_conc_ang, skiprows = 1 ).T

# because there are strings and floats you have to do some work
conc = np.genfromtxt( d_length_conc, skiprows = 1, dtype=None )
global conc_bin, pr_len, gd_len, ce_len
conc_bin, pr_len, gd_len, ce_len = [], np.array([]), np.array([]), np.array([])
for row in conc:
    conc_bin.append( row[0].decode( 'utf-8' ) )
    pr_len = np.append( pr_len, row[1] )
    gd_len = np.append( gd_len, row[2] )
    ce_len = np.append( ce_len, row[3] )

pl.close( 'all' ) # close all open figures
pl.figure( figsize = ( 3.33, 5.5 ) ) # create a figure of size ( width", height" )
ax = pl.gca() # store current axis

mpl_customizations() # apply customizations to matplotlib

pl.subplot( 2, 1, 1 ) # suplot 0 ( sub_y, sub_x, sub_i )
ax0 = pl.gca()
pl.plot( angle, ce_gb, c=ce_c, marker=sp0_m[0] )
pl.plot( angle, ce_gr, c=ce_c, marker=sp0_m[0], fillstyle='none', mew=m_width )
pl.plot( angle, gd_gb, c=gd_c, marker=sp0_m[1] )
pl.plot( angle, gd_gr, c=gd_c, marker=sp0_m[1], fillstyle='none', mew=m_width )
pl.plot( angle, pr_gb, c=pr_c, marker=sp0_m[2] )
pl.plot( angle, pr_gr, c=pr_c, marker=sp0_m[2], fillstyle='none', mew=m_width )
sp0_style( ax0 )
pl.ylabel( sp0_y_lab, labelpad=0.5 )
pl.xlabel( sp0_x_lab, labelpad=0.5 )
pl.legend( sp0_entries, loc=(0.03,0.25) ) # locate legend x,y from bottom left

pl.subplot( 2, 1, 2 ) # suplot 1 ( sub_y, sub_x, sub_i )
ax1 = pl.gca()
sp1_x = np.arange( len( pr_len ) )
pl.bar( sp1_x + bar_shift, pr_len, color=pr_c, alpha=0.5 )
pl.bar( sp1_x + bar_shift, gd_len, color=gd_c, alpha=0.5 )
pl.bar( sp1_x + bar_shift, ce_len, color=ce_c, alpha=0.5 )
sp1_style( ax1 )
pl.ylabel( sp1_y_lab, labelpad=0.5 )
pl.xlabel( sp1_x_lab, labelpad=0.5 )
pl.legend( sp1_entries )

# applies to all subplots, h_pad defined vertical spacing
pl.tight_layout( pad=0.3, h_pad=0.6 )

for dot in dots:
    output_name = wf.save_name( data_dir, output_file, dot, file_type )
    pl.savefig( output_name, format = file_type, dpi = dot, transparent = True )
    
''' ########################### REFERENCES ########################### '''