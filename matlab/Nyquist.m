w = [1e5:1:1e6]; %frequency input

%IS sample information - s = 1/r = L/RA (S/cm)
L = 0.077; %cm - sample thickness
d = 18e-3; %m - sample diameter
A = .914; %cm^2 - sample area
Tc = [100:50:800]; %C - sample temperature
Tk = Tc+273; %K - sample temperature

R_int_400 = 793.5; %ohm
R_gb_400 = 1.43e5; %ohm

rho_int_400 = R_int_400*A/L; %ohm-cm
rho_gb_400 = R_gb_400*A/L; %ohm-cm

Rsys = 0; %ohm - system 'offset' resistance
R1 = rho_int_400*L/A; %ohm - R1 resistance
R2 = rho_gb_400*L/A; %ohm - R2 resistance
R3 = 5e2; %ohm - R3 resistance
C1 = 4e-7; %F - C1 capacitance
C2 = 1.2e-8; %F - C2 capacitance
C3 = 20e-6; %F - C3 capacitance

Z_RC = R1./(1+w.^2*R1^2*C1^2)-(1i.*w*R1^2*C1)./(1+w.^2*R1^2*C1^2); %|| R-C Impedance
Z_RCreal = real(Z_RC); %Real impedance component
Z_RCimg = imag(Z_RC); %Imaginary impedance component

Z_RRC = Rsys + R1./(1+w.^2*R1^2*C1^2)-(1i.*w*R1^2*C1)./(1+w.^2*R1^2*C1^2); %|| R-C Impedance
Z_RRCreal = real(Z_RRC); %Real impedance component
Z_RRCimg = imag(Z_RRC); %Imaginary impedance component

Z_RRCRC = Rsys + 1./(1/R1+1i.*w*C1) + 1./(1/R2+1i.*w*C2);
Z_RRCRCreal = real(Z_RRCRC);
Z_RRCRCimg = imag(Z_RRCRC);

Z_RRCRCRC = Rsys + 1./(1/R1+1i.*w*C1) + 1./(1/R2+1i.*w*C2) + 1./(1/R3+1i.*w*C3);
Z_RRCRCRCreal = real(Z_RRCRCRC);
Z_RRCRCRCimg = imag(Z_RRCRCRC);

figure(1)
plot(Z_RRCRCreal,-Z_RRCRCimg);
%legend('R_1--C','R_0--R_1C','R_0--R_1C_1--R_2C_2','R_0--R_1C_1--R_2C_2--R_3C_3','SouthWest');
%title('R_0 = 10\Omega, R_1 = 100\Omega, C_1 = 2\muF, R_2 = 200\Omega, C_2 = 2\muF');
axis([0 R0+R1+R2 0 R0+R1+R2])

Rtot = R1 + R2; %ohm - Total resistance
Rint = R1; %ohm - grain interior resistance
Rgb = R2; %ohm - grain boundary resistance
Cint = C1; %F - grain interior capacitance 
Cgb = C2; %F - gring boundary capacitance

Stot = L/(Rtot*A); %S/m - total sample ionic conductivity
Sint = L/(Rint*A); %S/m - grain interior ionic conductivity
Sgb = Sint*(Rint*Cint/(Rgb*Cgb)); %S/m - grain boundary ionic conductivity