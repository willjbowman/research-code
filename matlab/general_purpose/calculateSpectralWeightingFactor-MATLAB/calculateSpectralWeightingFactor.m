% clear all
close all
%%
% import background-subtracted time-resolved EELS spectra
inFile = '140404_7bCeO2crush_Nion100kV_timeResolved-CeM-BKGDSUBSI-870.txt';
importdata(inFile);
d = ans.data;

%%
siz = size(d);
columns = siz(2);
spectra = 400;

%%
close all
% group multiple spectra to determine fractional contribution
group = 5;

eV = d(:,1); % energy window

% define constituent spectra
sInit = d(:,2); % initial acquisition
sFin = d(:,spectra); % final acquisiton

% define number of weighting combinations used for matching
steps = 100;

for i = 2 : spectra
    sSubj = d(:,i); % subject spectrum

    for a = 1 : steps
        b = steps - a;
        sTry = ( a * sInit + b * sFin ) / steps;
        diff(a,:) = abs ( sSubj - sTry );
        sumDiff(a,1) = sum(diff(a,:));
    end
    [minVal,minIndex] = min(sumDiff);
    fractionInitSpec(i) = minIndex;
    
    figure(1)
    
    r = 0;
    g = spectra-i;
    b = i;
    color = [g r b]/spectra;
    
    plot(sumDiff,'color',color)
    ylim([0 1e6]);
    hold on
end

hold off
xlabel('Fraction initial spectrum (Ce^{4+})');
ylabel('Actual signal - composition signal');

figure(2)
for col = 2 : spectra
    r = 0;
    g = spectra-col;
    b = col;
    color = [g r b]/spectra;
    plot(fractionInitSpec(col),'o','color',color);
end
ylabel('Fraction initial spectrum (Ce^{4+})');
xlabel('Acquisition');

%%

for i = 2 : spectra
    sSubj = d(:,i); % subject spectrum
%     counts(i) = sum(sSubj);
    counts = sum(sSubj);
    sSubjNorm = sSubj ./ counts;
    countsNorm(i) = sum(sSubjNorm);
end
figure
plot(countsNorm)
