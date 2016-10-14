''' ########################### OVERVIEW ########################### '''
'''
 Updated 2016-09-28 by Will Bowman.
 This script creates a figure for plotting composition line profiles for 2CCO
 and 10CCOO derived from EELS
'''

''' ########################### IMPORT MODULES ########################### '''
import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import wills_functions as wf
import csv, imp, os
imp.reload(wf) # reload wf

##

''' ########################### USER-DEFINED ########################### '''
# path to data file
paper_dir ='C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/'+\
    '15_WJB_IS EBSD EELS Ca-Ceria gbs/'
sub_dir = ''
# sub_dir = 'CCO-STEM-EELS/' # comment if no subdir
fig_name = 'CCO-EELS-composition-profiles'
fig_dir = paper_dir + 'figures/' + fig_name + '/'
data_dir = paper_dir + 'data/' + fig_name + '/'

d_in_0, d_in_0_ski = data_dir + 'CCO-EELS-composition-profiles_2_and_10.txt', 4
# d_in_1, d_in_1_ski = data_dir + 'CCO-gb-conductivity-300C.txt', 1

# naming sequence of figs with successive curves on same axis
file_anno = [ '-0of1', '-1of1' ] # for single fig with all curves
fig_size = [ (6,3), ( 3, 3 ) ] # ( width, hight ) in inches

# path to output directory
output_dir = fig_dir
output_file_name = fig_name
subfolder = True
save = True
# save = False

# font size, resolution (DPI), file type
leg_ents = [ [ ['[Ce]', '[Ca]'], ['[Ce]', '[Ca]'] ],
	['10%, [Ce]', r'$[Ca]_2$', r'$[Ce]_{10}$', r'$[Ca]_{10}$'] ]
leg_loc = 'best'
x_labs = [ 'Distance (nm)' ]
y_labs = [ r'Concentration (Mole frac.)' ]
x_lims = [ [-6,6] ]
y_lims = [ [ 0, 1 ] ]

fsize, dots, file_types = 10, [300], ['png','svg']
cols = wf.cols()
marks, msize, mwidth = wf.marks(), 5, 0.5

shif_x_10, shif_x_2 = -3.5, -9.2 # distance position of gb


''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize
        
''' ########################### MAIN SCRIPT ########################### '''

# READ AND STORE DATA IN VARIABLES
d0 = np.genfromtxt( d_in_0, skiprows=d_in_0_ski )
x_10, ca_10, ce_10, o_10, x_2, ca_2, ce_2, o_2 = d0.T


'''GENERATE FIGURES'''

# subplot fig for slide
pl.close( 'all' ) # close all open figures
pl.figure( figsize=fig_size[0] ) # create a figure ( w, h )
mpl_customizations() # apply customizations to matplotlib

pl.subplot2grid( (1,2), (0,0) ) # ((rows,cols),(subplot_index))
ax0 = pl.gca() # store current axis

ax0.plot( x_2+shif_x_2, ce_2, color=cols[0], marker=marks[0], ms=msize,
	ls='--' )
ax0.plot( x_2+shif_x_2, ca_2, color=cols[1], marker=marks[1], ms=msize )

# label_lim( ax0, [0] ) # this could be a nice method
ax0.set_xlim( x_lims[0] )
ax0.set_ylim( y_lims[0] )
ax0.set_xlabel( x_labs[0] )
ax0.set_ylabel( y_labs[0] )
ax0.minorticks_on()

ax0.legend( leg_ents[0][0], loc=leg_loc,
    numpoints=1, frameon=False, fontsize=fsize, labelspacing=.6,
    handletextpad=.6 )

pl.subplot2grid( (1,2), (0,1) ) # ((rows,cols),(subplot_index))
ax1 = pl.gca() # store current axis

ax1.plot( x_10+shif_x_10, ce_10, color=cols[0], marker=marks[0], ms=msize,
	ls='--' )
ax1.plot( x_10+shif_x_10, ca_10, color=cols[1], marker=marks[1], ms=msize )

# label_lim( ax1, [0] ) # this could be a nice method
ax1.set_xlim( x_lims[0] )
ax1.set_ylim( y_lims[0] )   
ax1.set_xlabel( x_labs[0] )
ax1.set_ylabel( y_labs[0] )
ax1.minorticks_on()

ax1.legend( leg_ents[0][1], loc=leg_loc,
    numpoints=1, frameon=False, fontsize=fsize, labelspacing=.6,
    handletextpad=.6 )
        
pl.tight_layout() # can run once to apply to all subplots, i think
if save:
    wf.save_fig( fig_dir, file_types, dots, output_file_name, anno,
        subfolder_save=subfolder )



# # overlaid compact figure for manuscript
# for i, anno in enumerate( file_anno ):
    
#     pl.close( 'all' ) # close all open figures
#     pl.figure( figsize=fig_size ) # create a figure ( w, h )
#     mpl_customizations() # apply customizations to matplotlib
    
#     # pl.subplot2grid( (1,2), (0,0) ) # ((rows,cols),(subplot_index))
#     ax0 = pl.gca() # store current axis

#     ax0.plot( x_2+shif_x_2, ce_2, color=cols[1], marker=marks[2], ms=msize,
#     	ls='--' )
#     ax0.plot( x_2+shif_x_2, ca_2, color=cols[1], marker='x', ms=msize )
#     ax0.plot( x_10+shif_x_10, ce_10, color=cols[0], marker=marks[0], ms=msize,
#     	ls='--' )
#     ax0.plot( x_10+shif_x_10, ca_10, color=cols[0], marker=marks[1], ms=msize )

#     # label_lim( ax0, [0] ) # this could be a nice method
#     ax0.set_xlim( x_lims[0] )
#     ax0.set_ylim( y_lims[0] )
#     ax0.set_xlabel( x_labs[0] )
#     ax0.set_ylabel( y_labs[0] )
#     ax0.minorticks_on()
    
#     ax0.legend( leg_ents, loc=leg_loc,
#         numpoints=1, frameon=False, fontsize=fsize, labelspacing=.1,
#         handletextpad=.1 )
            
#     pl.tight_layout() # can run once to apply to all subplots, i think
#     if save:
#         wf.save_fig( fig_dir, file_types, dots, output_file_name, anno,
#             subfolder_save=subfolder )


''' ########################### REFERENCES ########################### '''
'''
1. 
'''
