''' ########################### OVERVIEW ########################### '''
'''
 Created xxxx-xx-xx by Will Bowman. This ...
'''

''' ########################### IMPORT MODULES ########################### '''
import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import wills_functions as wf
# import csv, imp, os

##


''' ########################### USER-DEFINED ########################### '''
_data_path = '' # path to data file

# convolve step function with width and height 1
a = np.zeros( 10 )
ax = np.linspace( 0, 9, num = 10 )
b = a
a[ 3 ] = 1
b[ 5 ] = 1
ab = np.convolve( b, a, 'same' )
pl.figure()
pl.title( '1x1 * 1x1' )
pl.bar( ax, a, width = 1 )
pl.bar( ax, b, width = 1 )
pl.plot( ab, color = 'red' )

# convolve step functions of (a) 1x1, (c) 4x1
c = np.zeros( 10 )
cx = ax
c[ 3:7 ] = 1
ac = np.convolve( a, c, 'same' )
pl.figure()
pl.title( '1x1 * 4x1' )
# pl.bar( ax, a, width = 1 )
pl.bar( cx, c, width = 1 )
pl.plot( ac, color = 'red' )

# convolve step functions of (c) 4x1, (3) 4x2
d = np.zeros( 10 )
dx = cx
d[ 3:7 ] = 2
cd = np.convolve( c, d, 'same' )
pl.figure()
pl.title( '4x1 * 4x2' )
pl.bar( dx, d, width = 1 )
pl.bar( cx, c, width = 1 )
pl.plot( cd, color = 'red' )

# convolve step functions of (c) 4x1, (e) 4x2 offset by 3 channels
e = np.zeros( 10 )
ex = cx
e[ 5:9 ] = 2
ce = np.convolve( c, e, 'same' )
pl.figure()
pl.title( '4x1 * 4x2 offset' )
pl.bar( ex, e, width = 1 )
pl.bar( cx, c, width = 1 )
pl.plot( ce, color = 'red' )

# convolve step functions of (f) 4x1, (g) 4x2 offset 
fx = np.linspace( 0, 19, 20 )
f = np.zeros( 20 )
g = np.zeros( 20 )
gx = fx
f[ 8:12 ] = 2
g[ 8:12 ] = 1
fg = np.convolve( g, f, 'same' )
gf = np.convolve( f, g, 'same' )
pl.figure()
pl.title( '4x1 * 4x2' )
pl.bar( fx, f, width = 1, align = 'center', color = 'g' )
pl.bar( fx, g, width = 1, align = 'center', color = 'b' )
pl.plot( fg, color = 'r', marker = 'o' )
pl.plot( fg, color = 'k', marker = '^' )

# convolve step functions of (h) 1x1, (i) 1x1 offset 
convolution_type, alignment = 'full', 'center'
hx = np.linspace( 0, 19, 20 )
h = np.zeros( 20 )
i = np.zeros( 20 )
ix = hx
h[ 15 ] = 1
# h[ 17 ] = 1
i[ 7 ] = 2
i[ 10 ] = 1
hi = np.convolve( h, i, convolution_type )
ih = np.convolve( i, h, convolution_type )
pl.figure()
pl.title( '1x1 * 1x1 | conv. type: ' + convolution_type + ', align: ' + alignment )
pl.bar( hx, h, width = 1, align = alignment, color = 'g' )
pl.bar( ix, i, width = 1, align = alignment, color = 'b' )
pl.plot( hi, color = 'r', marker = 'o' )
pl.plot( ih, color = 'k', marker = '^' )
pl.minorticks_on()
pl.legend( ( 'h*i', 'i*h', 'h()', 'i()' ) )

''' ########################### FUNCTIONS ########################### '''
    
    
''' ########################### MAIN SCRIPT ########################### '''
# _data = np.loadtxt( _data_path, skiprows = 3 ) # read data, ignore first three rows

    
''' ########################### REFERENCES ########################### '''