% this script uses the updated function from Xiaorui to model divalent dopant
% profiles.

T = 440+273;                             % temperature
% na_bulks = [ 1e-3, .01, .1, .2 ];  % bulk dopant site fractions
na_bulks = [ .02, .05, .1 ];  % bulk dopant site fractions
node_n = 400;
r_gr = 1e-6;                             % grain radius
par_file = 'segpar_ceria3_xiaorui.txt';

ys = {};
vs = {};
phis = {};
lamvs = [];
lambds = [];
nodess = {};
flags = [];
fwhms = flags;

for i=1:length( na_bulks )
    na_b_i = na_bulks(i);
    disp( strcat( '@', datestr(now,'HH:MM:SS') ) );
    disp( strcat( 'tyring: na_b_i = ', num2str(na_b_i) ) );
    [y,v,phi,lamv,lambd,nodes,flag] = ...
        segregation_ceria_afe_chem_v1_2_divalent_cco( ...
            T, na_b_i, node_n, r_gr, par_file ...
        );
    ys{i} = y; % dopant site fraction
    vs{i} = v; % vacancy site fraction
    phis{i} = phi;
    lamvs(i) = lamv;
    lambds(i) = lambd;
    nodess{i} = nodes;
    flags(i) = flag;
    [ fwhm_ds, fwhm_ind ] = least_squares( y );
    fwhm_i = nodes( fwhm_ind );
    fwhms( i ) = fwhm_i;
    disp( strcat( '@', datestr(now,'HH:MM:SS') ) );
    disp( strcat( 'completed: na_b_i = ', num2str(na_b_i) ) );
end

%%
% close all
xlims = [ -.05e-8, 1.05e-8 ];
line_w = 1.5;
x_label = 'Distance from interface (m)';

figure()

subplot( 3, 1, 1 )
for i=1:length( na_bulks )
    plot( nodess{i}, vs{i}/(na_bulks(i)/2), 'Linewidth', line_w ) % v_bulk is half na_bulk for divalent
    hold on;
    legend_info{i} = [ strcat( ...
         'na=', num2str( na_bulks(i) ), ...
         '; fwhm=', num2str( fwhms(i)*1e9*2, 2 ), ' nm' ...
    ) ];
end
title( 'Segregation Simulation Divalent' )

ylabel( 'nv/nv_{bulk}' )
xlabel( x_label )
ylims = [ -0.3, 4.4 ];
ylim( ylims );
xlim( xlims );
legend( legend_info )

subplot( 3, 1, 2 )
for i=1:length( na_bulks )
    plot( nodess{i}, ys{i}/na_bulks(i), 'Linewidth', line_w )
    hold on;
end
ylabel( 'na/na_{bulk}' )
xlabel( x_label )
% xlims = [ 0, 1e-8 ];
ylims = [ 0, 10 ];
ylim( ylims );
xlim( xlims );

subplot( 3, 1, 3 )
for i=1:length( na_bulks )
    % plot( nodess{i}(1:length(nodess{i})-1), phis{i} )
    plot( nodess{i}, phis{i}, 'Linewidth', line_w )
    hold on;
end
ylabel( 'phi (V)' )
xlabel( x_label )
ylims = [ -0.1, 1.1 ];
ylim( ylims );
xlim( xlims );