clear all, format compact

%IS sample information - s = 1/r = L/RA (S/cm)
L = 0.0765; %cm - sample thickness
d = 18e-3; %m - sample diameter
A = .914; %cm^2 - sample area
Tc = [700 650 600]; %C - sample temperature
Tk = Tc + 273; %C - sample temperature

%Data collected from ASU gamry for GDC20 with R-RC-RC(sample "2a gdc")
%R0 = 11.86; %ohm - system 'offset' resistance
R1 = [91.3	217.8	572]; %ohm - R1 resistance
R2 = [390	1100	2800]; %ohm - R2 resistance
C1 = [0.00000001412	0.00000001214	0.00000001081]; %F - C1 capacitance (smaller capacitance is assigned to smaller diam arc
C2 = [0.0000006733	0.0000006557	0.000000757]; %F - C2 capactitance

raw_data = [R1; R2; C1; C2]; %combine data into single array
delta = [-.5 -.4 -.3 -.2 -.1 0 .1 .2 .3 .4 .5]; %percent difference relative to real data (delta = 0)

for i=1:4
    for j=1:length(delta)
alt_data = raw_data; %generate altered data array from raw_data
alt_data(i,:) = raw_data(i,:) + raw_data(i,:)*delta(j);

R1_alt = alt_data(1,:);
R2_alt = alt_data(2,:);
C1_alt = alt_data(3,:);
C2_alt = alt_data(4,:);

Rtot = R1_alt + R2_alt; %ohm - Total resistance
Rint = R1_alt; %ohm - grain interior resistance
Rgb = R2_alt; %ohm - grain boundary resistance
Cint = C1_alt; %F - grain interior capacitance 
Cgb = C2_alt; %F - grain boundary capacitance

Stot = L./(Rtot*A); %S/m - total sample ionic conductivity
Sint = L./(Rint*A); %S/m - grain interior ionic conductivity
Sgb = Sint.*(Rint.*Cint./(Rgb.*Cgb)); %S/m - grain boundary ionic conductivity

Sint_700(i,j) = Stot(1);
Sint_650(i,j) = Stot(2);
Sint_600(i,j) = Stot(3);
Sgb_700(i,j) = Stot(1);
Sgb_650(i,j) = Stot(2);
Sgb_600(i,j) = Stot(3);
Stot_700(i,j) = Stot(1);
Stot_650(i,j) = Stot(2);
Stot_600(i,j) = Stot(3);

        xtot = 1000./Tk;
        ytot = log(Tk.*Stot);
        xint = 1000./Tk;
        yint = log(Tk.*Sint);
        xgb = 1000./Tk;
        ygb = log(Tk.*Sgb);
        
%figure(1)
        %plot(xint,yint,'v',xgb,ygb,'o',xtot,ytot,'*'),
        %legend('int','gb','tot')
        %title('GDC 2a 700C - 600C')
        %xlabel('1000/T'); ylabel('ln(\sigma*T)')
        %axis([0 2.5 -12 4]); 
       
%figure(2)
        linfit_int = fit(xint',yint','poly1'); %fitting the data
        linfit_gb = fit(xgb',ygb','poly1');
        linfit_tot = fit(xtot',ytot','poly1');
        
        %plot(linfit_int,xint,yint,'v'); %plot the fit and data
        %plot(linfit_gb,xgb,ygb,'o');
        %plot(linfit_tot,xtot,ytot,'*');
        
        coef_linfit_int = coeffvalues(linfit_int); %store fit coefs for Ea caluculation
        coef_linfit_gb = coeffvalues(linfit_gb);
        coef_linfit_tot = coeffvalues(linfit_tot);
     
        %legend('S_i_n_t actual','S_i_n_t fit'); %label fitted data plot
        %title('Arrhenius plot');
        %xlabel('1000/T'); ylabel('log(\sigma_i*T)');
        %axis([1.02 1.18 -8 0]);

        Ea_int(i,j) = coef_linfit_int(1)*1000*-8.617e-5; %eV - activation energy for ion hopping, interior
        Ea_gb(i,j) = coef_linfit_gb(1)*1000*-8.617e-5; %eV - activation energy for ion hopping, interior
        Ea_tot(i,j) = coef_linfit_tot(1)*1000*-8.617e-5; %eV - activation energy for ion hopping, interior
    end
end
for k=1:4
    figure(k)
    plot(delta,Ea_int(k,:),delta,Ea_gb(k,:),delta,Ea_tot(k,:));
    legend('int','gb','tot')
    figure(5)
    plot(delta,Sint_700(1,:),'o',delta,Sint_700(2,:))
    figure(6)
    plot(delta,Stot_700(1,:),delta,Stot_700(2,:))
end
