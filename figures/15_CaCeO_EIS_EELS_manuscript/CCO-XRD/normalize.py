import numpy
def normalize( curve, max_normalized_value ) :
    data_max = numpy.nanmax( curve )
    scale_factor = max_normalized_value / data_max
    
    return curve * scale_factor