''' ########################### OVERVIEW ########################### '''
'''
Created 2015-09-07 by Will Bowman. This creates a figure with complex impedance
spectra from GPDC, and GB conductivity for GPDC and GDC
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
fig_dir = 'gpdc-electrical'
# this is the full path to figure directory (for reading data and writing files)
figs_dir = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/15_WJB_gb misorientation OIM EELS/figures/' + fig_dir + '/'

# sp0: GPDC Nyquist
d_0 = figs_dir + 'GPDC_200C_fitted_140305.txt'
d_0_skiprows = 1

# sp1: GPDC and GDC boundary conductivity
d_1 = figs_dir + 'Gpdc_CalculatedConductivityErr.txt'
d_1_skiprows = 1
d_2 = figs_dir + 'Gdc2b_CalculatedConductivityErr.txt'
d_2_skiprows = 1

# font size, resolution (DPI), file type, fig_size
# create a figure of size ( width", height" )
# font_size, dots, file_type, fig_size = 10, [ 300, 1200 ], 'png', ( 3.33, 4 )
font_size, dots, file_type, fig_size = 10, [ 300 ], 'png', ( 3.33, 4.5 )
# sub_plots = ( 2, 1, 1 ) # suplot 0 ( sub_y, sub_x, sub_i )

# subplot 0 (sp0): length fraction v misorientation angle
sp0_ax_labs = [ 'Z$_{Real}$ ($\Omega$)', '-Z$_{Imag.}$ ($\Omega$)' ]
sp0_entries = ( 'Data', 'Fit' ) # legend entries
sp0_c = [ 'maroon', 'grey' ] # line colors
sp0_m, sp0_m_width = [ 'o', None ], 1 # markers
sp0_ls = [ '', '-' ] # line styles (use '' instead of None)
sp0_lims = [ [ 0, 2.5e5 ], [ 0, 1.5e5 ] ] # x, y axis limits
sp0_maj_loc = [ 0.5e5, 0.5e5 ] # [x,y] major tick locators
sp0_leg_loc = 'upper right'

# subplot1 (sp1): length fraction v concentration
sp1_ax_labs = [ r'10$^{3}$/T (1/K)', r'$\sigma$ (S $cm^{-1})$' ]
sp1_entries = ( 'GdCeO$_2$', '(Pr,Gd)CeO$_2$' )
sp1_c = [ 'maroon', wf.colors('dark_grey') ] # line colors
sp1_m, sp1_m_width = [ '^', 'o' ], 1 # markers
sp1_ls = [ '-', '--' ] # line styles (use '' instead of None)
sp1_lims = [ [ .9, 2.8 ], [ 1e-12, 1e0 ] ] # axis limits
sp1_y_ticks = [ 1e0, 1e-4, 1e-8, 1e-12 ]
sp1_maj_loc = [ 0.5, 1e-2 ] # [x,y] major tick locators
sp1_leg_loc = 'upper right'

file_anno = [ '-0of1', '-1of1' ]

''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( font_size ) # pass the figure's fontsize
    # wf.slide_art_styles()
    # mpl.rc( 'font', family='serif', serif='Times New Roman', weight='normal' )
    mpl.rc( 'font', family='sans-serif', serif='Helvetica', weight='normal' )
    mpl.rc( 'lines', ls='', mew=0.01, markersize=6 )
    mpl.rc( 'legend', numpoints=1, handletextpad=0.2, borderpad=0.2, 
      frameon=False, fontsize=10, labelspacing=.01 )

def sp0_style( ax ):
    # wf.ax_limits( sp0_lims )
    pl.minorticks_on()
    wf.ax_labels( sp0_ax_labs )
    wf.major_ticks( ax, sp0_maj_loc, scientific=True )
    pl.legend( sp0_entries, loc=sp0_leg_loc ) # locate legend x,y from bottom left
    # ax.yaxis.set_ticklabels([]) # y tick labels off
    # ax.set_yticks([]) # no ticks

def sp1_style( ax ):
    wf.ax_limits( sp1_lims )
    pl.minorticks_on()
    wf.ax_labels( sp1_ax_labs )
    ax.set_yscale( 'log' )
    ax.set_yticks( sp1_y_ticks ) #add ticks and labels to axis
    pl.legend( sp1_entries, loc=sp1_leg_loc ) # locate legend x,y from bottom left
    # wf.major_ticks( ax, sp1_maj_loc )
    # ax.yaxis.set_ticklabels([]) # y tick labels off
    # ax.set_yticks([])


''' ########################### MAIN SCRIPT ########################### '''

# read data, skip header rows
sp0_x0, sp0_y0, sp0_x1, sp0_y1 = np.loadtxt( d_0, skiprows=d_0_skiprows ).T
a, gpdc_x, gpdc_gr_S, gpdc_gr_S_err, gpdc_gb_S, gpdc_gb_S_err = \
    np.loadtxt( d_1, skiprows=d_1_skiprows ).T
