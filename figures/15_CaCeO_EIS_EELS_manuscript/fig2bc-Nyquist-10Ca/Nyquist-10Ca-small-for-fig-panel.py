import numpy as np
import pylab as pl
import matplotlib as mpl
##
output_file_dir = 'C:/Users/willb/Dropbox/Crozier Group Users - Will Bowman/Crozier_Lab/Writing/2015_IS EBSD EELS of CaCeria grain boundaries/figures/nyquist/'
output_file_name = '140617_sd10CaDC-2_150-700c_(1)_nyquist_figure_200-250c'

# Ca10_200 = np.genfromtxt( '140617_sd10CaDC-2_200c_32_Fitted.txt', skip_header = 2 
Ca10_200 = np.genfromtxt( 'C:/Users/willb/Dropbox/Crozier Group Users - Will Bowman/Crozier_Lab/Writing/2015_IS EBSD EELS of CaCeria grain boundaries/figures/nyquist/140617_sd10CaDC-2_200c_32_Fitted.txt', skip_header = 2 )
nyq_x_200, nyq_y_200, fit_x_200, fit_y_200 = Ca10_200.T # cols to variables

# Ca10_225 = np.genfromtxt( '140617_sd10CaDC-2_225c_45_Fitted.txt', skip_header = 2 )
Ca10_225 = np.genfromtxt( 'C:/Users/willb/Dropbox/Crozier Group Users - Will Bowman/Crozier_Lab/Writing/2015_IS EBSD EELS of CaCeria grain boundaries/figures/nyquist/140617_sd10CaDC-2_225c_45_Fitted.txt', skip_header = 2 )
nyq_x_225, nyq_y_225, fit_x_225, fit_y_225 = Ca10_225.T # cols to variables

# Ca10_250 = np.genfromtxt( '140617_sd10CaDC-2_250c_59_Fitted.txt', skip_header = 2 )
Ca10_250 = np.genfromtxt( 'C:/Users/willb/Dropbox/Crozier Group Users - Will Bowman/Crozier_Lab/Writing/2015_IS EBSD EELS of CaCeria grain boundaries/figures/nyquist/140617_sd10CaDC-2_250c_59_Fitted.txt', skip_header = 2 )
nyq_x_250, nyq_y_250, fit_x_250, fit_y_250 = Ca10_250.T # cols to variables

## plot stuff
pl.close( 'all' )

mpl.rcParams[ 'font.family' ] = 'sans-serif' # modify matplotlib parameters
mpl.rcParams[ 'font.weight' ] = 'normal'
mpl.rcParams[ 'font.size' ] = 10
mpl.rcParams[ 'axes.formatter.limits' ] = -2, 2

x_axis_label = "Z' ($\Omega$)" # define axis labels
y_axis_label = 'Z" ($\Omega$)'

# x_axis_label = 'Z$_{real}$ ($\Omega$)' # define axis labels
# y_axis_label = 'Z$_{imag.}$ ($\Omega$)'

grain_text, gb_text = 'Grain', 'G.B.'
text_color = 'maroon'
grain_text_x, grain_text_y = 0.5e5, 1.3e5
gb_text_x, gb_text_y = 3e5, 0.9e5

legend_labels = ( '200$^\circ$C', '225', '250' ) # legend info
legend_location = 'best'

# capacitance annotations
C_x, C_y = 4e4, 1.2e5
col_labels = [ r'T ($^\circ$C)', r'$C_{Grain}$', r'$C_{G.B.}$' ]
row_labels = [ '200', '225', '250' ]
table_values = [ r'6.2$\times10^{-9}$', r'6.2$\times10^{-9}$', r'6.2$\times10^{-9}$',
r'6.2$\times10^{-9}$', r'6.2$\times10^{-9}$', r'6.2$\times10^{-9}$' ]
# table = r'''\begin{tabular}{ c | c | c | c } & col1 & col2 & col3 \\\hline row1 & 11 & 12 & 13 \\\hline row2 & 21 & 22 & 23 \\\hline  row3 & 31 & 32 & 33 \end{tabular}'''

ax_lim = [ 3.8e5, 1.5e5 ] #subplot axis limits
subplot_labels = [ '(a)', '(b)' ] # subplot labels
ax_label_x_fraction, ax_label_y_fraction = 0.925, 0.925
hor_align, ver_align = 'center', 'center' 

