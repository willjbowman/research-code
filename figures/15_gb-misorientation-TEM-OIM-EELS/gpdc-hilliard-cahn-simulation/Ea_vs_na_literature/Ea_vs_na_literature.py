''' ########################### OVERVIEW ########################### '''
'''
Created 2016-09-07 by Will Bowman.
This script reads digitized and prettified conductivity data from literature 
to make a figure showing Ea vs. na
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
# path to data file
paper_dir = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/' +\
    '15_WJB_gb misorientation OIM EELS/'
fig_name = 'gpdc-poisson-cahn-simulation'
sub_name = 'Ea_vs_na_literature'
fig_dir = paper_dir + 'figures/' + fig_name + '/' + sub_name + '/'
data_dir = paper_dir + 'data processing/' + fig_name + '/' + sub_name + '/'

d_in = [ 'Kudo T Obayashi H_J Electrochem Soc (1976) Fig 1',
    'Stefinak TS_MIT Dissertation (2004) Fig 1-5',
    'Avila-Paredes HJ Kim S etal_J mat chem (2009) Fig 6',
    'Zhang TS etal_Mat res bull (2006) Fig 4' ]

# the order is f-ed up bc i need to plot both graphs no matter how many in_file
tits = [ 'Kudo (76)', r'$E_a vs. [Solute]$', 'Stefinak (06)', 
	'Avila-Par. (09)', 'Zhang (06)' ]
leg_ents = [ 
	[ '10GCO', '20GCO', '30GCO', '40GCO', '50GCO' ],
    [ 
    	r'Gd$^{3+} \sigma_{Total}^{DC}$ [1]', 
    	r'Sm$^{3+} \sigma_{Total}^{DC}$ [2]', 
    	r'Gd$^{3+} \sigma_{Grain}^{AC}$ [3]', 
    	r'Gd$^{3+} \sigma_{Total}^{AC}$ [4]' 
    ],
	[ 'CeO2', '10SCO', '20SCO', '30SCO', '40SCO', '50SCO', '60SCO' ],
	[ 'Grain', 'Grain boundary' ],
	[ 'Total' ]
]
Xs = [
	[ .1, .2, .3, .4, .5 ],
	[ 0, .1, .2, .3, .4, .5, .6 ],
	[], []
]
Ts = [ [], [],
	np.array([ 500, 600, 700, 800, 900 ])
]

locs = [ 'upper right', 'upper left', 'lower left', 'best', 'best' ]
x_lab = [ '1000/T (1/K)', '[Solute] (Mole frac.)', '1000/T (1/K)', 
	'[Gd] (Mole frac.)', '[Gd] (Mole frac.)' ]
y_lab = [ r'$\sigma$T (S/cm K)', r'$E_a$ (eV)', r'$\sigma$T (S/cm K)', 
	r'$E_a$ (eV)', r'$E_a$ (eV)' ]
x_lims = [ [-0,1], [-.1,.7], [0,.7] ]
y_lims = [ [-.1,2.2], [.6,1.8], [-.1,3] ]

# path to output directory
output_dir = fig_dir
output_file_name = sub_name
subfolder = False
save = True
# save = False

# append string to in_file names
d_in = [ data_dir + s + '_PRETTY.txt' for s in d_in ]

# naming sequence of figs with successive curves on same axis
file_anno = [ '-0of0' ] # for single fig with all curves
# file_anno = [ '-area-ave-spectrum' ]
fig_size = [ (3,3), (4,4), (3,3) ] # ( wid, hi ) in inches

# font size, resolution (DPI), file type
fsize, dots, file_types = 10, [300], ['png','svg']
cols = wf.cols()
dash, width = [ 6, 1 ], 1 # [ pix_on pix_off ], linewidth
mark, msize, mwidth = wf.marks(), 7, 0.5
z_lims = [ [0,0], [.05,.2], [.8,.95] ]
z_lims = [ [0,0], [0,.2], [.8,1] ]
x_shift = [ '', 3, .5 ]
y_shift = [ '', .75, .5 ]
subplot_white_space = 0.1 # see pl.subplots_adjust()
# fill_x = [[[870,915],[930,960]],[[870,915],[930,960]]]
fill_xs = [ [ 875, 915, 925, 965 ] ]
fill_cs = [ 'lightgrey', wf.colors('pale_gold') ]

kb = wf.boltzmann_constant(0,1)
Eas = []


''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize

def add_legend( ax, leg_ents, loc='best' ):
    ax.legend( leg_ents, loc=loc, frameon=False, labelspacing=.1,
        handletextpad=.3, fancybox=False, borderpad=.3, fontsize=fsize,
        numpoints=1 )
    pl.tight_layout()

def add_labels( ax, fig_idx ):
	ax.set_title( tits[ fig_idx ] )
	ax.set_xlabel( x_lab[ fig_idx ] )
	ax.set_ylabel( y_lab[ fig_idx ] )
    
''' ########################### MAIN SCRIPT ########################### '''

