% parametric test to determine cv and cd values which reproduce the 
% correct FWHM of experimental profiles (~2-3nm)
% pseudo: solve profiles for each element 2d array [cv by cd ]
% determine FWHM for each profile
% identify cvs that provide proper FWHM for all cds
% compare na/na_bulks for different cds for these proper cvs to exp profiles
% use best fits to estimate phi for exp
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

T = 500+273;                             % temperature
% Ts = [ 440, ] + 273;                             % temperature
% fys = [ 1e3, 5e3, 1e4, 5e4, 1e5, 5e5, 1e6 ]; % =1e4 [published]
% fyvs = -[ 1e3, 5e3, 1e4, 5e4, 1e5, 5e5, 1e6 ]; % =-7e3 [published]
cvs = [ 5e-11, 1e-10, 5e-10, 1e-9, 5e-9, 1e-8, 5e-8 ]; % = 1e-9 [published]
cvs = [ 5e-10, 1e-9, 5e-9 ]; % = 1e-9 [published]
cds = [ 5e-10, 1e-9, 5e-9, 1e-8, 5e-8, 1e-7, 5e-7 ]; % = 1e-8 [published]
cds = [ 5e-9, 1e-8, 5e-8 ]; % = 1e-8 [published]
par_name = 'cv-cd';
par_vals = 1;
par_vals = cds;
save_dir = [ 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/' ...
    '15_WJB_gb misorientation OIM EELS/figures/'...
    'gpdc-cahn-hilliard-simulation/simulations/' ...
    par_name '_' datestr(now, 'YYMMDD') '-' datestr(now, 'HHMM') '/' ];
if ~exist( save_dir )
    mkdir( save_dir )
end

na_bulks = [ .15 ];  % bulk dopant site fractions (assume all Pr is 3+)
% na_bulks = [ 1e-3, .01, .1, .2 ];  % bulk dopant site fractions
node_n = 100;
r_gr = 5e-7;            % grain radius = .5 um
% par_file = 'segpar_ceria2_wb.txt';
par_file = 'segpar_ceria3_wb.txt'; % from David's student Xiaorui
par = importdata(par_file,' ',2); 

len_cvs = length( cvs );
len_cds = length( cds );
ys = cell( len_cvs, len_cds );
vs = ys;
phis = ys;
lamvs = zeros( len_cvs, len_cds );
lambds = lamvs;
nodess = ys;
flags = lamvs;
maxs = lamvs; % maxima of na/na_bulk profiles
fwhms = lamvs; % fwhm of na/na_bulk profiles

close all
fig_nv = figure( 'position', [0, 0, fig_w, fig_h] ); % [ bot_l, bot_r, w, h ]
fig_nd = figure( 'position', [fig_w, 0, fig_w, fig_h] );
fig_phi = figure( 'position', [2*fig_w, 0, fig_w, fig_h] );

f = 1;
for g = 1:len_cvs % loop on cvs
    cv_g = cvs(g);

    for h = 1:len_cds % loop on cds
        cd_h = cds(h);

        % for i=1:length( na_bulks )
            na_b_i = na_bulks(1);
            disp( strcat( {'@ '}, datestr(now,'HH:MM:SS') ) );
            disp( strcat( {'tyring: na_b_i = '}, num2str(na_b_i) ) );
            disp( strcat( {'cv = '}, num2str(cv_g) ) );
            disp( strcat( {'cd = '}, num2str(cd_h) ) );
            [ y, v, phi, lamv, lambd, nodes, flag ] = ...
                segregation_ceria_afe_chem_3_cvs_cds( ...
                    T, na_b_i, node_n, r_gr, par_file, cv_g, cd_h ...
                );
            ys{g,h} = y; % dopant site fraction
            vs{g,h} = v; % vacancy site fraction
            phis{g,h} = phi;
            lamvs(g,h) = lamv;
            lambds(g,h) = lambd;
            nodess{g,h} = nodes;
            flags(g,h) = flag;
            maxs(g,h) = max( y ) / na_b_i;
            [ fwhm_ds, fwhm_ind ] = least_squares( y );
            fwhm_i = nodes( fwhm_ind );
            fwhms(g,h) = fwhm_i;
            disp( strcat( {'completed @ '}, datestr(now,'HH:MM:SS') ) );
            disp( strcat( {'cv = '}, num2str(cv_g) ) );
            disp( strcat( {'cd = '}, num2str(cd_h) ) );
        % end

        no = par.data(1);       % surface site density for vacancies, mol/m^2 (NvGB)
        fv = par.data(2);       % vacancy self-interaction, J/mol
        fo = par.data(3);       % vacancy segregation energy, J/mol
        fy = par.data(4);       % dopant self-interaction, J/mol
        fyv = par.data(5);      % dopant-vacancy interaction, J/mol
        cv = par.data(6);       % vacancy gradient energy coefficient, J/mol-m
        cv = cv_g; % parametric study
        cd = par.data(7);       % dopant gradient energy coefficient, J/mol-m
        cd = cd_h; % parametric study
        epsr = par.data(8);     % relative permittivity
        latpar = par.data(9);   % lattice parameter, m

        legend_info{ f } = ...
            [ strcat( 'cv = ', num2str( cv ), '; cd = ', num2str( cd ) ) ];

        legend_info_y{ f } = [ strcat( ...
            'cv =', num2str( cv ), '; cd =', num2str( cd ), ...
            '; fwhm =', num2str( fwhm_i * 1e9, 2 ), ' nm' ...
        ) ];

        % red = f;
        % gre = 0;
        % blu = ( len_cvs * len_cds ) - f;
        % color = [ red gre blu ] / ( len_cvs * len_cds );
        red = g / len_cvs;
        gre = 0;
        blu = 1 - red;
        alp = 1 - h / ( 1.5 * len_cds );
        color = [ red gre blu, alp ];

        figure( fig_nv ) % make figure current
        plot( nodes, v/(na_b_i/4), 'Linewidth', line_w, 'color', color )
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
        plot( gca, nodes, y/na_b_i, 'Linewidth', line_w, 'color', color )
        ylims = [ 0, 22 ];
        if limit_x
            xlim( xlims );
        end
        if limit_y
            ylim( ylims );
        end
        ylabel( 'na/na_{bulk}' )
        xlabel( x_label )
        legend( legend_info_y )
        hold on
        drawnow

        figure( fig_phi )
        plot( gca, nodes(1:length(nodes)-1), phi, 'Linewidth', line_w, ...
            'color', color )
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

        f = f + 1;
    end
end

% saveas( gcf, sprintf([ ...
%     save_dir par_name '_' num2str(h) '_' num2str(par_val) '.png' ...
% ]) )