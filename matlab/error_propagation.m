%error propagation 
clear all; format compact
%GAMRY DATA FROM R-RQ-RQ ANALYSIS
gamry_data_RQ = ...
[8.92	80.01	433.3	3.008E-08	0.946	0.000005764	0.7517
8.92	187.9	1210	5.016E-08	0.9019	0.000006342	0.7085
8.92	520.9	2731	7.916E-08	0.8567	0.000006099	0.6907
29.39	1.38E+03	8.68E+03	2.29E-08	9.54E-01	6.57E-06	6.05E-01
67.47	5.21E+03	2.70E+04	2.11E-08	9.54E-01	3.63E-06	6.16E-01
2.86E+02	3.07E+04	1.50E+05	2.28E-08	9.28E-01	1.15E-06	6.87E-01
7.36E+02	1.48E+05	6.00E+05	2.61E-08	8.79E-01	5.17E-03	7.37E-01];
%gdc

d_gamry_data_RQ = ...
[0.4439	2.243	18.04	5.594E-09	0.0138	8.898E-07	0.01752
0	5.477	61.7	5.401E-09	0.00835	9.353E-07	0.01842
0	0	103.8	4.104E-09	0.003768	4.566E-07	0.008814
1.27	47.49	430.4	2.89E-09	1.23E-02	5.96E-07	1.55E-02
9.33E-01	0	877.9	8.90E-10	3.63E-03	4.90E-08	0
3.75E+00	9.19E+02	0.00E+00	1.58E-09	9.04E-03	6.75E-08	1.35E-02
7.44E+00	2.44E+04	0.00E+00	1.58E-09	1.47E-02	3.02E+01	280.9];
%dgdc

R1_RQ = [gamry_data_RQ(:,2)];
dR1_RQ = [d_gamry_data_RQ(:,2)];
R2_RQ = [gamry_data_RQ(:,3)];
dR2_RQ = [d_gamry_data_RQ(:,3)];
Y1_RQ = [gamry_data_RQ(:,4)];
dY1_RQ = [d_gamry_data_RQ(:,4)];
a1_RQ = [gamry_data_RQ(:,5)];
da1_RQ = [d_gamry_data_RQ(:,5)];
Y2_RQ = [gamry_data_RQ(:,6)];
dY2_RQ = [d_gamry_data_RQ(:,6)];
a2_RQ = [gamry_data_RQ(:,7)];
da2_RQ = [d_gamry_data_RQ(:,7)];

C1_RQ = (Y1_RQ.*R1_RQ.^(1-a1_RQ)).^(1./a1_RQ);
C2_RQ = (Y2_RQ.*R2_RQ.^(1-a2_RQ)).^(1./a2_RQ);

T = [973 923 873 823 773 723 673]'; %K
dT = [0 0 0 0 0 0 0]';
L = 0.07653; %cm
dL = 0.0; %cm
A = 0.914; %cm^2
dA = 0.0; %cm

%interior ion conductivity error propagation
%CONDUCTIVITY = (L/A)*1/R
D = L/A; %cm^-1 SAMPLE GEOMETRY
dD = D*sqrt((dL/L)^2+(dA/A)^2); %cm

sint = D./R1_RQ; %S/cm IONIC CONDUCTIVITY
dsint = sint.*sqrt((dD./D).^2+(dR1_RQ./R1_RQ).^2); %S/cm

Tsint = T.*sint; %S/cm*K TEMPERATURE * IONIC CONDUCTIVITY (FOR PLOTTING)
dTsint = Tsint.*sqrt((dsint./sint).^2+(dT./T).^2); %S/cm*K

Sint = log(Tsint); %LN(T*CONDUCTIVITY) Y-AXIS OF ARRHENIUS PLOT
dSint = dTsint./Tsint;

%gb ion conductivity error propagation
%NEED C1 AND C2 BECAUSE CONDUCTIVITY IS DEPENDENT ON TIME CONSTANTS
%IN THE CONSTANT PHASE ELEMENT ANALYSIS C DEPENDS ON Y, a, AND R
%C = [Y*R^(1-a)]^(1/a)
n1 = 1./a1_RQ; %
dn1 = n1.*sqrt(da1_RQ./a1_RQ).^2;

m1 = 1-a1_RQ;
dm1 = m1.*sqrt(a1_RQ.^2);