''' ### STORE DATA IN VARIABLES ### '''
d_0 = np.genfromtxt( d_in[0], delimiter='\t' ) # update when headers happen
d_2 = np.genfromtxt( d_in[1], delimiter='\t' )
d_3 = np.genfromtxt( d_in[2], delimiter='\t' )
d_4 = np.genfromtxt( d_in[3], delimiter='\t' )

pl.close('all')

'''SECTION FOR EACH INPUT FILE (THEY'RE ALL DIFFERENT)'''
'''Kudo T Obayashi H_J Electrochem Soc (1976) -- fig 1'''
fidx = 0
Eas.append([]) # New set of Eas

invKs = d_0.T[ [0,2,4,6,8],: ]
ST_exps = d_0.T[ [1,3,5,7,9],: ]

pl.figure( figsize=fig_size[fidx] )
for i, invK in enumerate( invKs ):
	ST_exp = ST_exps[i]
	invK_1 = invK / 1e3 # convert to 1/T for Ea computation
	ST = 10 ** ST_exp # compute SigT
	ST_ln = np.log( ST ) # compute ln( SigT ) for Ea calc
	m, b = np.polyfit( invK_1, ST_ln, 1 ) # fitting parameters for Ea
	Ea = - m * kb # compute Ea
	Eas[fidx].append( Ea )
	pl.plot( invK, ST_exp, marker=mark[i], c=cols[i] )

ax0 = pl.gca()
add_labels( ax0, fidx )
add_legend( ax0, leg_ents[fidx], loc=locs[fidx] )


'''Stefinak TS_MIT Dissertation (2004) Fig 1-5'''
fidx = 2 # fig index
Eas.append([]) # New set of Eas
pl.figure( figsize=fig_size[fidx] )

TCs = Ts[fidx] # array of T (C)
sig_exps_X = d_2.T[ [1,3,5,7,9],: ] # 2D array of SCO cond expon for each X
sig_exps_T = sig_exps_X.T # 2D array of SCO cond expon for each T
TKs = TCs + 273 # array of T (K)
invK_1 = 1 / TKs # array of 1/T (1/K)
invK_1e3 = np.around( ( 1e3 * invK_1 ), decimals=2 ) # array of 1e3/T (1/K)

for i in np.arange( np.shape(sig_exps_T)[0] ):
	# print(i)
	sig = 10 ** sig_exps_T[i] # compute sig
	sigT = sig * TKs # compute SigT
	pl.plot( invK_1e3, sig_exps_T[i], marker=mark[i], c=cols[i] )
	m, b = np.polyfit( invK_1, np.log(sigT), 1 ) # fitting parameters for Ea
	Ea = - m * kb # compute Ea
	Eas[fidx-1].append( Ea )

ax2 = pl.gca()
add_labels( ax2, fidx )
ax2.xaxis.set_major_locator( mpl.ticker.MultipleLocator( .1 ) )
add_legend( ax2, leg_ents[fidx], loc=locs[fidx] )


'''Avila-Paredes HJ Kim S etal_J mat chem (2009) Fig 6'''
fidx = 3 # fig index
pl.figure( figsize=fig_size[0] )

xs_gr_gb = d_3.T[ [0,2],: ]
Xs[ fidx-1 ] = d_3.T[ 0,: ]
Eas_gr_gb = d_3.T[ [1,3],: ]
Eas.append( d_3.T[ 1,: ] ) # grain Ea

for i, Ea in enumerate( Eas_gr_gb ):
	pl.plot( xs_gr_gb[i], Ea, marker=mark[i], c=cols[i] )

ax = pl.gca()
add_labels( ax, fidx )
add_legend( ax, leg_ents[fidx], loc=locs[fidx] )


'''Zhang TS etal_Mat res bull (2006) Fig 4'''
fidx = 4 # fig index
pl.figure( figsize=fig_size[0] )

xs_gr_gb = d_4.T[ 0,: ]
Xs[ fidx-1 ] = xs_gr_gb
Eas_gr_gb = d_4.T[ 1,: ]
Eas.append( d_4.T[ 1,: ] ) # grain Ea

# for i, Ea in enumerate( Eas_gr_gb ):
pl.plot( xs_gr_gb, Eas_gr_gb, marker=mark[0], c=cols[0] )

ax = pl.gca()
add_labels( ax, fidx )
add_legend( ax, leg_ents[fidx], loc=locs[fidx] )


'''SUMMARY FIGURE WITH ALL EAS'''
fidx = 1
pl.figure( figsize=fig_size[fidx] )

for k, Ea in enumerate( Eas ):
	pl.plot( Xs[k], Ea, marker=mark[k], c=cols[k] )

ax1 = pl.gca()
add_labels( ax1, fidx )
ax1.set_xlim( x_lims[fidx] )
ax1.set_ylim( y_lims[fidx] )
ax1.xaxis.set_major_locator( mpl.ticker.MultipleLocator( .1 ) )
add_legend( ax1, leg_ents[fidx], loc=locs[fidx] )
ax1.minorticks_on()

if save:
	wf.save_fig( output_dir, file_types, dots, output_file_name, anno='', 
		subfolder_save=subfolder )
        # pl.close('all')

''' ########################### REFERENCES ########################### '''
'''
1. 
'''