clear all
%w = linspace(1,1e2,10); %frequency input

%IS sample information - s = 1/r = L/RA (S/cm)
L = 0.0765; %cm - sample thickness
d = 18e-3; %m - sample diameter
A = .914; %cm^2 - sample area
Tk = [973 923 873 823 773 723 673 623 573 473]; %K - sample temperature
Tc = Tk - 273; %C - sample temperature

%Data collected from ASU gamry for GDC20 (sample "2a gdc")
R0 = 2; %ohm - system 'offset' resistance
R1 = [6.289	7.907 14.83	32.7 75.65 301.5 781 3934 19270	1309000]; %ohm - R1 resistance
R2 = [95.58	230.6	601.5	1928	7015	41940	136400	673500	3695000	647900000]; %ohm - R2 resistance
Y1 = [0.00002825	0.00001044	0.000000757	0.0007747	3.88E-10	2.806E-08	2.215E-08	1.706E-08	1.586E-08	1.015E-08]; %S*s^a - CPE1 factor(?)
Y2 = [4.497E-08	6.083E-08	4.799E-08	4.024E-08	3.302E-08	9.837E-10	8.2E-10	2.199E-09	6.868E-10	1.477E-10]; %CPE2
a1 = [0.0555 0.02355 0.04447 0.000000446 8.15E-02 0.8871 0.8972	0.9051 0.8914 0.8672]; %a - CPE1
a2 = [0.9122	0.882	0.8887	0.8889	0.8913	0.8266	0.8384	0.7587	0.816	0.8903]; %a - CPE2
data = [R1; R2];

D_data = data; %Populate 'D-data' matrix
delta = [-.5 -.4 -.3 -.2 -.1 0 .1 .2 .3 .4 .5]; %percent difference relative to real data (delta = 0)
Ea_int = zeros(2,11);

for k = 1:length(delta)
    for i = 1:2
            for j = 1:length(R1)
            D_data(i,j) = data(i,j) + data(i,j)*delta(k); %generate data with one misestimated component
            end
   
    %Calculate Ea based on mis-estimate data
        %Capacitances calculated from constant phase element parameters
        %C1(k,i) = (D_data(1,:).^(1./D_data(5,:).*D_data(3,:)).^(1-D_data(3,:)); %F - C1 capacitance (int)
        %C2(k,i) = (D_data(2,:).^(1./D_data(6,:).*D_data(5,:)).^(1-D_data(5,:)); %F - C2 capacitance (gb)
        
        %Rtot = D_data(1,:) + D_data(2,:); %ohm - Total resistance
        Rint = D_data(1,:); %ohm - grain interior resistance
        %Rgb = D_data(2,:); %ohm - grain boundary resistance
        %Cint = C1; %F - grain interior capacitance 
        %Cgb = C2; %F - gring boundary capacitance

        %Stot = L./(Rtot*A); %S/m - total sample ionic conductivity
        Sint = L./(Rint*A); %S/m - grain interior ionic conductivity
        %Sgb = Sint.*(Rint.*Cint./(Rgb.*Cgb)); %S/m - grain boundary ionic conductivity
        
        %xtot = 1000./Tk;
        %ytot = log(Tk.*Stot);
        xint = Sint;
        yint = log(Tk.*Sint);

       
        plot(xint,yint,'v');

        
        linfit = fit(xint',yint','poly1');
        plot(linfit,xint,yint,'o'),
        coef_linfit = coeffvalues(linfit);
        legend('S_i_n_t actual','S_i_n_t fit');
        title('Arrhenius plot');
        xlabel('1000/T'); ylabel('log(\sigma_i*T)');

        Ea_int(i,k) = coef_linfit(1)*1000*-8.617e-5; %eV - activation energy for ion hopping, interior
        D_data,
        D_data = data; %reset all experimental parameters
    end   
end

figure(1)
plot(delta,Ea_int(1,:))
%,delta,Ea_int(2,:),delta,Ea_int(3,:),delta,Ea_int(4,:),delta,Ea_int(5,:),delta,Ea_int(6,:));
%legend('R1','R2','Y1','Y2','a1','a2')
%Z_RRCRC = R0 + 1./(1./R1+1i.*w.*C1) + 1./(1./R2+1i.*w.*C2);
%Z_RRCRCreal = real(Z_RRCRC);
%Z_RRCRCimg = imag(Z_RRCRC);




%figure(3)
%K_scale = line(xint,yint,'Color','r'); %plot 1000/T, Kelvin
%ax1 = gca;
%set(ax1,'XColor','r','YColor','r','YTick',[])
%ax2 = axes('Position',get(ax1,'Position'),'XAxisLocation','top',...
    %'YAxisLocation','right','Color','none','XColor','k','YColor','k');
%C_scale = line(xtot,ytot,'Color','k','Parent',ax2);
