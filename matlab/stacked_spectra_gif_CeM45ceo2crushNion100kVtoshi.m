clear all
close all
matfile = 'CeM45crushedCeO2Nion100kV.mat';
load(matfile);
d = CeM45crushedCeO2Nion100kV;
output_file_name = 'CeM45crushedCeO2Nion100kV';
size = size(d);
signal_channels = size(1);
spectra = size(2);
yMin = mean(min(d));
yMax = 1.1*max(max(d));
% yMax = 2e5;

% figure(1)
% for i = 1:spectra
%     overlay = plot(d(:,i),'linewidth',2,'color','red');
%     hold on
% end
% hold off
%%
% chart info
eV_min = 875;
% eV_max = 1227.2; %comment if using dispersion
dispersion = 0.05; % eV
eV_max = eV_min + dispersion*signal_channels;
eV = linspace(eV_min,eV_max,signal_channels);

chart_title = 'Ce M-edge in CeO_2 (100 kV Nion STEM)'; %chart title
horiz_label = 'Energy Loss (eV)'; %horizontal axis label
vert_label = 'Arbitrary Units'; %vertical axis label
legend_entries = ['Initial'];

% gif speed
delay_time = 0.3; %sec


%%
figure
for i = 1:spectra
    % plot stuff
    r = 0;
    g = i;
    b = spectra-i;
    color = [g r b]/spectra;
    
    if i == 1
        plot(eV,d(:,1),':b','linewidth',2);
    else
        plot(eV, d(:,1), ':b', 'linewidth', 2 );
        hold on
        plot( eV, d(:,i), 'color', color, 'linewidth', 2 );
        hold off
    end
    
%     xlim([eV_min eV_max]);
    xlim([880 925]);
    ylim([yMin yMax]);
    title(chart_title,'FontSize',16,'FontName','Arial');
    xlabel(horiz_label,'FontSize',16,'FontName','Arial');
    ylabel(vert_label,'FontSize',16,'FontName','Arial');
    legend(legend_entries);
    set(gca,'YTick',[],'FontName','Arial','FontSize',16); 
    
    % gif stuff
    set(gcf,'color','w'); % white background
    text = uicontrol('style','text');
    set(text,'String',strcat(num2str(i),'/',num2str(spectra)),...
        'backgroundcolor',get(gcf,'color'));
    drawnow;
    frame = getframe(1);
    im = frame2im(frame);
    [imind,cm] = rgb2ind(im,256);
    outfile = strcat('C:\MatlabFigures\',output_file_name);

    % create file on 1st loop, append on each loop after
    if i == 1
        imwrite(imind,cm,outfile,'gif','DelayTime',delay_time,'loopcount',inf);
    else
        imwrite(imind,cm,outfile,'gif','DelayTime',delay_time,'writemode','append');
    end
end
%%
% close all
figure
for i = 1:spectra
    % plot stuff
    r = 0;
    g = i;
    b = spectra-i;
    color = [g r b]/spectra;
    acqisition = linspace(i,i,signal_channels);
    plot3(acqisition,eV,d(:,i),'color',color,'linewidth',1.4);
    view(90,0); %az el
    
%     xlim([eV_min eV_max]);
    ylim([880 925]);
    zlim([yMin yMax]);
    title(chart_title,'FontSize',16,'FontName','Arial');
    ylabel(horiz_label,'FontSize',16,'FontName','Arial');
    zlabel(vert_label,'FontSize',16,'FontName','Arial');
    xlabel('Acquisition','FontSize',16,'FontName','Arial');
%     legend(legend_entries);
    set(gca,'ZTick',[],'FontName','Arial','FontSize',16); 
    
    hold on
end
%% plot initial and final together
figure
plot( eV, d( :, 1 ), ':b', eV, d( :, end ), '-r', 'linewidth', 2 );
styleFont( 'bold', 'arial', 18 );
set(gca,'YTick',[],'FontName','Arial','FontSize',16);
legend( 'Initial', 'Final' );
xlim( [ 880 925 ] );
ylim( [ yMin yMax ] );
title( chart_title );
xlabel( horiz_label );
ylabel( vert_label );
