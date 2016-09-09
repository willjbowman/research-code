''' ########################### OVERVIEW ########################### '''
'''
Created 2016-09-07 by Will Bowman.
This script takes txt file created by digitize_plotted_data_in_image.py
and manipulates it as needed, then saves a pretty txt file to be read into 
other scripts.

If everything works, you should be able to save the txt file created via 
digitizing, along with the image which was digitized, together in data_dir
and a new txt and png (_PRETTY) will be saved alongside them. At the very least,
make sure to update section I for each new img/txt.

KNOWN ISSUES
- there is no column header saved.
- the precision is crazy, like 15 float
'''

''' ########################### IMPORT MODULES ########################### '''
import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import csv, imp, os
import wills_functions as wf
imp.reload(wf) # reload wf
##

''' ########################### USER-DEFINED ########################### '''
''' START SECTION I '''
# path to data file
data_dir = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/' +\
    '15_WJB_gb misorientation OIM EELS/data processing/' +\
    'gpdc-poisson-cahn-simulation/Ea_vs_na_literature/'
fig_name = 'Zhang TS etal_Mat res bull (2006) Fig 4'

# fig title, legend entries, axis labels
tits = [ fig_name, '' ]
leg_ents = [ 
    [ 'Total', 'Grain boundary' ]
]
x_lab = [ r'$[Gd^{3+}] (Mole frac.)$', '' ]
y_lab = [ r'$E_a (eV)$', '' ]
leg_loc = 'best'
''' END SECTION I '''

# path to output directory
output_dir = data_dir
output_file_name = fig_name + '_PRETTY'
subfolder = False
save = True
# save = False

in_file_name = data_dir + fig_name
d_in_0, skip_0 = in_file_name + '.txt', 1
img_in = in_file_name + '.png'

# naming sequence of figs with successive curves on same axis
# file_anno = [ '-0of0' ] # for single fig with all curves
# file_anno = [ '-area-ave-spectrum' ]
fig_size = [ (9,9), (6,6) ] # ( wid, hi ) in inches

# font size, resolution (DPI), file type
fsize, dots, file_types = 10, [300], ['png','svg']
cols = wf.cols()
dash, width = [ 6, 1 ], 1 # [ pix_on pix_off ], linewidth
mark, msize, mwidth = wf.marks(), 7, 0.5
x_lims = [ [-0,1], [0,.6], [870,970] ]
y_lims = [ [-.1,2.2], [.6,1.5], [-.1,7.5] ]


''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize

def add_legend( ax, leg_ents, loc='best' ):
    ax.legend( leg_ents, loc=loc, frameon=False, labelspacing=.1,
        handletextpad=.3, fancybox=False, borderpad=.3, fontsize=fsize,
        numpoints=1 )
    
''' ########################### MAIN SCRIPT ########################### '''

''' ### STORE DATA IN VARIABLES ### '''
img = mpl.image.imread( img_in ) # get image from paper
d_0 = np.genfromtxt( d_in_0, delimiter='\t', skiprows=skip_0 )

d_x = d_0.T[0,:] # first col
d_y = d_0.T[ 1:np.shape(d_0)[0] ] # rest of cols

# generate text file data
d_out, txt_out = [], []
for i, col in enumerate( d_y ):
    idx, stripped_d_y = wf.strip_nan( col ) # strip nans
    stripped_d_x = d_x[ idx ]
    d_out.append( [stripped_d_x, stripped_d_y] )
    txt_out.append( stripped_d_x )
    txt_out.append( stripped_d_y )

pl.close('all')
pl.figure( figsize=fig_size[0] )

# image from paper
'''( (rows,cols), (subplot_index), colspan=2, rowspan=1 )'''
pl.subplot2grid( (2,2), (0,0), rowspan=2 )
imgplot = pl.imshow( img )
ax0 = pl.gca()
ax0.set_xticks([])
ax0.set_xticklabels([])
ax0.set_yticks([])
ax0.set_yticklabels([])

# data from paper
'''( (rows,cols), (subplot_index), colspan=2, rowspan=1 )'''
pl.subplot2grid( (2,2), (0,1) )

for j, curve in enumerate( d_out ):
    pl.plot( d_out[j][0], d_out[j][1], marker=mark[j], c=cols[j] )

ax1 = pl.gca()
ax1.set_xlabel( x_lab[0] )
ax1.set_ylabel( y_lab[0] )
add_legend( ax1, leg_ents[0], loc='best' )
ax1.minorticks_on()
ax1.set_title( tits[0] )

pl.tight_layout()
if save:
    wf.save_fig( output_dir, file_types, dots, output_file_name, anno='',
        subfolder_save=subfolder )
    # pl.close('all')

    # save d_out to txt
    txt_out_T = np.asarray( txt_out ).T.tolist() # store txt as columns
    np.savetxt( data_dir+output_file_name+'.txt', txt_out_T, delimiter='\t')

''' ########################### REFERENCES ########################### '''
'''
1. 
'''