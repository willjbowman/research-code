''' ########################### OVERVIEW ########################### '''
'''
Created 2015-01-23 by Will Bowman. This figure compares a TEM EDX spectra from a 
50:50 atomic percent standard CaCeO and a nominally 10mol% Ca doped CeO2. This 
script creates and stores figures in the manuscript figures subdirectory and in
the script's current directory.
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

# data file paths
# these spectra are the result of summing all collected in DM [1], exporting as .msa, 
# then background stripping using NIST DTSA-II software [2]
path_std = 'C:/Dropbox/Crozier Group Users - Will Bowman/active_research/microscopy/150122_CaCe_5050STD_EtOH-mix_ARM200kV/150122_CaCe_5050STD_EtOH-mix_EDS_summed-Clayton[150122_CaCe_5050STD_EtOH-mix_EDS_summed].csv'
path_10Ca = 'C:/Dropbox/Crozier Group Users - Will Bowman/active_research/microscopy/150119_10Ca_ARM200kV/eds/150119_10Ca_EDS_summed_6c_a3_30um_60s-Clayton[150119_10Ca_EDS_summed_6c_a3_30um_60s].csv'

# integration window parameters
eV_min_CaK, eV_max_CaK = 3455, 4171 # (eV) integration window bounds
eV_min_CeL, eV_max_CeL = 4630, 5805
fill_color = ( 255/255,210/255,210/255 ) # rgb are values < 1

# spectrum normalization params
ev_per_chan = 10 # (eV/channel)
x_ray_energy_min, x_ray_energy_max = 4600, 5050 # (eV), normalize to max in this energy window

# figure paramerters
fig_size = ( wf.mm2in( 90 ), wf.mm2in( 90 ) )
manu_fontsize, slide_fontsize = 8, 10 # 8pt for print, 10pt for presentation
output_file_name = 'EDX_5050-Standard_10Ca'
 # absolute path to manuscript sub directory
output_file_path = "C:/Crozier_Lab/Writing/2015_conductvity and chemistry of CaDC grain boundaries/figures/EDX standard and 10mol"

# plot parameters
x_min, x_max, y_min, y_max = 3e3, 7e3, -50, 1.5e4 # axis limits
vshift = 3e3 # vertical shift spectra to separate
dash = [ 4, 2 ] # define dashes ( [ pix_on, pix_off ] )
x_label, y_label = 'X-ray energy (eV)', 'Counts (Arbitrary units)' # axis labels
legend_std, legend_10Ca = 'Ca:Ce standard', '10 mol%' # legend text
legend_location = 'upper left' # legend locator
curve_color = 'maroon'

# plot label parameters
labelsx = [ 4000, 4100, 4350, 5200, 5300, 5700, 6050, 6700 ] # label x position
labelsy = [ 11500, 4500, 3700, 12e3, 8700, 4900, 3900, 3500 ] # label y position
labels = [ r'Ca $K_{\alpha}$', r'Ca $K_{\beta}$', r'Ce $L_1$',
    r'Ce $L_{\alpha}$', r'Ce $L_{\beta_1}$', r'Ce $L_{\beta_2}$',
    r'Ce $L_{\gamma_1}$', r'Ce $L_{\gamma_2}$' ] # label text strings
label_color = 'black'


''' ########################### FUNCTIONS ########################### '''

def get_index( energy ):
    return int( energy / ev_per_chan )

def label_peak( x, y, label, fontsize ):
    wf.centered_annotation( x, y, label, label_color, fontsize )

def generate_plot( fontsize ):
    
    pl.plot( x_std, y_std_shifted, color = curve_color, dashes = dash ) # plot data
    pl.plot( x_10Ca, y_10Ca_scaled, color = curve_color )
    
    pl.fill_between( windx_CaK, windy_CaK_shift, y_min, color = fill_color )
    pl.fill_between( windx_CeL, windy_CeL_shift, y_min, color = fill_color )
    
    ax = pl.gca() # store current axis in variable
    
    pl.xlim( x_min, x_max ), pl.ylim( y_min, y_max ) # apply plot limits
    pl.xlabel( x_label ), pl.ylabel( y_label ) # apply plot labels
    pl.minorticks_on() # minor ticks on
    ax.yaxis.set_ticklabels([]) # y tick labels off
    
    # label peaks
    for i in np.arange( len ( labels ) ):
        label_peak( labelsx[ i ], labelsy[ i ], labels[ i ], fontsize )
    
    # apply legend
    legend_labels = ( legend_std, legend_10Ca ) # tuple passed to pl.legend()
    pl.legend( legend_labels, loc = legend_location, 
        numpoints = 1, frameon = False, fontsize = fontsize, labelspacing = .01,
        handletextpad = 1 )

    # change font size of axis objects
    for item in ( [ ax.xaxis.label, ax.yaxis.label ] + ax.get_xticklabels() + ax.get_yticklabels() ):
        item.set_fontsize( fontsize )
    
    pl.tight_layout()
    pl.show() # render plots
    
    
