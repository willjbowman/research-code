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

T = 800+273; % temperature; reduces na_max, fwhm
na_bulks = [ .13 ];  % bulk dopant site fractions
node_n = 100;
r_gr = 1e-6;                             % grain radius
par_file = 'segpar_ceria3_xiaorui.txt';

% fyv = fyv * 4 % scaling dopant-vacancy association energy
% cd = cd * 1.3 % scaling gradient energy coefficient
% nos = linspace( 0.1, 1.9, 10 ); % variable parameter (in dissertation)
nos = linspace( .3, 1, 8 ); % variable parameter
len_nos = length( nos );
par_name = 'no';
par_vales = nos;

paper_dir = [ 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/' ...
    '15_WJB_gb misorientation OIM EELS/' ];

save_dir = [ paper_dir 'figures/gpdc-poisson-cahn-simulation/' ...
    'conductivity-vs-length_fraction/' ...
    datestr(now, 'yymmdd') '_' datestr(now, 'hhMM') '_' par_name ...
    '_na-' num2str(na_bulks(1)*100) '/' ];

ys = cell( len_nos, 1 );
vs = ys;
phis = ys;
lamvs = zeros( len_nos, 1 );
lambds = lamvs;
nodess = ys;
flags = lamvs;
y_maxs = lamvs; % gb solute concentration
phi_maxs = lamvs;
fwhms = flags;
v_mins = lamvs; % minimum vacancy concentration at gb


saving = 1;
saving = 0;

close all

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
        % v_mins(h) = min(v) / na_b_i / 4; % O vacancy site frac. for 3+ solute
        v_mins(h) = min(v); % O vacancy site frac. for 3+ solute
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

    legend_info{g} = [ 'S = ' num2str( no_h ) ' ; ' ...
        num2str( fwhm*1e9*2, 3) ' nm' ];

    figure( fig_nv )
    plot( nodes, v/(na_b_i/4), 'Linewidth', line_w )
    xlims = [ 0, 5e-9 ];
    ylims = [ -.1, 4 ];
    xlim( xlims );
    ylim( ylims );
    ylabel( 'nv/nv_{bulk}' )
    xlabel( x_label )
    legend( legend_info )
    hold on
    drawnow

    figure( fig_nd )
    plot( gca, nodes, y/na_b_i, 'Linewidth', line_w )
    % ylims = [ 0, 2.5 ];
    xlim( xlims );
    % ylim( ylims );
    ylabel( 'na/na_{bulk}' )
    xlabel( x_label )
    % legend( legend_info_y )
    legend( legend_info )
    hold on
    drawnow

    figure( fig_phi )
    plot( gca, nodes(1:length(nodes)-1), phi, 'Linewidth', line_w )
    ylims = [ -0.1, 1.1 ];
    xlim( xlims );
    % ylim( ylims );
    ylabel( 'phi (V)' )
    xlabel( x_label )
    legend( legend_info )
    hold on
    drawnow

    g = g + 1;
end

% GET THE LINEAR FIT OF NA_MAX VS PHI_MAX (NEED FOR RELATING PHI TO MIS ANG)
P_phi_vs_na_gb = polyfit( y_maxs*na_b_i, phi_maxs, 3 )

% save
if saving
    [ 'saving now: ' 'fig_nv' ]
    % save_fig( save_dir, save_name, file_types ) % I want this method!!!!
    if ~exist( save_dir ) % create save directory if it doesn't exist
        mkdir( save_dir )
    end
    save_name = [ save_dir 'fig_nv' ];
    saveas( fig_nv, save_name, 'svg' )
    saveas( fig_nv, save_name, 'png' )
    
    [ 'saving now: ' 'fig_nd' ]
    % save_fig( save_dir, save_name, file_types ) % I want this method!!!!
    if ~exist( save_dir ) % create save directory if it doesn't exist
        mkdir( save_dir )
    end
    save_name = [ save_dir 'fig_nd' ];
    saveas( fig_nd, save_name, 'svg' )
    saveas( fig_nd, save_name, 'png' )

    [ 'saving now: ' 'fig_phi' ]
    % save_fig( save_dir, save_name, file_types ) % I want this method!!!!
    if ~exist( save_dir ) % create save directory if it doesn't exist
        mkdir( save_dir )
    end
    save_name = [ save_dir 'fig_phi' ];
    saveas( fig_phi, save_name, 'svg' )
    saveas( fig_phi, save_name, 'png' )
end



%% PLOT THE DATA PRETTY

fig_names = { 'Solute-concentration-sup', 'Solute-concentration-main', ...
    'Space-charge-sup', 'Vacancy-concentration-sup', ...
    'Vacancy-concentration-main', 'Ea_conductivitiy-ratio' };

