import numpy as np
import pylab as pl

file_path = "C:/Crozier_Lab/Writing/2015_PCO10 interband states/Dholobhai et al ceria PDOS_addPr.txt"
data = np.loadtxt( file_path, skiprows = 1 )

# A = data[ :, 1 ]


for col in np.arange( np.size( data, axis = 1 ) ):
    if col > 0:
        A = data[ :, col ]
        ok = -np.isnan(A)
        xp = ok.ravel().nonzero()[0]
        fp = A[-np.isnan(A)]
        x  = np.isnan(A).ravel().nonzero()[0]
        
        A[np.isnan(A)] = np.interp(x, xp, fp)
        
        pl.plot( data[ :, 0 ], A, marker = 'o' )


'''
interpolation:
http://stackoverflow.com/questions/6518811/interpolate-nan-values-in-a-numpy-array
'''