''' ########################### MAIN SCRIPT ########################### '''

# read .csv data files and store in variable
x_std, y_std = wf.read_csv_2col( path_std )
x_10Ca, y_10Ca = wf.read_csv_2col( path_10Ca )

# integration window highlighting
wind_minx_CaK = get_index( eV_min_CaK ) # store window bounds as int
wind_maxx_CaK = get_index( eV_max_CaK )
wind_minx_CeL = get_index( eV_min_CeL )
wind_maxx_CeL = get_index( eV_max_CeL )

windx_CaK = x_std[ wind_minx_CaK : wind_maxx_CaK ] # store spectra xi,yi w/in
windy_CaK = y_std[ wind_minx_CaK : wind_maxx_CaK ] # integration windows
windx_CeL = x_std[ wind_minx_CeL : wind_maxx_CeL ]
windy_CeL = y_std[ wind_minx_CeL : wind_maxx_CeL ]

windy_CaK_shift = wf.add_to_list( windy_CaK, vshift ) # vertical shift
windy_CeL_shift = wf.add_to_list( windy_CeL, vshift ) # spectra

eV_min_CaK, eV_max_CaK = 3455, 4171 # (eV) integration window bounds
eV_min_CeL, eV_max_CeL = 4630, 5805

# normalize spectra to Ce-L_alpha-1 x-ray line
i_l = get_index( x_ray_energy_min ) # indicies of x-ray line bounds
i_r = get_index( x_ray_energy_max ) # converted to int for list indexing

line_std = y_std[ i_l : i_r ] # store counts in normalization energy window
line_10Ca = y_10Ca[ i_l : i_r ]

# calculate scaling factor to normalize curves
scale_std_10 = np.sum( line_std ) / np.sum( line_10Ca )

 # iterate through list multiplying each element by scale factor
y_10Ca_scaled = wf.multiply_list( y_10Ca, scale_std_10 )

# vertical shift spectrum
y_std_shifted = wf.add_to_list( y_std, vshift )


# generate and save plot(s)

# define output filename for storage in manuscript figure directory
manu_output_basename = output_file_path + '/' + output_file_name

# get current script directory info to store a copy figure with script
script_name, script_dir_path = wf.current_script_info()
# define output filename for storage in script's current directory
local_output_basename = script_dir_path + '/' + output_file_name

pl.close( 'all' ) # close open figures

# manuscript figure
imp.reload( mpl ) # reload matplotlib module
pl.figure( figsize = fig_size ) # create new figure
generate_plot( 8 ) # generate plot, passing fontsize

# save figure as 1k dpi .pdf for manuscript in manuscript sub directory
pl.savefig( manu_output_basename + '_print_fig.pdf', format = 'pdf', dpi = 1000 )
# save figure as 1k dpi .pdf in cuurent directory
pl.savefig( local_output_basename + '_print_fig.pdf', format = 'pdf', dpi = 1000 )

# presentation figure
imp.reload( mpl )
pl.figure( figsize = fig_size ) # create second figure
generate_plot( 10 ) # generate plot on second figure

# save figure as .5k dpi .png for presentations in manuscript sub directory
pl.savefig( manu_output_basename + '_slide_fig.png', format = 'png', dpi = 500 )
# save figure as .5k dpi .png in cuurent directory
pl.savefig( local_output_basename + '_slide_fig.png', format = 'png', dpi = 500 )

    
''' ########################### REFERENCES ########################### '''
'''
[1] Gatan Digital Micrograph, http://www.gatan.com/products/tem-analysis/gatan-microscopy-suite-software
[2] NIST DTSA-II, http://www.cstl.nist.gov/div837/837.02/epq/dtsa2/index.html
'''