curve_colors = [ 'maroon', 'slategray', 'black' ]
markers = [ 'o', '^', 'x' ]

# # inset circuit diagram (http://matplotlib.org/examples/pylab_examples/demo_annotation_box.html)
# from matplotlib.offsetbox import OffsetImage, AnnotationBbox
# inset = mpl._png.read_png( 'R3RQ_circuit_model.png' )
# imagebox = OffsetImage( inset )
# xy = ( 0.5, 0.7 )
# ab = AnnotationBbox( imagebox, xy, xycoords = 'data',
#     boxcoords = 'offset points' )

major_locators = [ 1e5, 4e4 ]

# functions used on each subplot
def axes_format( subplot_number ):
    ax = pl.gca()
    ax.set_xlabel( x_axis_label )
    ax.set_ylabel( y_axis_label )
    ax.xaxis.major.formatter._useMathText = True
    ax.yaxis.major.formatter._useMathText = True
    majorLocator = mpl.ticker.MultipleLocator( major_locators[ subplot_number - 1 ] )
    ax.xaxis.set_major_locator( majorLocator )
    ax.yaxis.set_major_locator( majorLocator )
    pl.minorticks_on() # minor ticks on
    
def label_axes( subplot_number ):
    pl.xlim( [ 0, ax_lim[ subplot_number - 1 ] ] ) #define chart limits
    pl.ylim( [ 0, ax_lim[ subplot_number - 1 ] ] )

def label_subplot( subplot_number ):
    subplot_ax_lim = ax_lim[ subplot_number - 1 ]
    subplot_label = subplot_labels[ subplot_number - 1 ]
    pl.text( ax_label_x_fraction * subplot_ax_lim, ax_label_y_fraction * subplot_ax_lim,
        subplot_label, ha = hor_align, va = ver_align )

def format_subplot( subplot_number ):
    axes_format( subplot_number ) #format subplot axes
    label_axes( subplot_number ) #label the axes with words
    # label_subplot( subplot_number ) #label each subplot with letters

def plot_curves( curve_number, nyq_x, nyq_y, fit_x, fit_y ):
    pl.plot( nyq_x, nyq_y, marker = markers[ curve_number - 1 ],
        color = curve_colors[ curve_number - 1 ], linestyle = '', markersize = 4, 
        markerfacecolor = 'none', markeredgecolor = curve_colors[ curve_number - 1 ] )
    pl.plot( fit_x, fit_y, color = curve_colors[ curve_number - 1 ], label = '_nolegend_' )

def centered_annotation( x, y, string, color ):
    pl.text( x, y, string, color = color, ha = 'center', va = 'center' )
    
# create figure
# pl.figure( figsize = ( 7, 3.5 ) )
pl.figure( figsize = ( 4.5, 2.5 ) )

# three curves zoomed out
pl.subplot( 1, 2, 1 )
plot_curves( 1, nyq_x_200, nyq_y_200, fit_x_200, fit_y_200 )
plot_curves( 2, nyq_x_225, nyq_y_225, fit_x_225, fit_y_225 )
plot_curves( 3, nyq_x_250, nyq_y_250, fit_x_250, fit_y_250 )
format_subplot( 1 )

centered_annotation( grain_text_x, grain_text_y, grain_text, text_color )
centered_annotation( gb_text_x, gb_text_y, gb_text, text_color )

pl.legend( legend_labels, loc = legend_location, markerscale = 1.5,
    numpoints = 1, frameon = False, fontsize = 10, labelspacing = .01,
    handletextpad = 0, borderpad = 0 ) # add legend to subplot (a)

# zoomed in
pl.subplot( 1, 2, 2 )
plot_curves( 1, nyq_x_200, nyq_y_200, fit_x_200, fit_y_200 )
plot_curves( 2, nyq_x_225, nyq_y_225, fit_x_225, fit_y_225 )
plot_curves( 3, nyq_x_250, nyq_y_250, fit_x_250, fit_y_250 )
format_subplot( 2 )
# pl.gca().add_artist( ab )
# need latex
# pl.text( C_x, C_y, table, size = 10 )

pl.tight_layout()
pl.show()
dots = 1200
pl.savefig( output_file_dir + output_file_name + '-' + str( dots ) + 'dpi.png', format = 'png', dpi = dots )