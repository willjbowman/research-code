''' ########################### IMPORT MODULES ########################### '''
import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import wills_functions as wf
import csv, imp, os

'''
GOUY-CHAPMAN [1]

Debye length, lamb
lamb = [ (epsil * kB * T) / (2 z^2 e^2 C_bulk) ]^0.5

Degree of influence
dog = [ sprt( C(x) ) - 1 ] / [ sprt( C(x) ) + 1 ]

phi(x) = 2*kB*T/(z*e)*ln[(1+dog*exp(-x/lamb))/(1-dog*exp(-x/lamb))]
'''
epsil = 1e-8 # permitivity (A^2 s^4 kg^-1 m^-3) [=C(l/A) from A-P'09 eq.7]
kB = 1.381e-23 # Boltzmann constant (J/K = kg m^2 s^-2 K^-1)
T = 273 # temperature (K)
z = 2 # charge of defect Ca_Ce^.. (no units)
e = 1.602e-19 # coulomb (A s)
C_Ca10 = 2.525e27 # concentration (m^-3)

lamb = ( (epsil * kB * T) / (2 * z**2 * e**2 * C_Ca10) )**0.5
print( lamb * 1e9 )

# degree of influence
theta_Ca = ( np.sqrt( C_Ca10 ) - 1 ) / ( np.sqrt( C_Ca10 ) + 1 )

# debye length is a distance on the order of an Angstrom (Mebane'15)
debye = np.sqrt( epsil * kB * T / ( 2 * z**2 * e**2 * C_Ca10 ) )

# 
x = np.linspace( 0, 25, 51 )

bins = np.linspace( -10, 10, 101 )
mu = 0.25
sigma = 0.5
c_Ca = wf.normal( bins, mu, sigma ) # calcuate Gaussian

# pl.close( 'all' )
pl.plot( bins, c_Ca/2 )

ratio = 8
# d_scp = 8.62E-05*T/-1*np.( ratio**(1/-2) )
print(d_scp)

'''

1. Kim, Fleig, Maier. PCCP (2003).

'''