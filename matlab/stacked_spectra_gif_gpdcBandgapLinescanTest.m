clear all
close all
matfile = 'linescanTEst.mat';
load(matfile);
d = linescanTest';
output_file_name = 'gpdcDelocBandgaplinescanTest';
size = size(d);
signal_channels = size(1);
spectra = size(2);
ZLP_shift_total = 0.25; %eV
ZLP_shift = ZLP_shift_total / spectra;
% yMin = mean(min(d));
yMin = 0;
% yMax = 1.1*max(max(d));
yMax = 2e4;

% figure(1)
% for i = 1:spectra
%     overlay = plot(d(:,i),'linewidth',2,'color','red');
%     hold on
% end
% hold off
%%
% chart info
eV_min = -0.32;
% eV_max = 1227.2; %comment if using dispersion
dispersion = 0.003; % eV
eV_max = eV_min + dispersion*signal_channels;
eV = linspace(eV_min,eV_max,signal_channels);

chart_title = 'Gd_{0.11}Pr_{0.04}Ce_{0.85}O_{2-\delta} Bandgap (100kV Nion STEM)'; %chart title
horiz_label = 'Energy Loss (eV)'; %horizontal axis label
vert_label = 'Arbitrary Units'; %vertical axis label
legend_entries = ['On sample'];
xlim_min = eV_min; %eV
xlim_max = 5.5;

% gif speed
delay_time = 0.3; %sec

%%
figure(1)
for i = 1:spectra
    % plot stuff
    if i == 1
        plot(eV,d(:,1),':r','linewidth',2);
    else
        sh_eV = eV - ZLP_shift*(i-1);
        plot(eV,d(:,1),':r',sh_eV,d(:,i),'-b','linewidth',2);
    end
    
%     xlim([eV_min eV_max]);
    xlim([xlim_min xlim_max]);
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