c_maroon = [ 128, 0, 0 ] / 256;
c_gold = [ 218, 165, 32 ] / 256;

solute_label = '[A^{3+}]_{GB} (Mole frac.)';

msize = 4;
rgbs = {};

fig_idx = 1;
% plot the simulation
fig_name_1 = fig_names{ fig_idx };
if ~isempty(findall(0,'Type','Figure','Name',fig_name_1 ));
    close( fig_name_1 ); % close previous version of fig if it exists
end
figure( 'position', [0, 0, 3, 3]*96, 'name', fig_name_1 ) % 1 px = 1/96 in

% create the grey scale rgbs
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
    'markerfacecolor', c_maroon, ...
    'markeredgecolor', c_maroon )

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
    'markerfacecolor', c_gold, ...
    'markeredgecolor', c_gold )


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
if saving
    [ 'saving now: ' fig_name_1 ]
    if ~exist( save_dir )
        mkdir( save_dir )
    end
    save_name = [ save_dir fig_name_1 ];
    saveas( gcf, save_name, 'svg' )
    saveas( gcf, save_name, 'png' )
end


% [3+ SOLUTE] VS. DISTANCE - main text
fig_idx = fig_idx + 1;
fig_name = fig_names{ fig_idx };
if ~isempty(findall(0,'Type','Figure','Name', fig_name ));
    close( fig_name ); % close previous version of fig if it exists
end
figure( 'position', [0, 0, 3, 3]*96, 'name', fig_name ) % 1 px = 1/96 in

plot( (exp_h_nm_slice-9.4)*10^-9, exp_h_sol_ave, 'o', 'markersize', msize, ...
    'markerfacecolor', c_maroon, ...
    'markeredgecolor', c_maroon )
hold on
plot( nodess{6}, ys{6}, 'color', c_maroon, 'linewidth', line_w )

plot( (exp_l_nm_slice-7)*10^-9, exp_l_sol_ave, 's', 'markersize', msize, ...
    'markerfacecolor', c_gold, ...
    'markeredgecolor', c_gold )
plot( nodess{2}, ys{2}, 'color', c_gold, 'linewidth', line_w )

legend({ 'High-angle GB EELS', 'Simulation', 'Low-angle GB EELS', 'Simulation' })
legend( 'boxoff' )
xlim([ -1e-10, 7e-9 ])
ylim([ .1, .5 ])
ylabel( '3+ solute conc. (Mole frac.)' )
xlabel( 'Distance (m)' )
set( gca, 'XMinorTick', 'on', 'YMinorTick', 'on' )
set( findall( gcf , '-property', 'FontSize' ), 'FontSize', 10 )
set( findall( gcf , '-property', 'FontName' ), 'FontName', 'Arial' )

% create save directory if it doesn't exist
if saving
    [ 'saving now: ' fig_name ]
    if ~exist( save_dir )
        mkdir( save_dir )
    end
    save_name = [ save_dir fig_name ];
    saveas( gcf, save_name, 'svg' )
    saveas( gcf, save_name, 'png' )
end


% PHI VS. DISTANCE
fig_idx = fig_idx+1;
% plot the simulation
fig_name_2 = fig_names{ fig_idx };
if ~isempty(findall(0,'Type','Figure','Name',fig_name_2 ));
    close( fig_name_2 ); % close previous version of fig if it exists
end
figure( 'position', [4, 0, 3, 3]*96, 'name', fig_name_2 ) % 1 px = 1/96 in
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
% ylim([ -.1, 1.3 ])
ylabel( 'Space charge pot. (V)' )
xlabel( 'Distance (m)' )
set(gca,'XMinorTick','on','YMinorTick','on')
set( findall( gcf , '-property', 'FontSize' ), 'FontSize', 10 )
set( findall( gcf , '-property', 'FontName' ), 'FontName', 'Arial' )


