import numpy as np
import pylab as pl

#
'''
1. 2 nm step for concentration * 0.2 nm step for probe
2. 2 nm step for concentration * lorentzian w/ 0.2 nm FWHM
3. 2 nm FWHM lorentzian for concentration * lorentz w/ 0.2 nm FWHM
4. tilt concentration ( that will change the projected composition which will be convolved with the probe )
'''
x_min, x_max = -10, 10
x = np.linspace( x_min, x_max, 200 ) # distance in nm
y = x

# set probe to 1 with fwhm of 0.2 nm
probe_fwhm = 0.2
probe_max = 1

gb_fwhm = 2 # (nm)
gb_max = 1 # this is the A/B composition ratio; use 100% B for now

plot_x_min, plot_x_max = -5, 5
plot_y_min, plot_y_max = 0, 1.5

def step_function( y, fwhm, max ):
    fwqm = fwhm / 2
    function = np.piecewise( y, 
        [ ( y >= -fwqm ) & ( y <= fwqm ), ( y < -fwqm ) & ( y > fwqm ) ],
        [ max, 0 ] )
    return function

def lorentzianate( x, r ):
    lorentzian = 1 / ( x ** 2 + r ** 2 )
    reversed_lorenzian = lorentzian[::-1] # reverse it
#     maxima = np.nanmax( lorentzian ) + np.nanmin( lorentzian ) # set a maxima value
#     lorentzian_180 = np.append( np.array( [ maxima ] ), lorentzian ) # append
    lorentzian = np.insert( lorentzian, 0, reversed_lorenzian ) # prepend
    return lorentzian

def rotate_func( x, y, ang_rads ) :
    x_rotated = x * np.cos( ang_rads ) - y * np.sin( ang_rads )
    y_rotated = x * np.sin( ang_rads ) + y * np.cos( ang_rads )
    return x_rotated, y_rotated
    
# convolved step functions

probe = step_function( y, probe_fwhm, probe_max )
probe_rot_x, probe_rot_y = rotate_func( x, probe, np.deg2rad( 45 ) )
    
gb = step_function( y, gb_fwhm, gb_max )

pl.close( 'all' )
pl.figure( figsize = ( 3.5, 3.5 ) )
convolution = np.convolve( probe, gb, mode = 'same' )
convolution_norm = convolution / np.nanmax( convolution ) 
x_convolution = np.linspace( x_min, x_max, np.size( convolution ) )

pl.plot( x, probe, x, gb, x_convolution, convolution_norm, probe_rot_x, probe_rot_y )

legend_labels = [ 'probe', 'gb composition', 'convolution' ]
pl.legend( legend_labels )

pl.xlim( plot_x_min, plot_x_max )
pl.ylim( plot_y_min, plot_y_max )
pl.xlabel( 'nm' )

## one step and one lorenzian convolved
x_lor = np.linspace( 0, 10, 1e2 )
r = probe_fwhm / 2

probe_lorentzian = lorentzianate( x_lor, r )

probe_lorentzian_norm = probe_lorentzian / np.nanmax( probe_lorentzian )

pl.close( 'all' )

convolution = np.convolve( probe_lorentzian_norm, gb, mode = 'same' )
convolution_norm = convolution / np.nanmax( convolution ) 
x_convolution = np.linspace( x_min, x_max, np.size( convolution ) )

pl.plot( x, probe_lorentzian_norm, x, gb, x_convolution, convolution_norm )

pl.legend( legend_labels )

pl.xlim( plot_x_min, plot_x_max )
pl.ylim( plot_y_min, plot_y_max )
pl.xlabel( 'nm' )

## convolve two lorentzians
x_lor = np.linspace( 0, 10, 1e2 )
r_probe = probe_fwhm / 2
r_gb = gb_fwhm / 2
    
probe_lorentzian = lorentzianate( x_lor, r_probe )
probe_lorentzian_norm = probe_lorentzian / np.nanmax( probe_lorentzian )

gb_lorentzian = lorentzianate( x_lor, r_gb )
gb_lorentzian_norm = gb_lorentzian / np.nanmax( gb_lorentzian )

pl.close( 'all' )

convolution = np.convolve( probe_lorentzian_norm, gb_lorentzian_norm, mode = 'same' )
convolution_norm = convolution / np.nanmax( convolution ) 
x_convolution = np.linspace( x_min, x_max, np.size( convolution ) )

pl.plot( x, probe_lorentzian_norm, x, gb_lorentzian_norm, x_convolution, convolution_norm )

pl.legend( legend_labels )

pl.xlim( plot_x_min, plot_x_max )
pl.ylim( plot_y_min, plot_y_max )
pl.xlabel( 'nm' )

## plot2d



# rotate gb_lorentzian and integrate

ang_deg = -1
ang_rad = np.deg2rad( ang_deg )

x_lor_rot = x * np.cos( ang_rad ) - gb_lorentzian * np.sin( ang_rad )
gb_lorentzian_rot = x * np.sin( ang_rad ) + gb_lorentzian * np.cos( ang_rad )

pl.plot( x_lor_rot, gb_lorentzian_rot )












