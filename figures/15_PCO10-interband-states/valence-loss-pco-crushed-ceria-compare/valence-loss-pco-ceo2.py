''' ########################### OVERVIEW ########################### '''
'''
 Created 2016-07-26 by Will Bowman. This script plots valence-loss data for 
 ~30 nm PCO nanoparticles and fragments of crushed sintered ceria
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
writing_dir = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/'
data_path = writing_dir +\
	'15_WJB_PCO10 interband states/data/pco-valence-loss.txt'

data_path_ceo2 = writing_dir +\
	'15_WJB_PCO10 interband states/figures/valence-loss-pco-ceo2/' +\
	'140207_7bCeO2crush_Nion_EELS10_100kV_Ref20i_slit_1mm_5meV_25meV_5s_1frame.txt'

x_min, x_max = 0, 4.9 # eV
y_min, y_max = 0, 7e2 # eV
x_label, y_label = 'Energy-loss (eV)', 'Counts (Arbitrary units)'

output_file_name = 'valence-loss-pco-ceo2'
output_dir = writing_dir +\
	'15_WJB_PCO10 interband states/figures/' + output_file_name + '/'

# font size, resolution (DPI), file type
fsize, dots, file_types = 10, [300], ['png','svg']

saving = True
# saving = False


''' ########################### FUNCTIONS ########################### '''
    
def save_fig( output_direc, output_file_name, subfolder_save=True ):
    # create subfolder with date as name
    if subfolder_save:
        output_sub_dir = output_direc + wf.date_str() + '/'
        if not os.path.isdir( output_sub_dir ):
            os.mkdir( output_sub_dir )

    for file_type in file_types:
        if file_type == 'png':
            for dot in dots:
                output_name = wf.save_name( output_sub_dir, output_file_name, dot )
                pl.savefig( output_name + '.png', format=file_type, dpi=dot, 
                    transparent=True )
        elif file_type == 'svg':
                output_name = wf.save_name( output_sub_dir, output_file_name, False )
                pl.savefig( output_name + '.svg', format=file_type )

''' ########################### MAIN SCRIPT ########################### '''
# read data (raw and background subtracted valence loss)
data = np.loadtxt( data_path, delimiter = '\t' )
ev, raw, processed = data.T

ev_ceo2, raw_ceo2 = np.loadtxt( data_path_ceo2, skiprows=1, delimiter='\t' ).T
ev_ceo2_pl = ev_ceo2 - 0.05
ceo2_pl = raw_ceo2 / 21

pl.close( 'all' )

wf.slide_art_styles() # figure styling
fontsize = mpl.rcParams[ 'font.size' ]

pl.figure( figsize = ( 3.4, 3 ) )
ax = pl.gca()

pl.plot( ev_ceo2_pl, ceo2_pl, color='black', lw = 0.8, dashes = [ 2, 2 ] )
pl.plot( ev, raw, color = wf.colors('dark_grey'), lw = 0.8, dashes = [ 2, 2 ] )
pl.plot( ev, processed, color = 'maroon', lw = 0.5, ls = '-' )
pl.legend( ( r'CeO$_{2}$', 'PCO', 'PCO Processed' ), loc = 'upper left', fontsize = fontsize, frameon = False )
pl.xlim( x_min, x_max )
pl.ylim( y_min, y_max )
pl.xlabel( x_label )
pl.ylabel( y_label )
wf.centered_annotation( 0.5, 0.5 * y_max, 'ZLP', 'black', fontsize = fontsize )
wf.centered_annotation( 2.6, 0.19 * y_max, 'Plateau', 'black', fontsize = fontsize )
pl.minorticks_on()
ax.set_yticks([])
pl.tight_layout()

if saving:
	save_fig( output_dir, output_file_name )
	# pl.savefig( output_file_path + output_file_name + '-1200dpi.png', format = 'png', dpi = 1200 )
	# pl.savefig( output_file_path + output_file_name + '.pdf', format = 'pdf', dpi = 1000 )
    
''' ########################### REFERENCES ########################### '''