B1 = R1_RQ.^(m1);
dB1 = R1_RQ.*m1.*(dR1_RQ./R1_RQ);

E1 = Y1_RQ.*B1;
dE1 = E1.*sqrt((dY1_RQ./Y1_RQ).^2+(dB1./B1).^2);

C1_RQ = E1.^n1; %F C1 capacitance
dC1 = C1_RQ.*n1.*dE1;% F C1 capacitance error

t1 = C1_RQ.*R1_RQ; % F-ohms time constant for arc 1
dt1 = t1.*sqrt((dC1./C1_RQ).^2+(dR1_RQ./R1_RQ).^2);

%must calculate the same thing for C2 and t2 now
n2 = 1./a2_RQ; %
dn2 = n2.*sqrt(da2_RQ./a2_RQ).^2;

m2 = 1-a2_RQ;
dm2 = m2.*sqrt(a2_RQ.^2);

B2 = R2_RQ.^(m2);
dB2 = R2_RQ.*m2.*(dR2_RQ./R2_RQ);

E2 = Y2_RQ.*B2;
dE2 = E2.*sqrt((dY2_RQ./Y2_RQ).^2+(dB2./B2).^2);

C2_RQ = E2.^n2; %F C2 capacitance
dC2 = C2_RQ.*n2.*dE2;% F C2 capacitance error

t2 = C2_RQ.*R2_RQ; % F-ohms time constant for arc 2
dt2 = t2.*sqrt((dC2./C2_RQ).^2+(dR2_RQ./R2_RQ).^2);

tt = t1./t2;
dtt = tt.*sqrt((dt1./t1).^2+(dt2./t2).^2);

sgb = tt.*sint; %S/cm grain boundary ion conductivity
dsgb = sgb.*sqrt((dtt./tt).^2+(dsint./sint).^2); %sgb error

Tsgb = sgb.*T;
dTsgb = Tsgb.*sqrt((dsgb./sgb).^2+(dT./T).^2);

Sgb = log(Tsgb);
dSgb = dTsgb./Tsgb;

%total conductivity
%stot = L/(Rint+Rgb)/A
Rtot = R1_RQ+R2_RQ;
dRtot = sqrt(R1_RQ.^2+R2_RQ.^2);

stot = D./Rtot;
dstot = stot.*sqrt((dD./D).^2+(dRtot./Rtot).^2);

Tstot = T.*stot;
dTstot = Tstot.*sqrt((dT./T).^2+(dstot./stot).^2);

Stot = log(Tstot);
dStot = dTstot./Tstot;

S = [Sint Sgb Stot]; dS = [dSint dSgb dStot];
mark = ['d' 's' '^'];

figure(1)
for i = 1:3
    errorbar(1000./T,S(:,i),dS(:,1),mark(i))
    hold on
    linfit = fit([1000./T],S(:,i),'poly1');
    coef_linfit = coeffvalues(linfit); %store fit coefs for Ea caluculation
    Ea(i) = coef_linfit(1)*1000*-8.617e-5; %eV - activation energy
end
legend('int','gb','tot'); title('GDC ionic conductivity 450-700C [R-RQ-RQ]');
xlabel('1000/T (K^-1)'); ylabel('ln(\sigma*T)');
Ea_int = Ea(1), Ea_gb = Ea(2), Ea_tot = Ea(3),

%GAMRY DATA FROM R-RC-RC ANALYSIS
gamry_data_RC = ...
[11.68	91.3	390	1.412E-08	6.733E-07
11.68	217.8	1100	1.214E-08	6.557E-07
11.68	572	2800	1.081E-08	0.000000757
43.46	1.87E+03	8.13E+03	1.03E-08	8.25E-07
91.39	6.44E+03	2.53E+04	9.60E-09	6.23E-07
3.31E+02	3.29E+04	1.50E+05	9.07E-09	2.35E-07
8.07E+02	1.50E+05	8.47E+05	8.84E-09	2.56E-04];
%

d_gamry_data_RC = ...
[0.2269	0.5977	0	1.408E-10	7.434E-09
0	1.289	0	8.39E-11	6.544E-09
0	3.161	0	6.52E-11	7.556E-09
4.55E-01	10.17	0	5.71E-11	8.65E-09
7.44E-01	0	0	4.97E-11	6.78E-09
2.046	2.22E+02	0.00E+00	4.61E-11	4.84E-09
4.383	0.00E+00	2.76E+13	6.74E-11	4.15E-02];
%

