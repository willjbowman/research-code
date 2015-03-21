clear all
close all
matfile = 'crushedCeO2Nion100kV.mat';
load(matfile);
d = crushedCeO2Nion100kV;
output_file_name = 'OKcrushedCeO2Nion100kV';
size = size(d);
signal_channels = size(1);
spectra = size(2);
yMin = mean(min(d));
yMax = 1.1*max(max(d));

% figure(1)
% for i = 1:spectra
%     overlay = plot(d(:,i),'linewidth',2,'color','red');
%     hold on
% end
% hold off
% % close all
%%
% chart info
eV_min = 525;
% eV_max = 1227.2; %comment if using dispersion
dispersion = 0.05; % eV
eV_max = eV_min + dispersion*signal_channels;
eV = linspace(eV_min,eV_max,signal_channels);

chart_title = 'O K-edge in CeO_2 (100 kV Nion STEM)'; %chart title
horiz_label = 'Energy Loss (eV)'; %horizontal axis label
vert_label = 'Arbitrary Units'; %vertical axis label
legend_entries = ['Initial'];

% gif speed
delay_time = 0.3; %sec

%%
figure(1)
for i = 1:spectra
    % plot stuff
    if i == 1
        plot(eV,d(:,1),':r','linewidth',2);
    else
        plot(eV,d(:,1),':r',eV,d(:,i),'-b','linewidth',2);
    end
    
    xlim([eV_min eV_max]);
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