b, gdc_x, gdc_gr_S, gdc_gr_S_err, gdc_gb_S, gdc_gb_S_err = \
    np.loadtxt( d_2, skiprows=d_2_skiprows ).T

nyq_x_clip, nyq_y_clip, nyq_x_lims = wf.clip_xy( sp0_lims[0], sp0_x0, sp0_y0 )
fit_x_clip, fit_y_clip, fit_x_lims = wf.clip_xy( sp0_lims[0], sp0_x1, sp0_y1 )

gr_x = [ gdc_x, gpdc_x ]
gr_y = [ gdc_gr_S, gpdc_gr_S ]
gr_y_err = [ gdc_gr_S_err, gpdc_gr_S_err ]
gb_y = [ gdc_gb_S, gpdc_gb_S ]
gb_y_err = [ gdc_gb_S_err, gpdc_gb_S_err ]

legend_handles = [] # container for legend handles (filled in loop)

pl.close( 'all' ) # close all open figures
# for h in range( 1, len( file_anno ) + 1 ):
for h in range( 0, len( file_anno ) ):

    # pl.close( 'all' ) # close all open figures
    pl.figure( figsize=fig_size ) # create a figure of size ( width", height" )
    ax = pl.gca() # store current axis
    mpl_customizations() # apply customizations to matplotlib

    for i in range( 0, h+1 ):

        # print( h, i )
        pl.subplot( 2, 1, 1 ) # suplot 0 ( sub_y, sub_x, sub_i )
        ax0 = pl.gca()
        pl.plot( nyq_x_clip, nyq_y_clip, c=sp0_c[0], marker=sp0_m[0], ls=sp0_ls[0] )
        pl.plot( fit_x_clip, fit_y_clip, c=sp0_c[1], marker=sp0_m[1], ls=sp0_ls[1] )
        sp0_style( ax0 )
        ax0.set_xlim( nyq_x_lims )
        ax0.set_ylim( sp0_lims[1] )

        col, mark = sp1_c[i], sp1_m[i]

        pl.subplot( 2, 1, 2 ) # suplot 1 ( sub_y, sub_x, sub_i )
        ax1 = pl.gca()
        pl.errorbar( gr_x[i], gr_y[i], gr_y_err[i], c=col, marker=mark, 
            ls=sp1_ls[0] )
        pl.errorbar( gr_x[i], gb_y[i], gb_y_err[i], c=col, marker=mark,
            ls=sp1_ls[1] )
        sp1_style( ax1 )

        # if h == len( file_anno ):
            # legend handler for ith curve
        leg_info = mpl.lines.Line2D( [], [], color=col, marker=mark, 
            markersize=6, linestyle='-' )
        # legend_handles.append( leg_info ) # append ith legend handler to legend handles
        legend_handles.append( '' ) # append ith legend handler to legend handles
        legend_handles[h] = leg_info # store legend_info of h-th curve set

    ax2 = ax1.twiny() #create a second x-axis which shares ax1's y-axis
    Tc_axis_label = 'T ($^\circ$C)'
    ax2_Tc_ticks = np.linspace( 700, 100, 13 ) # Celcius axis ticks and labels
    ax2_Tc_ticklabels = np.array( [ 700, '', '', '', 500, '', 400, '', 300, '', 200, '', 100 ] )
    ax2_tick_Tk_locations = 1000 / ( ax2_Tc_ticks + 273 ) #calculate 2nd axis tick locations
    ax2_tick_Tc_locations = ( ax2_tick_Tk_locations - sp1_lims[0][0] ) / ( sp1_lims[0][1] - sp1_lims[0][0] )
    ax2.set_xticks( ax2_tick_Tc_locations ) #add ticks and labels to 2nd axis
    ax2.set_xticklabels( ax2_Tc_ticklabels )
    ax2.set_xlabel( Tc_axis_label )

    # applies to all subplots, h_pad defined vertical spacing
    pl.tight_layout( pad=0.3, h_pad=0.6 )

    j = h-1 
    ax1.legend( legend_handles, sp1_entries, loc=sp1_leg_loc )
    # if j > 0:
    #     pl.legend( sp1_entries[0::j], loc=sp1_leg_loc ) # locate legend x,y from bottom left
    # else:
    #     pl.legend( sp1_entries[0], loc=sp1_leg_loc ) # locate legend x,y from bottom left

    pl.show()
    
    # output file info
    output_dir = figs_dir + wf.date_str() + '/'
    output_file = fig_dir
        
    for dot in dots:
        # pass
        if not os.path.isdir( output_dir ):
            os.mkdir( output_dir )
        output_name = wf.save_name( output_dir, output_file+file_anno[h], 
            dot)
        pl.savefig( output_name+'.png', format='png', dpi=dot, transparent=True )
        pl.savefig( output_name+'.svg', format='svg', transparent=True )

''' ########################### REFERENCES ########################### '''