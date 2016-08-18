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
na_bulks = [ .13 ];  % bulk dopant site fractions
node_n = 100;
r_gr = 1e-6;                             % grain radius
par_file = 'segpar_ceria3_xiaorui.txt';

% fyv = fyv * 4 % scaling dopant-vacancy association energy
% cd = cd * 1.3 % scaling gradient energy coefficient
nos = linspace( 0.5, 1.9, 8 ); % variable parameter
len_nos = length( nos );
par_name = 'no';
par_vales = nos;

paper_dir = [ 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/' ...
    '15_WJB_gb misorientation OIM EELS/' ];

save_dir = [ paper_dir 'figures/'...
    'gpdc-hilliard-cahn-simulation/gpdc_segregation_simulation/' ...
    datestr(now, 'yymmdd') '_' par_name ...
    '_na-' num2str(na_bulks(1)*100) '/' ];

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

    for i=1:length( na_bulks )
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
        fwhms(h) = fwhm*2;
        disp( strcat( '@', datestr(now,'HH:MM:SS') ) );
        disp( strcat( 'completed: na_b_i = ', num2str(na_b_i) ) );
    end

    % legend_info{g} = [ strcat( 'no = ', num2str( no_h ) ), ...
    %         '; fwhm =', num2str( fwhm*1e9*2, 3), ' nm' ];

    legend_info{g} = [ 'n = ' num2str( no_h ) ' n*, ' ...
        num2str( fwhm*1e9*2, 3) ' nm' ];

    % figure( fig_nv )
    % plot( nodes, v/(na_b_i/4), 'Linewidth', line_w )
    % ylims = [ -0.3, 4.4 ];
    % % apply_limits();
    % if limit_x % refactor to a function
    %     xlim( xlims );
    % end
    % if limit_y
    %     ylim( ylims );
    % end
    % ylabel( 'nv/nv_{bulk}' )
    % xlabel( x_label )
    % legend( legend_info )
    % hold on
    % drawnow

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

%% GET THE LINEAR FIT OF NA_MAX VS PHI_MAX (NEED FOR RELATING PHI TO MIS ANG)
P = polyfit( y_maxs, phi_maxs, 1 )

%% PLOT THE DATA PRETTY

msize = 4;
rgbs = {};

% plot the simulation
figure( 'position', [0, 0, 3, 3] * 96 ) % 1 px = 1/96 in
grey = 170;
for j=1:len_nos
    rgb = j/len_nos * [ grey, grey, grey ] / 256;
    rgbs{j} = rgb;
    plot( nodess{j}, ys{j}, 'color', rgb, 'linewidth', line_w )
    hold on
    drawnow
end

% exp high segregation: AB
exp_h_file = [ paper_dir 'figures/gpdc-gb-eels/composition-profiles/'...
    '140203_3aGPDCfib_EELSSI2_highloss_gbAB_1LO.txt' ];
% exp low segregation: FH
exp_l_file = [ paper_dir 'figures/gpdc-gb-eels/composition-profiles/'...
    '140729_gpdcFIB_EELSSI-11_gb5_1FH.txt' ];

%# read the whole file to a temporary cell array
fid = fopen(exp_h_file,'rt');
tmp = textscan(fid,'%s','Delimiter','\n');
fclose(fid);

%# remove the headerlines
tmp = tmp{1};
header_lines = 2;
header_line = 1;
while header_line < (header_lines + 1)
    tmp(1,:) = []; % delete top row
    header_line = header_line + 1;
end

% tmp = tmp{1};
% idx = cellfun(@(x) strcmp(x(1:10),'headerline'), tmp);
% tmp(idx) = [];

%# split and concatenate the rest
result = regexp(tmp,' ','split');
result = cat(1,result{:});

for row = 1:length( result )
    ch = char( result{ row } ); % convert to char
    sp = strsplit( ch, '\t' ); % split on \t
    exp_h_nm( row ) = str2double( sp( 1 ) );
    exp_h_pr( row ) = str2double( sp( 2 ) );
    exp_h_gd( row ) = str2double( sp( 3 ) );
    exp_h_ce( row ) = str2double( sp( 4 ) );
end

% flip solute profiles about gb to smooth
[ h_gd_max, h_gd_i ] = max( exp_h_gd ); % max val and max index of gd

exp_h_nm_slice = exp_h_nm( 1: 2*h_gd_i );

exp_h_gd_slice = exp_h_gd( 1: 2*h_gd_i );
exp_h_gd_flip = fliplr( exp_h_gd_slice );
exp_h_gd_ave = ( exp_h_gd_slice + exp_h_gd_flip ) / 2;

exp_h_pr_slice = exp_h_pr( 1: 2*h_gd_i );
exp_h_pr_flip = fliplr( exp_h_pr_slice );
exp_h_pr_ave = ( exp_h_pr_slice + exp_h_pr_flip ) / 2;

tri_pr_frac = .5;
exp_h_sol_ave = exp_h_gd_ave + tri_pr_frac * exp_h_pr_ave;

plot( (exp_h_nm_slice-9.4)*10^-9, exp_h_sol_ave, 'o', 'markersize', msize, ...
    'markerfacecolor', [ 128, 0, 0 ] / 256, ...
    'markeredgecolor', [ 128, 0, 0 ] / 256 )

%# read the whole file to a temporary cell array
fid = fopen(exp_l_file,'rt');
tmp = textscan(fid,'%s','Delimiter','\n');
fclose(fid);

