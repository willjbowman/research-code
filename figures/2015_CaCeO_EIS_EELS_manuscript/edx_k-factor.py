''' ########################### OVERVIEW ########################### '''
'''
Created 2015-01-23 by Will Bowman
'''

''' ########################### IMPORT MODULES ########################### '''
import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import wills_functions as wf
import csv
import imp

##


''' ########################### USER-DEFINED ########################### '''

# data file paths
# these spectra are the result of summing all collected in DM [1], exporting as .msa, 
# then background stripping using NIST DTSA-II software [2]
path_std = 'C:/Dropbox/Crozier Group Users - Will Bowman/active_research/microscopy/150122_CaCe_5050STD_EtOH-mix_ARM200kV/150122_CaCe_5050STD_EtOH-mix_EDS_summed-Clayton[150122_CaCe_5050STD_EtOH-mix_EDS_summed].csv'
path_10Ca = 'C:/Dropbox/Crozier Group Users - Will Bowman/active_research/microscopy/150119_10Ca_ARM200kV/eds/150119_10Ca_EDS_summed_6c_a3_30um_60s-Clayton[150119_10Ca_EDS_summed_6c_a3_30um_60s].csv'

# normalization params
ev_per_chan = 10 # (eV/channel)
x_ray_energy_min, x_ray_energy_max = 4600, 5050 # (eV), normalize to max in this energy window

# plot parameters
x_min, x_max, y_min, y_max = 3e3, 7e3, -50, 1.5e4 # axis limits
vshift = 3e3 # vertical shift spectra to separate
dash = [ 4, 2 ] # define dashes ( [ pix_on, pix_off ] )
x_label, y_label = 'X-ray energy (eV)', 'Counts (Arbitrary units)' # axis labels
legend_std, legend_10Ca = 'Ca:Ce standard', '10 mol%' # legend text
legend_location = 'upper left' # legend locator

# modify matplotlib parameters
# wf.elsvier_art_styles() # import elsevier art styles

# mpl.rcParams[ 'axes.formatter.limits' ] = -1, 1


''' ########################### FUNCTIONS ########################### '''
# wf.read_csv_2col()
def read_csv_2col( file_path ):
    f = open( file_path ) # create a TextIOWrapper object
    d = csv.reader( f ) # create csv reader object
    x, y = [], [] # create blank lists to store datas
    for row in d: # iterate through rows of input .csv file
        if len( row ) == 2: # ignore row if it doesn't have (*only) 2 entries
#         need to convert to float!!!
            
            x.append( float( row[ 0 ] ) ) # append row entries to lists
            y.append( float( row[ 1 ] ) )
    
    return x, y # return lists containing .csv columns
    
def generate_plot( fontsize ):
    
    pl.plot( x_std, y_std_shifted, color = "maroon", dashes = dash ) # plot data
    pl.plot( x_10Ca, y_10Ca_scaled, color = "maroon" )
    
    ax = pl.gca() # store current axis in variable
    
    pl.xlim( x_min, x_max ), pl.ylim( y_min, y_max ) # apply plot limits
    
    pl.xlabel( x_label ), pl.ylabel( y_label ) # apply plot labels
    
    pl.minorticks_on() # minor ticks on
    ax.yaxis.set_ticklabels([]) # y tick labels off
    
    legend_labels = ( legend_std, legend_10Ca ) # tuple passed to pl.legend()
#     fontsize = mpl.rcParams[ 'font.size' ] # store fontsize for legend
    
    # apply legend
    pl.legend( legend_labels, loc = legend_location, 
        numpoints = 1, frameon = False, fontsize = fontsize, labelspacing = .01,
        handletextpad = 1 )

    # change font size of axis objects
    for item in ( [ ax.xaxis.label, ax.yaxis.label ] + ax.get_xticklabels() + ax.get_yticklabels() ):
        item.set_fontsize( fontsize )
    
    pl.show() # render plots
    
''' ########################### MAIN SCRIPT ########################### '''

# read .csv data files and store in variable
# x_std, y_std = read_csv_2col( path_std )
# x_10Ca, y_10Ca = read_csv_2col( path_10Ca )
x_std, y_std = wf.read_csv_2col( path_std )
x_10Ca, y_10Ca = wf.read_csv_2col( path_10Ca )

# normalize spectra to Ce-L_alpha-1 x-ray line
i_l = int( x_ray_energy_min / ev_per_chan ) # indicies of x-ray line bounds
i_r = int( x_ray_energy_max / ev_per_chan ) # converted to int for list indexing

line_std = y_std[ i_l : i_r ] # store counts in normalization energy window
line_10Ca = y_10Ca[ i_l : i_r ]

# calculate scaling factor to normalize curves
scale_std_10 = np.sum( line_std ) / np.sum( line_10Ca )

 # iterate through list multiplying each element by scale factor
y_10Ca_scaled = [ i * scale_std_10 for i in y_10Ca ]

# vertical shift spectrum
y_std_shifted = [ i + vshift for i in y_std ]


# generate plot(s)
pl.close( 'all' ) # close open figures

'''manuscript figure'''
imp.reload( mpl ) # reload matplotlib module
# wf.elsvier_art_styles() # import elsevier art styles
pl.figure( figsize = ( wf.mm2in( 90 ), wf.mm2in( 90 ) ) ) # create new figure

generate_plot( 8 )
# save

'''presentation figure'''
imp.reload( mpl )
pl.figure() # create second figure
generate_plot( 10 ) # generate plot on second figure
# save
    
''' ########################### REFERENCES ########################### '''
'''
[1] Gatan Digital Micrograph, http://www.gatan.com/products/tem-analysis/gatan-microscopy-suite-software
[2] NIST DTSA-II, http://www.cstl.nist.gov/div837/837.02/epq/dtsa2/index.html
'''