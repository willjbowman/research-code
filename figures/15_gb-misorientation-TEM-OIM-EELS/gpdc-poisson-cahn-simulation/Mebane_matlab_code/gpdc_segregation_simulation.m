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

T = 500+273;                             % temperature
% Ts = [ 440, ] + 273;                             % temperature
% fys = [ 1e3, 5e3, 1e4, 5e4, 1e5, 5e5, 1e6 ]; % =1e4 [published]
% fyvs = -[ 1e3, 5e3, 1e4, 5e4, 1e5, 5e5, 1e6 ]; % =-7e3 [published]
cvs = [ 5e-11, 1e-10, 5e-10, 1e-9, 5e-9, 1e-8, 5e-8 ]; % = 1e-9 [published]
cds = [ 5e-10, 1e-9, 5e-9, 1e-8, 5e-8, 1e-7, 5e-7 ]; % = 1e-8 [published]
par_name = 'cd';
par_vals = 1;
par_vals = cds;
save_dir = [ 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/' ...
    '15_WJB_gb misorientation OIM EELS/figures/'...
    'gpdc-cahn-hilliard-simulation/simulations/' ...
    par_name '_' datestr(now, 'YYMMDD') '-' datestr(now, 'HHMM') '/' ];
if ~exist( save_dir )
    mkdir( save_dir )
end
na_bulks = [ .1, .15, .2 ];  % bulk dopant site fractions
% na_bulks = [ 1e-3, .01, .1, .2 ];  % bulk dopant site fractions
node_n = 100;
r_gr = 5e-7;            % grain radius
% par_file = 'segpar_ceria2_wb.txt';
par_file = 'segpar_ceria3_wb.txt'; % from David's student Xiaorui

for h = 1:length( par_vals )

    if isempty( par_vals ) % if par_vals is empty
        par_val = '';
    else
        par_val = par_vals(h);
    end
    
    ys = {};
    vs = {};
    phis = {};
    lamvs = [];
    lambds = [];
    nodess = {};
    flags = [];

    for i=1:length( na_bulks )
        na_b_i = na_bulks(i);
        disp( strcat( {'@ '}, datestr(now,'HH:MM:SS') ) );
        disp( strcat( {'tyring: na_b_i = '}, num2str(na_b_i) ) );
        [y,v,phi,lamv,lambd,nodes,flag] = ...
            segregation_ceria_afe_chem_3_sim( ...
                T, na_b_i, node_n, r_gr, par_file, par_val ...
            );
        ys{i} = y; % dopant site fraction
        vs{i} = v; % vacancy site fraction
        phis{i} = phi;
        lamvs(i) = lamv;
        lambds(i) = lambd;
        nodess{i} = nodes;
        flags(i) = flag;
        disp( strcat( {'@ '}, datestr(now,'HH:MM:SS') ) );
        disp( strcat( {'completed: na_b_i = '}, num2str(na_b_i) ) );
    end

    par = importdata(par_file,' ',2); 
    no = par.data(1);       % surface site density for vacancies, mol/m^2 (NvGB)
    fv = par.data(2);       % vacancy self-interaction, J/mol
    fo = par.data(3);       % vacancy segregation energy, J/mol
    fy = par.data(4);       % dopant self-interaction, J/mol
    fyv = par.data(5);      % dopant-vacancy interaction, J/mol
    cv = par.data(6);       % vacancy gradient energy coefficient, J/mol-m
    cd = par.data(7);       % dopant gradient energy coefficient, J/mol-m
    cd = par_val; % parametric study
    epsr = par.data(8);     % relative permittivity
    latpar = par.data(9);   % lattice parameter, m

    %%
    close all
    figure( 'position', [2000, -500, 600, 1200] )
    subplot( 3, 1, 1 )
    for i=1:length( na_bulks )
        plot( nodess{i}, vs{i}/(na_bulks(i)/4), 'Linewidth', 3 )
        hold on;
        legend_info{i} = [ strcat( 'na= ', num2str( na_bulks(i) ) ) ];
    end
%     xlims = [ -.05e-8, 1.05e-8 ];
    ylims = [ -0.3, 4.4 ];
    if limit_x
        xlim( xlims );
    end
    if limit_y
        ylim( ylims );
    end
    ylabel( 'nv/nv_{bulk}' )
    legend( legend_info )

    title( ...
        sprintf([ ...
            'T = ' num2str( T ) ' K; nodes = ' num2str( node_n ) ';' ...
            'r_{gr} = ' num2str( r_gr ) ' m; parfile = ' par_file ';\n' ...
            'no = ' num2str( no ) ' mol/m^2; fv = ' num2str( fv ) ' J/mol; ' ...
            'fo = ' num2str( fo ) ' J/mol;\nfy = ' num2str( fy ) ' J/mol; ' ...
            'fyv = ' num2str( fyv ) ' J/mol; ' ...
            'cv = ' num2str( cv ) ' J/mol-m;\ncd = ' num2str( cd ) ' J/mol-m; ' ...
            'epsr = ' num2str( epsr ) '; latpar = ' num2str( latpar ) ' m' ...
        ]) ...
    )

    subplot( 3, 1, 2 )
    for i=1:length( na_bulks )
        plot( nodess{i}, ys{i}/na_bulks(i), 'Linewidth', 3 )
        hold on;
    end
    % title( 'na/na_bulk' )
    % xlims = [ 0, 1e-8 ];
    ylims = [ 0, 22 ];
    if limit_x
        xlim( xlims );
    end
    if limit_y
        ylim( ylims );
    end
    ylabel( 'na/na_{bulk}' )

    subplot( 3, 1, 3 )
    for i=1:length( na_bulks )
        plot( nodess{i}(1:length(nodess{i})-1), phis{i}, 'Linewidth', 3 )
        hold on;
    end
    % title( 'phi' )
    % xlims = [ 0, 1e-8 ];
    ylims = [ -0.1, 1.1 ];
    if limit_x
        xlim( xlims );
    end
    if limit_y
        ylim( ylims );
    end
    ylabel( 'phi (V)' )
    xlabel( 'distance from interface (m)' )
    
    saveas( gcf, sprintf([ ...
        save_dir par_name '_' num2str(h) '_' num2str(par_val) '.png' ...
    ]) )
end