% create smaller axes in top right, and plot on it
% ax1 = axes( 'Position', [ .4 .4 .45 .35 ] ) % [L B W H] w/ n/n*
ax1 = axes( 'Position', [ .4 .53 .45 .35 ] ); % [L B W H] w/ n/n*
box on
for phi_i = 1:length( phi_maxs )
    % plot( nos( phi_i ), phi_maxs( phi_i ), 'o', 'markersize', msize, ...
    plot( y_maxs(phi_i)*na_b_i, phi_maxs(phi_i), 'o', 'markersize', msize, ...
    'markerfacecolor', rgbs{ phi_i }, 'markeredgecolor', rgbs{ phi_i } )
    hold on
    drawnow
end
% xlabel( 'n/n*' )
ylabel( 'Sp. chg. pot. (V)' )
xlim([ .1, .5 ])
% ylim([ .1, 1.2 ])
set( gca, 'XMinorTick', 'on', 'YMinorTick', 'on', 'TickLength', [.02,.02] )

% ax1_pos = ax1.Position;
% ax2 = axes( 'position', ax1_pos, 'XAxisLocation', 'top', 'Color', 'none' );
% line( y_maxs*na_b_i, phi_maxs, 'Parent', ax2, 'Color', 'none' )
xlabel( solute_label )
set( findall( gcf , '-property', 'FontSize' ), 'FontSize', 10 )
set( findall( gcf , '-property', 'FontName' ), 'FontName', 'Arial' )

% save
if saving
    [ 'saving now: ' fig_name_2 ]
    % save_fig( save_dir, save_name, file_types ) % I want this method!!!!
    if ~exist( save_dir ) % create save directory if it doesn't exist
        mkdir( save_dir )
    end
    save_name = [ save_dir fig_name_2 ];
    saveas( gcf, save_name, 'svg' )
    saveas( gcf, save_name, 'png' )
end




% vacancy concentration VS. distance
fig_idx = fig_idx+1;
% % plot the simulation
fig_name_3 = fig_names{ fig_idx };
if ~isempty(findall(0,'Type','Figure','Name',fig_name_3));
    close( fig_name_3 ); % close previous version of fig if it exists
end
figure( 'position', [8, 0, 3, 3]*96, 'name', fig_name_3 ) % 1 px = 1/96 in
grey = 170;
for j=1:len_nos
    % rgb = j / len_nos * [ grey, grey, grey ] / 256;
    nodes = nodess{j};
    % plot( nodes(1:length(nodes)-1), vs{j}, 'color', rgbs{j}, ...
    plot( nodes, vs{j}, 'color', rgbs{j}, ...
        'linewidth', line_w )
    hold on
    drawnow
end

xlim([ -1e-10, 5.1e-9 ])
ylim([ -.0, .25 ])
ylabel( 'O vacancy concentration (Mole frac.)' )
xlabel( 'Distance (m)' )
set( gca,'XMinorTick','on','YMinorTick','on' )
set( findall( gcf , '-property', 'FontSize' ), 'FontSize', 10 )
set( findall( gcf , '-property', 'FontName' ), 'FontName', 'Arial' )


% create smaller axes in top right, and plot on it
ax1 = axes( 'Position', [ .4 .53 .45 .35 ] ); % [L B W H]
box on
for v_min_i = 1:length( v_mins )
    plot( y_maxs(v_min_i)*na_b_i, v_mins(v_min_i), 'o', 'markersize', msize, ...
    'markerfacecolor', rgbs{ v_min_i }, 'markeredgecolor', rgbs{ v_min_i } )
    hold on
    drawnow
end
xlabel( solute_label )
ylabel( '[O vac.]^{min.}' )
xlim([ .1, .5 ])
% ylim([ .01, .03 ])
set( gca, 'XMinorTick', 'on', 'YMinorTick', 'on', 'TickLength', [.02,.02] )

% ax1_pos = ax1.Position;
% ax2 = axes( 'position', ax1_pos, 'XAxisLocation', 'top', 'Color', 'none' );
% plot( y_maxs*na_b_i, v_mins, '-o', 'markersize', 0 )
% line( y_maxs*na_b_i, phi_maxs, 'Parent', ax2, 'Color', 'none' )
% xlabel( '[3+ solute]_{GB} (Mole frac.)' )
set( findall( gcf , '-property', 'FontSize' ), 'FontSize', 10 )
set( findall( gcf , '-property', 'FontName' ), 'FontName', 'Arial' )

% save
if saving
    [ 'saving now: ' fig_name_3 ]
    % save_fig( save_dir, save_name, file_types ) % I want this method!!!!
    if ~exist( save_dir )
        mkdir( save_dir )
    end
    save_name = [ save_dir fig_name_3 ];
    saveas( gcf, save_name, 'svg' )
    saveas( gcf, save_name, 'png' )
end




% vacancy concentration VS. distance - main text
fig_idx = fig_idx+1;
% % plot the simulation
fig_name = fig_names{ fig_idx };
if ~isempty(findall(0,'Type','Figure','Name',fig_name));
    close( fig_name ); % close previous version of fig if it exists
end
figure( 'position', [8, 0, 3, 3]*96, 'name', fig_name ) % 1 px = 1/96 in
plot( nodess{6}, vs{6}, 'color', c_maroon, 'linewidth', line_w )
hold on
plot( nodess{2}, vs{2}, 'color', c_gold, 'linewidth', line_w )

% legend({ 'High-ang. GB Simulation','Low-ang. GB Simulation' })
legend( char({'High-angle', 'GB Simulation'}), ...
    char({'Low-angle', 'GB Simulation'}) )
legend( 'boxoff' )
xlim([ -1e-10, 5.1e-9 ])
ylim([ 0, .10 ])
ylabel( 'O vacancy concentration (Mole frac.)' )
xlabel( 'Distance (m)' )
set( gca,'XMinorTick','on','YMinorTick','on' )
set( findall( gcf , '-property', 'FontSize' ), 'FontSize', 10 )
set( findall( gcf , '-property', 'FontName' ), 'FontName', 'Arial' )



% save
if saving
    [ 'saving now: ' fig_name ]
    % save_fig( save_dir, save_name, file_types ) % I want this method!!!!
    if ~exist( save_dir )
        mkdir( save_dir )
    end
    save_name = [ save_dir fig_name ];
    saveas( gcf, save_name, 'svg' )
    saveas( gcf, save_name, 'png' )
end




%%
% Ea vs. na
fig_idx = fig_idx+1;
kb = 8.612e-5; % eV/K
T = 800 + 273; % K
Ea_gr_PGCO = 0.78; % eV

na = y_maxs * na_b_i;
nv_gr = na_b_i / 2 / 2;
% make array (size na) with Ea
% Ea_n = -10*na.^3 + 7.7143*na.^2 + 0.1714*na + 0.634; % est from grain; wrong
Ea_n = -109.66*na.^3 + 143.55*na.^2 - 59.666*na + 8.8666; % Ea_GB Gd-only
Ea_n = -47.831*na.^3 + 64.583*na.^2 - 28.225*na + 5.0159; % Ea_GB all
Ea_n = 2e-4 * na .^ -5 + .92; % Ea_GB all ax^r+c


nv_gbs = v_mins;

% compute Sig_grain assuming .13 3+ solutes and Ea_grain from PGCO
S_gr = nv_gr * exp( -Ea_gr_PGCO/(kb*T) );
S_gb = nv_gbs .* exp( -Ea_n/(kb*T) );
S_gb_gr = S_gb / S_gr;

% plot the simulation
fig_name = fig_names{ fig_idx };
if ~isempty(findall(0,'Type','Figure','Name',fig_name));
    close( fig_name ); % close previous version of fig if it exists
end
figure( 'name', fig_name, 'position', [8, 4, 3, 3]*96) % 1 px = 1/96 in
left_color = [0 0 0];
right_color = left_color;
set(gcf,'defaultAxesColorOrder',[left_color; right_color]);

yyaxis left
plot( na, Ea_n, '--k' ) % eyeguide for Ea

yyaxis right
% semilogy( na, S_gb_gr, '--r' ) % eyeguide
% polynomial fitting log( conductivity ratio ) vs [A3+]
polyfit_log10_S_gb_gr = polyfit( na, log10(S_gb_gr), 3 ) % print to console
log10_S_gb_gr_polyfit = polyval( polyfit_log10_S_gb_gr, na );
semilogy( na, 10.^log10_S_gb_gr_polyfit, '-k' ) % underlay polyfit
hold on
drawnow

legend( {'E_a^{GB}, eye guide', '\sigma_{GB}/\sigma_{Grain}, fit'}, ...
    'Position', [.33 .77 .5 .1] ); % [left bottom width height] relat to fig
legend boxoff

grey = 170;
for j=1:length(na)
    yyaxis left
    plot( na(j), Ea_n(j), 'o', 'markersize', msize, ...
    'markerfacecolor', rgbs{j}, 'markeredgecolor', rgbs{j} )
    yyaxis right
    semilogy( na(j), S_gb_gr(j), 's', 'markersize', msize, ...
    'markerfacecolor', rgbs{j}, 'markeredgecolor', rgbs{j} )
    hold on
    drawnow
end

yyaxis left
xlim([ .1, .5 ])
% ylim([ .6, 1.7 ])
ylabel( 'E_a^{GB} (eV)' )
xlabel( solute_label )
set( gca,'XMinorTick','on','YMinorTick','on' )

yyaxis right
xlim([ .1, .5 ])
ylim([ 1e-8, 1e-1 ])
ylabel( '\sigma_{GB}/\sigma_{Grain}' )
set( gca,'XMinorTick','on','YMinorTick','on' )

set( findall( gcf , '-property', 'FontSize' ), 'FontSize', 10 )
set( findall( gcf , '-property', 'FontName' ), 'FontName', 'Arial' )

% save
if saving
    [ 'saving now: ' fig_name ]
    % save_fig( save_dir, save_name, file_types ) % I want this method!!!!
    if ~exist( save_dir )
        mkdir( save_dir )
    end
    save_name = [ save_dir fig_name ];
    saveas( gcf, save_name, 'svg' )
    saveas( gcf, save_name, 'png' )
end