R1_RC = [gamry_data_RC(:,2)];
dR1_RC = [d_gamry_data_RC(:,2)];
R2_RC = [gamry_data_RC(:,3)];
dR2_RC = [d_gamry_data_RC(:,3)];
C1_RC = [gamry_data_RC(:,4)];
dC1_RC = [d_gamry_data_RC(:,4)];
C2_RC = [gamry_data_RC(:,5)];
dC2_RC = [d_gamry_data_RC(:,5)];

%interior ion conductivity error propagation
%CONDUCTIVITY = (L/A)*1/R
D = L/A; %cm^-1 SAMPLE GEOMETRY
dD = D*sqrt((dL/L)^2+(dA/A)^2); %cm

sint_RC = D./R1_RC; %S/cm IONIC CONDUCTIVITY
dsint_RC = sint.*sqrt((dD./D).^2+(dR1_RC./R1_RC).^2); %S/cm

Tsint_RC = T.*sint_RC; %S/cm*K TEMPERATURE * IONIC CONDUCTIVITY (FOR PLOTTING)
dTsint_RC = Tsint_RC.*sqrt((dsint_RC./sint_RC).^2+(dT./T).^2); %S/cm*K

Sint_RC = log(Tsint_RC); %LN(T*CONDUCTIVITY) Y-AXIS OF ARRHENIUS PLOT
dSint_RC = dTsint_RC./Tsint_RC;

%gb ion conductivity error propagation
t1_RC = C1_RC.*R1_RC; % F-ohms time constant for arc 1
dt1_RC = t1_RC.*sqrt((dC1_RC./C1_RC).^2+(dR1_RC./R1_RC).^2);

t2_RC = C2_RC.*R2_RC; % F-ohms time constant for arc 2
dt2_RC = t2_RC.*sqrt((dC2_RC./C2_RC).^2+(dR2_RC./R2_RC).^2);

tt_RC = t1_RC./t2_RC;
dtt_RC = tt_RC.*sqrt((dt1_RC./t1_RC).^2+(dt2_RC./t2_RC).^2);

sgb_RC = tt_RC.*sint_RC; %S/cm grain boundary ion conductivity
dsgb_RC = sgb_RC.*sqrt((dtt_RC./tt_RC).^2+(dsint_RC./sint_RC).^2); %sgb error

Tsgb_RC = sgb_RC.*T;
dTsgb_RC = Tsgb_RC.*sqrt((dsgb_RC./sgb_RC).^2+(dT./T).^2);

Sgb_RC = log(Tsgb_RC);
dSgb_RC = dTsgb_RC./Tsgb_RC;

%total conductivity
%stot_RC = L/(Rint+Rgb)/A
Rtot_RC = R1_RC+R2_RC;
dRtot_RC = sqrt(R1_RC.^2+R2_RC.^2);

stot_RC = D./Rtot_RC;
dstot_RC = stot_RC.*sqrt((dD./D).^2+(dRtot_RC./Rtot_RC).^2);

Tstot_RC = T.*stot_RC;
dTstot_RC = Tstot_RC.*sqrt((dT./T).^2+(dstot_RC./stot_RC).^2);

Stot_RC = log(Tstot_RC);
dStot_RC = dTstot_RC./Tstot_RC;

S_RC = [Sint_RC Sgb_RC Stot_RC]; dS_RC = [dSint_RC dSgb_RC dStot_RC];
mark = ['d' 's' '^'];

figure(2)
for i = 1:3
    errorbar(1000./T,S_RC(:,i),dS_RC(:,1),mark(i))
    hold on
    linfit_RC = fit([1000./T],S_RC(:,i),'poly1');
    coef_linfit_RC = coeffvalues(linfit_RC); %store fit coefs for Ea caluculation
    Ea_RC(i) = coef_linfit_RC(1)*1000*-8.617e-5; %eV - activation energy
end
legend('int','gb','tot'); title('GDC ionic conductivity 450-700C [R-RC-RC]');
xlabel('1000/T (K^-1)'); ylabel('ln(\sigma*T)');
axis([1 1.5 -30 5]);
Ea_int_RC = Ea_RC(1), Ea_gb_RC = Ea_RC(2), Ea_tot_RC = Ea_RC(3),


