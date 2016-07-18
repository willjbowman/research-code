T = 440+273;                             % temperature
% na_bulks = [ 1e-3, .01, .1, .2 ];  % bulk dopant site fractions
na_bulks = [ .01, .05, .1, .15 ];  % bulk dopant site fractions
node_n = 100;
r_gr = 1e-6;                             % grain radius
par_file = 'segpar_ceria3.txt';
ys = {};
vs = {};
phis = {};
lamvs = [];
lambds = [];
nodess = {};
flags = [];

for i=1:length( na_bulks )
    na_b_i = na_bulks(i);
    disp( strcat( '@', datestr(now,'HH:MM:SS') ) );
    disp( strcat( 'tyring: na_b_i = ', num2str(na_b_i) ) );
    [y,v,phi,lamv,lambd,nodes,flag] = ...
        segregation_ceria_afe_chem_v1_2_divalent( ...
            T, na_b_i, node_n, r_gr, par_file ...
        );
    ys{i} = y; % dopant site fraction
    vs{i} = v; % vacancy site fraction
    phis{i} = phi;
    lamvs(i) = lamv;
    lambds(i) = lambd;
    nodess{i} = nodes;
    flags(i) = flag;
    disp( strcat( '@', datestr(now,'HH:MM:SS') ) );
    disp( strcat( 'completed: na_b_i = ', num2str(na_b_i) ) );
end

%%
% close all
figure()
subplot( 3, 1, 1 )
for i=1:length( na_bulks )
    plot( nodess{i}, vs{i}/(na_bulks(i)/4) )
    hold on;
    legend_info{i} = [ strcat( 'na=',num2str(na_bulks(i)) ) ];
end
title( 'nv/nv_bulk' )
xlims = [ -.05e-8, 1.05e-8 ];
ylims = [ -0.3, 4.4 ];
xlim( xlims );
ylim( ylims );
legend_labels = [ '1e-3' ];
legend( legend_info )

subplot( 3, 1, 2 )
for i=1:length( na_bulks )
    plot( nodess{i}, ys{i}/na_bulks(i) )
    hold on;
end
title( 'na/na_bulk' )
% xlims = [ 0, 1e-8 ];
ylims = [ 0, 10 ];
xlim( xlims );
ylim( ylims );

subplot( 3, 1, 3 )
for i=1:length( na_bulks )
    % plot( nodess{i}(1:length(nodess{i})-1), phis{i} )
    plot( nodess{i}, phis{i} )
    hold on;
end
title( 'phi' )
% xlims = [ 0, 1e-8 ];
xlims = [ -.05e-8, 1.05e-8 ];
ylims = [ -0.1, 1.1 ];
xlim( xlims );
ylim( ylims );
xlabel( 'distance from interface (m)' )

