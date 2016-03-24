
import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import wills_functions as wf
import csv, imp, os

# path to data file
data_dir = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/15_WJB_IS EBSD EELS Ca-Ceria gbs/figures/Ca2 coreloss comparison plasmon inset/'

# path to output directory
output_dir = data_dir + wf.date_str() + '/'
output_file = 'Ca2-coreloss-plasmon-inset'

plasmon_input_file_root = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/15_WJB_IS EBSD EELS Ca-Ceria gbs/figures/Ca2 coreloss comparison plasmon inset/141007_2Ca_ARM200kV_06_EELS_LL_gb4_6C_2.5mm'
plasmon_on_gb_suffix, plasmon_off_gb_suffix = '_OnGb.s', '_OffGb.s'

coreloss_input_file_root = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/15_WJB_IS EBSD EELS Ca-Ceria gbs/figures/Ca2 coreloss comparison plasmon inset/141007_2Ca_06'
coreloss_on_gb_suffix, coreloss_off_gb_suffix = '.s', '_off.s'

output_file_name = 'Ca2_coreloss_comparison_plasmon_inset'

# font size, resolution (DPI), file type
fsize, dots, file_type = 10, [300,1200], 'png'
inset = False

## store data
# import data
plasmon_on = np.loadtxt( plasmon_input_file_root + plasmon_on_gb_suffix )
plasmon_off = np.loadtxt( plasmon_input_file_root + plasmon_off_gb_suffix )

coreloss_on = np.loadtxt( coreloss_input_file_root + coreloss_on_gb_suffix )
coreloss_off = np.loadtxt( coreloss_input_file_root + coreloss_off_gb_suffix )

# store variables
plasmon_on_x, plasmon_on_y = plasmon_on.T
plasmon_off_x, plasmon_off_y = plasmon_off.T

coreloss_on_x, coreloss_on_y = coreloss_on.T
coreloss_off_x, coreloss_off_y = coreloss_off.T

## plot stuff
pl.close( 'all' )
pl.figure( figsize = ( 3.5, 3.5 ) )
ax1 = pl.gca()

mpl.rcParams[ 'font.family' ] = 'sans serif' # modify matplotlib parameters
mpl.rcParams[ 'font.weight' ] = 'normal'
mpl.rcParams[ 'font.size' ] = fsize
mpl.rcParams[ 'mathtext.default' ] = 'regular'

legend_labels = [ 'On', 'Off' ]
xaxis_label = 'Energy loss (eV)'
yaxis_label = 'Counts (Arbitrary units)'
axin_yaxis_label = 'Counts\n(Arbitrary units)'
# legend_title = '2 mol% Ca$^{2+}$'

ax1_xlim = ( 300, 1000 )
ax1_ylim = ( 1.5e4, 1.4e5 )
axin_xlim = ( -10, 80 )
axin_ylim = ( 0, 3e5 )

dash = [ 4, 1 ] # [ pix_on pix_off ]

pl.xlim( ax1_xlim ), pl.ylim( ax1_ylim )

shift0, shift1 = 1e4, -1.2e4
pl.plot( coreloss_on_x, coreloss_on_y + shift0, color = 'maroon', linestyle = '-' )
# pl.plot( coreloss_off_x, coreloss_off_y + shift1, color = 'maroon', dashes = dash )

wf.centered_annotation( 380, 1.05e5, 'Ca $L_{23}$', 'black', fontsize=fsize )
wf.centered_annotation( 553, 0.54e5, 'O K', 'black', fontsize=fsize )
wf.centered_annotation( 815, 0.35e5, 'Ce $M_{45}$', 'black', fontsize=fsize )
wf.centered_annotation( 450, 1.3e5, '2 mole% Ca$^{2+}$', 'black', fontsize=fsize )

pl.xlabel( xaxis_label ), pl.ylabel( yaxis_label )

pl.minorticks_on()
ax1.set_yticks([])

# add inset axes
if inset:
    axin = pl.axes([ .5, .535, .4, .4 ]) 
    pl.xlim( axin_xlim ), pl.ylim( axin_ylim )
    
    pl.plot( plasmon_on_x, plasmon_on_y, color = 'maroon', linestyle = '-' )
    pl.plot( plasmon_off_x, plasmon_off_y, color = 'maroon', dashes = dash )
    
    wf.centered_annotation( 15, 2.7e5, 'ZLP', 'black', fontsize=fontsize )
    wf.centered_annotation( 33, 0.7e5, 'Plasmon', 'black', fontsize=fontsize )
    
    # pl.xlabel( xaxis_label ), pl.ylabel( axin_yaxis_label )
    
    pl.minorticks_on()

    axin.set_xticks( np.linspace( 0, 75, 4 ) )
    axin.set_yticks([])

    pl.legend( legend_labels, frameon = False, fontsize = 10, labelspacing = .01,
        handletextpad = 0.2, loc = 'upper right' )

pl.tight_layout()
pl.show()

for dot in dots:
    # pass
    if not os.path.isdir( output_dir ):
        os.mkdir( output_dir )
    output_name = wf.save_name( output_dir, output_file, dot, file_type )
    pl.savefig( output_name, format = file_type, dpi = dot, transparent = True )