function [ diff_squared, ind ] = least_square( varargin )
    y = varargin{1}; % array 1D
    y_hmax = ( max(y) + min(y) ) / 2
    [ diff_squared, ind ] = min( (y - y_hmax).^2 )
end