% This script loops through interface site-density, executing Mebane code on
% each iteration.

xlims = [ -.05e-8, 1.05e-8 ];
limit_x = false;
limit_x = true;
limit_y = false;
% limit_y = true;
fig_w = 420; % pixels
fig_h = fig_w;
line_w = 1.5;
x_label = 'Distance from interface (m)';
legend_info = {}; % cell array for legend entries

T = 800+273; % temperature; inversely prop to na_max, fwhm
na_bulks = [ .15 ];  % bulk dopant site fractions
node_n = 100;
r_gr = 1e-6;                             % grain radius
par_file = 'segpar_ceria3_xiaorui.txt';

% fyv = fyv * 4 % scaling dopant-vacancy association energy
% cd = cd * 1.3 % scaling gradient energy coefficient
nos = linspace( 0.5, 1.9, 8 ); % variable parameter
len_nos = length( nos );
par_name = 'no';
par_vales = nos;

save_dir = [ 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/' ...
    '15_WJB_gb misorientation OIM EELS/figures/'...
    'gpdc-hilliard-cahn-simulation/gpdc_segregation_simulation/' ...
    par_name '_' datestr(now, 'YYMMDD') '-' datestr(now, 'HHMM') '/' ];
if ~exist( save_dir )
    mkdir( save_dir )
end

ys = cell( len_nos, 1 );
vs = ys;
phis = ys;
lamvs = zeros( len_nos, 1 );
lambds = lamvs;
nodess = ys;
flags = lamvs;
y_maxs = lamvs;
phi_maxs = lamvs;
fwhms = flags;

% close all
fig_nv = figure( 'position', [0, 0, fig_w, fig_h] ); % [ bot_l, bot_r, w, h ]
fig_nd = figure( 'position', [fig_w, 0, fig_w, fig_h] );
fig_phi = figure( 'position', [2*fig_w, 0, fig_w, fig_h] );

g = 1;
for h = 1:len_nos
    no_h = nos(h);

    % for i=1:length( na_bulks )
        na_b_i = na_bulks(i);
        disp( strcat( '@', datestr(now,'HH:MM:SS') ) );
        disp( strcat( 'tyring: na_b_i = ', num2str(na_b_i) ) );
        [y,v,phi,lamv,lambd,nodes,flag] = ...
            segregation_ceria_afe_chem_v1_1_trivalent_gpdc( ...
                T, na_b_i, node_n, r_gr, par_file, no_h ...
            );
        ys{h} = y; % dopant site fraction
        vs{h} = v; % vacancy site fraction
        phis{h} = phi;
        lamv(h) = lamv;
        lambd(h) = lambd;
        nodess{h} = nodes;
        flag(h) = flag;
        y_maxs(h) = max(y) / na_b_i;
        phi_maxs(h) = max(phi);
        [ fwhm_ds, fwhm_ind ] = least_squares( y );
        fwhm = nodes( fwhm_ind );
        fwhms(h) = fwhm;
        disp( strcat( '@', datestr(now,'HH:MM:SS') ) );
        disp( strcat( 'completed: na_b_i = ', num2str(na_b_i) ) );
    % end

    legend_info{g} = [ strcat( 'no = ', num2str( no_h ) ), ...
            '; fwhm =', num2str( fwhm*1e9*2, 3), ' nm' ... % profile fwhm*2 ];
        ];

    figure( fig_nv )
    plot( nodes, v/(na_b_i/4), 'Linewidth', line_w )
    ylims = [ -0.3, 4.4 ];
    % apply_limits();
    if limit_x % refactor to a function
        xlim( xlims );
    end
    if limit_y
        ylim( ylims );
    end
    ylabel( 'nv/nv_{bulk}' )
    xlabel( x_label )
    legend( legend_info )
    hold on
    drawnow

    figure( fig_nd )
    plot( gca, nodes, y/na_b_i, 'Linewidth', line_w )
    ylims = [ 0, 22 ];
    if limit_x
        xlim( xlims );
    end
    if limit_y
        ylim( ylims );
    end
    ylabel( 'na/na_{bulk}' )
    xlabel( x_label )
    % legend( legend_info_y )
    legend( legend_info )
    hold on
    drawnow

    figure( fig_phi )
    plot( gca, nodes(1:length(nodes)-1), phi, 'Linewidth', line_w )
    ylims = [ -0.1, 1.1 ];
    if limit_x
        xlim( xlims );
    end
    if limit_y
        ylim( ylims );
    end
    ylabel( 'phi (V)' )
    xlabel( x_label )
    legend( legend_info )
    hold on
    drawnow

    g = g + 1;
end

% saveas( gcf, sprintf([ ...
%     save_dir par_name '_' num2str(h) '_' num2str(par_val) '.png' ...
% ]) )