%# remove the headerlines
tmp = tmp{1};
header_lines = 2;
header_line = 1;
while header_line < (header_lines + 1)
    tmp(1,:) = []; % delete top row
    header_line = header_line + 1;
end

% tmp = tmp{1};
% idx = cellfun(@(x) strcmp(x(1:10),'headerline'), tmp);
% tmp(idx) = [];

%# split and concatenate the rest
result = regexp(tmp,' ','split');
result = cat(1,result{:});

for row = 1:length( result )
    ch = char( result{ row } ); % convert to char
    sp = strsplit( ch, '\t' ); % split on \t
    exp_l_nm( row ) = str2double( sp( 1 ) );
    exp_l_pr( row ) = str2double( sp( 2 ) );
    exp_l_gd( row ) = str2double( sp( 3 ) );
    exp_l_ce( row ) = str2double( sp( 4 ) );
end

% flip solute profiles about gb to smooth
[ l_gd_max, l_gd_i ] = max( exp_l_gd ); % max val and max index of gd

exp_l_nm_slice = exp_l_nm( 1: 2*l_gd_i );

exp_l_gd_slice = exp_l_gd( 1: 2*l_gd_i );
exp_l_gd_flip = fliplr( exp_l_gd_slice );
exp_l_gd_ave = ( exp_l_gd_slice + exp_l_gd_flip ) / 2;

exp_l_pr_slice = exp_l_pr( 1: 2*l_gd_i );
exp_l_pr_flip = fliplr( exp_l_pr_slice );
exp_l_pr_ave = ( exp_l_pr_slice + exp_l_pr_flip ) / 2;

% tri_pr_frac = .5;
exp_l_sol_ave = exp_l_gd_ave + tri_pr_frac * exp_l_pr_ave;

plot( (exp_l_nm_slice-7)*10^-9, exp_l_sol_ave, 's', 'markersize', msize, ...
    'markerfacecolor', [ 218, 165, 32 ] / 256, ...
    'markeredgecolor', [ 218, 165, 32 ] / 256 )

%# delete temporary array (if you want)
% clear tmp

legend( legend_info )
legend( 'boxoff' )
xlim([ -1e-10, 7e-9 ])
ylim([ .1, .5 ])
ylabel( '3+ solute conc. (Mole frac.)' )
xlabel( 'Distance (m)' )
set( gca, 'XMinorTick', 'on', 'YMinorTick', 'on' )
set( findall( gcf , '-property', 'FontSize' ), 'FontSize', 10 )
set( findall( gcf , '-property', 'FontName' ), 'FontName', 'Arial' )

% create save directory if it doesn't exist
if ~exist( save_dir )
    mkdir( save_dir )
end
save_name = [ save_dir 'solute-concentration' ];
saveas( gcf, save_name, 'svg' )
saveas( gcf, save_name, 'png' )

% PHI VS. DISTANCE

% plot the simulation
figure( 'position', [4, 0, 3, 3] * 96) % 1 px = 1/96 in
grey = 170;
for j=1:len_nos
    % rgb = j / len_nos * [ grey, grey, grey ] / 256;
    nodes = nodess{j};
    plot( nodes(1:length(nodes)-1), phis{j}, 'color', rgbs{j}, ...
        'linewidth', line_w )
    hold on
    drawnow
end

xlim([ -1e-10, 5.1e-9 ])
ylim([ -.2, 1.6 ])
ylabel( 'Space charge pot. (V)' )
xlabel( 'Distance (m)' )
set(gca,'XMinorTick','on','YMinorTick','on')
set( findall( gcf , '-property', 'FontSize' ), 'FontSize', 10 )
set( findall( gcf , '-property', 'FontName' ), 'FontName', 'Arial' )


% create smaller axes in top right, and plot on it
% ax1 = axes( 'Position', [ .42 .45 .45 .45 ] ) % [L B W H]
ax1 = axes( 'Position', [ .4 .4 .45 .35 ] ) % [L B W H]
box on
for phi_i = 1:length( phi_maxs )
    plot( nos( phi_i ), phi_maxs( phi_i ), 'o', 'markersize', msize, ...
    'markerfacecolor', rgbs{ phi_i }, 'markeredgecolor', rgbs{ phi_i } )
    hold on
    drawnow
end
xlabel( 'n/n*' )
ylabel( 'Sp. chg. pot. (V)' )
set(gca,'XMinorTick','on','YMinorTick','on')

ax1_pos = ax1.Position;
ax2 = axes( 'position', ax1_pos, 'XAxisLocation', 'top', 'Color', 'none' );
% plot( y_maxs*na_b_i, phi_maxs, 'o', 'markersize', 0 )
line( y_maxs*na_b_i, phi_maxs, 'Parent', ax2, 'Color', 'none' )
xlabel( '[3+ solute]_{GB} (Mole frac.)' )
set( findall( gcf , '-property', 'FontSize' ), 'FontSize', 10 )
set( findall( gcf , '-property', 'FontName' ), 'FontName', 'Arial' )

% save
save_name = [ save_dir 'space-charge' ];
saveas( gcf, save_name, 'svg' )
saveas( gcf, save_name, 'png' )

% saveas( gcf, sprintf([ ...
%     save_dir par_name '_' num2str(h) '_' num2str(par_val) '.png' ...
% ]) )