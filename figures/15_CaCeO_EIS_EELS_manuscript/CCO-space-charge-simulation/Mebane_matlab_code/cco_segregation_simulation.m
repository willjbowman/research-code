T = 700+273;                             % temperature
fys = [ 1e3, 5e3, 1e4, 5e4, 1e5, 5e5, 1e6 ]; % =1e4 [published]
fyvs = -[ 1e3, 5e3, 1e4, 5e4, 1e5, 5e5, 1e6 ]; % =-7e3 [published]
save_dir = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/2015_IS EBSD EELS Ca-Ceria gbs/data/space-charge-simulation/cahn-hilliard/fyvs/';
% na_bulks = [ 1e-3, .01, .1, .2 ];  % bulk dopant site fractions
na_bulks = [ .05, .1 ];  % bulk dopant site fractions
% na_bulks = [ .02, .05, .1 ];  % bulk dopant site fractions
node_n = 100;
r_gr = 5e-7;            % grain radius
par_file = 'segpar_ceria3.txt';
% par_file = 'segpar_ceria3_wb.txt';

% for h = 1:length( fys )
for h = 1:length( fyvs )    
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
            segregation_ceria_afe_chem_v1_2_divalent( ...
                T, na_b_i, node_n, r_gr, par_file, fyvs(h) ...
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
%     fy = fys(h);
    fyv = par.data(5);      % dopant-vacancy interaction, J/mol
    fyv = fyvs(h);
    cv = par.data(6);       % vacancy gradient energy coefficient, J/mol-m
    cd = par.data(7);       % dopant gradient energy coefficient, J/mol-m
    epsr = par.data(8);     % relative permittivity
    latpar = par.data(9);   % lattice parameter, m

    %%
    % close all
    figure( 'position', [2000, -500, 600, 1200] )
    subplot( 3, 1, 1 )
    for i=1:length( na_bulks )
        plot( nodess{i}, vs{i}/(na_bulks(i)/4) )
        hold on;
        legend_info{i} = [ strcat( 'na= ', num2str( na_bulks(i) ) ) ];
    end
    xlims = [ -.05e-8, 1.05e-8 ];
    ylims = [ -0.3, 4.4 ];
    % xlim( xlims );
    % ylim( ylims );
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
        plot( nodess{i}, ys{i}/na_bulks(i) )
        hold on;
    end
    % title( 'na/na_bulk' )
    % xlims = [ 0, 1e-8 ];
    ylims = [ 0, 22 ];
    % xlim( xlims );
    % ylim( ylims );
    ylabel( 'na/na_{bulk}' )

    subplot( 3, 1, 3 )
    for i=1:length( na_bulks )
        plot( nodess{i}(1:length(nodess{i})-1), phis{i} )
        hold on;
    end
    % title( 'phi' )
    % xlims = [ 0, 1e-8 ];
    ylims = [ -0.1, 1.1 ];
    % xlim( xlims );
    % ylim( ylims );
    ylabel( 'phi (V)' )
    xlabel( 'distance from interface (m)' )
    
    % saveas( gcf, sprintf([ save_dir 'fy-' num2str( fyv ) '.png' ]) )
end