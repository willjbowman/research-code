clear all
close all
file = '140410_2CoGdcFIB_Nion60kV_EELSSI10_p3_CeGd2d_1mm_12mrad10i.mat';
load(file);
d = a140410_2CoGdcFIB_Nion60kV_EELSSI10_p3_CeGd2d_1mm_12mrad10i;
vertical_shift = 1.5e5; %shifts the spectra
chart_title = 'eels'; %chart title
horiz_label = 'energy loss'; %horizontal axis label
vert_label = 'Arbitrary units'; %vertical axis label


size = size(d);
spectra = size(2);
for i = 1:spectra
    if mod(i,2) == 0
        plot(d(:,i) + i*vertical_shift)
        hold on
    end
end
