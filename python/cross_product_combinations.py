import numpy as np

a = [0,0,2]
b = [2,2,4]

aas = []
bbs = []

for i in range( 0, len( a ) ):
    if i == 0:
        aas.append( [ a[i], a[1], a[2] ] )
        aas.append( [ a[i], a[2], a[1] ] )
    elif i == 1:
        aas.append( [ a[i], a[0], a[2] ] )
        aas.append( [ a[i], a[2], a[0] ] )
    elif i == 2:
        aas.append( [ a[i], a[0], a[1] ] )
        aas.append( [ a[i], a[1], a[0] ] )

for i in range( 0, len( b ) ):
    if i == 0:
        bbs.append( [ b[i], b[1], b[2] ] )
        bbs.append( [ b[i], b[2], b[1] ] )
    elif i == 1:
        bbs.append( [ b[i], b[0], b[2] ] )
        bbs.append( [ b[i], b[2], b[0] ] )
    elif i == 2:
        bbs.append( [ b[i], b[0], b[1] ] )
        bbs.append( [ b[i], b[1], b[0] ] )

print( aas )
print( bbs )

crosses = []

for i, aa in enumerate( aas ):
    for i, bb in enumerate( bbs ):
        aaxbb = np.cross( aa, bb )
        print( aa, bb, aaxbb )
        crosses.append( aaxbb )

# print( crosses )